---
name: github-pr-mainline-release
description: Use when a feature branch has been accepted by the user and they ask to push, create or reuse a GitHub pull request, wait for GitHub Actions CI, merge safely to main, delete the merged remote feature branch when appropriate, and restore the local workspace to an up-to-date main branch. Repository-agnostic; discover repo, CI, and validation commands from local context before acting.
---

# GitHub PR Mainline Release

## Purpose

Use this skill only after the user has reviewed or accepted a completed change and explicitly asks to merge it back to the mainline branch.

The required outcome is:

1. Push the accepted feature branch.
2. Create or reuse a GitHub pull request targeting the mainline branch.
3. Wait for GitHub Actions CI to complete for the PR head commit.
4. Merge only when CI succeeds for the exact commit being merged.
5. Delete the merged remote feature branch when it is safe.
6. Restore the local workspace to the latest mainline branch.

## Preconditions

- Do not run this flow immediately after finishing implementation unless the user explicitly says to merge.
- If the user asks only for a summary, test, build, package, or review, stop before PR/merge work.
- Confirm the current branch with `git status --short --branch`.
- Do not start from `main` or `master`; ask for the intended feature branch.
- Inspect uncommitted changes before staging. Commit only the accepted task scope.
- Discover the repository's validation commands from `AGENTS.md`, `README.md`, `docs/engineering/`, CI workflow files, package scripts, or build files.
- Run the narrow local checks expected by the repository before pushing, unless they were already run after the final change.

## Workflow

### 1. Discover Context

Find:

- remote repository name and URL
- mainline branch, usually `main` or `master`
- current feature branch
- PR convention, if documented
- required local validation commands
- GitHub Actions workflow names and jobs

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

### 4. Wait For CI

Use GitHub Actions workflow/run data as the source of truth.

Require:

- workflow run belongs to the PR head SHA
- status is completed
- relevant jobs conclude with success

Do not treat an empty legacy commit-status result as proof that CI is absent or passing. If no workflow run appears immediately after PR creation, wait and retry.

If CI fails:

- inspect failed jobs and logs
- summarize the root cause
- stop before merging

### 5. Merge Safely

Before merging:

- re-read PR info
- require the PR to still be open and unmerged
- require the latest PR head SHA to match the SHA whose CI passed
- require mergeability according to the repository's policy

Use the repository's preferred merge method. If undocumented, prefer squash merge for feature branches. Do not merge if CI is missing, pending, cancelled, skipped, failed, or tied to an older SHA.

### 6. Delete The Remote Feature Branch

After GitHub reports the PR merged, delete the remote source branch unless it is protected or long-lived:

```bash
git push origin --delete <merged-feature-branch>
```

Never delete:

- `main`
- `master`
- release branches
- shared integration branches
- branches the user asks to keep

If deletion fails because the branch is already gone, continue.

### 7. Restore Local Mainline

After the PR is merged:

```bash
git checkout <mainline-branch>
git pull origin <mainline-branch>
git status --short --branch
```

The final local state should be clean and aligned with `origin/<mainline-branch>`. If local changes, conflicts, or pull failures appear, stop and report the blocker.

## Final Response

Report only decision-relevant facts:

- PR URL and number
- CI result
- merge commit or squash commit SHA
- deleted remote branch, or why it was kept
- final local branch
- whether the local workspace is clean and up to date
