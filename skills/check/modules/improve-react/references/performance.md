# 2. Performance

This category covers work repeated in render, layout, the main thread, or the
network. Leverage is impact multiplied by frequency and fan-out: a per-keystroke
editor, provider, or 10,000-row list outranks the same pattern in a settings
dialog. Do not optimize cold paths merely because a rule can be satisfied.

**Hunt for:**

- `jsx-no-constructed-context-values` — Unstable context provider value; all
  consumers can re-render when the provider renders.
- `jsx-no-new-object-as-prop` — New object passed as a prop.
- `jsx-no-new-array-as-prop` — New array passed as a prop.
- `jsx-no-new-function-as-prop` — New function passed as a prop.
- `no-inline-prop-on-memo-component` — Inline prop defeats `memo()`.
- `rerender-dependencies` — Unstable value recreated every render.
- `no-layout-property-animation` — Animating a layout property.
- `no-transition-all` — `transition: all` animates unintended properties.

**Beyond the scan:** Profile before and after. Hunt context fan-out, expensive
selectors, waterfalls, cache misses, image and bundle costs, and work that can
move to a server or transition. Reject premature `useMemo`/`memo` on cold paths:
the optimization can be noise, add dependency hazards, and obscure code.
