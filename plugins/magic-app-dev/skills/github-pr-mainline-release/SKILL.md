---
name: github-pr-mainline-release
description: "Use when a feature branch has been accepted and the user asks to push, create or reuse a GitHub pull request, merge safely to the mainline branch, delete the merged source branch, and restore the local workspace. Discover whether CI is configured: require successful CI for the exact PR head when present, or use completed repository-local validation without asking again when the repository has no CI."
---

# GitHub PR Mainline Release

## Purpose

Use this skill only after the user has reviewed or accepted a completed change and explicitly asks to merge it back to the mainline branch.

The required outcome is:

1. Push the accepted feature branch.
2. Create or reuse a GitHub pull request targeting the mainline branch.
3. Determine whether the repository has CI configured.
4. Require successful CI for the exact PR head when configured, or require final local validation when no CI exists.
5. Merge the exact reviewed PR head safely.
6. Restore the local workspace to the latest mainline branch.
7. Delete the merged remote and local source branches when safe.

## Preconditions

- Do not run this flow immediately after finishing implementation unless the user explicitly says to merge.
- If the user asks only for a summary, test, build, package, or review, stop before PR/merge work.
- Confirm the current branch with `git status --short --branch`.
- Do not perform the release from `main` or `master`; discover and check out the intended feature branch, and ask only if it cannot be determined unambiguously.
- Inspect uncommitted changes before staging. Commit only the accepted task scope.
- Discover the repository's validation commands from `AGENTS.md`, `README.md`, `docs/engineering/`, CI workflow files, package scripts, or build files.
- Run the narrow local checks expected by the repository before pushing, unless they were already run after the final change.
- Treat the user's explicit request to merge as authorization for the normal commit, push, PR, merge, safe source-branch deletion, and local-main restoration flow. Do not ask for a second confirmation when the target branch, change scope, and merge method are already discoverable.
- Ask only when proceeding requires a material new choice, such as changing the target branch, including unrelated changes, force-pushing a shared branch, bypassing configured CI, or deleting a protected/long-lived branch.

## Workflow

### 1. Discover Context

Find:

- remote repository name and URL
- mainline branch, usually `main` or `master`
- current feature branch
- PR convention, if documented
- required local validation commands
- CI workflow files and their triggers or path filters
- documented external checks, branch-protection requirements, workflow names, and jobs

Inspect the PR head tree for GitHub Actions workflows, for example:

```bash
git ls-tree -r --name-only HEAD .github/workflows
```

Classify CI according to checks that are intended or required to validate the proposed PR. A release-only, scheduled, or manual workflow is not PR CI merely because its file exists. Account for workflow triggers, target-branch filters, path filters, external providers, and required status checks.

Classify the repository as having no CI only when no relevant workflow, required status check, documented external check, or repository rule applies to the proposed PR. An empty workflow-run or legacy commit-status response alone is not evidence that CI is absent.

Prefer repository-specific rules over this generic flow when they are stricter.

### 2. Push The Branch

Use the current feature branch as the PR head:

```bash
git branch --show-current
git push -u origin <current-branch>
```

If push fails because the remote branch has moved, stop and inspect. Do not force push unless the user explicitly approves and the branch is known to be agent-owned.

### 3. Create Or Reuse The PR

Create a PR only if an open PR for the branch does not already exist.

The PR should include:

- concise title
- changed behavior
- validation that ran
- skipped checks or residual risks

Target the discovered mainline branch. Do not hardcode repository names.

### 4. Apply The Correct Validation Gate

Choose exactly one path.

#### CI Is Configured

Use the configured provider's workflow, check-run, or commit-status data as the source of truth.

Require:

- record the PR head SHA covered by each successful required validation run
- each required validation run belongs to the current PR and covers its current head source revision
- if the provider tests a synthetic PR merge revision, the run must belong to the current PR and be constructed from its current head and target base revisions
- each required validation status is completed and successful under the repository's policy
- neutral or skipped non-applicable jobs are accepted only when repository policy does not require them

Do not treat an empty legacy commit-status result as proof that CI is absent or passing. If no workflow run appears immediately after PR creation, wait and retry.

If CI fails:

- inspect failed jobs and logs
- summarize the root cause
- stop before merging

If a relevant check is configured but no matching current-PR run appears, use bounded polling and inspect triggers, filters, permissions, or provider state. Prefer a repository- or provider-defined timeout; otherwise poll only long enough to rule out normal propagation delay, then stop and report the configured-CI blocker. Do not wait indefinitely or silently use local checks instead.

#### No CI Is Configured

When no relevant CI workflow, documented external check, required status check, or repository rule applies to the proposed PR:

- require the repository's final local build, tests, lint/typecheck, and `git diff --check` as applicable
- require a clean worktree and evidence that those checks cover the exact pushed PR head commit rather than an older working-tree state
- record `CI not configured` in the PR or final handoff
- continue directly to merge when the user already asked to merge; do not ask for another confirmation
- do not add a new workflow merely to complete this release task unless the user asks for CI setup

### 5. Merge Safely

Before merging:

- re-read PR info
- require the PR to still be open and unmerged
- require the latest PR head SHA to match the recorded validated PR head SHA
- when CI used a synthetic PR merge revision, require its successful evidence to remain associated with the current head and current target base revisions
- require mergeability according to the repository's policy

Use the repository's preferred merge method. If undocumented, use squash merge for short-lived feature branches. When CI is configured, do not merge if a required result is missing, pending, cancelled, skipped, failed, or tied to an older SHA.

For a repository confirmed to have no CI, replace the CI-SHA requirement with evidence that final local validation passed for the exact pushed head SHA. Still require the PR head to match that SHA immediately before merging.

### 6. Restore Local Mainline

After the PR is merged, record the validated PR head SHA and the provider-reported integration result: the merge or squash commit SHA, or the rebased commit range and final rebased SHA. Then restore mainline:

```bash
git fetch origin
git checkout <mainline-branch>
git pull --ff-only origin <mainline-branch>
git status --short --branch
```

Require the recorded integration result to exist on local mainline, the worktree to be clean, and local mainline to match `origin/<mainline-branch>`. If the provider does not expose enough evidence to verify a rebase result, preserve the source branch. If local changes, divergence, conflicts, or pull failures appear, stop and report the blocker.

### 7. Delete The Source Branch

Delete only the exact source branch whose validated PR head was merged. Immediately before remote deletion, fetch and require the remote source ref to be absent or still equal to the recorded PR head SHA. If it moved, preserve it and report the new commits instead of deleting them.

When the remote ref still matches, delete it with an expected-SHA lease so a concurrent update cannot be lost:

```bash
git push --force-with-lease=refs/heads/<merged-feature-branch>:<pr-head-sha> origin --delete <merged-feature-branch>
```

If the remote branch is already gone, continue.

Never delete:

- `main`
- `master`
- release branches
- shared integration branches
- branches the user asks to keep

Before deleting the local source branch, require its tip to equal the recorded PR head SHA. A different local tip may contain unpushed work; preserve it and report the mismatch. For a normal merge, prefer checked deletion:

```bash
git branch -d <merged-feature-branch>
```

For a verified squash or rebase merge, use forced local deletion only after all preceding identity, synchronization, and tip checks pass:

```bash
git branch -D <merged-feature-branch>
```

Squash and rebase merges do not necessarily make the feature tip an ancestor of mainline, so `git branch -d` may reject an otherwise safe cleanup. The user's merge request authorizes this verified cleanup without another confirmation; a protected, long-lived, shared, or moved branch requires a new decision instead.

## Final Response

Report only decision-relevant facts:

- PR URL and number
- CI result, or `CI not configured` plus the local validation result
- merge commit or squash commit SHA
- deleted remote and local source branches, or why either was kept
- final local branch
- whether the local workspace is clean and up to date
