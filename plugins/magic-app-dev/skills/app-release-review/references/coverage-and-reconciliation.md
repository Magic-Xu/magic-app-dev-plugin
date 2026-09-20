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

For each material change or retained critical outcome, connect:

| Change and promises to preserve / source | Reachable paths, owners and affected consumers | Scenario and expected outcome | Evidence / disposition |
| --- | --- | --- | --- |
| New outcome and existing obligations it touches | Entry, state/rule, platform operation, result; old path if replaced | What would expose a regression, and what must hold | Located defect, inspected/verified with limits, or explicit gap |

Include retained core flows and release configuration in the inventory. Inspect the candidate's dependency
and ownership structure, not only added lines. Review changed behavior deeply, trace affected shared owners
and unchanged consumers, and check critical retained paths. Expand when evidence reveals wider coupling.
Full-version coverage does not imply every line was inspected; state sampled or unverified areas precisely.

## Derive The Impact Of Each Change

Start from what changed in user behavior, not a fixed catalog of feature types. Identify changed inputs,
state/identity lifetimes, data representation, business decisions, ordering, external operations and
dependencies. Follow these to their owners and consumers, including unchanged callers. A new entrypoint,
alternate executor or moved responsibility can bypass old behavior without deleting its implementation.

When a route is replaced or split, compare the responsibilities along both complete paths: admission,
validation, transformation, commit, acknowledgement and cleanup. Account for each affected obligation in
the new route or an explicitly approved removal. Check early exits before the usual handler and work after
the apparent success point. Follow both normal results and error propagation; merely finding the old
helper or a new equivalent name does not establish that it still runs with the same meaning.

Screen these dimensions against the release's actual changes and retained critical flows. Expand affected
dimensions in the map; briefly justify material exclusions or unchanged evidence reuse. This is a coverage
check, not a demand for a feature-by-dimension Cartesian checklist or new product capabilities.

| Responsibility | Questions that determine affected scope |
| --- | --- |
| User outcomes and business rules | Do entrypoints, settings, defaults, output fidelity, entitlements and external effects still fulfill accepted behavior? Does a new route preserve rules enforced by the old one? |
| State, time and ownership | Have identity, cardinality, lifetime, ordering or concurrency changed? Can old results, retries, navigation or restoration act on a different entity or repeat an effect? |
| Data and trust boundaries | Are persistence, migration, privacy, permissions and account boundaries preserved across new storage, services or dependencies? Does accepted input still produce compatible output? |
| Failure and recovery | Who reports rejection, cancellation, partial completion and errors before/after commit? Can the user recover without false success, lost data, duplicate work or leaked resources? |
| Measurement and diagnosis | Do existing metrics still measure the same entity, unit, source, denominator and completion boundary? Can changed-path failures be located from safe diagnostics, including failures outside the old instrumented region? |
| Experience and operating limits | Are interaction, accessibility, localization, latency, memory, battery/storage use and offline behavior preserved under representative workloads and affected devices? |
| Delivery and public promises | Do build variants, SDK/service configuration, package/upgrade behavior, store/legal claims and support information still match the candidate? |

These dimensions identify questions, not automatic defects. Use the product's accepted constraints and
baseline to judge consequences. Approved trade-offs are not regressions. An absent optional metric or
service is not a blocker simply because this skill mentions measurement; a broken existing contract is
different from a proposed improvement. A first release uses accepted outcomes and platform obligations
instead of inventing historical behavior.

## Turn Impact Into Discriminating Scenarios

For each affected promise, state what must remain true and how the change could violate it. Choose inputs,
operation orderings and failure points that distinguish the required behavior from a plausible faulty
implementation. Inspect or exercise those paths, including their real dispatch and terminal consumers.
Use the scenario to select proof; do not choose scenarios only because tests already exist for them.

Changed multiplicity, identity or lifetime calls for checking the unit of ownership: one action, item,
session, account or committed operation may no longer coincide. This can affect business rules, resource
cleanup, analytics deduplication and diagnostic context alike. Changed asynchronous or external work calls
for examining admission, cancellation, commit and retry separately. Changed storage or dependencies calls
for compatibility and affected-consumer checks. Apply only the transformations that actually occurred.

Where measurement is affected, follow values and event timing to their producer and declared consumer;
event existence/schema validity does not prove attribution, counts or funnel semantics. Where diagnosis is
affected, check that relevant failures retain a useful stage/cause and bounded context without exposing
user content; adding raw logging everywhere is not a repair. Select local, device and service evidence
according to what changed, as described in [release-evidence.md](release-evidence.md).

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
