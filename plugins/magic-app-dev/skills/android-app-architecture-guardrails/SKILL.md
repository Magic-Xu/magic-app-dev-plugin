---
name: android-app-architecture-guardrails
description: Review Android changes that affect responsibility boundaries, MVI state, Compose side effects, resources, or platform gateways.
---

# Android App Architecture Guardrails

Use for Android changes whose architecture or state/effect ownership needs judgment. Apply the target repository's actual contracts; user instructions take precedence over this skill's guidance. Reuse established context and validation evidence from the active task.

## Scope The Review

Inspect the changed behavior and nearby code first. Read engineering docs, decisions, module boundaries, or CI definitions when they govern that change or resolve an uncertainty. Widen the review when the affected dependencies require it.

For review-only requests, report findings with locations and evidence; do not edit. During an authorized
implementation, fix the ownership problem required by that behavior. Report unrelated debt separately.
For a whole-version audit, use the selected baseline and feature inventory from
[版本与改动审查](../app-change-self-check/SKILL.md), not just the current dirty diff.

## Responsibility Boundaries

The Factory default dependency direction is `app -> feature -> domain -> core`; upper layers may use
lower layers, never the reverse, and features do not import siblings. Keep cross-feature coordination
in `app`. Apply the target repository's established equivalent boundaries. For MVI/Pulse state and
effect choices, read [mvi-pulse-compose.md](references/mvi-pulse-compose.md) only when needed.

- Compose UI renders state and dispatches events. Platform calls, navigation, storage, SDK effects, and repository mutations belong in gateways or route/effect coordinators.
- Presentation owns state transitions, reducers and UI-facing state mapping. Domain owns pure business rules and algorithms. App-level coordination owns cross-feature routing and lifecycle effects.
- Use the repository's MVI contract pattern for independently stateful pages. Add only the state, intents, effects and state holder the behavior needs; extend existing ownership for subordinate UI.
- Extract helpers or components when distinct responsibilities, reuse or testability justify them. File length is a review signal, not an automatic refactoring requirement. Preserve explicit repository limits enforced by its engineering contract.
- User-visible text uses Android resources. Update supported translations when changing localized text; preserve design tokens for existing colors, spacing, shapes and typography.
- Add dependencies only when needed for the task. Record a new durable boundary or architectural decision in the appropriate engineering documentation when maintainers need it.

## Validation Evidence

Use the task's validation plan or `$app-change-self-check` when selecting evidence needs further guidance. Inspect changed contracts, resource use and side-effect ownership as part of the final diff. Run focused checks for unresolved risks; broaden to shared boundaries when affected.

Reuse checks already passed for the same relevant code and environment. New changes, failures, or remaining uncertainty justify reruns. Report the implemented behavior, material architectural decisions, and any unverified boundary.
