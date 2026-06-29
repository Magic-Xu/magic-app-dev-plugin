# Android App Bootstrap Checklist

Use this reference when starting a new Android app or turning a product idea into a buildable V1.

## 1. Product Boundary

Write these before code:

- Product sentence: `[App] helps [user] do [job] with [constraint or differentiator].`
- Core loop: `open -> act -> result -> next action`.
- V1 includes: only the smallest complete loop.
- V1 excludes: tempting features that would expand scope.
- Sensitivity model: local data, export data, logged data, network data.

If the includes list does not form a complete loop, shrink or reorder it. If the excludes list is empty, the scope is probably not real yet.

## 2. First Documents

Create or update:

- `docs/product/v1-requirements.md`
- `docs/product/v1-development-tasks.md`
- `docs/design/ui-preview.*` or a design tool link
- `docs/engineering/architecture.md`
- `docs/engineering/development-rules.md`
- `docs/engineering/testing-rules.md`
- `docs/decisions/README.md`
- `AGENTS.md`

Do not scatter product docs, design files, logo sources, or generated assets at repository root.

## 3. Recommended Package Boundaries

Start with packages before splitting Gradle modules:

- `app`
- `core/designsystem`
- `core/ui`
- `core/common`
- `core/navigation`
- `core/media`
- `feature/<feature>/contract`
- `feature/<feature>/presentation`
- `feature/<feature>/domain`
- `feature/<feature>/data`
- `feature/<feature>/ui`

Split Gradle modules only when build speed, ownership, reuse, or dependency boundaries justify the cost.

## 4. Phase Order

Prefer this order:

1. Engineering base: dependency versions, app shell, theme, navigation, MVI pattern, test command.
2. Main loop UI: static but realistic screens wired to state.
3. Platform gateways: picker, camera, save, share, external navigation, permissions.
4. Domain engine: business rules, algorithms, renderers, storage, network.
5. Persistence and release surfaces: settings, legal pages, analytics, ads, monitoring.
6. Store readiness: privacy declarations, screenshots, release checklist.

Avoid starting with monetization, accounts, cloud sync, automation, or batch workflows unless they are part of the core loop.
