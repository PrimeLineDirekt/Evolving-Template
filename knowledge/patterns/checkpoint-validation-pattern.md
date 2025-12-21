# Checkpoint Validation Pattern

**Typ**: Infrastructure Pattern
**Confidence**: 88%
**Source**: ucbepic/docetl (DSLRunner)
**Priority**: P2 - Medium

---

## Problem

Checkpoint-basierte Systeme können stale (veraltete) Checkpoints verwenden, wenn sich die Konfiguration geändert hat. Dies führt zu:

- Inkonsistenten Ergebnissen (alter Output + neue Config)
- Schwer zu debuggenden Fehlern
- Falsche Wiederaufnahme nach Crashes

## Solution

Hash-basierte Checkpoint-Validierung: Jeder Checkpoint enthält einen Hash der relevanten Konfiguration. Vor dem Laden wird der Hash verglichen.

```
Pipeline Config
     │
     ▼
┌─────────────────┐
│  Generate Hash  │
│  (SHA-256)      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐     ┌─────────────────┐
│  Load Checkpoint│────►│  Compare Hashes │
└─────────────────┘     └────────┬────────┘
                                 │
                   ┌─────────────┴─────────────┐
                   │                           │
                   ▼                           ▼
            ┌──────────┐               ┌──────────────┐
            │  MATCH   │               │  MISMATCH    │
            │  Use CP  │               │  Invalidate  │
            └──────────┘               │  Re-execute  │
                                       └──────────────┘
```

## Implementation

### Hash Generation

```python
import hashlib
import json
from typing import Any

def generate_config_hash(config: dict, include_keys: list[str] = None) -> str:
    """
    Generate deterministic hash of configuration.

    Args:
        config: Configuration dictionary
        include_keys: Specific keys to include (None = all)

    Returns:
        SHA-256 hash string
    """
    if include_keys:
        config_subset = {k: config[k] for k in include_keys if k in config}
    else:
        config_subset = config

    # Ensure deterministic serialization
    config_str = json.dumps(config_subset, sort_keys=True, default=str)
    return hashlib.sha256(config_str.encode()).hexdigest()


def generate_agent_hash(
    agent_id: str,
    system_prompt: str,
    query: str,
    model: str
) -> str:
    """Generate hash for agent execution context."""
    context = {
        "agent_id": agent_id,
        "system_prompt_hash": hashlib.md5(system_prompt.encode()).hexdigest(),
        "query_hash": hashlib.md5(query.encode()).hexdigest(),
        "model": model
    }
    return generate_config_hash(context)
```

### Checkpoint with Validation

```python
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

@dataclass
class ValidatedCheckpoint:
    """Checkpoint with validation metadata."""

    # Checkpoint data
    session_id: str
    agent_id: str
    result: Any

    # Validation
    config_hash: str
    created_at: datetime = field(default_factory=datetime.now)

    # Metadata
    pipeline_version: str = "1.0.0"


class CheckpointManager:
    """Manages checkpoints with staleness detection."""

    def __init__(self, checkpoint_dir: str):
        self.checkpoint_dir = Path(checkpoint_dir)
        self.hash_registry: dict[str, str] = {}  # session_id -> config_hash

    def save_checkpoint(
        self,
        session_id: str,
        agent_id: str,
        result: Any,
        config_hash: str
    ) -> ValidatedCheckpoint:
        """Save checkpoint with config hash."""
        checkpoint = ValidatedCheckpoint(
            session_id=session_id,
            agent_id=agent_id,
            result=result,
            config_hash=config_hash
        )

        # Save to disk
        checkpoint_path = self.checkpoint_dir / session_id / f"{agent_id}.json"
        checkpoint_path.parent.mkdir(parents=True, exist_ok=True)

        with open(checkpoint_path, "w") as f:
            json.dump(asdict(checkpoint), f, default=str)

        # Update registry
        self.hash_registry[f"{session_id}:{agent_id}"] = config_hash

        return checkpoint

    def load_checkpoint(
        self,
        session_id: str,
        agent_id: str,
        current_config_hash: str
    ) -> Optional[ValidatedCheckpoint]:
        """
        Load checkpoint if valid.

        Returns:
            Checkpoint if hash matches, None if stale/missing
        """
        checkpoint_path = self.checkpoint_dir / session_id / f"{agent_id}.json"

        if not checkpoint_path.exists():
            return None

        with open(checkpoint_path) as f:
            data = json.load(f)

        checkpoint = ValidatedCheckpoint(**data)

        # Validate hash
        if checkpoint.config_hash != current_config_hash:
            print(f"⚠️ Checkpoint stale for {agent_id}: config changed")
            print(f"   Stored hash: {checkpoint.config_hash[:16]}...")
            print(f"   Current hash: {current_config_hash[:16]}...")
            return None  # Checkpoint invalid

        return checkpoint

    def invalidate_session(self, session_id: str) -> int:
        """Invalidate all checkpoints for a session."""
        session_dir = self.checkpoint_dir / session_id
        if not session_dir.exists():
            return 0

        count = 0
        for checkpoint_file in session_dir.glob("*.json"):
            checkpoint_file.unlink()
            count += 1

        # Clear from registry
        keys_to_remove = [k for k in self.hash_registry if k.startswith(f"{session_id}:")]
        for key in keys_to_remove:
            del self.hash_registry[key]

        return count
```

### Integration with Pipeline

```python
class ResilientOrchestrator:
    """Orchestrator with checkpoint validation."""

    async def execute_agent_with_checkpoint(
        self,
        agent_id: str,
        profile: UserProfile,
        query: str,
        session: Session
    ) -> tuple[str, AgentOutput]:
        """Execute agent with checkpoint validation."""

        # Generate config hash for this execution
        agent = self.agents[agent_id]
        config_hash = generate_agent_hash(
            agent_id=agent_id,
            system_prompt=agent.system_prompt,
            query=query,
            model=agent.model_tier
        )

        # Try to load valid checkpoint
        checkpoint = self.checkpoint_manager.load_checkpoint(
            session_id=session.session_id,
            agent_id=agent_id,
            current_config_hash=config_hash
        )

        if checkpoint:
            print(f"   ✅ {agent_id}: Using cached result (hash valid)")
            return agent_id, checkpoint.result

        # Execute fresh
        print(f"   🔄 {agent_id}: Executing (no valid checkpoint)")
        result = await agent.run(profile, query)

        # Save with hash
        self.checkpoint_manager.save_checkpoint(
            session_id=session.session_id,
            agent_id=agent_id,
            result=result,
            config_hash=config_hash
        )

        return agent_id, result
```

## What to Include in Hash

### Must Include (Changes Invalidate)

| Component | Reason |
|-----------|--------|
| System Prompt | Core logic changes |
| Query/Input | Different questions = different answers |
| Model ID | Different model = different output |
| Temperature | Affects randomness |
| KB Query Config | Different context = different results |

### May Include (Optional)

| Component | When to Include |
|-----------|-----------------|
| Model Version | If outputs must be reproducible |
| KB Content Hash | If KB updates should invalidate |
| Agent Version | For versioned deployments |

### Don't Include

| Component | Reason |
|-----------|--------|
| Timestamp | Always changes |
| Random Seeds | Defeats caching purpose |
| Logging Config | Doesn't affect output |

## Integration Example

**Status**: RECOMMENDED

Systems with checkpointing can benefit from hash-based validation.

### Recommended Changes

In your checkpoint manager:

```python
# CURRENT
def save_agent_result(self, session_id: str, result: AgentResult):
    # Saves result without config hash
    ...

# RECOMMENDED
def save_agent_result(
    self,
    session_id: str,
    result: AgentResult,
    config_hash: str  # NEW
):
    result.config_hash = config_hash  # Store with result
    ...

def load_agent_result(
    self,
    session_id: str,
    agent_id: str,
    current_config_hash: str  # NEW: Validate before returning
) -> Optional[AgentResult]:
    result = self._load_from_disk(session_id, agent_id)
    if result and result.config_hash != current_config_hash:
        return None  # Stale
    return result
```

### Affected Components

- Checkpoint manager - Add hash storage
- Session models - Add `config_hash` field
- Orchestrator - Generate + validate hashes

### Effort Estimation

- **Implementation**: ~2-3h
- **Testing**: ~1h
- **Impact**: Low risk, backwards compatible

---

## Trade-offs

| Pro | Contra |
|-----|--------|
| Verhindert stale Checkpoints | Hash-Berechnung Overhead (~1ms) |
| Klare Invalidierungs-Logik | Mehr Speicher für Hashes |
| Debug-freundlich (Hash-Diff) | Initial Setup-Aufwand |
| Backwards-compatible erweiterbar | - |

## When to Use

- **JA**: Multi-Agent Pipelines, resumable Sessions, Production Systems
- **NEIN**: Stateless APIs, Kurze Tasks ohne Recovery-Bedarf

## Related Patterns

- [PEV Pattern](pev-pattern.md) - Verify-Phase nutzt ähnliche Validierung

---

**Navigation**: [← Patterns](README.md) | [Knowledge Index](../index.md)
