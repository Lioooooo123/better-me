# 1. Bugs & correctness

This category covers behavior that can render the wrong UI, lose state, create
stale data, or break React's rendering model. High leverage means a defect on a
shared route, a hot interaction, or a stateful list—not a theoretical issue in
dead or rarely reached code.

**Hunt for:**

- `no-array-index-as-key` — Array index used as a key; insertion and reordering
  can attach state to the wrong row.
- `no-random-key` — Random value used as a key; every render remounts the item.
- `jsx-key` — Missing key in list; React cannot reconcile siblings reliably.
- `exhaustive-deps` — Missing effect dependencies; closures observe stale state.
- `no-self-updating-effect` — Effect updates its own dependency; feedback loops.
- `no-set-state-in-render` — State update during render; render-loop risk.
- `no-uncontrolled-input` — Uncontrolled input value; controlled behavior drifts.
- `rendering-conditional-render` — Number before `&&` renders stray `0`.

**Beyond the scan:** Check async races, cancellation on unmount, state machines
with impossible transitions, optimistic updates that need rollback, and whether
an effect belongs in an event handler. Look for missing error and Suspense
boundaries around failure-prone or loading-sensitive subtrees.
