---
name: app-release-review
description: 版本发布审查与修复：从累计变化核验需求、既有能力、跨功能冲突、架构实现及本地功能与性能；按现象、引入原因、方案和影响汇报。只审查时保持只读，授权后修复；正式包、签名与 Play 分发由 google-play-release 负责。
---

# App Release Review And Repair

Determine whether the candidate delivers the accepted changes while preserving the product's existing
promises, and whether engineering evidence supports proceeding to release preparation. Derive review
scenarios from the actual changes and their affected responsibilities; prior bugs or passing checks do not
define the review scope. Reconcile requirements, implementation and proof, then repair confirmed defects
when authorized.

## Establish Scope And Authority

The primary use is a whole-version review before Google Play release. Read
[coverage-and-reconciliation.md](references/coverage-and-reconciliation.md) to establish the published
baseline, candidate, cumulative feature inventory and interactions with retained behavior. A clean
working tree does not reduce the review to zero changes. First releases have no prior published baseline.

An explicitly scoped feature/fix review or pre-implementation architecture check stays within that
scope. Use the same reasoning and relevant references without starting a whole-version audit or claiming
release readiness. Preserve repository-required architecture checks before implementation.

Separate review from repair authorization. Review-only requests leave implementation and external state
unchanged, apart from a requested report artifact. A request to review and fix authorizes necessary repairs
inside the agreed scope; existing implementation authorization covers task-caused defects. Reuse that
authorization without asking for each reversible fix. Product changes and unrelated debt need their own scope.
A follow-up request to add verification refines the ongoing task; it does not revoke existing repair
authorization or reduce the original completion requirement unless the user explicitly changes the scope.

This skill owns source/architecture review, functional regression and affected local device/performance
validation. Formal release versioning, signed distributable artifacts, final package verification and
Play-dependent distribution/acceptance belong to [Google Play 发版](../google-play-release/SKILL.md).
Their absence does not block this engineering review or justify a recurring generic acceptance-gap list.
Record only a concrete dependency of this candidate as a handoff to that stage, when useful. Local test
builds and Release-like benchmark variants remain in scope; do not defer executable local checks to Play.

## Review The Candidate

- Build the coverage map in [coverage-and-reconciliation.md](references/coverage-and-reconciliation.md):
  cumulative changes, affected existing promises, reachable paths/shared owners, discriminating scenarios
  and evidence or gaps. Screen the cross-cutting responsibilities there even when the user does not name
  them. Trace new and bypassed paths; do not assume a replacement inherits the old path's safeguards.
- Derive expected outcomes from accepted behavior and applicable constraints before trusting current code
  or tests. Select scenarios that could disprove preservation of those outcomes, including affected failure
  and interaction paths. Investigate discovered coupling until the relevant responsibilities are accounted for.
- Read [architecture-and-implementation.md](references/architecture-and-implementation.md) for ownership,
  quality trade-offs and suspicious implementation. For Android state, concurrency, effects or recovery,
  also read [mvi-pulse-compose.md](references/mvi-pulse-compose.md).
- Read [release-evidence.md](references/release-evidence.md) for combined behavior proof, local performance
  validation and the engineering review decision. Choose checks by actual risk and complete applicable
  project gates; distinguish review gates from later release-preparation gates.

Distinguish confirmed defects, hypotheses, missing evidence and optional improvements. A finding needs
an affected outcome, concrete location, expected versus observed behavior and supporting evidence.
Use the finding analysis in [coverage-and-reconciliation.md](references/coverage-and-reconciliation.md):
explain the visible symptom first, distinguish discovery by new evaluation inputs from introduction by
code changes, then give a concrete response and assess its effects on existing behavior and normal
workflows. Product-specific criteria and regression cases belong in the project, not in this shared skill.
Architecture preference, file length, a new failed check or absence of a direct caller alone is not a
release blocker.

Track each material change and affected responsibility to a finding, supporting inspection/validation
evidence, or an open gap. Recording a finding or naming a gap does not complete the work: follow the
completion conditions below. Existing tests and prior review conclusions are inputs to this map, not
substitutes for it. Continue independent inspection and executable local validation while another check
or a later distribution task is blocked.

## Repair And Clean Up

Work in the project's required branch/worktree, preserving unrelated changes. Fix the smallest complete
root cause, including wiring, affected consumers and necessary documentation. Prove the violated behavior
before/after where practical; do not rewrite the requirement or weaken its proof to legalize a defect.
Changes to accepted UI, core behavior, data handling or release authority follow the project's gates.

Within repair/cleanup authorization, remove demonstrably superseded code, skill/config entries and
stateful documentation together with their callers. Check build variants, dynamic/resource registration,
external consumers, migrations and recovery compatibility before declaring something unused. Preserve
required historical records and compatibility behavior. Investigate uncertain ownership using available
consumers and history; retain items whose removal cannot be justified. Batch only genuine remaining owner
decisions for handoff. Ask earlier if a decision blocks dependent work; continue independent repairs.
Do not turn uncertainty into deletion or speculative design.

After repairs, rerun affected checks and combined paths; rebuild affected local validation artifacts. Reuse
successful checks only for unchanged relevant inputs and environment. Integrate the project's artifact
boundary review into this final review, without another duplicate report.

## Complete The Authorized Work

A failed check is an input to investigation, not a reason to end the task. Use available evidence and
focused diagnostics to distinguish the cause, choose a response and complete the work within scope:

- **Review only:** Complete applicable checks and investigate material findings enough to support an
  actionable recommendation and impact assessment. Leave implementation unchanged; a confirmed defect
  can block the candidate even though the requested review is complete.
- **Review and repair:** Carry confirmed in-scope defects through cause, smallest complete repair and
  affected regression verification. A proposed fix or a failing test run is not a completed repair.
  A supported no-change conclusion or an explicitly accepted deferral may close an item; do not invent
  acceptance, weaken the requirement or change normal behavior merely to obtain passing checks.

Before final handoff, reconcile the original task with the coverage and repair status. If authorized,
necessary work remains executable, continue it instead of reporting it as a future step. Stop incomplete
only for a demonstrated access/resource limit, evidence unavailable after relevant diagnostics, a necessary
owner decision, or an explicit user stop or scope change. Explain the concrete impediment, available alternatives already checked and the smallest
input needed to resume; finish unaffected work. Preserve failed evidence and uncertainty. This does not
require unrelated debt cleanup or exhaustive investigation after the agreed outcome has been verified.

## Deliver The Review Decision

Lead with engineering review passed, blocked by a confirmed defect, or not yet verified within this scope.
For each material finding, report in this order: **observable symptom → origin and evidence → recommended
action → affected users/paths and repair side effects**. Use plain product language before technical detail.
Distinguish newly introduced regressions, pre-existing limitations, incomplete new capability and unknown
origin; note separately when expanded evaluation first exposed the behavior. Include why an earlier check
missed it when asked. State the recommendation now, including a justified no-change decision when appropriate;
do not stop at a severity label or ask the owner to infer a solution from test metrics.
Report material fixes/removals, remaining findings, coverage limits and unresolved decisions.
Use one report at the user/project destination when required; otherwise the conversation is sufficient.
Keep coverage compact and link detailed proof. Engineering review completion is distinct from release
preparation completion. Uninspected in-scope areas remain review gaps; absent later-stage release artifacts
are not missing engineering work. Distinguish the candidate's verdict from completion of the requested
task; an interrupted repair is incomplete even when its diagnostic report is finished. Qualify negative
findings by their actual coverage; never claim full coverage or executed tests without evidence.

Integration uses [合并主干](../github-pr-mainline-release/SKILL.md); Play preparation/upload uses
[Google Play 发版](../google-play-release/SKILL.md) with the corresponding authorization. A review verdict
does not itself merge, upload, submit, publish or schedule monitoring.
