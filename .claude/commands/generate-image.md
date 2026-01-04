# /generate-image

Generiere Bilder mit FAL.ai Nano Banana Pro.

## Trigger-Patterns
- "erstelle ein bild"
- "generiere ein bild"
- "bild erstellen"
- "create an image"
- "mach ein bild von"

## Model: sonnet

## Workflow

1. **Content Understanding**
   - Analysiere User-Input auf Stil-Signale
   - Erkenne Intent (Infografik, Product Shot, Portrait, etc.)
   - Empfehle passenden Stil falls nicht explizit

2. **Prompt Enhancement** (ICS Framework)
   - **I**mage Type: Art des Bildes definieren
   - **C**ontent: Subjekt, Aktion, Environment, Details
   - **S**tyle: Ästhetik, Lighting, Mood, Colors

3. **Photography Layer** (für fotorealistische Bilder)
   - Camera/Lens (z.B. "85mm at f/2.8")
   - Lighting Setup (z.B. "golden hour", "three-point softbox")
   - Composition (z.B. "rule of thirds", "negative space")

4. **Quality Check**
   - Kein Tag Soup (Komma-Listen vermeiden)
   - Narrative Beschreibung statt Keywords
   - Spezifische Details statt vage Begriffe

5. **Generation**
   ```bash
   python3 .claude/scripts/fal_generate.py "ENHANCED_PROMPT" --aspect RATIO
   ```

6. **Output**
   - Bild anzeigen
   - Kosten nennen ($0.15/Bild)
   - Prompt dokumentieren
   - Metadata-JSON erstellt

## Aspect Ratios

| Ratio | Use Case |
|-------|----------|
| 1:1 | Instagram Feed, Profile |
| 4:5 | Instagram Portrait, Etsy |
| 16:9 | YouTube, Presentations |
| 9:16 | Stories, Reels, TikTok |

## Beispiel

```
User: "Erstelle ein Bild für meinen Kaffee-Blog"

Claude:
1. Erkennt: "blog" → Editorial Style
2. Enhanced Prompt:
   "Editorial lifestyle photograph of an artisan latte
    with intricate foam art, served in a handcrafted
    ceramic cup on a rustic wooden table. Morning
    sunlight streaming through a nearby window,
    shot with 50mm lens at f/2.8, shallow depth of field,
    warm and inviting color palette."
3. Generiert Bild
4. Zeigt: Bild + Kosten ($0.15) + Prompt
```

## Related

- Agent: `.claude/agents/fal-image-generator-agent.md`
- Script: `.claude/scripts/fal_generate.py`
- Stats: `python3 .claude/scripts/fal_generate.py --stats`
