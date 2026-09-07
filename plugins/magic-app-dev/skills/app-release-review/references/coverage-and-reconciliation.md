# Release Coverage And Reconciliation

## Identify The Actual Version

Resolve the app, previous published version and its binary/source identity, candidate source revision
and artifact when available, and which uncommitted or unmerged work is included. Use release records,
history and accessible Console evidence. The latest tag, branch name, filename or changelog alone does
not prove what shipped. Keep the live store revision separate from the source/binary baseline.

Respect a user-selected comparison range. When histories diverge, inspect merge bases without silently
replacing the release baseline. Do not merge other active feature worktrees to manufacture a candidate;
identify unintegrated requirements and assess their available source separately. For a first release,
review the accepted product and candidate as a whole without inventing a previous release.

If plausible baselines materially change the result, inspect records before asking. Continue independent
inspection with provisional coverage and label the unresolved scope. Do not issue a complete release verdict
when the baseline, included requirements or candidate cannot be established.

## Reconstruct The Product, Not Just The Diff

Use accepted requirements/designs, decisions, release records, history, merged PRs/issues when available,
and the net diff to inventory delivered feature outcomes. Account for squash commits, reversions and
partial implementations. Commit titles/counts are not a feature inventory.

For each material outcome, connect:

| Accepted behavior / source | Implementation path and shared owners | Proof | Gap / conflict |
| --- | --- | --- | --- |
| What must happen and what must remain available | Entry, state/rule, platform operation, result | Test or observed outcome tied to candidate | Missing, contradicted, unverified, or none observed |

Include retained core flows and release configuration in the inventory. Inspect the candidate's dependency
and ownership structure, not only added lines. Review changed behavior deeply, trace affected shared owners
and unchanged consumers, and check critical retained paths. Expand when evidence reveals wider coupling.
Full-version coverage does not imply every line was inspected; state sampled or unverified areas precisely.

## Reconcile Conflicting Sources

Separate normative evidence (accepted behavior and enforced project constraints) from descriptive evidence
(what code, tests, comments and store content currently do). Check applicability and supersession using
decisions and history, not filename freshness. Exact APIs must also match installed/locked dependencies.

When sources disagree, determine whether the problem is stale documentation, a real implementation
regression or an unresolved product decision. Code is not automatically correct because it compiles;
documentation is not automatically current because it calls itself authoritative. Do not alter requirements
to match accidental behavior, nor restore obsolete behavior solely to satisfy an old paragraph. Preserve
project approval rules and ask when the conflict cannot be resolved from authoritative evidence.

## Inspect Both Directions

- **Requirement to implementation:** Follow the real entry through state transitions, business rules,
  dependency wiring and final observable result. Look for inert controls, unreachable implementations,
  missing error/cancel/retry paths, incomplete locale or build-variant coverage, and removed retained behavior.
- **Implementation to requirement:** Explain substantial new state, branches, persistence, background work,
  abstractions, dependencies and permissions. An engineering/platform obligation may justify code without
  a standalone feature requirement. Verify actual consumers and compatibility before calling it excess.
- **Proof to behavior:** A test can share the implementation's wrong assumption. Derive the expected outcome
  from independent accepted behavior and inspect what the assertion really establishes.

Do not infer that a defect was caused by AI or a large context. Identify the verifiable failure: nonexistent
or version-incompatible API, disconnected implementation, invented product rule, false success, swallowed
failure, stale source or unsupported recovery promise.

## Inspect Feature Interactions

Identify shared mutable facts, settings, output pipelines, entitlements, navigation, resource lifetimes
and external commits. Select combinations through these shared owners and product invariants, rather than
testing every possible pair or assuming separately passing features integrate correctly.

Exercise relevant orderings: A then B versus B then A, overlapping operations, late completion after a
replacement, cancellation/retry, navigation/backgrounding, and recreation or upgrade during a critical flow.
Verify which version of settings/input an operation consumes and who may commit its result. Compare preview
and final output when both claim the same business semantics.

Examples of useful probes include changing input while analysis runs, saving while another entry imports
media, settings updates during export, and restoration after an external write. Choose only scenarios that
apply to the target product; these are review prompts, not required features or assumed existing defects.
