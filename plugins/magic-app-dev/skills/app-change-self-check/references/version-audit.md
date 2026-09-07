# Audit A Whole Version

Use for cumulative release/iteration review. The unit of analysis is all delivered behavior between a
selected baseline and candidate, plus interactions with retained behavior, not just the latest commit.

## Establish Coverage

Resolve the target app, prior published binary/source identity, candidate commit or supplied artifact,
and whether specified uncommitted work belongs in scope. Use release records, tags and Console evidence
when accessible; a latest Git tag or changelog alone may not identify the published source. Keep the
live store revision separate. A user-specified comparison range takes precedence.

Use history, net diff, merged PRs/issues when accessible, and accepted requirements to inventory feature
outcomes. Account for squash commits, reverted work and already merged features; commit counts and titles
are not a reliable product inventory. Label sources that cannot be mapped to a release instead of
inventing provenance. Compare merge bases when histories diverge, but do not silently replace the chosen
release baseline with a convenient merge base.

For each material feature, connect intended behavior, implementing paths, changed data/commercial
boundaries, design/docs, and relevant proof. Keep a compact table in the requested report; use existing
release records rather than a mandatory new file per audit.

## Inspect Across Features

| Area | Review question |
| --- | --- |
| Product behavior | Did the version deliver its accepted scope while preserving retained core behavior? Are removals or paid restrictions explicitly accepted? |
| Architecture | Do state, domain, platform and app coordination still have clear owners across features? Have dependency cycles, sibling imports or duplicated business state appeared? |
| State and lifecycle | Do navigation, effects, process recreation, cancellation, persistence and shared resources behave consistently when features interact? |
| Design and resources | Does implemented behavior match approved design, supported locales, accessibility and tokens? |
| Data and monetization | Do actual SDK/data flows, entitlements, ads, permissions and offline behavior match requirements and declarations? |
| Documentation | Do current requirements, architecture decisions, operator commands and design sources reflect the candidate? Are obsolete constraints still instructing new work? |
| Release/store truth | Do live claims and screenshots remain accurate across cumulative changes? Report None/Partial/Full recommendation via the Play assessment without writing Console in an audit. |
| Verification | Does proof cover the combined core flow and relevant regressions, not merely each feature in isolation? |

Use [architecture review](../../android-app-architecture-guardrails/SKILL.md) for boundary judgments and
the self-check evidence matrix for validation. Follow the repository's mandatory audit/release gates
when applicable. Existing valid evidence can be reused, but separate per-feature tests may leave a
cross-feature integration gap. Read-only audit does not authorize installing over user data or changing
external configuration; observe the requested device/test scope.

## Return A Decision-Ready Review

Lead with severity-ranked findings: concrete location/source, observed conflict, user/maintenance impact,
and smallest useful correction. Separate blockers, important follow-up and optional debt; architecture
preference alone is not a defect. Include baseline/candidate, feature coverage and evidence gaps.

When sources disagree, distinguish stale documentation, a real implementation regression and an
unresolved product decision. Do not automatically update the requirement to legalize observed behavior.
If fixes are later requested, reuse this inventory, branch/worktree mapping and still-valid evidence;
changes to approved UI, core behavior or publication scope follow the corresponding gate.
