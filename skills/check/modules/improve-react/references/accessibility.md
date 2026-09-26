# 3. Accessibility

This category covers whether keyboard, screen-reader, zoom, and other assistive
technology users can discover and operate the interface. Leverage is highest on
primary navigation, forms, dialogs, and controls used in every session; verify
the semantic and interaction context rather than blindly silencing a rule.

**Hunt for:**

- `alt-text` — Image missing alt text.
- `control-has-associated-label` — Control missing accessible label.
- `click-events-have-key-events` — Click handler missing keyboard handler.
- `no-static-element-interactions` — Interaction on static element.
- `prefer-tag-over-role` — Role used instead of the native HTML tag.
- `no-autofocus` — Autofocus on an element.
- `no-outline-none` — `outline:none` removes the focus ring.
- `no-disabled-zoom` — Zoom disabled on the viewport.

**Beyond the scan:** Test the actual tab order, focus return after dialogs,
keyboard escape and roving focus, live-region announcements, loading and error
states, contrast in real themes, reduced motion, touch target size, and zoom at
200–400%. A valid static label can still be misleading in the product flow.
