"""
Workflow Engine - Knowledge Base Connector

Bidirectional integration with the Evolving Knowledge Base.
"""

import json
import re
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

from workflows.engine.models import StepDefinition, WorkflowResult


# ═══════════════════════════════════════════════════════════════
# DATA MODELS
# ═══════════════════════════════════════════════════════════════

@dataclass
class KnowledgeItem:
    """A single piece of knowledge from the KB."""
    type: str  # project, pattern, learning, prompt, idea
    name: str
    path: Path
    content: str
    tags: List[str] = field(default_factory=list)
    confidence: Optional[int] = None
    relevance_score: float = 0.0

    @property
    def brief(self) -> str:
        """Get first 200 chars as brief."""
        return self.content[:200].strip() + "..." if len(self.content) > 200 else self.content


@dataclass
class AgentInfo:
    """Information about an available agent."""
    name: str
    path: Path
    description: str
    type: str = "specialist-agent"
    complexity: str = "high"
    tags: List[str] = field(default_factory=list)


@dataclass
class FrameworkInfo:
    """Information about a framework."""
    name: str
    path: Path
    description: str
    modes: List[str] = field(default_factory=list)


@dataclass
class Link:
    """A discovered link between entities."""
    source_type: str
    source_name: str
    target_type: str
    target_name: str
    relationship: str
    confidence: float = 0.0


@dataclass
class Suggestion:
    """A suggestion for connections."""
    message: str
    links: List[Link]
    priority: str = "medium"


@dataclass
class Learning:
    """A learning extracted from workflow execution."""
    title: str
    content: str
    source_workflow: str
    source_step: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    confidence: int = 80
    timestamp: datetime = field(default_factory=datetime.now)


# ═══════════════════════════════════════════════════════════════
# KNOWLEDGE BASE PATHS
# ═══════════════════════════════════════════════════════════════

def get_kb_root() -> Path:
    """Get the knowledge base root directory."""
    return Path("knowledge")


def get_agents_path() -> Path:
    """Get the agents directory."""
    return Path(".claude/agents")


def get_prompts_path() -> Path:
    """Get the prompts directory."""
    return get_kb_root() / "prompts"


def get_patterns_path() -> Path:
    """Get the patterns directory."""
    return get_kb_root() / "patterns"


def get_learnings_path() -> Path:
    """Get the learnings directory."""
    return get_kb_root() / "learnings"


def get_ideas_path() -> Path:
    """Get the ideas directory."""
    return Path("ideas")


# ═══════════════════════════════════════════════════════════════
# PROMPT REGISTRY
# ═══════════════════════════════════════════════════════════════

class PromptRegistry:
    """Access to the prompt library."""

    def __init__(self, prompts_path: Optional[Path] = None):
        self.prompts_path = prompts_path or get_prompts_path()
        self._cache: Dict[str, Dict] = {}
        self._load_registry()

    def _load_registry(self):
        """Load prompt registry index."""
        index_path = self.prompts_path / "index.json"
        if index_path.exists():
            self._cache = json.loads(index_path.read_text())
        else:
            # Build from files
            self._build_registry()

    def _build_registry(self):
        """Build registry by scanning prompt files."""
        if not self.prompts_path.exists():
            return

        for prompt_file in self.prompts_path.rglob("*.md"):
            if prompt_file.name.startswith("_"):
                continue

            content = prompt_file.read_text()
            metadata = self._extract_metadata(content)

            self._cache[prompt_file.stem] = {
                "name": prompt_file.stem,
                "path": str(prompt_file.relative_to(self.prompts_path)),
                "type": metadata.get("type", "unknown"),
                "description": metadata.get("description", ""),
                "tags": metadata.get("tags", []),
                "confidence": metadata.get("confidence", 0),
            }

    def _extract_metadata(self, content: str) -> Dict[str, Any]:
        """Extract metadata from prompt content."""
        metadata = {}

        # Look for YAML frontmatter or structured comments
        if content.startswith("---"):
            end = content.find("---", 3)
            if end > 0:
                import yaml
                try:
                    metadata = yaml.safe_load(content[3:end]) or {}
                except Exception:
                    pass

        # Look for inline metadata
        type_match = re.search(r'\*\*Type\*\*:\s*(.+)', content)
        if type_match:
            metadata["type"] = type_match.group(1).strip()

        conf_match = re.search(r'\*\*Confidence\*\*:\s*(\d+)', content)
        if conf_match:
            metadata["confidence"] = int(conf_match.group(1))

        return metadata

    def get_agent(self, name: str) -> Optional[AgentInfo]:
        """Get agent by name."""
        agent_path = get_agents_path() / f"{name}.md"
        if not agent_path.exists():
            # Try without -agent suffix
            agent_path = get_agents_path() / f"{name}-agent.md"

        if not agent_path.exists():
            return None

        content = agent_path.read_text()
        first_line = content.split("\n")[0].replace("#", "").strip()

        return AgentInfo(
            name=name,
            path=agent_path,
            description=first_line,
            tags=self._extract_tags(content),
        )

    def get_framework(self, name: str) -> Optional[FrameworkInfo]:
        """Get framework by name."""
        framework_path = self.prompts_path / "frameworks" / f"{name}.md"
        if not framework_path.exists():
            return None

        content = framework_path.read_text()
        first_line = content.split("\n")[0].replace("#", "").strip()

        # Extract modes if present
        modes = []
        modes_match = re.search(r'modes?:\s*\[([^\]]+)\]', content.lower())
        if modes_match:
            modes = [m.strip() for m in modes_match.group(1).split(",")]

        return FrameworkInfo(
            name=name,
            path=framework_path,
            description=first_line,
            modes=modes,
        )

    def list_agents(self) -> List[AgentInfo]:
        """List all available agents."""
        agents_path = get_agents_path()
        if not agents_path.exists():
            return []

        agents = []
        for agent_file in agents_path.glob("*-agent.md"):
            agent = self.get_agent(agent_file.stem.replace("-agent", ""))
            if agent:
                agents.append(agent)

        return agents

    def list_frameworks(self) -> List[FrameworkInfo]:
        """List all available frameworks."""
        frameworks_path = self.prompts_path / "frameworks"
        if not frameworks_path.exists():
            return []

        frameworks = []
        for fw_file in frameworks_path.glob("*.md"):
            if fw_file.name.startswith("_") or fw_file.name == "README.md":
                continue
            fw = self.get_framework(fw_file.stem)
            if fw:
                frameworks.append(fw)

        return frameworks

    def get_by_confidence(self, min_confidence: int = 90) -> List[Dict]:
        """Get prompts with confidence >= threshold."""
        return [
            p for p in self._cache.values()
            if p.get("confidence", 0) >= min_confidence
        ]

    def get_by_domain(self, domain: str) -> List[Dict]:
        """Get prompts matching a domain tag."""
        domain_lower = domain.lower()
        return [
            p for p in self._cache.values()
            if domain_lower in [t.lower() for t in p.get("tags", [])]
        ]

    def _extract_tags(self, content: str) -> List[str]:
        """Extract tags from content."""
        tags = []
        tags_match = re.search(r'\*\*Tags?\*\*:\s*(.+)', content)
        if tags_match:
            tags = [t.strip() for t in tags_match.group(1).split(",")]
        return tags


# ═══════════════════════════════════════════════════════════════
# KNOWLEDGE CONNECTOR
# ═══════════════════════════════════════════════════════════════

class KnowledgeConnector:
    """
    Bidirectional Knowledge Base Integration.

    Provides:
    - Context injection: KB → Workflow (inject relevant knowledge)
    - Learning extraction: Workflow → KB (extract and store learnings)
    - Link discovery: Find connections between entities
    - Agent/Framework discovery: Find suitable agents for tasks
    """

    def __init__(self, kb_path: Optional[Path] = None):
        self.kb_path = kb_path or get_kb_root()
        self.prompt_registry = PromptRegistry()
        self._patterns_cache: Optional[List[KnowledgeItem]] = None

    # ─────────────────────────────────────────────────────────────
    # CONTEXT INJECTION: KB → Workflow
    # ─────────────────────────────────────────────────────────────

    async def inject_context(self, step: StepDefinition) -> str:
        """
        Inject relevant knowledge into a step.

        Args:
            step: The step to inject context for

        Returns:
            Formatted context string to prepend to prompts
        """
        relevant = await self._find_relevant_knowledge(step)

        if not relevant:
            return ""

        # Format context
        context_parts = ["## Relevant Context\n"]

        for item in relevant[:5]:  # Limit to top 5
            context_parts.append(f"### {item.type.title()}: {item.name}")
            context_parts.append(item.brief)
            if item.confidence:
                context_parts.append(f"*Confidence: {item.confidence}%*")
            context_parts.append("")

        return "\n".join(context_parts)

    async def _find_relevant_knowledge(
        self, step: StepDefinition
    ) -> List[KnowledgeItem]:
        """Find knowledge relevant to a step."""
        relevant = []

        # Extract keywords from step
        keywords = self._extract_keywords(step)

        if not keywords:
            return []

        # Search patterns
        for pattern in self._get_patterns():
            score = self._calculate_relevance(pattern, keywords)
            if score > 0.3:
                pattern.relevance_score = score
                relevant.append(pattern)

        # Search learnings
        for learning in self._get_learnings():
            score = self._calculate_relevance(learning, keywords)
            if score > 0.3:
                learning.relevance_score = score
                relevant.append(learning)

        # Sort by relevance
        relevant.sort(key=lambda x: x.relevance_score, reverse=True)
        return relevant

    def _extract_keywords(self, step: StepDefinition) -> Set[str]:
        """Extract keywords from step definition."""
        keywords = set()

        text_sources = [
            step.name,
            step.description or "",
            step.prompt or "",
            step.agent or "",
            step.framework or "",
        ]

        for text in text_sources:
            if text:
                # Simple tokenization
                words = re.findall(r'\b\w{4,}\b', text.lower())
                keywords.update(words)

        return keywords

    def _calculate_relevance(
        self, item: KnowledgeItem, keywords: Set[str]
    ) -> float:
        """Calculate relevance score between item and keywords."""
        item_text = f"{item.name} {item.content}".lower()
        item_words = set(re.findall(r'\b\w{4,}\b', item_text))

        if not item_words:
            return 0.0

        # Jaccard similarity
        intersection = len(keywords & item_words)
        union = len(keywords | item_words)

        return intersection / union if union > 0 else 0.0

    # ─────────────────────────────────────────────────────────────
    # LEARNING EXTRACTION: Workflow → KB
    # ─────────────────────────────────────────────────────────────

    async def extract_learnings(
        self, workflow_result: WorkflowResult
    ) -> List[Learning]:
        """
        Extract learnings from workflow execution.

        Args:
            workflow_result: Completed workflow result

        Returns:
            List of extracted learnings
        """
        learnings = []

        # Only extract from successful workflows
        if not workflow_result.success:
            return learnings

        # Look for patterns in step results
        for step_name, result in workflow_result.step_results.items():
            if isinstance(result, str):
                learning = self._identify_learning(
                    result, workflow_result.workflow_name, step_name
                )
                if learning:
                    learnings.append(learning)

        return learnings

    def _identify_learning(
        self,
        content: str,
        workflow_name: str,
        step_name: str,
    ) -> Optional[Learning]:
        """Identify if content contains a learning."""
        # Look for explicit learning markers
        learning_patterns = [
            r"(?:learned|learning|insight|takeaway):\s*(.+)",
            r"(?:key finding|important):\s*(.+)",
            r"(?:best practice|pattern):\s*(.+)",
        ]

        for pattern in learning_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                return Learning(
                    title=f"Learning from {step_name}",
                    content=match.group(1).strip(),
                    source_workflow=workflow_name,
                    source_step=step_name,
                    confidence=75,
                )

        return None

    async def store_learning(self, learning: Learning) -> Path:
        """
        Store a learning in the knowledge base.

        Args:
            learning: The learning to store

        Returns:
            Path to the created file
        """
        learnings_path = get_learnings_path()
        learnings_path.mkdir(parents=True, exist_ok=True)

        # Generate filename
        date_str = learning.timestamp.strftime("%Y-%m-%d")
        slug = re.sub(r'[^a-z0-9]+', '-', learning.title.lower())[:50]
        filename = f"{date_str}-{slug}.md"

        filepath = learnings_path / filename

        # Format content
        content = f"""# {learning.title}

**Source**: {learning.source_workflow}
**Step**: {learning.source_step or 'N/A'}
**Confidence**: {learning.confidence}%
**Date**: {learning.timestamp.strftime('%Y-%m-%d %H:%M')}

## Content

{learning.content}

## Tags

{', '.join(learning.tags) if learning.tags else 'auto-extracted'}
"""

        filepath.write_text(content)
        return filepath

    # ─────────────────────────────────────────────────────────────
    # LINK DISCOVERY
    # ─────────────────────────────────────────────────────────────

    async def find_links(self, content: str) -> List[Link]:
        """
        Find links between content and KB entities.

        Args:
            content: Text content to analyze

        Returns:
            List of discovered links
        """
        links = []

        # Extract entity mentions
        entities = self._extract_entities(content)

        for entity_type, entity_name in entities:
            # Find matches in KB
            matches = await self._find_matches(entity_type, entity_name)
            for match in matches:
                links.append(Link(
                    source_type="content",
                    source_name="workflow_output",
                    target_type=match["type"],
                    target_name=match["name"],
                    relationship="mentions",
                    confidence=match.get("confidence", 0.5),
                ))

        return links

    def _extract_entities(self, content: str) -> List[tuple]:
        """Extract entity mentions from content."""
        entities = []

        # Look for idea references
        idea_matches = re.findall(r'idea[_-]?(\d{4}[_-]\d{3})', content.lower())
        for match in idea_matches:
            entities.append(("idea", match))

        # Look for project references
        project_patterns = [
            r'(?:project|projekt):\s*(\w+)',
            r'(?:evolving)',
        ]
        for pattern in project_patterns:
            matches = re.findall(pattern, content.lower())
            for match in matches:
                entities.append(("project", match))

        # Look for pattern references
        pattern_matches = re.findall(r'pattern:\s*(\w+[-\w]*)', content.lower())
        for match in pattern_matches:
            entities.append(("pattern", match))

        return entities

    async def _find_matches(
        self, entity_type: str, entity_name: str
    ) -> List[Dict]:
        """Find KB matches for an entity."""
        matches = []

        if entity_type == "idea":
            ideas_index = get_ideas_path() / "index.json"
            if ideas_index.exists():
                ideas = json.loads(ideas_index.read_text())
                for idea in ideas:
                    if entity_name in idea.get("id", ""):
                        matches.append({
                            "type": "idea",
                            "name": idea.get("title", entity_name),
                            "confidence": 0.9,
                        })

        elif entity_type == "pattern":
            for pattern in self._get_patterns():
                if entity_name.lower() in pattern.name.lower():
                    matches.append({
                        "type": "pattern",
                        "name": pattern.name,
                        "confidence": 0.8,
                    })

        elif entity_type == "project":
            projects_path = self.kb_path / "projects"
            if projects_path.exists():
                for project_dir in projects_path.iterdir():
                    if project_dir.is_dir() and entity_name in project_dir.name.lower():
                        matches.append({
                            "type": "project",
                            "name": project_dir.name,
                            "confidence": 0.85,
                        })

        return matches

    async def suggest_connections(
        self, workflow_result: WorkflowResult
    ) -> List[Suggestion]:
        """
        Suggest connections based on workflow results.

        Args:
            workflow_result: Completed workflow

        Returns:
            List of connection suggestions
        """
        suggestions = []

        # Analyze all step results
        all_content = ""
        for result in workflow_result.step_results.values():
            if isinstance(result, str):
                all_content += result + "\n"

        links = await self.find_links(all_content)

        if links:
            suggestions.append(Suggestion(
                message=f"Found {len(links)} potential connections",
                links=links,
                priority="medium" if len(links) < 5 else "high",
            ))

        return suggestions

    # ─────────────────────────────────────────────────────────────
    # AGENT & FRAMEWORK DISCOVERY
    # ─────────────────────────────────────────────────────────────

    def discover_agents(self, domain: str) -> List[AgentInfo]:
        """
        Find agents suitable for a domain.

        Args:
            domain: Domain to search for (e.g., "idea", "research")

        Returns:
            List of matching agents
        """
        agents = self.prompt_registry.list_agents()
        domain_lower = domain.lower()

        matching = []
        for agent in agents:
            # Check name
            if domain_lower in agent.name.lower():
                matching.append(agent)
                continue

            # Check description
            if domain_lower in agent.description.lower():
                matching.append(agent)
                continue

            # Check tags
            if any(domain_lower in tag.lower() for tag in agent.tags):
                matching.append(agent)

        return matching

    def get_framework(self, name: str) -> Optional[FrameworkInfo]:
        """Get framework info by name."""
        return self.prompt_registry.get_framework(name)

    def get_agent(self, name: str) -> Optional[AgentInfo]:
        """Get agent info by name."""
        return self.prompt_registry.get_agent(name)

    # ─────────────────────────────────────────────────────────────
    # INTERNAL HELPERS
    # ─────────────────────────────────────────────────────────────

    def _get_patterns(self) -> List[KnowledgeItem]:
        """Get all patterns from KB."""
        if self._patterns_cache is not None:
            return self._patterns_cache

        patterns = []
        patterns_path = get_patterns_path()

        if patterns_path.exists():
            for pattern_file in patterns_path.glob("*.md"):
                if pattern_file.name.startswith("_") or pattern_file.name == "README.md":
                    continue

                content = pattern_file.read_text()
                patterns.append(KnowledgeItem(
                    type="pattern",
                    name=pattern_file.stem,
                    path=pattern_file,
                    content=content,
                    confidence=self._extract_confidence(content),
                ))

        self._patterns_cache = patterns
        return patterns

    def _get_learnings(self) -> List[KnowledgeItem]:
        """Get all learnings from KB."""
        learnings = []
        learnings_path = get_learnings_path()

        if learnings_path.exists():
            for learning_file in learnings_path.glob("*.md"):
                if learning_file.name.startswith("_") or learning_file.name == "README.md":
                    continue

                content = learning_file.read_text()
                learnings.append(KnowledgeItem(
                    type="learning",
                    name=learning_file.stem,
                    path=learning_file,
                    content=content,
                    confidence=self._extract_confidence(content),
                ))

        return learnings

    def _extract_confidence(self, content: str) -> Optional[int]:
        """Extract confidence from content."""
        match = re.search(r'\*\*Confidence\*\*:\s*(\d+)', content)
        if match:
            return int(match.group(1))
        return None


# ═══════════════════════════════════════════════════════════════
# AUTO-LINK DISCOVERY
# ═══════════════════════════════════════════════════════════════

class AutoLinkDiscovery:
    """
    Automatically discovers links between workflow outputs and KB.

    Used for:
    - Finding related patterns
    - Connecting to existing ideas
    - Suggesting knowledge updates
    """

    def __init__(self, connector: Optional[KnowledgeConnector] = None):
        self.connector = connector or KnowledgeConnector()

    async def analyze(self, content: str) -> Dict[str, Any]:
        """
        Analyze content for KB connections.

        Args:
            content: Content to analyze

        Returns:
            Analysis results with links and suggestions
        """
        links = await self.connector.find_links(content)

        return {
            "links": [
                {
                    "source": f"{link.source_type}:{link.source_name}",
                    "target": f"{link.target_type}:{link.target_name}",
                    "relationship": link.relationship,
                    "confidence": link.confidence,
                }
                for link in links
            ],
            "summary": f"Found {len(links)} connections",
        }

    async def suggest_updates(self, workflow_result: WorkflowResult) -> List[Dict]:
        """
        Suggest KB updates based on workflow results.

        Args:
            workflow_result: Completed workflow

        Returns:
            List of suggested updates
        """
        suggestions = []

        # Check for new patterns
        if "pattern" in workflow_result.workflow_name.lower():
            suggestions.append({
                "type": "new_pattern",
                "message": "Consider documenting this pattern",
                "priority": "medium",
            })

        # Check for learnings
        learnings = await self.connector.extract_learnings(workflow_result)
        for learning in learnings:
            suggestions.append({
                "type": "new_learning",
                "message": f"Learning identified: {learning.title}",
                "content": learning.content,
                "priority": "low",
            })

        return suggestions
