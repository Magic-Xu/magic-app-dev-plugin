---
name: app-change-self-check
description: 版本与改动审查：交付前自检，或汇总整版本全部 feature，检查架构偏移、文档/设计一致性和回归证据。Review a change or audit a whole release against its baseline; audit-only requests remain read-only.
---

# Version And Change Review

Establish enough evidence that the requested behavior works and its affected boundaries remain valid.
Apply repository contracts and reuse context and verification already gathered for unchanged inputs.

## Select The Review Scope

- **Change self-check:** Review an implemented feature/fix against its accepted requirement and actual
  change base, including relevant uncommitted changes. This is the usual development handoff.
- **Whole-version audit:** Use when the user asks for 版本总审、全部 feature、架构偏移、文档一致性 or cumulative
  review across releases. Follow [version-audit.md](references/version-audit.md). Include already merged
  work since the selected release baseline; an empty working tree does not mean an empty version.

Do not promote routine edits to a full version audit. If the requested baseline is ambiguous, inspect
release records first and ask only when plausible alternatives materially change the review. Label a
provisional scope while continuing independent inspection; do not claim full coverage without a baseline.

A review-only request is read-only, apart from a requested report artifact. Return located findings and
smallest useful recommendations. During already-authorized implementation, fix task-caused defects and
recheck them. Findings outside that scope do not authorize broad refactoring or rewriting contracts.

## Choose Evidence By Risk

| Affected behavior | Relevant evidence |
| --- | --- |
| Pure logic | Focused behavior tests and affected compilation |
| UI or orchestration | State/interaction evidence; device, emulator or browser proof when rendering, navigation or lifecycle matters |
| Platform or IO gateway | Deterministic contract tests plus real provider, persistence, permission or system integration evidence |
| Build, manifest or shared contracts | Relevant lint/dependency checks, rule tests and affected consumers; Platform changes may need maintained consumer and Factory smoke builds |
| Factory initialization | Generator/layout/Git checks and the Factory's full `check`, Debug/Release APK and Release AAB acceptance flow |
| Documentation or metadata | Syntax, links, consistency and reader path; execute changed commands or generation paths when relevant |

Complete applicable repository-mandated gates. Reuse successful checks for unchanged relevant inputs;
rerun after relevant changes, failures or unresolved concerns. AAB/APK builds matter when release or
packaged integration is in scope. A screenshot proves appearance, not an interaction or persistence
outcome. Use [真机验证](../android-instrumentation-qa-guardrails/SKILL.md) for needed Android proof.

Add tests for meaningful behavior, not implementation mirrors. If credentials, devices or infrastructure
block required checks, continue independent checks and state the exact gap. Do not call weaker evidence
equivalent to the missing gate, or claim manual/device/CI validation that did not run.

## Review And Complete

Inspect the relevant diff and state for ownership, changed contracts, dependencies, resource/permission
changes, secrets and generated artifacts. Use targeted searches for plausible risks. Integrate the
repository's artifact-boundary review here, without duplicate review reports.

Report findings by impact, with evidence/location, affected behavior and suggested action; distinguish
confirmed defects, hypotheses and missing evidence. Include the covered baseline and validation limits.
No findings means none observed within that coverage, not a guarantee of no defects. Push, PR, merge,
release upload and deployment require corresponding authorization and their dedicated workflow.
