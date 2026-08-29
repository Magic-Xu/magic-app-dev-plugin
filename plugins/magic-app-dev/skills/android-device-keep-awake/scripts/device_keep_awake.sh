#!/usr/bin/env bash
set -euo pipefail

readonly AC_STAY_AWAKE_MASK=1
readonly USB_STAY_AWAKE_MASK=2
readonly WIRELESS_STAY_AWAKE_MASK=4
readonly DOCK_STAY_AWAKE_MASK=8

adb_bin="adb"
device_serial=""
action=""

usage() {
  cat <<'EOF'
Usage: device_keep_awake.sh <enable|status|restore> [--serial SERIAL] [--adb PATH]

  enable   Add stay-awake bits for the active charging source and verify them.
  status   Report the current stay-awake bitmask, power source, and saved session state.
  restore  Clear only the stay-awake bits added by this helper.
EOF
}

fail() {
  printf 'android-device-keep-awake: %s\n' "$*" >&2
  exit 1
}

while (($# > 0)); do
  case "$1" in
    enable|status|restore)
      [[ -z "$action" ]] || fail "specify exactly one action"
      action="$1"
      shift
      ;;
    --serial)
      (($# >= 2)) || fail "--serial requires a value"
      device_serial="$2"
      shift 2
      ;;
    --adb)
      (($# >= 2)) || fail "--adb requires a path"
      adb_bin="$2"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      fail "unknown argument: $1"
      ;;
  esac
done

[[ -n "$action" ]] || {
  usage >&2
  exit 1
}

resolve_adb_binary() {
  local resolved
  resolved="$(command -v "$adb_bin" 2>/dev/null || true)"
  if [[ -n "$resolved" ]]; then
    adb_bin="$resolved"
    return
  fi

  [[ "$adb_bin" == "adb" ]] || fail "adb not found: $adb_bin"

  local -a candidates=()
  [[ -z "${ANDROID_SDK_ROOT:-}" ]] || candidates+=("${ANDROID_SDK_ROOT%/}/platform-tools/adb")
  [[ -z "${ANDROID_HOME:-}" ]] || candidates+=("${ANDROID_HOME%/}/platform-tools/adb")
  [[ -z "${HOME:-}" ]] || candidates+=("${HOME%/}/Library/Android/sdk/platform-tools/adb")

  local candidate
  for candidate in "${candidates[@]}"; do
    if [[ -x "$candidate" ]]; then
      adb_bin="$candidate"
      return
    fi
  done

  fail "adb not found in PATH or a standard Android SDK location"
}

resolve_device() {
  if [[ -n "$device_serial" ]]; then
    local state
    state="$("$adb_bin" -s "$device_serial" get-state 2>/dev/null || true)"
    state="${state//$'\r'/}"
    [[ "$state" == "device" ]] || fail "device '$device_serial' is not connected and authorized"
    return
  fi

  local -a available_devices=()
  local candidate state remainder
  while read -r candidate state remainder; do
    [[ "$state" == "device" ]] && available_devices+=("$candidate")
  done < <("$adb_bin" devices)

  case "${#available_devices[@]}" in
    0)
      fail "no connected and authorized adb device found"
      ;;
    1)
      device_serial="${available_devices[0]}"
      ;;
    *)
      fail "multiple adb devices found (${available_devices[*]}); rerun with --serial"
      ;;
  esac
}

run_adb() {
  "$adb_bin" -s "$device_serial" "$@"
}

read_stay_awake_setting() {
  local value
  value="$(run_adb shell settings get global stay_on_while_plugged_in)"
  value="${value//$'\r'/}"
  value="${value//$'\n'/}"
  value="${value// /}"

  if [[ -z "$value" || "$value" == "null" ]]; then
    printf '0\n'
    return
  fi

  [[ "$value" =~ ^[0-9]+$ ]] || fail "unexpected stay_on_while_plugged_in value: $value"
  printf '%s\n' "$value"
}

read_power_source_mask() {
  local battery
  battery="$(run_adb shell dumpsys battery 2>/dev/null || true)"
  local mask=0

  [[ "$battery" == *"AC powered: true"* ]] && mask=$((mask | AC_STAY_AWAKE_MASK))
  [[ "$battery" == *"USB powered: true"* ]] && mask=$((mask | USB_STAY_AWAKE_MASK))
  [[ "$battery" == *"Wireless powered: true"* ]] && mask=$((mask | WIRELESS_STAY_AWAKE_MASK))
  [[ "$battery" == *"Dock powered: true"* ]] && mask=$((mask | DOCK_STAY_AWAKE_MASK))

  printf '%s\n' "$mask"
}

power_source_names() {
  local mask="$1"
  local names=""

  ((mask & AC_STAY_AWAKE_MASK)) && names="ac"
  ((mask & USB_STAY_AWAKE_MASK)) && names="${names:+$names,}usb"
  ((mask & WIRELESS_STAY_AWAKE_MASK)) && names="${names:+$names,}wireless"
  ((mask & DOCK_STAY_AWAKE_MASK)) && names="${names:+$names,}dock"

  printf '%s\n' "${names:-none}"
}

state_file_path() {
  local state_root="${TMPDIR:-/tmp}/magic-app-dev/android-device-keep-awake"
  local state_key="${device_serial//[^[:alnum:]._-]/_}"
  printf '%s/%s.added-mask\n' "${state_root%/}" "$state_key"
}

read_added_mask() {
  local state_file value
  state_file="$(state_file_path)"
  [[ -f "$state_file" ]] || {
    printf '0\n'
    return
  }

  value="$(sed -n '1p' "$state_file")"
  [[ "$value" =~ ^[0-9]+$ ]] || fail "invalid saved session state: $state_file"
  printf '%s\n' "$value"
}

write_added_mask() {
  local value="$1"
  local state_file state_dir
  state_file="$(state_file_path)"
  state_dir="${state_file%/*}"
  mkdir -p "$state_dir"
  chmod 700 "$state_dir"
  printf '%s\n' "$value" > "$state_file"
}

clear_added_mask() {
  local state_file
  state_file="$(state_file_path)"
  [[ ! -e "$state_file" ]] || rm -f "$state_file"
}

print_status() {
  local setting power_mask added_mask
  setting="$(read_stay_awake_setting)"
  power_mask="$(read_power_source_mask)"
  added_mask="$(read_added_mask)"

  printf 'serial=%s\n' "$device_serial"
  printf 'stay_on_while_plugged_in=%s\n' "$setting"
  printf 'active_power_mask=%s\n' "$power_mask"
  printf 'active_power_sources=%s\n' "$(power_source_names "$power_mask")"
  printf 'session_added_mask=%s\n' "$added_mask"
}

resolve_adb_binary
resolve_device

case "$action" in
  enable)
    before="$(read_stay_awake_setting)"
    power_mask="$(read_power_source_mask)"
    ((power_mask != 0)) || fail "device reports no active charging source"
    desired=$((before | power_mask))
    newly_added=$((power_mask & ~before))
    previous_added="$(read_added_mask)"
    session_added=$((previous_added | newly_added))
    ((session_added == 0)) || write_added_mask "$session_added"
    if ((desired != before)); then
      run_adb shell settings put global stay_on_while_plugged_in "$desired" >/dev/null
    fi
    after="$(read_stay_awake_setting)"
    (((after & power_mask) == power_mask)) || fail "stay-awake verification failed"
    printf 'previous_stay_on_while_plugged_in=%s\n' "$before"
    printf 'newly_added_mask=%s\n' "$newly_added"
    print_status
    ;;
  status)
    print_status
    ;;
  restore)
    before="$(read_stay_awake_setting)"
    added_mask="$(read_added_mask)"
    desired=$((before & ~added_mask))
    if ((desired != before)); then
      run_adb shell settings put global stay_on_while_plugged_in "$desired" >/dev/null
    fi
    after="$(read_stay_awake_setting)"
    (((after & added_mask) == 0)) || fail "stay-awake restore verification failed"
    clear_added_mask
    printf 'previous_stay_on_while_plugged_in=%s\n' "$before"
    printf 'restored_mask=%s\n' "$added_mask"
    print_status
    ;;
esac
