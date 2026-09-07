# Project Sources And Release State

Read this when onboarding a project, resolving conflicting sources, or resuming an interrupted release.
Follow the repository's layout. Link existing sources rather than copying them into a skill-specific file.

## Find The Operational Inputs

Search release/build scripts, Gradle variants, publishing metadata, marketing design sources, product and
monetization docs, privacy/data declarations, release archives and existing operation instructions.
If links are missing, add a concise source map in the existing Google Play operations document. It should
resolve these decisions without hardcoding a particular developer's machine, phone serial or browser tab:

| Concern | Project-owned source |
| --- | --- |
| Identity and target | Package/application ID, Console app link, normal track, owner submission boundary, established rollout policy. |
| Product truth | Maintained behavior/monetization/data-flow sources, supported features and explicit marketing exclusions. |
| Build and proof | Release variant, version policy, build/signature/device/CI gates, artifact archive commands. Reference secret configuration locations, never secret values. |
| Market coverage | Console locale inventory, app UI languages, default and custom listings, text/image inheritance and existing translation sources. |
| Brand and capture | Editable design/render sources, approved copy, source captures, fonts, export formats, device setup and project-approved demo/ad settings. |
| Publication evidence | Last live binary, last live store revision, current prepared work and Console evidence. |

Capture preferences such as temporarily hiding ads apply to that app's screenshot session. They do not
change release monetization or imply that the product is ad-free. Feature exclusions and pricing language
belong to the app. Do not embed one app's package, version, language list or screenshots in this plugin.

If accepted assets live in an active feature worktree, resolve that worktree and approval before reuse.
Do not silently substitute older mainline assets or merge the feature as a side effect of release work.

## Keep Binary And Store Baselines Independent

Use an existing release record or manifest; extend it only for information needed to resume or compare.
Keep one source for each fact. Immutable completed-release evidence can reference a versioned archive;
the current live pointer is updated when publication is confirmed. Reproducible previews/logs belong in
the project's ignored output area.

Minimum useful facts, expressed in the project's current format:

- Binary: source commit plus any included diff identity, version name/code, package/variant, AAB path and
  SHA-256, matching mapping/symbol files, validation evidence, Console track/release reference and status.
- Store: approved source revision or content hashes, affected locales/listings, text and asset order,
  fallback/override map, owner approval scope, Console observation and publication status.
- Assessment: None/Partial/Full, affected product differences and required accuracy corrections. Keep it
  concise in the release record or handoff; do not generate a separate audit document on every run.
- Observations: timestamp, evidence source and scope. An owner saying “submitted” is owner-reported
  submitted status, not proof of approval or live availability. Unknown stays unknown.

If no historical source revision exists, establish a dated snapshot from observable live content and
record that provenance. Do not invent the code version at which an old screenshot was captured. Compare
actual current content with the candidate product and maintain a usable baseline from this point onward.

## Resume From Evidence

Before retrying a timed-out upload/save, read the target state. Match package/version, track, relevant
content and recorded artifact identity. Reuse a proven identical uploaded bundle; equal version code or
filename alone does not prove identical bytes. If identity remains uncertain, inspect bundle details and
the upload record rather than rebuild or bump the version automatically.

Preserve unrelated drafts, pending reviews and approved changes. If they block creating a version, explain
the concrete conflict and request the needed owner decision after completing independent preparation.
Never clear it by publishing to 100%, discarding changes, cancelling review, or altering distribution.
