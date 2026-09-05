# iOS Accessibility

## VoiceOver Support

Every interactive element needs an accessible name. Prefer native labels; add explicit labels when the visible content does not convey the action.

```swift
// Accessible label (what it is)
Image(systemName: "heart.fill")
    .accessibilityLabel("Favorite")

// Accessible value (current state)
Slider(value: $volume)
    .accessibilityLabel("Volume")
    .accessibilityValue("\(Int(volume * 100))%")

// Accessible hint (what it does)
Button("Share") { share() }
    .accessibilityHint("Shares this item with others")

// Group related elements
HStack {
    Image(systemName: "person")
    Text("John Doe")
}
.accessibilityElement(children: .combine)
```

## Dynamic Type

Support user font size preferences:

```swift
// Use semantic text styles (automatically scales)
Text("Content")
    .font(.body)

// For custom fonts, scale with Dynamic Type
@ScaledMetric var customSize: CGFloat = 16

Text("Custom")
    .font(.system(size: customSize))
```

## High Contrast Mode

```swift
@Environment(\.colorSchemeContrast) var contrast

var textColor: Color {
    contrast == .increased ? .primary : .secondary
}
```

## Accessibility Checklist

- [ ] Meaningful images have useful accessible descriptions; decorative images are hidden from accessibility, and images inside labeled controls do not duplicate their labels
- [ ] Touch targets are minimum 44×44pt
- [ ] Text scales with Dynamic Type
- [ ] Color contrast meets WCAG standards
- [ ] Motion can be reduced
- [ ] VoiceOver navigation is logical
- [ ] Don't rely solely on color to convey meaning
