---
name: google-play-release
description: Google Play 首次上架、AAB 版本更新、商店截图与描述更新及草稿续办；核验包体与多语言内容，评估无需/局部/全面刷新，默认停在用户送审和发布之前。
---

# Google Play Release

## Outcome And Authority

One entry point prepares a first launch, version update, or store-only change and determines the needed store work.
Deliver a verified release draft, any approved store changes, and the exact remaining owner action.
For a store-only request, run the assessment and refresh path without building or uploading a new binary.
For a supplied AAB, establish its identity and evidence before deciding whether another build is needed.

The default endpoint is **before review submission and before rollout/publication on every track**.
The owner reviews changed store design/copy and performs final submission/publication. A request to
prepare and upload a release covers the necessary build, validation, upload and draft saves; reuse that
authorization without repeated confirmation. Automatic skill selection alone does not authorize writes.
Honor a user's explicit change to this boundary, but never interpret “prepare a release” as permission
to submit, publish, expand a staged rollout, or distribute to testers. Check the effect of an action:
Console can offer Save or Publish depending on state; a button's position is not a permission boundary.

Creating a release does not authorize merging code, changing billing products/prices, signing keys,
distribution countries, account permissions, managed publishing, or unrelated pending changes. Use the
project's existing release policy and session decisions; clarify only a missing decision that changes
the release target, user-visible meaning, data handling, authority or deliverable.

## Select The Release Mode

- **First launch:** The app has no published product/store baseline. Read
  [first-launch.md](references/first-launch.md) for initial Console setup, declarations and store design.
  An existing unpublished Console app or test release should be resumed, not created again.
- **Version update:** Establish the two independent baselines below and run the cumulative store assessment.
- **Store-only:** Assess and update the requested listing content without building/uploading a new binary.
- **Resume:** Inspect saved state and artifact identity, then continue the matching mode from its actual state.

## Establish The Two Baselines

Read the target repository's instructions and release/store sources. Reuse established worktrees,
scripts, build configuration, approved assets and valid test results. Apply its branch/worktree rules
before persistent edits. Android project creation belongs to Factory; initial Console app creation follows
the first-launch scope. Do not create a new Codex task merely to run this workflow.

Establish:

- The requested app/package, accepted code or supplied artifact, version, target track and release policy.
- The last actually released binary and the **last actually published store content**, independently.
  For first launch, record absent baselines as not yet established; do not confuse this with unknown history.
- Current Console state: uploaded bundles, drafts, pending/reviewed changes, locale coverage and overrides.
- Current product facts and exclusions: features, UI, free/paid boundaries, ads, privacy/data flows,
  supported devices, app languages, store locales, brands, editable assets and capture setup.

Use code and device behavior to establish capability; use Console and maintained publishing records to
establish distribution and status. Reconcile conflicts instead of treating an outdated product document, version
label, changelog or draft as proof of current behavior or publication. Store locales, app UI languages
and distribution countries are separate sets. Preserve their verified scope.

If the project lacks a usable source map or release record, follow
[project-context.md](references/project-context.md). Keep project facts in the app repository, not this
shared plugin. Do not introduce a parallel configuration when the existing sources answer the questions.

## Assess Store Changes On Every Version Update

Compare the candidate product with the live store and **cumulative changes since its last store refresh**.
Account for already approved/pending store edits so they are not regenerated or overwritten. Choose the
smallest complete tier and briefly state the evidence and affected fields/locales:

| Tier | Evidence | Work |
| --- | --- | --- |
| None | Existing claims, screenshots and commercial/data disclosures remain accurate and representative; changes do not materially change the value shown. | AAB and localized release notes only. |
| Partial | A bounded feature, screen, availability, paid boundary or disclosure has changed. | Update only affected text/images and corresponding locale variants. Preserve the visual system and accurate assets. |
| Full | Positioning, primary workflows, main UI or the core value proposition have changed enough that the existing story no longer represents the product. | Replan the screenshot story and relevant descriptions, review the design, then localize and replace affected assets. |

Version size/number, elapsed time and personal aesthetic preference alone do not select Full. Missing
evidence is not evidence for None: finish independent preparation, then obtain the missing product or
Console facts before completing the assessment. Do not repeatedly research competitors on routine runs.

Separate **accuracy corrections** from **optional conversion improvements**. Correct affected false or
obsolete claims before handing off a ready-to-submit release, even if they do not warrant a redesign.
New paid restrictions or data flows may need a small copy/declaration correction rather than new art.
Do not promise conversion gains without evidence. Investigate external examples when a redesign or an
observed conversion problem calls for it; distinguish verified recommendations from visual inspiration.

## Execute The Selected Path

1. For a binary release, use [release-preparation.md](references/release-preparation.md) for build,
   package verification, localized notes, upload and Console readback. Complete mandatory project
   release/device checks. Store-only work skips binary preparation and upload.
2. For initial store content, Partial or Full, use [store-refresh.md](references/store-refresh.md). Produce a concrete review
   with changed copy and images before asking the owner to approve them. Continue independent build and
   validation while design review is pending; do not upload unapproved store content.
3. Consolidate review into one useful package. Routine version notes are included in the final release
   preview, without an extra approval stop unless requested. Reuse approval of unchanged material. After
   approval, finish localization, export, saves and verification. New product claims or meaningful design
   changes outside that approval return to review; ordinary faithful translation/formatting does not.
4. Resume the same release using artifact identity and fresh Console state. Do not duplicate a bundle,
   regenerate unchanged assets, or discard someone else's draft to clear a blocked action.
5. Reopen saved pages and compare actual values/assets with the intended sources. Review all affected
   locales, inheritance, screenshot order, relevant declarations and release warnings. Perform any
   repository-required artifact-boundary review in this final pass.

If a gate fails, repair a task-caused issue within scope, rerun affected checks and continue. If a login,
device, product decision or external check is unavailable, state the exact gap and finish unaffected work.
Never weaken a required check or silently switch account, target, session or release channel to proceed.

## Handoff And Continued Use

Report the version/code, track, artifact identity, assessment tier and reason, what was saved and verified,
remaining checks, and the precise owner action/link. Present updated copy/design when review is needed.
Do not label a draft with unresolved required checks as ready for submission.

Keep binary and store status independent: prepared, saved, submitted, approved and live are distinct facts.
Record evidence and observation time; distinguish owner-reported submission from a Console observation.
Update a live baseline only after live status is established, not when a file is generated or uploaded.
Store-only updates must remain runnable between binary releases. When an iteration has a metric or
recovery target, connect the published version/store revision to its existing
[outcome record](../app-end-to-end-delivery/references/iteration-outcomes.md). No periodic monitor is
created unless the user requests one.
