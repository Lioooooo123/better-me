# iOS Typography Reference

Use semantic text styles and the product's typography system. Validate readability at supported Dynamic Type sizes; do not apply a universal point-size, line-height, or line-length rule. Verify version-sensitive values against current Apple documentation when exact values matter.

## System Font: San Francisco

iOS uses San Francisco (SF Pro) as the default typeface. Always reach the styles through semantic APIs (`.font(.title)`, `.font(.body)`, `.font(.caption)`) so Dynamic Type scaling and these colors apply automatically — never hardcode the point sizes or hex values below.

## Light-Mode Color Values

The values below are illustrative historical examples, not a platform contract. Semantic colors depend on appearance and accessibility settings; use the system APIs rather than copying these values.

| Element | Semantic style | Color (light) |
|---------|----------------|---------------|
| Large Title / Title / Body | `.largeTitle` `.title` `.body` | `#000000` (label) |
| Secondary text | `.subheadline` + `.secondary` | `#3C3C43` @ 60% (secondaryLabel) |
| Caption / Tertiary | `.caption` + `.secondary` | `#3C3C43` @ 60% |
| Tab bar labels (unselected) | 10pt | `#8A8A8E` (tertiaryLabel) |

```swift
Text("Caption")
    .font(.caption)
    .foregroundColor(.secondary)   // resolves to secondaryLabel in both modes
```

## Dark Mode Color Mapping

Semantic styles flip automatically; this is the mapping they apply so you can verify a custom color matches it:

- Primary text `#000000` -> `#FFFFFF` (label)
- Secondary/tertiary gray -> lighter gray at the same opacity (secondaryLabel/tertiaryLabel)
- Backgrounds shift darker while preserving the relative hierarchy between layers

If you define a custom text color, put light/dark variants in the Asset Catalog so it follows this mapping instead of staying fixed.
