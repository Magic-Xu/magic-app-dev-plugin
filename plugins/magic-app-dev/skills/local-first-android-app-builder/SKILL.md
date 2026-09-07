---
name: local-first-android-app-builder
description: Define or review a local-first Android product's core user loop, V1 scope, data boundaries, and project-specific engineering choices before implementation or workspace creation.
---

# Local-first Android App Builder

Turn an app idea into a small, complete user loop with explicit data and operating-cost boundaries. Use this
skill for product planning and project kickoff; reuse accepted decisions when work continues in an existing app.

## Establish The Product Boundary

Resolve only what the current decision needs:

- Who the app serves, the job it completes, and the path from user intent to a useful result.
- What belongs in the requested version and which plausible expansions are outside it.
- Required system capabilities such as picking, capture, storage, sharing, billing, or analytics.
- Which data stays on-device, what may be exported or transmitted, and what must never be logged.
- Offline behavior and acceptable ongoing server or vendor costs.

Use the user's requirements and relevant product or engineering context already available. Ask when missing
information changes product meaning, permissions, data handling, or the deliverable; continue independent work.
Routine implementation details can be resolved from the repository's patterns without reopening accepted scope.

## Make Project-Specific Choices

- Keep the core loop usable independently of analytics, advertising, and monitoring. Treat network-dependent
  features according to the agreed offline behavior rather than assuming every feature must work offline.
- Keep sensitive content out of logs and telemetry. When adding a collecting SDK, align the actual data flow,
  privacy documentation, and required store declarations before publication.
- Extend established state and platform ownership. Use the repository's MVI and Pulse conventions where required;
  only independently stateful pages need their own page contract and state holder.
- Add packages, modules, gateways, or shared components when behavior, ownership, reuse, or testability needs them.
  Preserve repository-enforced quality rules, resource localization, and design tokens.

Record decisions in existing product or engineering documents when maintainers need them. Create a new document
only for a distinct reader and purpose.

## Continue Into The Requested Work

- For kickoff scope and artifact placement, consult [references/bootstrap-checklist.md](references/bootstrap-checklist.md).
- For page state and effect ownership, consult [references/mvi-pulse-compose.md](references/mvi-pulse-compose.md).
- When creating or reviewing repository rules, consult [references/repo-rules-template.md](references/repo-rules-template.md).
- For a new Magic Android workspace, use `$android-app-factory` and its authoritative generator and acceptance flow.
- For implementation in a Magic Android Factory workspace, use `$app-end-to-end-delivery`. In other repositories,
  follow their delivery conventions; use `$android-app-architecture-guardrails` or `$app-change-self-check` when a
  boundary or validation choice needs further guidance.

Load only the guidance needed for that next step. If implementation is already requested, continue into it after
resolving the product boundary; a completed plan is the deliverable only when the user requested planning.
