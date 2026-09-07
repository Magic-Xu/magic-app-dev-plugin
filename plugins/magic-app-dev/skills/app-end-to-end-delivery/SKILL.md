---
name: app-end-to-end-delivery
description: Implement and validate app, Platform, or Factory requirements in Magic Android App Factory workspaces, routing changes to their owning boundary.
---

# App End-to-End Delivery

## Outcome

Turn an app requirement into the smallest complete set of correctly owned changes and enough evidence
to show the accepted behavior works. Apply the target repository's relevant engineering contracts; user
instructions take precedence over this skill's guidance. Reuse context and evidence from the active task.

This skill coordinates delivery; it is not a feature generator or a product framework.

## Boundaries

- Factory creates new product workspaces. It does not generate routine changes for existing apps.
- Platform owns build conventions, dependency baselines, and mandatory quality rules shared by apps. It
  does not own product behavior.
- Keep product-specific behavior in the consumer app. A possible shared runtime remains app-owned until
  at least two maintained real apps share its semantics, lifecycle, and test contract.
- Do not create empty layers, placeholder abstractions, or parallel `Screen`, Contract, and ViewModel files
  merely to make a change resemble a template.
- Push, PR, merge, branch deletion, release, store upload, and deployment require the user's corresponding
  instruction. Reuse existing authorization and use the dedicated workflow for the requested external operation.

## Establish The Delivery Target

Establish the accepted behavior, its owner, affected boundaries and the evidence needed to show it works.
Inspect nearby code and the current diff; consult governing requirements, engineering docs, decisions, and validation
commands as needed. Reuse current task context.

For a defect, fix the violated behavior or invariant within the requested scope. Ask when missing
information changes product meaning, permissions, data handling or the deliverable; continue independent
work while awaiting that answer. Otherwise make an evidence-backed decision and proceed.

A short route map is useful when ownership spans multiple boundaries or is unclear. For each concern,
identify the owner, minimum change, dependency direction and proof. Keep this reasoning in the conversation
unless a persistent design artifact is needed by maintainers.

## Route By Semantic Owner

Use the target app's established module names when they express the same boundaries.

| Requirement shape | Default owner | Typical artifacts |
| --- | --- | --- |
| UI with its own product state and interaction | `feature` | Existing or new feature state handling, UI, and behavior tests |
| Stable business rule independent of UI and Android | `domain` | Model, policy, use case, engine, or pure Kotlin tests |
| File, network, media, storage, SDK, or Android system capability | `core` gateway | Boundary interface when useful, platform implementation, contract or integration tests |
| Cross-feature navigation, effects, or lifecycle coordination | `app` | Effect handler, composition, navigation, or session coordination |
| Build, dependency, or quality decision shared by apps | Magic Android Platform | Convention plugin, quality rule, and consumer contract or smoke tests |
| New product workspace | Android App Factory | Paired Android/legal repositories and complete generation validation |

The dependency direction is `app -> feature -> domain -> core`: higher layers may depend on lower layers,
never the reverse. Features do not depend on sibling features. Put cross-feature coordination in `app`, and
put genuinely shared business state in `domain` rather than using one feature as another's service.

Route to Platform only when the requirement is a shared engineering baseline. Do not move a product runtime
there because reuse seems plausible. Route to Factory only for new workspace initialization or a change to
what every newly generated workspace must contain; do not use it to update an existing app.

## Choose The Minimum Artifacts

- Use a page MVI skeleton only when the requirement creates independently owned page state and interaction.
  Then use the repository's page Contract, mutation or reducer, ViewModel, route or screen, and behavior-test
  pattern.
- For stateful UI inside an existing page or flow, extend its feature-owned state and behavior, or add a
  focused component state holder when ownership requires one. Do not create another page Contract,
  `Screen`, or ViewModel.
- For pure domain behavior, prefer a named rule, function, policy, or use case plus pure tests. Add an
  interface only when substitution, ownership, or a real side-effect boundary requires one.
- For Android or IO behavior, keep Android classes and side effects behind the existing or smallest useful
  core gateway. UI sends events; it does not call the system, filesystem, network, or SDK directly.
- For app orchestration, consume typed feature outcomes and coordinate routes, effects, and lifecycles
  without absorbing feature state or domain rules into the app shell.
- Reuse existing helpers and contracts when their semantics match. Do not add an otherwise unused layer or
  product-specific exception to satisfy structural symmetry or a quality gate.

Use `$android-app-architecture-guardrails` when state, side-effect ownership or module boundaries need
additional architectural judgment. Reuse its relevant guidance if already loaded; ordinary edits within
an established boundary do not require a separate architecture pass.

If the correct owner or acceptance evidence is unclear, consult the relevant example in
[references/routing-scenarios.md](references/routing-scenarios.md).

## Place Persistent Artifacts By Meaning

Before creating or moving a file, identify its reader, use, and lifetime. Follow the target repository's
layout contract and validator when present. In Factory-generated workspaces, use these defaults:

| Artifact meaning | Default location |
| --- | --- |
| Current product facts | `docs/product/` |
| Current engineering rules | `docs/engineering/` |
| Operator and external-system procedures | `docs/operations/` |
| Durable decision history | `docs/decisions/` |
| Editable visual sources | `design/` |
| Executable helpers and validators | `tools/` |
| Store, website, and other external publishing inputs | `publishing/` |
| Immutable completed-release evidence | `releases/` |
| Reproducible logs, screenshots, media, reports, and build output | ignored `build/` |

Keep one current source for each stateful topic; update it instead of adding `final`, copied, dated,
archived, or version-suffixed variants. Git preserves superseded states. A feature requirement may produce
artifacts in several top-level areas, but each artifact follows its own meaning rather than being placed
under the feature by association. Do not create a persistent file when its reader or lifetime is unknown.

## Implement Within The Selected Boundary

- Work on a task branch or worktree when repository policy forbids direct mainline edits. Preserve unrelated
  user changes.
- Implement the root behavior in its owner, then wire only the dependencies needed to expose it. Re-check the
  route map if implementation requires a lower layer to import a higher layer or one feature to import another.
- Use repository resource, localization, permission, manifest, dependency injection, and testing mechanisms.
- After adding or moving files, run an applicable layout validator when available. Run the validator's own
  contract tests when its implementation or layout contract changes. Fix ownership rather than adding a
  product-specific exception to satisfy a gate.
- When the route is a new product workspace, invoke `$android-app-factory` and use its authoritative generator
  and acceptance flow instead of reproducing workspace creation here.
- Keep Factory and Platform changes in their own repositories and branches. Generated apps consume the
  Factory-tested published Platform version; local composite paths are temporary validation inputs and are
  never persisted in generated workspaces.
- Choose implementation tools within the agreed goal, repository scope, data source, permissions/session,
  quality and deliverable. If recovery from failure would change those boundaries, explain the cause and
  impact and ask before changing them; continue independent authorized work.

## Validate And Complete

Choose enough evidence for the affected behavior and complete repository-mandated checks. Reuse results valid for
current relevant inputs; rerun after changes, failures, or unresolved concerns. Use `$app-change-self-check` when
selecting evidence or assessing a gap needs guidance, within this same validation and final-review pass.

| Affected boundary | Candidate evidence and when to broaden |
| --- | --- |
| Feature UI or app orchestration | State/effect and interaction evidence; affected compilation. Add device or lifecycle proof when real navigation, rendering, or recreation matters. |
| Pure domain rule | Focused pure Kotlin behavior tests and affected compilation; dependency/quality checks when packages or module edges change. |
| Android or IO gateway | Deterministic contract tests plus real provider, permission, persistence, or lifecycle evidence for the changed boundary; relevant Android compilation and lint. |
| Platform engineering | Plugin/quality-rule tests and consumer contracts or smoke builds. Cover a maintained consumer and Factory generation when compatibility or the generated baseline changes. |
| Factory initialization | The Factory's full generator, layout, Git-boundary, `check`, Debug/Release APK, and Release AAB acceptance flow. |
| Documentation | Changed content, links, and reader path; execute app checks when changed executable instructions or behavior require them. |

Platform Quality remains mandatory in Factory apps. Use the repository's task names and required gates. Outside
Factory initialization or an explicit packaging deliverable, select APK/AAB builds when packaged integration is part
of the evidence needed. A screenshot alone proves appearance; accepted interactions and outcomes need corresponding
behavioral evidence. Run independent valid checks and identify precise gaps when required infrastructure is unavailable.

Inspect the final diff and status for ownership, contracts, dependencies, resources/permissions, secrets, local paths,
generated outputs, and unrelated changes. Integrate any required artifact-boundary review here. Report changed behavior,
material ownership choices, validation evidence, applicable package/device status, and remaining limitations.

Continue through implementation, validation, result inspection, and repair of task-caused defects until the agreed
deliverable is complete or a genuine blocker needs user input or external change. For an already requested external
operation, continue with its dedicated workflow and current remote state. Claim only completion that was verified.
