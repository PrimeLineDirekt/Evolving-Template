# Ultrathink: Software Craftsmanship Principles

**Quelle**: Session 2025-12-16 - Dashboard Refactoring
**Typ**: Technical Learning
**Tags**: design-system, architecture, craftsmanship

---

## Core Philosophy

> "The goal is not just working code, but maintainable, elegant, and intentional design."

### 1. Foundation First

Bevor man Features baut, muss das Fundament stimmen:
- **Design Tokens** definieren (Farben, Spacing, Typografie)
- **Utility Functions** für wiederkehrende Patterns
- **Component Library** als Basis für alle UI-Elemente

### 2. Single Source of Truth

Keine Duplikation von Styling-Logic:
- Farbdefinitionen an EINER Stelle (`tokens.ts`)
- Varianten-Styling zentral definiert
- Components nutzen shared utilities

### 3. Composition over Configuration

Kleine, fokussierte Components die sich kombinieren lassen:
```tsx
// Statt einer "mega" Card mit 20 Props:
<Card variant="accent" accent="blue">
  <CardHeader>
    <CardTitle>Titel</CardTitle>
    <CardDescription>Beschreibung</CardDescription>
  </CardHeader>
  <CardContent>...</CardContent>
</Card>
```

### 4. Semantic Naming

Namen die Intent kommunizieren:
- `getAccentClasses(color, variant)` statt `getStyles()`
- `StatusBadge` vs generische `Badge`
- `CardHeader` macht klar wo es hingehört

### 5. Progressive Enhancement

Starte einfach, erweitere bei Bedarf:
- Basis-Komponente funktioniert ohne Props
- Optionale Props für Customization
- Variants für häufige Use Cases

---

## Implementierte Patterns

### Design System Struktur

```
lib/design-system/
├── tokens.ts      # Farben, AccentColor Type
├── utils.ts       # cn(), getAccentClasses(), etc.
└── index.ts       # Zentrale Exports
```

### Component Pattern

```typescript
interface ComponentProps {
  variant?: 'default' | 'accent';
  accent?: AccentColor;
  className?: string;
  children: React.ReactNode;
}

export function Component({
  variant = 'default',
  accent = 'blue',
  className,
  children
}: ComponentProps) {
  return (
    <div className={cn(
      'base-styles',
      variant === 'accent' && getAccentClasses(accent),
      className
    )}>
      {children}
    </div>
  );
}
```

### Utility Function Pattern

```typescript
export function getAccentClasses(
  color: AccentColor,
  variant?: 'default' | 'tile' | 'badge'
): string {
  const config = accentColors[color];

  switch (variant) {
    case 'tile':
      return cn(config.bg, config.border, 'hover:...');
    case 'badge':
      return cn(config.badge);
    default:
      return cn(config.bg, config.border);
  }
}
```

---

## Angewandt auf Dashboard

| Vorher | Nachher |
|--------|---------|
| colorMap in jeder Komponente | Zentrale `accentColors` in tokens.ts |
| Inline Tailwind überall | `getAccentClasses()` utility |
| Dunkles Theme hardcoded | Light Theme mit konsistenten Tokens |
| Redundante Button-Styles | `<Button variant="primary">` |
| Unstrukturierte Cards | `Card`, `CardHeader`, `CardContent` |

---

## Key Takeaways

1. **Invest in Foundation**: 30 Min für Design System spart Stunden später
2. **DRY für Styling**: Keine color-maps in einzelnen Components
3. **Type Safety**: AccentColor Type verhindert Typos
4. **Consistency**: Alle Components nutzen dieselben Tokens
5. **Light Theme = Professional**: Helle, einladende UIs sind Standard

---

## Related

- [Design System Tokens](/dashboard/src/lib/design-system/tokens.ts)
- [UI Components](/dashboard/src/components/ui/)
- [TileGrid Refactoring](../projects/evolving-dashboard/)
