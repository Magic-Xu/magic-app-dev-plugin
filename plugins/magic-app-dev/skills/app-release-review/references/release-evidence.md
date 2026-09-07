# Validation Evidence And Release Readiness

Use the project's validation commands and reuse evidence tied to the same relevant code, dependencies,
build variant, device/environment and artifact. Inspect what each check proves. New changes, failures
or unresolved risks justify reruns; separate per-feature tests may not cover the combined release.

## Choose The Necessary Proof

| Affected behavior | Relevant evidence |
| --- | --- |
| Pure rules/state | Focused behavior/transition tests and affected compilation |
| Feature interaction/orchestration | Shared-owner integration tests plus the combined user path |
| UI/lifecycle | Interaction, navigation and recreation evidence; visual inspection for rendered changes |
| Platform/IO | Contract tests plus actual provider, persistence, permissions and external outcome where needed |
| Release packaging/configuration | Candidate Release build, manifest/resources/dependencies, variant flags and packaged runtime proof |
| Shared Platform/Factory contracts | Affected consumers and maintained smoke/contract tests; Factory changes use its full generation/build acceptance |
| Documentation/tools/metadata | Syntax, links, reader path and source consistency; execute changed commands/helpers |

Complete mandatory repository gates. Prefer behavior-oriented tests derived from accepted outcomes;
do not add tests that merely repeat implementation structure. A mock can validate a call without validating
the provider, a screenshot can validate appearance without validating persistence, and compiled instrumented
tests have not run on a device. Use [真机验证](../../android-instrumentation-qa-guardrails/SKILL.md) when
device/system proof is needed. Preserve the authorized device/data scope; a review does not authorize
overwriting personal data to run a test.

## Inspect The Release Candidate

Confirm source-to-artifact identity, package/version identity, relevant SDK/dependency versions, build
variant and configuration. Inspect Release-specific behavior such as shrinking/keep rules, manifest
merging, debug-only entrypoints, resource packaging and production service configuration where applicable.
If repairs affect the binary, rebuild and verify the replacement; earlier artifact checks do not transfer
to different bytes. Keep secrets and signing credentials out of reports.

Cover retained core flows, fresh install and upgrade/recreation according to risk and the product's
storage/compatibility promises. Check supported languages, accessibility and approved designs where
affected. Assess representative CPU/memory/latency and resource cleanup for intensive media or background
work using applicable product baselines, not invented universal performance thresholds.

Check actual permissions, SDK/data flows, offline behavior, entitlements, ads and purchase restrictions
against accepted requirements and declarations. A local-first label does not imply that all SDK traffic is
absent; verify what data leaves the app and whether optional services can break the core user path.

Compare cumulative product changes with live store claims, screenshots, legal and Data safety material
when available. Use [store refresh](../../google-play-release/references/store-refresh.md) for a
None/Partial/Full recommendation. For current Play requirements consult official sources. Assessing these
does not authorize changing Console or making factual attestations without evidence.

## State The Decision Precisely

- **Ready within stated coverage:** No unresolved release blockers and required evidence is satisfied for
  the identified candidate. Optional debt can remain with its impact explained.
- **Blocked:** A confirmed defect or unmet requirement prevents release; give its consequence and next action.
- **Not yet verified:** Required provenance, acceptance or validation is missing. Do not report this as ready
  or claim a hypothetical failure has been reproduced. A blocked release can also have verification gaps.

Report the most consequential findings first, with trigger, expected/actual outcome, location, evidence,
repair status and remaining action. Include the baseline/candidate, feature/critical-path coverage and
material checks that did not run. Reuse the requested report or existing release record rather than a
second checklist. Bundle uncertain cleanup/product decisions with enough context for the owner to decide.

Unavailable devices, credentials or infrastructure do not invalidate independent completed work. State
the exact missing proof and continue what can be verified. Static review alone cannot certify runtime
behavior, and a release recommendation does not guarantee the absence of undiscovered defects.
