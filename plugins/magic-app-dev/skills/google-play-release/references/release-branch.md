# Establish And Preserve The Binary Release Branch

Run this gate for the requested binary version before release preparation, including draft resumption.
The formal branch preserves the version's source line for release fixes; a temporary task branch is an
editing boundary and may be deleted after integration. Do not treat the two roles as interchangeable.
Store-only edits and read-only inspections use the project's normal task rules without creating a new
binary release branch.

## Resolve, Create Or Reuse

1. Resolve the version name, configured project remote, mainline and accepted source commit. Use the
   project's release naming; otherwise use `release/<versionName>`. Fetch the remote and inspect both
   local and remote release refs and linked worktrees. A missing local ref alone does not mean the
   release branch is absent. If fetching fails, report the gate as blocked rather than use stale refs.
2. For a new release without an existing branch, use the freshly fetched remote mainline after confirming
   it is the accepted candidate. A user-specified or project-defined release baseline takes precedence.
   For a supplied AAB or resumed upload, verify its recorded source instead of substituting today's
   mainline. If the source cannot be established, or required code is still on an unmerged feature branch,
   resolve that gap before proceeding; creating the release does not authorize merging code.
3. Reuse an existing branch only after checking its version/source relationship. If only the remote ref
   exists, create a local tracking branch at that ref. If neither exists, create the local release branch
   at the resolved source, push it to the configured remote and set its upstream. These routine steps are
   covered by an authorized release-preparation request; do not wait for the user to request them again.
4. When only a local branch exists, check its provenance and task scope before pushing. If both refs
   exist at different SHAs, inspect the commits and worktree state; reconcile only verified in-scope
   fast-forward changes. Preserve divergent or unexplained changes and resolve the conflict. Never reset
   or force-push an existing release branch to the newest mainline to make the gate pass.
5. Verify the remote ref and local ref agree at the intended SHA and the upstream targets that branch.
   Record this branch, remote and source baseline in the existing release record. If creation, push or
   verification is blocked, continue independent read-only assessment, report the precise gap, and keep
   builds, persistent release changes and Console writes behind the gate.

## Use The Project's Editing Boundary

A formal release branch can be established without switching the current checkout. If project policy
requires a separate `codex/*` branch and linked worktree, create or reuse that task workspace as directed;
retain the formal release branch alongside it. Otherwise use a release worktree without displacing another
task. Preserve unrelated dirty files and existing worktree ownership.

Before accepting or uploading the final AAB, verify its packaged code is represented by the formal release
history. Build and test version bumps or fixes in the permitted task workspace, then use the project's
authorized integration path before accepting that binary. Once integrated, advance the release branch only through the verified,
permitted fast-forward path and push it; do not pull unrelated newer mainline changes into a frozen release.
Keep the exact packaged source SHA separate from later documentation/store-only commits. A changed branch
tip alone does not require rebuilding an unchanged, verified AAB.

## Verify At Handoff

Recheck branch/source correspondence and local/remote agreement before declaring preparation complete.
Retain the formal release branch through later PR cleanup; only a verified short-lived task branch is a
cleanup candidate. Report the release branch, remote SHA, packaged source SHA and final working location.
If mainline restoration was requested, restore the task's mainline checkout safely after preserving its
work; do not discard unfinished edits just to switch branches.
