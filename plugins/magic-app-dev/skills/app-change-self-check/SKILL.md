---
name: app-change-self-check
description: "Use after Codex changes app code, resources, build files, tests, or docs and needs to self-check before handoff. Guides repository-agnostic validation: inspect local rules, run risk-based checks, rescan architecture and UI regressions, confirm git diff/status, and report concrete evidence plus skipped validation. Do not use for PR creation, merge, release, store upload, or production deployment."
---

# App Change Self Check

## Purpose

Use this skill after an app change is implemented and before handing it back to the user. The goal is to prove the change is coherent, scoped, and ready for the user's next validation step without pretending that unrun device, browser, CI, or manual checks happened.

Prefer repository-specific rules when they are stricter.

## Workflow

### 1. Reconstruct The Actual Change

- Read the newest user request and any explicit exclusions.
- Check `git status --short --branch`.
- Inspect the diff with `git diff --stat` and targeted `git diff` for risky files.
- Separate your changes from unrelated dirty work. Do not stage, revert, or summarize unrelated changes as yours.
- Identify the changed user workflow or engineering boundary in observable terms.

### 2. Re-read Local Validation Rules

Look for local sources before choosing commands:

- `AGENTS.md` or equivalent agent instructions.
- `README`, `docs/engineering`, architecture decisions, release checklists, or validation docs.
- CI/workflow files.
- Build files and package scripts.
- Nearby tests for changed modules.

Use the repo's exact commands when available. If rules conflict, follow the stricter local rule.

### 3. Select Checks By Risk

Run the narrowest checks that can catch the likely regressions, then broaden when the blast radius is larger.

Always consider:

- Syntax/format safety: `git diff --check`, formatter, typecheck, or lint.
- Compile/build for the changed target.
- Unit tests for changed pure logic, reducers, mappers, repositories, or gateway wrappers.
- UI/integration tests when screen state, navigation, persistence, import/export, playback, network, or platform effects changed.
- Device/emulator/browser validation when visible behavior or platform APIs changed and the user did not explicitly skip it.

If a check needs network, a device, credentials, paid services, production resources, or approval, do not fake it. Run what is available and state the gap.

### 4. Run Focused Static Rescans

Choose rescans that match the app and change type. Examples:

- File size hotspots: `rg --files -g '*.kt' | xargs wc -l | sort -nr | head`.
- Hardcoded UI strings in code when resources/i18n are required.
- Direct platform calls from UI layers when gateways/effect handlers are expected.
- Secrets, API keys, raw prompts, paths, filenames, URIs, or provider responses in source/logging.
- Unexpected dependency, permission, manifest, entitlement, or build config changes.
- Duplicate helpers or mixed responsibilities introduced by the change.

Treat scan results as evidence to interpret, not as a checklist to pass mechanically.

### 5. Verify Behavior Boundaries

Before handoff, answer these questions from the diff and checks:

- Does the change solve the original problem rather than patching a symptom?
- Is the responsibility in the right layer for this repo?
- Did any public contract, navigation route, persistence schema, resource set, permission, or provider boundary change?
- Are existing user flows preserved unless the user asked to change them?
- Are new failure states explicit and user-safe?

If the answer is uncertain, either inspect more, run another focused check, or report the residual risk clearly.

### 6. Final Git And Evidence Check

Before final response:

- Re-run `git status --short --branch`.
- Confirm generated artifacts, build outputs, screenshots, logs, or temporary files are not accidentally included.
- Capture the exact commands that passed or failed.
- Note skipped checks with the reason, especially device/browser/manual validation.

Do not end with running sessions still active.

## Handoff Format

Keep the final answer concise and decision-relevant:

- What changed, grouped by behavior or architecture boundary.
- Why the structure is safer or more maintainable.
- Validation commands and pass/fail result.
- What was not validated and why.
- Residual risk or the next user validation step.

Do not list every file unless the user asks. Do not claim "fully verified" if only compile or unit tests ran.

## Escalation Boundary

This skill stops at self-check and handoff. If the user asks to push, create a PR, merge, release, upload, or clean branches, use a dedicated repository release or GitHub mainline skill when available.
