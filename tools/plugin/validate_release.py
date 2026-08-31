#!/usr/bin/env python3
"""Validate the Magic App Dev plugin manifest and release version progression."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any


SEMVER_RE = re.compile(
    r"^(0|[1-9]\d*)\."
    r"(0|[1-9]\d*)\."
    r"(0|[1-9]\d*)"
    r"(?:-([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?"
    r"(?:\+([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?$"
)


@dataclass(frozen=True)
class SemVer:
    major: int
    minor: int
    patch: int
    prerelease: tuple[str, ...]
    build: tuple[str, ...]


def parse_semver(value: str) -> SemVer:
    match = SEMVER_RE.fullmatch(value)
    if match is None:
        raise ValueError(f"version must use strict SemVer: {value}")
    prerelease = tuple(match.group(4).split(".")) if match.group(4) else ()
    for identifier in prerelease:
        if identifier.isdigit() and len(identifier) > 1 and identifier.startswith("0"):
            raise ValueError(
                f"numeric prerelease identifiers cannot have leading zeroes: {value}"
            )
    build = tuple(match.group(5).split(".")) if match.group(5) else ()
    return SemVer(
        major=int(match.group(1)),
        minor=int(match.group(2)),
        patch=int(match.group(3)),
        prerelease=prerelease,
        build=build,
    )


def compare_precedence(left: SemVer, right: SemVer) -> int:
    left_core = (left.major, left.minor, left.patch)
    right_core = (right.major, right.minor, right.patch)
    if left_core != right_core:
        return 1 if left_core > right_core else -1
    if not left.prerelease and not right.prerelease:
        return 0
    if not left.prerelease:
        return 1
    if not right.prerelease:
        return -1
    for left_id, right_id in zip(left.prerelease, right.prerelease):
        if left_id == right_id:
            continue
        left_numeric = left_id.isdigit()
        right_numeric = right_id.isdigit()
        if left_numeric and right_numeric:
            return 1 if int(left_id) > int(right_id) else -1
        if left_numeric != right_numeric:
            return -1 if left_numeric else 1
        return 1 if left_id > right_id else -1
    if len(left.prerelease) == len(right.prerelease):
        return 0
    return 1 if len(left.prerelease) > len(right.prerelease) else -1


def _read_manifest(raw: str, source: str) -> tuple[dict[str, Any] | None, list[str]]:
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as error:
        return None, [f"{source} must contain valid JSON: {error}"]
    if not isinstance(payload, dict):
        return None, [f"{source} must contain a JSON object"]
    return payload, []


def _require_string(
    payload: dict[str, Any], key: str, source: str, errors: list[str]
) -> str | None:
    value = payload.get(key)
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{source} field {key!r} must be a non-empty string")
        return None
    return value


def validate_manifest(
    plugin_root: Path, payload: dict[str, Any], source: str
) -> tuple[SemVer | None, list[str]]:
    errors: list[str] = []
    name = _require_string(payload, "name", source, errors)
    if name is not None and name != plugin_root.name:
        errors.append(
            f"{source} name {name!r} must match plugin directory {plugin_root.name!r}"
        )
    version_value = _require_string(payload, "version", source, errors)
    version: SemVer | None = None
    if version_value is not None:
        try:
            version = parse_semver(version_value)
        except ValueError as error:
            errors.append(f"{source} {error}")
        else:
            if len(version.build) < 2 or version.build[0] != "codex":
                errors.append(
                    f"{source} version must end with one +codex.<cachebuster> suffix"
                )
    _require_string(payload, "description", source, errors)

    author = payload.get("author")
    if not isinstance(author, dict):
        errors.append(f"{source} field 'author' must be an object")
    else:
        _require_string(author, "name", f"{source} author", errors)

    skills = payload.get("skills")
    if skills != "./skills/" or not (plugin_root / "skills").is_dir():
        errors.append(f"{source} must point 'skills' at the existing ./skills/ directory")

    interface = payload.get("interface")
    if not isinstance(interface, dict):
        errors.append(f"{source} field 'interface' must be an object")
    else:
        for field in (
            "displayName",
            "shortDescription",
            "longDescription",
            "developerName",
            "category",
        ):
            _require_string(interface, field, f"{source} interface", errors)
        capabilities = interface.get("capabilities")
        if not isinstance(capabilities, list) or not all(
            isinstance(item, str) and item.strip() for item in capabilities
        ):
            errors.append(
                f"{source} interface field 'capabilities' must be an array of strings"
            )
        prompts = interface.get("defaultPrompt")
        if not isinstance(prompts, list) or not 1 <= len(prompts) <= 3:
            errors.append(
                f"{source} interface field 'defaultPrompt' must contain 1 to 3 prompts"
            )
        elif not all(
            isinstance(prompt, str) and prompt.strip() and len(prompt) <= 128
            for prompt in prompts
        ):
            errors.append(
                f"{source} interface prompts must be non-empty strings of at most 128 characters"
            )
    return version, errors


def _git(repo_root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=repo_root,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def validate_release(
    repo_root: Path, plugin_root: Path, base_ref: str | None = None
) -> list[str]:
    repo = repo_root.resolve()
    plugin = plugin_root.resolve()
    try:
        plugin_relative = plugin.relative_to(repo)
    except ValueError:
        return ["plugin root must be inside the repository root"]

    manifest_path = plugin / ".codex-plugin" / "plugin.json"
    if not manifest_path.is_file():
        return [f"missing plugin manifest: {manifest_path}"]
    current_payload, errors = _read_manifest(
        manifest_path.read_text(encoding="utf-8"), str(manifest_path)
    )
    if current_payload is None:
        return errors
    current_version, manifest_errors = validate_manifest(
        plugin, current_payload, str(manifest_path)
    )
    errors.extend(manifest_errors)

    if not base_ref:
        return errors
    if base_ref.startswith("-"):
        return errors + ["base ref cannot start with '-'"]
    resolved = _git(repo, "rev-parse", "--verify", f"{base_ref}^{{commit}}")
    if resolved.returncode != 0:
        return errors + [f"unable to resolve base ref {base_ref!r}"]
    base_commit = resolved.stdout.strip()

    changed = _git(
        repo,
        "diff",
        "--name-only",
        base_commit,
        "--",
        plugin_relative.as_posix(),
    )
    if changed.returncode != 0:
        return errors + ["unable to inspect plugin changes from the base ref"]
    if not changed.stdout.strip():
        return errors

    manifest_relative = manifest_path.relative_to(repo).as_posix()
    previous = _git(repo, "show", f"{base_commit}:{manifest_relative}")
    if previous.returncode != 0:
        return errors
    previous_payload, previous_errors = _read_manifest(
        previous.stdout, f"{base_commit}:{manifest_relative}"
    )
    errors.extend(previous_errors)
    if previous_payload is None or current_version is None:
        return errors
    previous_value = previous_payload.get("version")
    if not isinstance(previous_value, str):
        return errors + ["base plugin manifest has no valid version"]
    try:
        previous_version = parse_semver(previous_value)
    except ValueError as error:
        return errors + [f"base plugin manifest {error}"]
    if compare_precedence(current_version, previous_version) <= 0:
        current_value = current_payload.get("version")
        errors.append(
            "plugin content changed without increasing SemVer precedence: "
            f"{previous_value} -> {current_value}; changing only the cachebuster is insufficient"
        )
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate the Magic App Dev plugin release contract."
    )
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument(
        "--plugin-root", type=Path, default=Path("plugins/magic-app-dev")
    )
    parser.add_argument("--base-ref")
    args = parser.parse_args()
    plugin_root = (
        args.plugin_root
        if args.plugin_root.is_absolute()
        else args.repo_root / args.plugin_root
    )
    errors = validate_release(args.repo_root, plugin_root, args.base_ref)
    if errors:
        print("Plugin release validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Plugin release validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
