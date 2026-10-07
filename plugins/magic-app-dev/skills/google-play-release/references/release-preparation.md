# Prepare The Binary, Notes And Console Draft

## Release Inputs And Verification

Complete the [release branch gate](release-branch.md) before these preparation steps. Reusing an AAB or
resuming a saved draft still requires a verified formal branch tied to its source.

1. Confirm the accepted source or supplied AAB, target app and track. Read repository-specific versioning
   and release commands. Compare the intended version code against uploaded bundles across tracks, not
   only the live production version. Reuse a verified existing bundle when appropriate; a genuinely new
   upload needs an unused code. Resolve the requested version using the established policy, not a guessed
   major/minor release. Apply changes in the permitted task branch/worktree.
2. Reuse configured upload signing and production build configuration. Never print passwords, place keys
   in artifacts, reset signing or create replacement keys. Confirm debug/test settings are absent from
   the release variant, including ad IDs, billing overrides and backend endpoints where applicable.
3. Use local packages for app validation and reuse valid unit/integration/device/performance evidence
   for unchanged code and configuration. Compare the tested package with the candidate; run only checks
   affected by meaningful differences, including packaging-sensitive behavior where necessary. Successful
   compilation alone is not functional evidence. Record the tested variant and device/OS coverage honestly.
   Do not add a Play installation, startup, purchase/restore or internal-track round trip as a routine
   submission prerequisite. Routine preparation does not replace or uninstall the user's existing store
   installation; use the project's isolated local test package when additional device testing is needed.
   A real Play-channel check is a separate task when explicitly required by the agreed acceptance scope.
   Local controlled responses cannot prove real purchases or store delivery; report that boundary without
   blocking on optional checks. Publishing to a test track requires explicit distribution authorization.
4. Inspect the final bundle's package, version, SDK/variant and upload signature with the project's tools
   (for example bundletool, jarsigner and its expected upload certificate). The upload key and Google Play
   app-signing key can differ; compare the appropriate certificate. Include mapping/native symbols from
   the same build when applicable, checking whether they are already bundled/accepted before extra upload.
5. Archive the verified AAB, SHA-256, build/source identity, matching symbols and validation evidence with
   the project's existing archive tool. Validate the exact artifact to be uploaded. If it is rebuilt,
   re-establish its identity and any checks affected by the change.

## Optional Real Play Update Verification

For routine preparation, reuse local tests of update states, retries, store navigation and return behavior.
Only perform the following Play-channel procedure when real update availability is explicitly required by
the agreed acceptance scope. It is not a default release gate, including for a newly added update control.

Do not require two public production releases. Google documents testing with internal app sharing: install
a lower-versionCode build that already contains the update-check feature through its sharing link, upload
a compatible higher-versionCode build, open the higher build's sharing link without installing it, then
reopen the lower build to query update availability. Recheck current [official testing guidance](https://developer.android.com/guide/playcore/in-app-updates/test)
for package, signing and account eligibility. Keep both test builds inside the project's release/version
policy; do not bump a feature branch or replace an existing user's differently signed install.

Test only the product's accepted behavior. An availability check plus an external store link does not
require implementing or validating Play's in-app download/install UI. Use the sharing setup to verify the
real availability query and test the app's link/return behavior; if end-to-end updating through the normal
store listing is required, use an authorized internal/closed test track with both eligible builds, since
sharing-link visibility is not proof of normal-listing distribution. Local controlled responses separately
cover unavailable/current/available, retry and navigation logic. Neither method authorizes upload or tester
distribution merely because a review identified the scenario.

## Localized Version Notes

Write concise user-facing changes from the accepted release delta. Do not copy commit logs, announce
unreleased capabilities, invent performance gains, add promotional calls to action, or disclose internal
details that do not help users. Observe the project's marketing exclusions here as well as in screenshots.

Use verified Console release-note locales and the project's terminology. They need not equal the app UI
language list. Preserve existing locale coverage and prepare faithful translations; inspect RTL, scripts,
numbers and product names. Routine notes can accompany the final owner submission preview.

Google currently documents at most **500 Unicode characters per locale**. The bundled standard-library
helper validates an explicit locale set and produces the tagged Console import text without changing copy:

```bash
python3 <skill-dir>/scripts/prepare_release_notes.py <notes.json> \
  --locales en-US zh-CN --output <existing-output-directory>/release-notes.txt
```

Replace the example locales with the observed target set. Input is a JSON object mapping each locale to
its complete plain-text note, for example `{"en-US":"Improved export reliability.","zh-CN":"优化导出稳定性。"}`.
Prefer an existing project notes validator if it provides equivalent checks. Use a generated adapter when
the canonical source has another format, without creating a second editable source. Without `--output`,
the helper only validates. It rejects empty, missing, extra or duplicated locales, overlong text and
standalone locale-tag lines inside notes; invalid input leaves an existing output untouched. It checks
syntax and coverage, not translation quality, product truth or whether a locale exists in Console.

## Upload And Save

Use the user's specified browser/session, or an already authorized purpose-built integration. Discover
current browser-tool documentation and inspect visible UI/DOM before acting. Do not substitute another
account/session or bypass the selected browser with hidden endpoints. Keep credentials in their existing
providers. Let the owner complete sign-in/second-factor steps when needed, then resume.

1. Inspect the app, exact track, existing release and Publishing overview. Match them to the intended
   target and pending state before mutation. Reuse the matching draft; preserve unrelated work.
2. Upload the verified AAB or select its verified existing library entry. Wait for processing and compare
   parsed package, version name/code and release inclusion with the intended artifact. Inspect rejected
   bundle errors, SDK/permission declarations and applicable mapping/symbol warnings.
3. Fill the release name and all intended locale notes exactly from the source. Reuse the established
   rollout policy for preparation; do not invent 100% or change countries, products/prices or publication
   settings. Check data safety, ads, app access and content declarations against actual changed behavior.
   If they need amendment, prepare the concrete correction for owner review; never guess attestations.
4. Save only through an action whose effect stays inside the authorized boundary. **Save as draft** and
   **Save** may differ from **Publish/Start rollout**. If the next action would submit or publish, stop
   there. After an ambiguous timeout, inspect state before retrying.
5. Reopen the release and affected listing pages. Compare the persisted artifact/version/track and every
   changed locale against the source. Review errors/warnings and pending checks. Fix in-scope failures;
   report unresolved required checks and do not describe an in-progress check as passed.
6. Deliver the Console link and exact next owner action. State whether the result is a saved draft,
   ready-to-submit changes, or a draft with a named blocker. Upload success is not review submission,
   review approval or live release.

## Current Official References

Recheck official guidance when executing a release if rules may have changed, or Console requirements
conflict with this reference. Keep live-policy requirements distinct from project conventions.

- [Prepare and roll out a release](https://support.google.com/googleplay/android-developer/answer/9859348)
  — bundle/notes preparation, draft saves, errors and rollout actions.
- [Prepare your app for review](https://support.google.com/googleplay/android-developer/answer/9859455)
  — app content, access and declarations.
- [Version your app](https://developer.android.com/studio/publish/versioning)
  — version codes and package version metadata.
