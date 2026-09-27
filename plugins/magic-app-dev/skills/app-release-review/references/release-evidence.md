# Engineering Validation And Release Handoff

Use the project's validation commands and reuse evidence tied to the same relevant code, dependencies,
build variant, device/environment and artifact. Inspect what each check proves. New changes, failures
or unresolved risks justify reruns; separate per-feature tests may not cover the combined release.

Attach evidence to the expected outcome and scenario in the coverage map. Inspect assertions, inputs,
dispatch path and observed boundary before reusing it. Test counts, green CI, prior fixes and SDK/event
presence do not establish coverage of a new workflow or preservation of its inherited responsibilities.
Distinguish static confirmation, executed behavior, packaged runtime and external-service receipt.

## Choose The Necessary Proof

| Affected behavior | Relevant evidence |
| --- | --- |
| Pure rules/state | Focused behavior/transition tests and affected compilation |
| Feature interaction/orchestration | Shared-owner integration tests plus the combined user path |
| UI/lifecycle | Interaction, navigation and recreation evidence; visual inspection for rendered changes |
| Platform/IO | Contract tests plus actual provider, persistence, permissions and external outcome where needed |
| Build/configuration behavior | Source and merged manifest/resources/dependencies, variant flags and affected local runtime proof; formal signed artifact verification belongs to release preparation |
| Shared Platform/Factory contracts | Affected consumers and maintained smoke/contract tests; Factory changes use its full generation/build acceptance |
| Measurement/diagnostics semantics | Real event/error producers and consumers; focused checks of attribution, units, timing, terminal outcomes and safe context; packaged/service receipt where changed wiring or the release contract requires it |
| Documentation/tools/metadata | Syntax, links, reader path and source consistency; execute changed commands/helpers |

Complete repository gates applicable to this review stage. Distinguish locally executable checks from
formal release/package/distribution gates; neither skip the former nor report the latter as unfinished
review work. Prefer behavior-oriented tests derived from accepted outcomes;
do not add tests that merely repeat implementation structure. A mock can validate a call without validating
the provider, a screenshot can validate appearance without validating persistence, and compiled instrumented
tests have not run on a device. Use [真机验证](../../android-instrumentation-qa-guardrails/SKILL.md) when
device/system proof is needed. Preserve the authorized device/data scope; a review does not authorize
overwriting personal data to run a test.

## Inspect The Engineering Candidate

Identify the source, relevant SDK/dependency versions and configuration. For local validation artifacts,
record their source, package and build variant. Inspect Release-specific code/configuration such as
shrinking/keep rules, manifest merging, debug-only entrypoints and resource packaging where affected.
A local optimized test build can establish behavior without creating a formal release bundle. If repairs
affect that build, rebuild and verify it; old artifact evidence does not transfer to different bytes.
Formal signing, upload-certificate checks and final distributable identity belong to release preparation.

Cover retained core flows, fresh install and upgrade/recreation according to risk and the product's
storage/compatibility promises. Check supported languages, accessibility and approved designs where
affected.

Run affected local performance checks on an authorized physical device using representative workloads
and the product's baselines. Use the existing optimized, non-debuggable/profileable benchmark variant for
timing claims; debug runs can aid diagnosis but do not establish release performance. Local test signing
and sideloading suffice for CPU, memory, frame timing, latency and resource cleanup: Google Play delivery
is not a prerequisite. Check device availability, existing workload and build/tooling before claiming a
blocker, and state the concrete failure if one remains. Reuse unaffected evidence; do not demand all-device
or full performance qualification merely because a version is being reviewed. Workloads, commands,
thresholds and product-specific acceptance remain in the project's engineering sources.

Check run validity separately from product acceptance: a completed run or usable trace can still show a
failed requirement. Investigate material failures under the skill's completion conditions; retain original
failures alongside diagnostic runs and repaired-candidate verification. A diagnostic setting change must
not silently become the accepted product configuration or substitute for verifying normal operation.

Check actual permissions, SDK/data flows, offline behavior, entitlements, ads and purchase restrictions
against accepted requirements and declarations. A local-first label does not imply that all SDK traffic is
absent; verify what data leaves the app and whether optional services can break the core user path.

Compare cumulative product changes with live store claims, screenshots, legal and Data safety material
when available. Use [store refresh](../../google-play-release/references/store-refresh.md) for a
None/Partial/Full recommendation. For current Play requirements consult official sources. Assessing these
does not authorize changing Console or making factual attestations without evidence.

## Handoff Only Play-Dependent Work

When changed behavior truly depends on Play distribution, identify the local proof already completed and
the exact service-dependent scenario for [release preparation](../../google-play-release/references/release-preparation.md).
Examples include production purchase entitlement receipt or an update becoming available to an eligible
account. Do not append a generic signed-package, purchasing, upgrade and device-performance checklist to
every review. Missing signing/upload/distribution work does not itself block engineering review; a confirmed
defect in the query, state handling, migration or other app logic does. If the user explicitly includes
distribution acceptance in the task, apply the release workflow and its existing authorization boundary.

## State The Decision Precisely

Before closing the review, reconcile the coverage map with the cumulative change inventory. Each material
change and affected responsibility must have a supported disposition. Close executable in-scope gaps;
only carry unresolved work under the completion conditions in [the skill](../SKILL.md#complete-the-authorized-work).
Do not convert missing evidence to "no issues found." Keep this in the same review record, not a second
ceremonial checklist. Required in-scope gaps prevent a passed engineering review; later-stage release
tasks do not. A candidate verdict alone does not establish that the authorized task is complete.

- **Engineering review passed within stated coverage:** No confirmed blocking defects and the review's
  required local evidence is satisfied. Optional debt can remain with its impact and recommendation explained.
- **Blocked by a confirmed defect:** An accepted product requirement is violated; give the symptom, origin,
  concrete fix and its impact. Test severity alone does not establish the product consequence.
- **Not yet verified in this review:** Required source provenance or in-scope validation is missing. Give the
  exact cause and next action; do not substitute later-stage formal release work for this explanation.

Report the most consequential findings first, each as observable symptom, origin with evidence,
recommended action, then affected scope and normal-use side effects. Link locations and detailed proof.
Include the baseline/candidate, feature/critical-path coverage and material checks that could not run.
A no-findings statement describes only the inspected paths and their evidence limits; it must not imply
that unsampled responsibilities were verified. Reuse the requested report or existing release record
rather than a second checklist. Give genuine remaining owner decisions enough context to choose.

Unavailable devices, credentials or infrastructure do not invalidate independent completed work. State
the exact missing proof and continue what can be verified. Static review alone cannot certify runtime
behavior, and a release recommendation does not guarantee the absence of undiscovered defects.
