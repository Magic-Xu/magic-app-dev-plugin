---
name: github-pr-mainline-release
description: Merge accepted work into the repository mainline when the user explicitly requests integration, with validation of the current PR head, safe source-branch cleanup, and local workspace restoration.
---

# GitHub PR Mainline Release

Complete an explicitly requested mainline integration: commit and push the accepted scope, create or reuse its PR,
validate the current head, merge, and safely restore the workspace and clean up the source branch. A request only
to push or create a PR authorizes that narrower operation; do not run the merge and cleanup flow for it.

## Establish Scope And Repository Policy

Inspect the branch, diff, worktree ownership, remote, target mainline, and any existing PR. Commit only the accepted
task changes. Use the intended feature branch for integration; if it cannot be identified unambiguously, ask.
Discover the applicable validation, branch protection, required checks, and merge convention from repository policy
and provider state. Reuse checks already passed for the final relevant code and environment.

The merge request authorizes the normal commit, push, PR, merge, verified short-lived source-branch deletion, and
local-main restoration flow. Reuse that authorization. Ask before changing the target or accepted scope, force-pushing
a shared branch, bypassing CI, or deleting a protected/long-lived branch. Preserve unrelated changes and worktrees.

## Push And Open The PR

Push the selected feature branch and create a PR only if none is already open for it. Target the discovered mainline.
Describe changed behavior, validation evidence, and material gaps. If the remote branch moved, inspect before
retrying; a history-rewriting push needs explicit authorization and confirmed agent ownership.

Determine which CI applies to this PR from workflow triggers, branch/path filters, external providers, required
status checks, and repository rules. Scheduled, manual, or release-only workflows are not automatically PR CI.
Empty run lists or legacy commit-status responses do not establish that relevant CI is absent or passing.

## Validate The Current Head

Record the PR head SHA and apply the appropriate gate:

| Relevant CI | Required evidence |
| --- | --- |
| Configured | All required validation is completed and successful under repository policy for the current PR and head. A synthetic merge run must correspond to its current head and target base revisions. Accept neutral/skipped non-applicable jobs only when policy does not require them. |
| Not configured | Repository-required local build, tests, lint/typecheck, and diff checks as applicable, with a clean worktree and evidence covering the exact pushed head. Record `CI not configured` and continue without requesting confirmation again. |

If CI fails, pause merging, inspect the failure, and fix task-caused defects within the authorized scope. Run affected
validation and update the PR; changed code requires evidence for the new head. Report failures that need new scope,
credentials, permissions, or external recovery while continuing independent authorized work. Do not bypass the gate.

If an expected run is missing, allow normal propagation and inspect triggers, filters, permissions, or provider
state. Use bounded polling with the repository/provider timeout when defined; otherwise stop after ruling out normal
propagation delay and report the blocker. Do not wait indefinitely or silently substitute local checks for configured
CI. A no-CI repository does not require adding a workflow just to complete this integration.

## Merge And Record The Result

Immediately before merging, re-read the PR and require that it is open, unmerged, mergeable under repository policy,
and still at the validated head. For synthetic merge validation, verify that the evidence still covers the current
base as well. Missing, pending, cancelled, failed, required-skipped, or stale results block merging.

Use the repository's merge method; default to squash for a short-lived feature branch when none is documented.
Record the validated source head and the provider-reported integration result: merge/squash SHA, or the rebased
commit range and final SHA. If a rebase result cannot be verified, preserve the source branch.

## Restore The Workspace

Fetch and update the task's mainline checkout with fast-forward-only operations. Account for linked worktrees;
do not switch or modify another active task's checkout to restore this one. If ownership or local divergence prevents
a safe restoration, retain the current worktree and report the gap.

Require the integration result to exist on local mainline, local mainline to match `origin/<mainline>`, and the task
worktree to be clean before the normal cleanup flow. Preserve local edits, divergent commits, and unresolved worktree
state. A completed remote merge and an incomplete local restoration must be reported separately.

## Delete Only The Merged Source

Delete only the short-lived source branch whose recorded head was integrated. Preserve mainline, release/shared
integration branches, branches the user wants to keep, and any source branch whose tip moved.

Immediately before remote deletion, fetch and require the remote source to be absent or still at the recorded PR
head. If it matches, use an expected-SHA lease so a concurrent update is protected:

```bash
git push --force-with-lease=refs/heads/<merged-feature-branch>:<pr-head-sha> origin --delete <merged-feature-branch>
```

If it is already absent, continue. Before local deletion, require the local tip to equal the recorded head and
confirm it is not in use by another worktree. Prefer `git branch -d <merged-feature-branch>` for a normal merge.
For a verified squash or rebase, `git branch -D <merged-feature-branch>` is allowed only after the integration,
synchronization, ownership, and tip checks above pass; the source tip need not be an ancestor after those methods.
A moved ref or failed lease is a reason to preserve and report the branch, not to retry unconditionally.

## Hand Off

Report the PR URL, validated head and CI result (or no-CI local evidence), integration result, source branches deleted
or retained, final local branch/worktree, and whether it is clean and synchronized. Claim only operations verified
complete; identify any remaining external or local blocker.
