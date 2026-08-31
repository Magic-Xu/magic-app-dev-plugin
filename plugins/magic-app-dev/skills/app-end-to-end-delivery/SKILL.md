---
name: app-end-to-end-delivery
description: Use as the unified delivery entry for requirements and bug fixes in Magic Android App Factory workspaces, including stateful UI, domain logic, Android or IO gateways, cross-feature orchestration, shared Platform engineering, and new product initialization. Route work to the owning boundary before implementing, then validate and hand it off with evidence. Do not use it to push, open PRs, merge, release, or deploy unless the user explicitly asks for those actions.
---

# App End-to-End Delivery

## Outcome

Turn an app requirement into the smallest complete set of correctly owned changes and enough evidence
to show the accepted behavior works. Route the requirement before choosing files or templates. Follow the
target repository's rules when they are stricter.

This skill coordinates delivery; it is not a feature generator or a product framework.

## Boundaries

- Factory creates new product workspaces. It does not generate routine changes for existing apps.
- Platform owns build conventions, dependency baselines, and mandatory quality rules shared by apps. It
  does not own product behavior.
- Keep product-specific behavior in the consumer app. A possible shared runtime remains app-owned until
  at least two maintained real apps share its semantics, lifecycle, and test contract.
- Do not create empty layers, placeholder abstractions, or parallel `Screen`, Contract, and ViewModel files
  merely to make a change resemble a template.
- Do not start PR, merge, branch deletion, release, store upload, or deployment work without explicit user
  instruction. Implementation, validation, packaging, or approval of local behavior does not imply it.

## Establish The Delivery Target

Before editing:

1. Read `AGENTS.md`, the root and documentation indexes, the requirement baseline, relevant engineering
   docs and decisions, nearby code and tests, CI or validation commands, and `git status --short --branch`.
2. Express the requested result as observable behavior, non-functional constraints, and evidence that can
   prove it. For a defect, identify the violated ownership or invariant instead of patching only the symptom.
3. Inspect how the target app already represents the same kind of state, rule, gateway, or orchestration.
   Existing names are evidence, not authority when they violate repository rules.
4. Ask only when missing information changes product meaning, permissions, data handling, or the deliverable.
   Otherwise make the narrowest evidence-backed assumption and continue.

Keep a concise route map in the conversation or task notes unless the repository explicitly requires a
design artifact:

| Concern | Semantic owner | Minimum artifact | Allowed dependency | Proof |
| --- | --- | --- | --- | --- |
| One behavior or constraint | One owning layer | Only what behavior needs | Higher layer to lower layer | Risk-matched evidence |

For every row, explain why that owner holds the semantic decision. A requirement may span several rows,
but each row must retain only its layer's meaning.

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

Load `$android-app-architecture-guardrails` when Android implementation or review touches architecture,
state flow, Compose, resources, platform calls, or long-term maintainability. Apply its page-specific MVI
rules only to independently stateful pages, not to domain, gateway, app orchestration, or subordinate UI
work.

For realistic routing examples and acceptance expectations, read
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
- After adding or moving persistent files, run the repository's layout validator and its contract tests when
  available. Fix the artifact ownership or the validator's generic analysis; do not add a product exception
  merely to make the gate pass.
- When the route is a new product workspace, invoke `$android-app-factory` and use its authoritative generator
  and acceptance flow instead of reproducing workspace creation here.
- Keep Factory and Platform changes in their own repositories and branches. Generated apps consume the
  Factory-tested published Platform version; local composite paths are temporary validation inputs and are
  never persisted in generated workspaces.
- Do not switch repositories, data sources, permissions, validation quality, or delivery form as a fallback
  when the selected path fails. Report the root cause and ask before changing the intended path.

## Validate By Risk

Run the narrowest check that can fail for the changed semantic, then broaden until the accepted behavior and
affected integration boundary are covered. Repository-mandated checks remain mandatory.

| Change | Primary evidence | Broaden when |
| --- | --- | --- |
| Stateful feature UI | State, reducer, or ViewModel tests; Compose/UI behavior test; affected compile target | Run Platform Quality and Lint for structure/resources; use a device for real interaction or lifecycle; build an APK when installation or packaged integration matters |
| Pure domain rule | Focused pure Kotlin unit tests and affected module compile | Run dependency/quality checks when packages or module edges changed; no APK, AAB, or device proof solely for isolated logic |
| Android or IO gateway | Contract/unit tests for deterministic behavior; Android integration or instrumentation proof for the real boundary; affected compile target | Run Lint for APIs, resources, permissions, or manifest changes; use a device for OS/provider/lifecycle semantics; package when runtime integration requires it |
| Cross-feature orchestration | Effect-handler, route, or coordinator tests plus an integration path across the involved features | Run Platform Quality to prove feature isolation; use a device when navigation, process, or lifecycle behavior is material |
| Platform engineering | Plugin or quality-rule tests and executable consumer contracts or smoke builds | Validate a maintained real consumer and Factory generation when compatibility or the generated baseline changes |
| Factory initialization | Generator dry run, structural validation, clean generated Git boundaries, and the Factory's full generated-app check | Build Debug/Release APK and Release AAB as required by Factory acceptance; use a device only for product behavior added beyond the starter |

In Factory-generated apps, do not disable or relax Platform Quality. Use the repository's exact task names;
`check`, Lint, compile, APK, AAB, and device validation are distinct evidence and are not interchangeable.
A screenshot is only visual evidence unless the recorded interaction covers the accepted path and resulting
state. If a required proof needs unavailable credentials, network, SDK, or hardware, run the remaining valid
checks and report the gap precisely.

## Review And Hand Off

Before delivery:

1. Inspect the final diff and `git status --short --branch`; exclude build outputs, local paths, credentials,
   temporary evidence, and unrelated changes.
2. Re-check each route-map row for ownership, minimum artifacts, dependency direction, and matching proof.
3. Perform any repository-required artifact-boundary review. Keep persistent artifacts focused on the final
   behavior and durable constraints rather than rejected approaches or agent work history.
4. Report changed behavior and its owning boundary, the reason for that route, commands and evidence that
   passed, packaging or device status when applicable, and any unverified risk.

Do not claim CI, PR, merge, release, or production completion unless it actually happened.

## Delivery Escalation

Only after an explicit request to push, create a PR, merge, release, or clean branches, re-check remote state
and use the repository's dedicated release or mainline skill when available. Keep that workflow separate from
local requirement delivery.
