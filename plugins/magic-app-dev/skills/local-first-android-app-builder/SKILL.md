---
name: local-first-android-app-builder
description: Use when starting, structuring, implementing, or reviewing a focused Android app where local-first behavior, clear V1 scope, Jetpack Compose UI, MVI contracts, pulse state management, resource/i18n hygiene, platform-boundary control, and AI-friendly engineering guardrails matter. Trigger for Android app bootstrapping, page creation, feature planning, architecture review, or repo agent rule creation.
---

# Local-first Android App Builder

## Core Rule

Start from the product's smallest complete user loop, not from a generic app template.

Before editing code, identify:

- Product sentence: what the app does for whom.
- V1 loop: the shortest complete path from user intent to value delivered.
- Explicit non-goals: features that must not be added without confirmation.
- System capabilities: picker, camera, file IO, share, billing, ads, analytics, etc.
- Data sensitivity: what must stay local, what can leave the device, and what must never be logged.

If the user's goal or scope is unclear, stop and ask. Do not invent a broad app.

## Required Reading

When available in the target repository, read these before changing files:

- `AGENTS.md`
- `docs/product/`
- `docs/design/`
- `docs/engineering/`
- `docs/decisions/`
- Nearby feature files and existing page templates

If this package was copied into the repo, also read:

- `docs/engineering/android-app-bootstrap-playbook.md`
- `docs/engineering/architecture-guardrails.md`
- `docs/engineering/mvi-pulse-compose-pattern.md`
- `docs/engineering/validation-checklist.md`

Use the reference files in this skill only when the matching task appears:

- Product or project kickoff: `references/bootstrap-checklist.md`
- New page or state-flow work: `references/mvi-pulse-compose.md`
- Repo rule creation or review: `references/repo-rules-template.md`

## Workflow

1. Confirm branch and write boundary.
   - Do not edit code, resources, generated assets, or engineering docs on `main` or `master`.
   - If already on a relevant feature branch, continue there.
   - If on `main` or `master`, create a task branch before edits.

2. Define scope before implementation.
   - Write the V1 included and excluded lists.
   - Prefer one complete core loop over many partial features.
   - Challenge requested expansions when they are not needed for the loop.

3. Establish architecture boundaries.
   - `ui`: Compose rendering and event dispatch only.
   - `contract`: public page state, intents, effects, UI-facing enums.
   - `presentation`: ViewModel, reducer, state mapping, effect emission.
   - `domain`: pure rules, models, algorithms, render engines.
   - `data` or platform gateways: SDK calls, file IO, pickers, permissions, sharing.
   - `core/designsystem`: tokens and theme.
   - `core/ui`: reusable UI primitives.
   - `core/common`: business-agnostic helpers.

4. Create page contracts before UI behavior.
   - Define `XxxContract`, `XxxState`, `XxxIntent`, `XxxEffect`, and `XxxViewModel`.
   - Use pulse for state management when the repo standard requires it.
   - Model navigation, picker launch, save, share, toast, and external intents as effects or app-level effect handling.

5. Keep Compose pure.
   - Composables receive state and callbacks.
   - Do not place business decisions, navigation decisions, SDK calls, file reads/writes, or image processing in Composables.
   - Split large screens by role: route/shell, top bar, content, controls, sheet/dialog, rows.

6. Resource and design hygiene.
   - Put all user-visible strings in Android resources.
   - Update every supported locale together.
   - Use design tokens for colors, typography, spacing, radius, and component sizes.
   - Add narrow tokens before scattering repeated literals.

7. Platform and privacy boundaries.
   - Wrap system capabilities behind gateways or app-level coordinators.
   - Do not log sensitive data such as image URI, filename, user text, email, exact location, or raw content.
   - Analytics, ads, and monitoring are side channels; they must not block the core loop.
   - If adding SDKs that collect data, update privacy docs and store console declarations.

8. Validate narrowly before handoff.
   - Run the smallest useful compile/test command.
   - Search for hardcoded UI text and direct platform calls in UI.
   - Check large Kotlin/Compose files and split if responsibility is mixed.
   - Report what changed, why, what ran, and residual risk.

## Page Contract Pattern

Use this shape unless the target repo already has a stricter template:

```kotlin
data class ExampleState(
    val isLoading: Boolean = false,
)

sealed interface ExampleIntent {
    data object OnPrimaryClick : ExampleIntent
}

sealed interface ExampleEffect {
    data object NavigateBack : ExampleEffect
}
```

Prefer specific intent names such as `OnSaveClick`, `OnImagePicked`, `OnStrengthChanged`. Avoid vague names such as `UpdateData`, `HandleAction`, or `DoSomething`.

## Review Checklist

- Is the V1 loop explicit and smaller than the wish list?
- Are non-goals written down?
- Are UI, state, domain, and platform responsibilities separated?
- Is each page contract defined before behavior is added?
- Are all user-visible strings resource-backed and localized?
- Are visual values tokenized?
- Are system calls outside Composables?
- Are sensitive values excluded from logs, analytics, crashes, and backups?
- Did validation run, and are skipped checks explained?
