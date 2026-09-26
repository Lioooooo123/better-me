# iOS Colors & Theming Reference

Use semantic colors for content hierarchy and backgrounds, then verify their appearance with the product's supported light, dark, and accessibility settings. The examples below show additional layering tokens.

## Extra Semantic Tokens (beyond the core set)

For multi-level hierarchy and grouped layouts, reach past the core six:

```swift
Color(.tertiaryLabel)              // 3rd-level text (placeholders, disabled)
Color(.quaternaryLabel)            // 4th-level (separators, faint glyphs)
Color(.secondarySystemBackground)  // elevated cards / grouped table sections
Color(.tertiarySystemBackground)   // a layer above secondary
Color(.systemGroupedBackground)    // base behind grouped lists (Settings style)
Color(.separator)                  // hairline dividers (already mode-aware)
```

Use the grouped-background family for `.insetGrouped` lists; use the plain `systemBackground` family for full-bleed content.

## Color Contrast (full WCAG table)

Common WCAG contrast thresholds are shown below. Verify the applicable standard and the actual rendered contrast; system color names alone do not prove compliance.

| Content | Minimum ratio |
|---------|---------------|
| Normal text (< 18pt, or < 14pt bold) | 4.5:1 |
| Large text (>= 18pt, or >= 14pt bold) | 3:1 |
| UI components and graphical objects (icons, control borders, focus rings) | 3:1 |

Verify with Xcode's Accessibility Inspector color contrast check, in both light and dark modes and with Increase Contrast enabled.
