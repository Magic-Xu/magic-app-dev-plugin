# Workspace Specification

Use these fields when translating a user's request into generator arguments.

## Required

| Field | CLI argument | Rule |
|---|---|---|
| App name | "--app-name" | Human-facing name used in Android and the website |
| Slug | "--slug" | Lowercase letters, digits, and single hyphens; must start and end with a letter or digit |
| Application ID | "--application-id" | Dot-separated Java identifiers with at least two segments |
| GitHub owner | "--github-owner" | User or organization that will own both repositories |
| English product sentence | "--product-sentence-en" | One sentence describing the user and job |
| Chinese product sentence | "--product-sentence-zh" | Faithful Simplified Chinese equivalent |
| Parent directory | "--parent-dir" | Existing directory under which the workspace directory is created |

## Optional

- "--magic-platform-version": defaults to the Factory-tested stable version `1.0.0`. Override only
  with another already-published stable `x.y.z` version with major >= 1; 0.x, snapshots, and local
  paths are rejected.
- "--app-repo-name": defaults to "<slug>-android".
- "--legal-repo-name": defaults to "<slug>-legal".
- "--android-locales": comma-separated locale tags. Defaults to:
  "en,zh-CN,zh-Hant,es,pt-BR,hi,ur,fr,ja,ko,id,th,vi,ms,fil".
- "--legal-locales": currently supports "en,zh-CN" and defaults to both.
- "--effective-date": ISO date used in generated legal documents; defaults to the current local date.
- "--no-git": generate files without initializing the two local Git repositories.
- "--dry-run": resolve and print the plan without writing files.

## Privacy Baseline

The generated Android shell has all of the following set to false:

- Accounts.
- Server or cloud upload.
- Advertising.
- Billing or subscriptions.
- Analytics or crash-reporting SDKs.
- Sensitive runtime permissions.

This baseline describes the generated code, not a promised permanent product design. If the real initial app includes any of these capabilities, the default policy must not be published unchanged.

## Naming Invariants

- The workspace directory is "<parent-dir>/<slug>".
- The two repositories are siblings, never nested Git repositories.
- Local child directory names match repository names.
- The Android application ID is independent of the GitHub repository name.
- Existing workspace, child, or staging paths are never overwritten.
