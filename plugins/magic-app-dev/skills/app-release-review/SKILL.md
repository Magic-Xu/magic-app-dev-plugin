---
name: app-release-review
description: 版本发布审查与修复：Google Play 上架前从累计变化推导影响范围，核验新需求与既有能力是否退化、跨功能冲突、架构实现及发布证据；也支持限定范围审查。只审查时保持只读，要求修复时完成范围内修复与验证。
---

# App Release Review And Repair

Determine whether the candidate delivers the accepted changes while preserving the product's existing
promises, and whether the evidence supports release. Derive review scenarios from the actual changes and
their affected responsibilities; a list of prior bugs or passing checks is not the review scope. Reconcile
requirements, implementation and proof, then repair confirmed defects when authorized.

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
- Read [release-evidence.md](references/release-evidence.md) for combined behavior proof, packaged release
  checks and the release decision. Choose checks by actual risk and complete applicable project gates.

Distinguish confirmed defects, hypotheses, missing evidence and optional improvements. A finding needs
an affected outcome, concrete location, expected versus observed behavior and supporting evidence.
Architecture preference, file length or absence of a direct caller alone is not a defect.

Keep coverage open until each material change and affected responsibility has an explicit finding,
supporting inspection/validation evidence, or a named gap. Existing tests and prior review conclusions
are inputs to this map, not substitutes for it. Do not narrow a whole-version review merely because a
packaging or infrastructure blocker already prevents release; continue independent inspection.

## Repair And Clean Up

Work in the project's required branch/worktree, preserving unrelated changes. Fix the smallest complete
root cause, including wiring, affected consumers and necessary documentation. Prove the violated behavior
before/after where practical; do not rewrite the requirement or weaken its proof to legalize a defect.
Changes to accepted UI, core behavior, data handling or release authority follow the project's gates.

Within repair/cleanup authorization, remove demonstrably superseded code, skill/config entries and
stateful documentation together with their callers. Check build variants, dynamic/resource registration,
external consumers, migrations and recovery compatibility before declaring something unused. Preserve
required historical records and compatibility behavior. Retain uncertain items, record why their purpose
is unresolved, and batch the remaining decisions for the final handoff. Ask earlier only if a decision
blocks dependent work; continue independent repairs. Do not turn uncertainty into deletion or speculative design.

After repairs, rerun affected checks and combined paths; rebuild any affected release artifact. Reuse
successful checks only for unchanged relevant inputs and environment. Integrate the project's artifact
boundary review into this final review, without another duplicate report. Finish when authorized repairs
are verified and unresolved blockers/decisions are explicit; optional debt does not justify endless refactoring.

## Deliver The Release Decision

Lead with ready, blocked, or not yet verified for the stated candidate and scope. Report material fixes
and removals, severity-ranked remaining findings, coverage/evidence limits and unresolved decisions.
Use one report at the user/project destination when required; otherwise the conversation is sufficient.
Keep coverage compact and link detailed proof. Distinguish review completion from release readiness:
uninspected applicable areas remain review gaps, even if the inspected paths have no findings. Qualify
negative findings by their actual coverage; never claim full coverage or executed tests without evidence.

Integration uses [合并主干](../github-pr-mainline-release/SKILL.md); Play preparation/upload uses
[Google Play 发版](../google-play-release/SKILL.md) with the corresponding authorization. A review verdict
does not itself merge, upload, submit, publish or schedule monitoring.
