---
name: app-end-to-end-delivery
description: 协调 app 从需求、设计到开发、发布和持续迭代的当前阶段；不确定该用哪个 Magic Skill 时使用。Route the requested product lifecycle work and deliver accepted implementation changes.
---

# App Development And Iteration

Identify where the product is now and complete the requested stage or connected stages. This is the
lightweight entry point when the user does not know which Magic skill to select. A focused task can
start directly in its specialist skill; it need not traverse the full lifecycle.

## Establish The Current Task

Resolve the app/repositories, requested outcome, current stage, accepted scope, and evidence needed.
Reuse session decisions and the project's current sources. When context is scattered or a new product
needs a durable handoff, use [project-context.md](references/project-context.md). Do not create another
configuration layer when existing sources suffice.

Ask only for missing facts that change product meaning, permissions, data handling, or the deliverable.
Continue independent work. Skill routing does not authorize adjacent work: an audit or analysis remains
read-only; implementation does not itself authorize merge, store upload, or publication. Reuse existing
authorization for the requested operation instead of asking at every step.

## Route The Work

| Current need | Owner / next step | Completion evidence |
| --- | --- | --- |
| Validate an opportunity or unmet demand | [需求调研](../indie-app-demand-research/SKILL.md) | Demand evidence, key uncertainty, next validation decision |
| Define product loop, scope, data and commercial boundaries | [产品规划](../local-first-android-app-builder/SKILL.md) | Accepted behavior, exclusions and acceptance criteria |
| Design or change visible product behavior | [Design and approval](references/design-and-acceptance.md) | Reviewable design source and owner approval before UI implementation |
| Create a new Android workspace | [创建项目](../android-app-factory/SKILL.md) | Validated paired repositories; generated shell is not a finished product |
| Implement an accepted feature or fix | [Implementation delivery](references/implementation-delivery.md) | Correctly owned changes and relevant proof |
| Resolve architecture/state ownership | [架构审查](../android-app-architecture-guardrails/SKILL.md) | Located findings or scoped fixes against actual contracts |
| Prove Android UI, system or lifecycle behavior | [真机验证](../android-instrumentation-qa-guardrails/SKILL.md) | Reproducible device evidence and honest coverage gaps |
| Check a change or audit a whole version | [版本与改动审查](../app-change-self-check/SKILL.md) | Risk-ranked findings and evidence across the selected baseline |
| Integrate accepted code, when requested | [合并主干](../github-pr-mainline-release/SKILL.md) | Verified mainline integration and scoped cleanup |
| First Play launch, version update, or store-only refresh | [Google Play 发版](../google-play-release/SKILL.md) | Verified Console draft; final submission/publication remains owner-controlled by default |
| Understand usage, conversion or revenue | [产品数据分析](../app-product-analytics/SKILL.md) | Decision supported by comparable product metrics |
| Diagnose crashes, ANRs or release regressions | [稳定性分析](../app-stability-analysis/SKILL.md) | Impact, diagnostic evidence and recovery criteria |
| Verify an iteration's product outcome | [Iteration outcomes](references/iteration-outcomes.md) plus the relevant analysis | Result against the original hypothesis and observation window |

Load only the relevant specialist and references. Keep one shared task context and reuse checks across
stages; do not restart discovery or invoke this coordinator recursively after each specialist step.
Device keep-awake is an explicit utility, not a default stage of development or QA.

## Continue And Hand Off

For user-visible changes, follow the design gate before implementation. A design-only request ends with
the review package; a development request continues after required approval through implementation,
verification and scoped repairs. Do not substitute a plan for already authorized executable work.

Leave a concise handoff in the existing issue, requirement or release record when another run needs it:
current source/baseline, completed work, relevant evidence, approval scope, unresolved decisions and next
action. Chat is sufficient when no durable handoff is needed. Record actual state, not an intended future
state. A merged feature, uploaded binary, live release and successful product outcome are different facts.

Use [iteration outcomes](references/iteration-outcomes.md) when a release or analysis needs a measurable
follow-through. Do not start development, publish, or schedule monitoring solely because it is the next
possible lifecycle stage.
