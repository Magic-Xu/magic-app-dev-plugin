# Prepare The Binary, Notes And Console Draft

## Release Inputs And Verification

1. Confirm the accepted source or supplied AAB, target app and track. Read repository-specific versioning
   and release commands. Compare the intended version code against uploaded bundles across tracks, not
   only the live production version. Reuse a verified existing bundle when appropriate; a genuinely new
   upload needs an unused code. Resolve the requested version using the established policy, not a guessed
   major/minor release. Apply changes in the permitted task branch/worktree.
2. Reuse configured upload signing and production build configuration. Never print passwords, place keys
   in artifacts, reset signing or create replacement keys. Confirm debug/test settings are absent from
   the release variant, including ad IDs, billing overrides and backend endpoints where applicable.
3. Run the repository's mandatory release checks and relevant unit/integration/device regression. Reuse
   current evidence for unchanged inputs. Verify the packaged release path using the project's AAB/device
   tooling; successful compilation alone does not prove installation or user flows. Record unavailable
   device/OS coverage honestly. Play purchase behavior may require an authorized testing-track build;
   local sideloading is not equivalent evidence. Distributing that test build requires existing explicit
   authorization, since the default endpoint excludes publication on test tracks too.
4. Inspect the final bundle's package, version, SDK/variant and upload signature with the project's tools
   (for example bundletool, jarsigner and its expected upload certificate). The upload key and Google Play
   app-signing key can differ; compare the appropriate certificate. Include mapping/native symbols from
   the same build when applicable, checking whether they are already bundled/accepted before extra upload.
5. Archive the verified AAB, SHA-256, build/source identity, matching symbols and validation evidence with
   the project's existing archive tool. Validate the exact artifact to be uploaded. If it is rebuilt,
   re-establish its identity and any checks affected by the change.

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
