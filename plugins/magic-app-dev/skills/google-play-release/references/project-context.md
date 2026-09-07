# Release Context And Resumption

Use the shared [project source map](../../app-end-to-end-delivery/references/project-context.md) for
identity, current product facts, authority, design/capture sources and market coverage. Extend existing
release operations records only for missing information needed by this workflow.

Capture preferences such as temporarily hiding ads apply to that app's screenshot session; they do not
change release monetization or imply the product is ad-free. Feature exclusions and pricing language
belong to the app, not the plugin. If accepted assets live in an active feature worktree, resolve it and
its approval before reuse. Do not substitute older mainline assets or merge as a release side effect.

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
