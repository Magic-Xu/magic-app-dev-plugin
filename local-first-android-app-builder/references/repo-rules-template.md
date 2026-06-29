# Repo Rules Template

Use this reference when creating or updating `AGENTS.md` or repo engineering rules for a new Android app.

## Minimum Sections

1. Product goal
2. V1 scope
3. Explicit non-goals
4. Technology constraints
5. Directory layout
6. Page architecture
7. Design system rules
8. Resource and locale rules
9. Branch and editing rules
10. Architecture governance
11. Delivery requirements

## Rules That Should Be Explicit

- No edits on `main` or `master`; create or use a feature branch.
- Product docs live in `docs/product/`.
- Design previews live in `docs/design/`.
- Engineering rules live in `docs/engineering/`.
- Architecture decisions live in `docs/decisions/`.
- Brand source assets live outside final Android resource folders.
- Android final resources live in `app/src/main/res/`.
- Composables render state and dispatch events only.
- Business logic, navigation decisions, file IO, SDK calls, and image/media processing stay outside Composables.
- All user-visible strings are Android resources.
- Every supported locale is updated together.
- Validation run and skipped checks are reported in every handoff.

## Product-Specific Overrides

Each app must add its own stricter rules:

- supported locales
- privacy constraints
- store/release obligations
- monetization constraints
- core domain boundaries
- forbidden expansions for V1
