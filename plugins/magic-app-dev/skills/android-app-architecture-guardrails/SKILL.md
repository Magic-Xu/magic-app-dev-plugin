---
name: android-app-architecture-guardrails
description: Review Android changes that affect responsibility boundaries, MVI state, Compose side effects, resources, or platform gateways.
---

# Android App Architecture Guardrails

Use for Android changes whose architecture or state/effect ownership needs judgment. Apply the target repository's actual contracts; user instructions take precedence over this skill's guidance. Reuse established context and validation evidence from the active task.

## Scope The Review

Inspect the changed behavior and nearby code first. Read engineering docs, decisions, module boundaries, or CI definitions when they govern that change or resolve an uncertainty. Widen the review when the affected dependencies require it.

Fix the ownership problem needed for the requested behavior. Existing debt outside that scope can be reported without expanding the implementation.

## Responsibility Boundaries

- Compose UI renders state and dispatches events. Platform calls, navigation, storage, SDK effects, and repository mutations belong in gateways or route/effect coordinators.
- Presentation owns state transitions, reducers and UI-facing state mapping. Domain owns pure business rules and algorithms. App-level coordination owns cross-feature routing and lifecycle effects.
- Use the repository's MVI contract pattern for independently stateful pages. Add only the state, intents, effects and state holder the behavior needs; extend existing ownership for subordinate UI.
- Extract helpers or components when distinct responsibilities, reuse or testability justify them. File length is a review signal, not an automatic refactoring requirement. Preserve explicit repository limits enforced by its engineering contract.
- User-visible text uses Android resources. Update supported translations when changing localized text; preserve design tokens for existing colors, spacing, shapes and typography.
- Add dependencies only when needed for the task. Record a new durable boundary or architectural decision in the appropriate engineering documentation when maintainers need it.

## Validation Evidence

Use the task's validation plan or `$app-change-self-check` when selecting evidence needs further guidance. Inspect changed contracts, resource use and side-effect ownership as part of the final diff. Run focused checks for unresolved risks; broaden to shared boundaries when affected.

Reuse checks already passed for the same relevant code and environment. New changes, failures, or remaining uncertainty justify reruns. Report the implemented behavior, material architectural decisions, and any unverified boundary.
