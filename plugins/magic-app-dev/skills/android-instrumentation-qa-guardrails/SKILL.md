---
name: android-instrumentation-qa-guardrails
description: Validate Android UI flows with reproducible adb, Compose, UIAutomator, or instrumentation evidence, including test-owned launch and relevant lifecycle behavior. Diagnose device installation or startup blockers when needed.
---

# Android Instrumentation QA Guardrails

Prove that automation drove the accepted user flow. If a person launches, advances, accepts a prompt in, or recovers
the tested flow, label the run assisted; fix the automation gap and rerun from a test-owned launch before claiming
unassisted evidence. Describe manual device provisioning separately from the flow being tested.

## Establish The Test Boundary

Use the task's accepted behavior, current build, and existing validation evidence. Identify the intended authorized
device and package/variant; use an explicit serial when multiple devices are present. Inspect only the device or
package state needed for a reliable run. Reuse valid build and install evidence for unchanged artifacts.

The test or adb must launch the target app and reach an asserted ready state. Use the repository's normal test
runner and startup mechanism. If installation or launch fails, consult
[references/device-install-and-launch.md](references/device-install-and-launch.md) for the relevant recovery path.
Do not count a manual icon tap as automated launch or treat a device policy failure as an app regression.

## Exercise And Observe

- Synchronize on meaningful readiness and completion conditions. Prefer stable semantics or test tags when locale
  or dynamic content can vary; select visible text when the text itself is the tested requirement.
- Add production test tags only at interaction boundaries that need stable automation, not on every visual element.
- Assert the changed behavior and resulting state or output, including failure paths material to acceptance.
- When lifecycle, configuration, or media behavior is affected, read
  [references/lifecycle-and-media.md](references/lifecycle-and-media.md). Do not expand unrelated UI checks into a
  full editor or recreation suite.
- Preserve commands, results, and the screenshots or logs needed to substantiate the run. A screenshot supports
  visual claims; interaction and outcome evidence establish the automated flow.

Restore settings changed by the test. Rerun affected checks after manual intervention in the flow, relevant code or
artifact changes, or unresolved failures. Reuse valid evidence for unchanged inputs rather than repeating every run.

## Report The Evidence

Distinguish automated, assisted, and blocked results. Report the relevant build/install identity, device, test
command and result count, and any unresolved device or coverage limitation. Keep detailed logs with the evidence;
the handoff needs only enough detail to assess and reproduce the result. Continue independent checks while a
required device path is blocked, and state precisely what remains unverified.
