# Device Installation And Launch Troubleshooting

Read when device installation or test-owned app startup fails. Use the selected adb serial and the repository's
actual package, build variant, activity, APK paths, runner, and test class. Preserve failure logs before resetting
anything; do not clear app data unless the accepted test setup requires it.

## Installation

Confirm the current device and package state with `adb devices` and the package manager. If connected Gradle install
fails with `INSTALL_FAILED_USER_RESTRICTED`, investigate device policy or installer permission before treating it as
an app regression. When the selected device permits direct adb installation, use the built app and test APKs:

```bash
adb -s '<serial>' install -r app/build/outputs/apk/debug/app-debug.apk
adb -s '<serial>' install -r -t app/build/outputs/apk/androidTest/debug/app-debug-androidTest.apk
```

Record any manual provisioning and distinguish it from intervention in the accepted automated flow. If the device
requires approval for each run, report that limitation rather than describing the workflow as unattended.

Capture relevant failure evidence, for example:

```bash
adb -s '<serial>' exec-out screencap -p > /tmp/android-qa-failure.png
adb -s '<serial>' logcat -d -v time > /tmp/android-qa-logcat.txt
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
adb -s '<serial>' shell am instrument -w -r \
  -e class '<package>.flow.SomeInstrumentedTest' \
  '<testPackage>/androidx.test.runner.AndroidJUnitRunner'
```

The output or log should show the launch command and then the first UI assertion quickly. If the app only appears after a person taps the icon, the test has not validated launch.
