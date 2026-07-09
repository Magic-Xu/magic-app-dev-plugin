---
name: android-instrumentation-qa-guardrails
description: Use when validating Android app UI flows with adb, instrumentation, Compose UI tests, UIAutomator, or connected-device tests, especially when the test must prove app launch, language or configuration changes, Activity recreation, editor state preservation, save/share flows, or other end-to-end behavior without manual interaction. Guards against false positives from manual icon taps, flaky ActivityScenario startup, localized text selectors, and hidden device install restrictions.
---

# Android Instrumentation QA Guardrails

## Principle

An Android UI test is not valid evidence if a human opened the app, accepted a prompt, advanced a screen, or recovered the flow manually. If manual help happened, report it as assisted or blocked, fix the automation gap, then rerun the test from a clean app launch.

Use this skill to turn device QA into reproducible evidence rather than a demonstration that happens to pass while someone is watching.

## Workflow

1. Confirm the device and package state before testing.
2. Install the app and test APKs explicitly when connected Gradle install is blocked.
3. Launch the target app from the test or from adb, not by tapping the launcher icon.
4. Wait on stable semantics/test tags, not localized text.
5. Exercise the full flow, including Activity recreation or configuration changes when relevant.
6. Save commands, screenshots, and log evidence that prove the automation drove the app.
7. Rerun after any manual intervention; do not count the assisted run.

## Device Setup

Start with the real state:

```bash
adb devices
adb shell pm list packages | grep '<package>'
adb logcat -c
```

If Gradle connected install fails with `INSTALL_FAILED_USER_RESTRICTED`, treat it as a device policy or installer permission problem, not an app regression. A common reliable path is:

```bash
adb install -r app/build/outputs/apk/debug/app-debug.apk
adb install -r -t app/build/outputs/apk/androidTest/debug/app-debug-androidTest.apk
```

Use screenshots and logs around failures:

```bash
adb exec-out screencap -p > /tmp/android-qa-failure.png
adb logcat -d -v time > /tmp/android-qa-logcat.txt
```

## Reliable Launch

Prefer a launch that is owned by the test. For Compose instrumentation tests, use `createEmptyComposeRule()` when `createAndroidComposeRule` or `ActivityScenario` cannot reliably start the app on the target device.

Launch the app with `am start` from instrumentation:

```kotlin
private val composeRule = createEmptyComposeRule()

private fun launchApp() {
    val packageName = targetContext().packageName
    val output = executeShellCommand(
        "am start -W -n $packageName/.MainActivity -f 0x10008000"
    )
    Log.i("AndroidQa", "launch/output=$output")

    composeRule.waitUntil(20_000) {
        composeRule
            .onAllNodesWithTag("<ROOT_OR_SCREEN_READY_TAG>")
            .fetchSemanticsNodes()
            .isNotEmpty()
    }
    composeRule.waitForIdle()
}

private fun executeShellCommand(command: String): String {
    val descriptor = InstrumentationRegistry
        .getInstrumentation()
        .uiAutomation
        .executeShellCommand(command)

    return descriptor.use {
        FileInputStream(it.fileDescriptor)
            .bufferedReader()
            .use { reader -> reader.readText() }
    }
}

private fun targetContext(): Context =
    InstrumentationRegistry.getInstrumentation().targetContext
```

`0x10008000` is `FLAG_ACTIVITY_NEW_TASK | FLAG_ACTIVITY_CLEAR_TASK`; it gives the test a clean Activity task. Do not call `am force-stop` from inside the instrumentation process because it can kill the runner. If a force-stop is required, do it host-side before invoking instrumentation.

Run the test directly:

```bash
adb shell am instrument -w -r \
  -e class '<package>.flow.SomeInstrumentedTest' \
  '<testPackage>/androidx.test.runner.AndroidJUnitRunner'
```

The output or log should show the launch command and then the first UI assertion quickly. If the app only appears after a person taps the icon, the test has not validated launch.

## Selector Rules

Use stable test tags for automation-critical UI:

- screen-ready roots
- primary actions
- dialog options
- dynamic list rows
- language options
- apply/confirm buttons

Avoid selecting by visible text unless the test is specifically validating localization. Localized strings make tests fail in one language and accidentally pass in another.

For Compose, add tags in production code only at interaction boundaries that need stable automation. Do not add tags to every visual element.

## Configuration Changes

Any language, theme, font scale, orientation, or system configuration change may recreate the Activity. Tests that touch those paths must verify the runtime state that should survive recreation.

Look for split-brain state:

- UI state says content exists, but runtime bitmap/media object is null.
- ViewModel keeps intent state, but Compose `remember` lost the backing object.
- screen route survives, but transient operation state is reset.

State that must survive Activity recreation belongs in a ViewModel or other lifecycle-aware holder. Large images should not be put into saved instance state. Persist or re-decode media only when process-death recovery is part of the requirement.

## Editor And Media Flows

For image editors or media tools, validate more than navigation:

- load or create image
- apply an edit
- undo/redo if supported
- change language or configuration if relevant
- save/export
- verify the saved result exists
- verify share/save screen actions still work

When a test changes app language or settings, restore the previous value in cleanup so the device remains reusable.

## Reporting

Always distinguish:

- automated: fully driven by adb/instrumentation/test code
- assisted: a human clicked, unlocked, accepted, or opened something
- blocked: device policy, permission, install restriction, missing dependency, or app crash prevents valid automation

Report the exact build commands, install commands, instrumentation command, result count, and any residual device limitation. A passing test without the launch and interaction evidence is weak evidence.
