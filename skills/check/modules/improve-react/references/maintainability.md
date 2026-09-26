# 5. Maintainability & architecture

This category covers structures that make changes risky, conventions unclear,
and ownership or rendering behavior hard to reason about. Leverage means
repeated cost across a team or a component's centrality—not a preference for
abstraction or a low-risk style nit.

**Hunt for:**

- `no-giant-component` — Large component is hard to read and change.
- `no-nested-component-definition` — Component defined inside another component.
- `no-many-boolean-props` — Boolean prop combinations are hard to test.
- `prefer-module-scope-static-value` — Static value rebuilt every render.
- `prefer-module-scope-pure-function` — Pure function rebuilt every render.
- `no-event-handler` — Event logic handled in an effect.
- `no-mirror-prop-effect` — Prop mirrored into state via effect.
- `design-no-vague-button-label` — Vague button label.

**Beyond the scan:** Examine ownership boundaries, public component APIs,
context design, dependency direction, test seams, duplicated domain logic, and
whether abstractions communicate intent. Hunt missing error/Suspense boundaries,
overloaded providers, optimistic UI opportunities, and premature memoization.
Do not split a component or add a hook just to satisfy a metric.
