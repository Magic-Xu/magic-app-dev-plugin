---
name: android-device-keep-awake
description: Prepare one connected Android device for an explicitly requested long-running development or device-QA task by enabling and verifying Android's stay-awake setting for the active charging source through adb.
---

# Android Device Keep Awake

Keep the selected device available for a long development task by enabling Android's stay-awake setting for the power source the device actually reports. The setting prevents automatic screen-off while that source remains connected; it does not bypass a secure lock screen or prevent the user from locking the device manually.

## Start The Device Session

Run `scripts/device_keep_awake.sh enable` from this skill directory before device-dependent work. The helper:

- requires an authorized adb device;
- refuses to guess when multiple devices are connected;
- reads the active AC, USB, wireless, or dock source from Android's battery service;
- preserves existing stay-awake bits and records only the bits added for this task;
- verifies the stored value and reports the active power source;
- locates adb from `PATH`, Android SDK environment variables, or the standard macOS SDK path.

When multiple devices are connected, identify the intended serial with the user or task context, then run:

```bash
bash scripts/device_keep_awake.sh enable --serial '<serial>'
```

If adb reports no authorized device, say that keep-awake is not active and ask the user to connect the device or accept its USB-debugging prompt. Continue device-independent work only when that remains within the requested task.

If Android reports no active charging source, say that keep-awake cannot become active and ask the user to connect power. Do not infer the power source from the adb transport; use the battery-service value.

If the display is already asleep, `adb -s '<serial>' shell input keyevent KEYCODE_WAKEUP` may wake it. Do not swipe, enter credentials, dismiss security, or claim the phone is ready until the user unlocks it.

## Verify And Restore The State

Check the device-side state when needed with:

```bash
bash scripts/device_keep_awake.sh status --serial '<serial>'
```

Do not run a background input loop or periodically tap, swipe, or press navigation keys. Those actions interfere with manual and automated UI testing.

If the helper verifies the setting but an OEM still turns the display off, report the observed override and stop. Changing `screen_off_timeout`, disabling device security, installing a keep-awake app, or starting an input loop is a different fallback and requires the user's explicit approval.

At the end of the invoked development task, restore only the stay-awake bits this Skill added. Preserve bits that were enabled before the task or added independently:

```bash
bash scripts/device_keep_awake.sh restore --serial '<serial>'
```

If the user explicitly asks to keep the device awake after handoff, leave the state active and report that it remains enabled.
