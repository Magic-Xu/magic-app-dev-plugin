---
name: app-end-to-end-delivery
description: Use when implementing, validating, packaging, or handing off an app feature or bug fix end to end across a local repository. Guides Codex through requirement clarification, branch/worktree hygiene, scoped implementation, automated and device/browser validation, install/package verification, and delivery reporting. Do not use it to push, open PRs, merge to main, delete branches, or release unless the user explicitly asks for those delivery actions.
---

# App End-to-End Delivery

## Purpose

Use this skill to turn an app change request into a complete, evidence-backed handoff. It is repository-agnostic: follow local project rules first, then use this workflow to avoid stopping at "code compiles" when the user expected a working product path.

## Hard Boundary

Do not start PR, mainline merge, branch deletion, release, store upload, or production deployment work unless the user explicitly asks for that action.

Treat phrases like "继续开发", "验证一下", "重新安装", "打包", "给我看效果", or "可以了" as implementation or validation instructions, not permission to merge.

If the user explicitly asks to merge, release, or clean branches, use the repository's dedicated release/PR skill if one exists. Otherwise discover the repo policy and ask before any irreversible remote operation.

## Workflow

### 1. Clarify The Target

Start from the user's real desired outcome, not from a template.

- Identify the user-visible workflow being changed.
- Define success in observable terms: screen state, persisted data, generated file, installed app behavior, API response, or test result.
- Ask only if the missing answer changes implementation or validation. Otherwise make a conservative assumption and state it.
- Record explicit non-goals when the user rejects a path or scope.

### 2. Inspect Local Rules And State

Before editing:

- Read `AGENTS.md` or equivalent local instructions.
- Inspect relevant docs such as `README`, `docs/engineering`, architecture decisions, workflow docs, or CI files.
- Check branch and worktree state with `git status --short --branch`.
- If the repo forbids direct edits on `main` or `master`, create or use an existing feature branch/worktree before editing.
- Never revert unrelated user changes. If unrelated dirty files exist, leave them alone.

### 3. Implement In The Right Layer

Keep the change aligned with the app's architecture.

- Put UI rendering in UI components only.
- Put navigation, state transitions, persistence, playback, network, file, and platform decisions in the existing app/state/platform layers.
- Prefer existing helpers, design tokens, resource systems, and test patterns.
- Keep edits tightly scoped. Avoid opportunistic refactors unless they remove real risk for this request.
- Add strings, accessibility labels, permissions, and platform declarations through the repo's normal mechanisms.

### 4. Validate By Risk

Run the narrowest checks that can prove the change, then broaden when the blast radius is larger.

Always consider:

- Compile/build for the changed target.
- Unit tests for changed business logic or reducers.
- Static checks, lint, typecheck, formatting, or `git diff --check`.
- UI tests or integration tests when a stateful user flow changed.
- Device/emulator/browser validation when the change affects visible app behavior.

For app UI work, validation should include real interaction evidence where practical:

- Launch the app from a clean or known state.
- Navigate through the changed user flow from the real entry point.
- Exercise the success path and at least the likely regression path.
- Capture screenshots, UI tree, logs, terminal output, or generated artifacts as evidence.
- Verify after installation/package if the user asked to install, package, or "see it on device".

Do not call a single adb/browser screenshot "full end-to-end delivery" unless it covers the complete accepted path and post-change state. Label it accurately as smoke, regression, device, browser, or full E2E validation.

### 5. Package Or Install Only When Requested Or Needed

If the app must run from an installable package, build the package and install it when the user asks or when device validation requires it.

- Use the repo's normal build command.
- Install the artifact that was just built.
- Re-run the user-visible flow after install when install behavior matters.
- Report the exact artifact type and validation device/simulator/browser.

### 6. Prepare A Handoff

Before final response:

- Check `git status --short --branch`.
- Summarize what changed and why, not every file touched.
- List validation commands and whether they passed.
- Include concrete evidence paths only when useful.
- State anything not validated and why.
- Do not claim PR, CI, merge, release, or production completion unless those actions actually happened.

## Delivery Escalation

Only after explicit user instruction such as "走 PR", "创建 PR", "合并到主干", "发布", "清理远端分支", or equivalent:

1. Re-check branch status and remote state.
2. Commit only accepted in-scope changes.
3. Push the feature branch.
4. Create or reuse a PR targeting the mainline branch.
5. Wait for CI for the exact PR head SHA.
6. Merge only when CI succeeds and repository policy allows it.
7. Clean merged branches only when safe and requested or documented.
8. Restore local mainline and verify it is clean and up to date.

If a dedicated PR/mainline-release skill exists, use it for this section instead of reimplementing it.

## Final Response Template

Use concise prose. Include:

- Changed behavior.
- Important implementation boundary or root cause.
- Validation run.
- Install/package status if applicable.
- Remaining risk or skipped validation.

Avoid long file inventories unless the user asked for them.
