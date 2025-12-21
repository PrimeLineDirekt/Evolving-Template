# Observation Compression Pattern

> **Source**: thedotmack/claude-mem
> **Type**: Token Efficiency Pattern
> **Problem**: Tool Outputs verbrauchen zu viele Tokens im Context Window
> **Solution**: AI-gestützte Kompression zu semantischen Observations

## Das Problem

```
Standard Claude Code Session:
- Tool Output: ~2000-10000 Tokens pro Ausführung
- 50 Tool Uses = Context Window erschöpft
- Komplexität: O(N²) - Claude re-synthetisiert alle vorherigen Outputs
```

## Die Lösung

```
Tool Output (~5000 Tokens)
         ↓
    AI Compression
         ↓
Observation (~500 Tokens)
         ↓
75-95% Token-Reduktion
```

## Observation Struktur

### Minimales Model

```typescript
interface Observation {
  id: string;
  type: 'decision' | 'bugfix' | 'feature' | 'refactor' | 'discovery' | 'change';
  title: string;           // ~10 Tokens
  subtitle?: string;       // ~20 Tokens
  narrative?: string;      // ~100-200 Tokens
  facts?: string[];        // ~100-200 Tokens
  files?: string[];        // ~20 Tokens
  timestamp: number;
}
```

### Token Budget

| Feld | Max Tokens | Zweck |
|------|------------|-------|
| title | 15 | Einzeiler-Summary |
| subtitle | 30 | Zusätzlicher Kontext |
| narrative | 200 | Was passiert ist |
| facts | 200 | Key Takeaways |
| files | 30 | Betroffene Dateien |
| **Total** | **~475** | **Pro Observation** |

## Compression Prompt

### System Prompt

```
Du bist ein Observer der Tool-Ausführungen in semantische Observations komprimiert.

REGELN:
1. Fokus auf DELIVERABLES: Was wurde GEBAUT/GEFIXT/GELERNT?
2. NICHT dokumentieren was du tust, sondern was passiert ist
3. Verwende Action Verbs: implemented, fixed, deployed, configured
4. Max 500 Tokens pro Observation

GUTE Observation: "Authentication unterstützt jetzt OAuth2 mit Google Provider"
SCHLECHTE Observation: "Ich habe mir den Auth-Code angesehen"
```

### Input Format

```xml
<tool_execution>
  <tool_name>Edit</tool_name>
  <timestamp>2025-12-16T14:30:00Z</timestamp>
  <working_directory>/project/src</working_directory>
  <input>
    {"file_path": "auth/oauth.ts", "old_string": "...", "new_string": "..."}
  </input>
  <outcome>
    File edited successfully. Added OAuth2 configuration...
  </outcome>
</tool_execution>
```

### Output Format

```xml
<observation>
  <type>feature</type>
  <title>Added OAuth2 authentication with Google provider</title>
  <subtitle>Passport.js integration for social login</subtitle>
  <narrative>
    Implemented OAuth2 support using passport-google-oauth20.
    Users can now sign in with their Google accounts.
  </narrative>
  <facts>
    - Created auth/oauth.ts with passport configuration
    - Added GOOGLE_CLIENT_ID to environment
    - Extended User model with provider field
  </facts>
  <files>src/auth/oauth.ts, src/models/user.ts</files>
</observation>
```

## Token-Berechnung

```typescript
const CHARS_PER_TOKEN = 4;

function estimateTokens(text: string): number {
  return Math.ceil(text.length / CHARS_PER_TOKEN);
}

function calculateObservationCost(obs: Observation): number {
  const content = [
    obs.title,
    obs.subtitle || '',
    obs.narrative || '',
    (obs.facts || []).join(' '),
    (obs.files || []).join(', ')
  ].join(' ');

  return estimateTokens(content);
}
```

## Wann komprimieren?

### Immer komprimieren

- Write/Edit Tool Outputs (oft sehr lang)
- Bash Command Outputs (können riesig sein)
- Read Tool für große Dateien
- Search Results mit vielen Matches

### Nicht komprimieren

- Kurze Outputs (< 200 Tokens)
- User-generierte Inhalte (Privacy)
- Fehler-Details (für Debugging wichtig)

## Integration in Evolving

### Möglicher Hook: observation-compression.sh

```bash
#!/bin/bash
# PostToolUse Hook für Observation Compression

read -r input

tool_name=$(echo "$input" | jq -r '.tool_name')
tool_output=$(echo "$input" | jq -r '.tool_response')

# Nur für bestimmte Tools
case "$tool_name" in
  Write|Edit|Bash)
    # Token-Schätzung
    tokens=$(echo "$tool_output" | wc -c)
    tokens=$((tokens / 4))

    if [ "$tokens" -gt 500 ]; then
      # Kompression triggern
      echo '{"compress": true, "estimated_tokens": '$tokens'}'
    fi
    ;;
esac
```

### Mögliche Experience-Erweiterung

```json
{
  "type": "observation",
  "compressed_from": "Edit tool output",
  "original_tokens": 2500,
  "compressed_tokens": 450,
  "compression_ratio": "82%"
}
```

## Endless Mode Konzept

Mit konsequenter Observation Compression:

```
Standard Mode:
  Full Context → O(N²) → ~50 Tool Uses

Endless Mode:
  Compressed Observations → O(N) → ~1000+ Tool Uses
  Full Outputs → Archived to Disk
```

### Vorteile

- **~95% Token-Reduktion** pro Tool Use
- **~20x mehr Tool Uses** pro Session
- **Lineare Skalierung** statt quadratisch
- **Vollständige History** auf Disk verfügbar

## Best Practices

1. **Budget einhalten**: Max 500 Tokens pro Observation
2. **Deliverable-fokussiert**: Was wurde erreicht, nicht was getan
3. **Strukturiert**: XML/JSON für einfaches Parsing
4. **Typisiert**: Observation Types für Filterung
5. **File-Referenzen**: Immer betroffene Dateien nennen

## Vergleich: Vorher/Nachher

### Vorher (Full Output)

```
Tool: Edit
File: src/auth/oauth.ts
Diff:
-// TODO: Add OAuth
+import passport from 'passport';
+import { Strategy as GoogleStrategy } from 'passport-google-oauth20';
+
+passport.use(new GoogleStrategy({
+    clientID: process.env.GOOGLE_CLIENT_ID,
+    clientSecret: process.env.GOOGLE_CLIENT_SECRET,
+    callbackURL: "/auth/google/callback"
+  },
+  function(accessToken, refreshToken, profile, cb) {
+    User.findOrCreate({ googleId: profile.id }, function (err, user) {
+      return cb(err, user);
+    });
+  }
+));
+
+export const googleAuth = passport.authenticate('google', { scope: ['profile', 'email'] });
+export const googleCallback = passport.authenticate('google', { failureRedirect: '/login' });

~1200 Tokens
```

### Nachher (Compressed Observation)

```
[feature] OAuth2 authentication with Google
- Added passport-google-oauth20 integration
- Created googleAuth and googleCallback exports
- Uses GOOGLE_CLIENT_ID from environment
Files: src/auth/oauth.ts

~80 Tokens (93% Reduktion)
```

---

## Related

- `knowledge/learnings/claude-mem-persistent-memory.md` - Source Analysis
- `knowledge/patterns/progressive-disclosure-pattern.md` - Companion Pattern
- `.claude/hooks/` - Hook Implementation Location
