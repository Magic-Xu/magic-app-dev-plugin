---
name: app-change-self-check
description: Validate an implemented app change before handoff when choosing checks or assessing missing evidence needs guidance.
---

# App Change Self Check

Establish enough evidence that the requested behavior works and affected boundaries remain valid. Apply the repository's relevant engineering contracts; user instructions take precedence over this skill's guidance.

## Use The Existing Task Context

Use the accepted requirement, current diff, applicable rules and validation results already gathered. Inspect missing or changed context as needed, including nearby tests and the repository's exact build or CI commands. Separate this task's changes from unrelated work.

## Choose Evidence By Risk

- Pure logic: focused behavior tests and compilation for the affected target.
- UI or orchestration: state and interaction evidence for the changed flow; use a device, emulator or browser when visible behavior, navigation or lifecycle requires it.
- Platform or IO: deterministic tests plus integration evidence for the real provider, persistence, permission or system boundary that changed.
- Build, manifest or shared contracts: relevant lint, dependency checks and affected consumer compilation.
- Documentation or metadata: validate links, syntax, consistency and the affected reader path; compile or run the app only if executable behavior or instructions require it.

Complete applicable repository-mandated checks. A successful check for unchanged relevant inputs can be reused across delivery, architecture and self-check workflows. Rerun only after relevant changes, failures, or unresolved concerns. Add tests when they protect meaningful behavior, not merely to mirror an implementation.

If credentials, a device, network access or authorization prevents a required check, continue independent checks and state the exact evidence gap. Do not substitute weaker evidence and call the original check passed.

## Review And Complete

Inspect the final diff and status for ownership, changed contracts, unintended dependencies, resource or permission changes, secrets and generated artifacts. Use targeted searches for a plausible risk rather than rescanning the entire repository by default. Integrate any required artifact-boundary review here.

Fix defects introduced by the requested change and recheck the affected behavior before handing back. Report what changed, the material evidence and any remaining limitation; keep detailed logs out of the final answer unless needed for a decision. Do not claim device, CI or manual validation that did not run.

Push, PR, merge, release, upload and deployment require the user's corresponding authorization and the relevant delivery workflow.
