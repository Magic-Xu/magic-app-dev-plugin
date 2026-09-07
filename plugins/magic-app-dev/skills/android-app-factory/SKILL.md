---
name: android-app-factory
description: "Bootstrap a new Android app workspace as two sibling Git repositories: a private-ready Jetpack Compose and pulse MVI app repository plus a public-ready multilingual GitHub Pages product and legal repository. Use for repeatable new-app creation, not routine feature work in an existing app."
---

# Android App Factory

Create a locally coherent app workspace while preserving the two visibility boundaries required by GitHub Pages on GitHub Free.

## Outcome

Generate one parent workspace containing:

- An Android repository with a minimal compiling Jetpack Compose shell, pulse MVI contract, design tokens, tests, localized resources, and a repository information architecture with an automated layout gate.
- A public-site repository with a product homepage, Privacy Policy, User Agreement, English and Simplified Chinese routes, and GitHub Pages files.
- A private copy of the legal-site source plus a safe sync script, so the Android repository remains the source of truth and the public repository is a publishing target.

Do not copy an existing business app as the template. The starter must not include ads, analytics, accounts, billing, server upload, Firebase, ML Kit, or product-specific permissions.

## Required Inputs

Before creating files, resolve:

- App display name.
- Filesystem and repository slug.
- Android application ID.
- GitHub owner.
- One English product sentence and one Simplified Chinese product sentence.
- Parent directory for the generated workspace.
- Whether the user is requesting local repositories only or also remote GitHub creation and Pages publishing.

Repository names default to "<slug>-android" and "<slug>-legal". Read [references/spec-schema.md](references/spec-schema.md) when validating or changing the accepted inputs.

The Factory selects its tested stable Magic Android Platform version by default. Do not ask the
user to choose a version during normal app creation. Use `--magic-platform-version` only when the
request explicitly requires testing another already-published stable version.

Before advancing the Factory default, manually run the repository's `Android App Factory`
workflow with the published candidate in `magic_platform_version`. This validates a newly generated
workspace without changing the current default. Only after that run succeeds, update the default
version in a separate change; pull-request CI then repeats the full generation and build against the
new default.

If a product sentence cannot be derived without inventing the app's purpose, stop and ask. Repository names and the standard locale set may use the defaults unless the user says otherwise.

## Workflow

1. Preflight before any mutation.
   - Confirm the parent directory and exact destination paths.
   - Refuse an existing destination rather than merging or overwriting it.
   - Confirm JDK 17 or newer is available, including Android Studio's bundled JBR.
   - If remote creation was requested, run "gh auth status" before creating local files. An authentication failure changes the deliverable; ask before switching to local-only creation.
2. Create the local workspace with "scripts/create_workspace.py".
   - Run with "--dry-run" first and inspect the resolved paths and names.
   - Then run without "--dry-run".
   - Omit "--magic-platform-version" for normal generation so the Factory-tested default is used.
   - The generator stages all files before moving the completed workspace into place.
3. Validate with "scripts/validate_workspace.py".
   - Always run structural validation, including the generated repository-layout validator and its contract tests.
   - Run `check`, Debug and Release APK builds, and the Release AAB when an Android SDK is available.
   - The validator may use `--platform-source` for local Factory acceptance only. Never persist that local path in a generated repository.
4. Review legal accuracy.
   - The generated shell truthfully declares no accounts, server upload, ads, billing, analytics, or sensitive permissions.
   - If the requested initial implementation adds any of those capabilities, do not publish the default legal pages. Update the capability model and legal content after inspecting the real implementation.
5. Publish only when authorized.
   - Read [references/github-publishing.md](references/github-publishing.md).
   - Run "scripts/publish_github.py" without "--apply" to inspect the plan.
   - Use "--apply" only when the user explicitly asked to create or publish the remote repositories.
6. Report the two local paths, remote visibility, Pages URL, validation commands, and any incomplete external step.

## Important Boundaries

- The bundled generator is the authoritative project template because the official Android CLI's built-in templates do not encode this repository's pulse, MVI, localization, legal-publishing, and paired-repository conventions.
- The Factory seeds each Android repository's own layout policy and CI gate because required sources and compatibility paths remain app-owned. Promote only proven cross-app invariants to Platform Quality; keep product-specific paths in the consumer app.
- Android CLI may still be used for SDK, emulator, project inspection, and device QA. Do not invoke the deprecated SDK "tools/android" binary as the new Android CLI.
- Never create public repositories containing Android source, secrets, signing material, local properties, internal specifications, or private product documents.
- Never silently adopt an existing remote repository. Stop if a target remote name already exists and is not already the expected origin of the generated local repository.
- Do not delete partially created remote repositories automatically. Report the exact state and use the publisher's resumable behavior after the user resolves the failure.
- GitHub Pages content is public even when a plan permits Pages from a private repository.

## Product Lifecycle Handoff

The generated documentation index is the project's source map and includes a product-design approval
policy. Use accepted product decisions from [产品规划](../local-first-android-app-builder/SKILL.md);
the generated ready screen does not constitute approval of the product UI. Before later user-visible
features, follow the generated design gate. Console setup and live release baselines are established
by [Google Play 发版](../google-play-release/SKILL.md) when that work is requested, not by scaffolding.
Do not retrofit another existing app as a side effect of updating the generator.

## Generated Structure

Read [references/generated-layout.md](references/generated-layout.md) when changing template contents or diagnosing a generated workspace.

## Acceptance

- Both child directories are independent Git repositories on branch "main" with clean initial commits.
- The Android app passes `check`, `:app:assembleDebug`, `:app:assembleRelease`, and `:app:bundleRelease`.
- The app uses the released Magic Android Platform Application, Compose, Pulse, and Quality plugins at one pinned version.
- The app uses Pulse 0.4 feature-owned Stores with State, UI Intent, Effect, typed Mutation, reducer, and ViewModel boundaries.
- Only independent pages use the `XxxScreen` name and page contract; subordinate visual states use `XxxContent` or `XxxComponent`.
- Platform quality checks are mandatory: consumers cannot disable dependency, feature-UI platform boundary, MVI, locale, package-path, or 400-line file-size rules.
- User-visible Android strings exist in every generated Android locale.
- The Android repository separates current documentation, editable design sources, executable tools, publishing inputs, release evidence, and generated output by lifecycle; its layout tests and validator pass locally and are wired into CI.
- Canonical public-site and legal sources live under `publishing/legal`, outside product and engineering documentation.
- The public repository contains no private app source or secrets.
- Root English legal URLs and localized English and Simplified Chinese URLs exist.
- When remote publishing is requested, repository visibility is verified and GitHub Pages is configured from "main" at "/".
