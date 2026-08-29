#!/usr/bin/env python3
"""Create and publish the paired GitHub repositories for a generated workspace."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


class PublishError(RuntimeError):
    pass


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace", required=True)
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Create repositories, push commits, and enable Pages.",
    )
    return parser.parse_args()


def run(
    command: list[str],
    cwd: Path | None = None,
    input_text: str | None = None,
    allow_failure: bool = False,
) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        command,
        cwd=cwd,
        input=input_text,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if result.returncode != 0 and not allow_failure:
        detail = (result.stderr or result.stdout).strip()
        raise PublishError(
            f"command failed: {' '.join(command)}"
            + (f"\n{detail}" if detail else "")
        )
    return result


def load_workspace(workspace: Path) -> tuple[dict, Path, Path]:
    candidates = list(workspace.glob("*/.app-factory/spec.json"))
    if len(candidates) != 1:
        raise PublishError(
            "expected exactly one child Android repository with .app-factory/spec.json"
        )
    spec_path = candidates[0]
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    app_root = spec_path.parents[1]
    legal_root = workspace / spec["repositories"]["legal"]
    if not legal_root.is_dir():
        raise PublishError(f"legal repository directory is missing: {legal_root}")
    return spec, app_root, legal_root


def validate_local_repo(repo: Path) -> None:
    if not (repo / ".git").is_dir():
        raise PublishError(f"not an initialized Git repository: {repo}")
    branch = run(["git", "branch", "--show-current"], cwd=repo).stdout.strip()
    if branch != "main":
        raise PublishError(f"{repo} must be on main before initial publishing")
    status = run(["git", "status", "--short"], cwd=repo).stdout.strip()
    if status:
        raise PublishError(f"{repo} has uncommitted changes:\n{status}")
    run(["git", "rev-parse", "--verify", "HEAD"], cwd=repo)


def remote_exists(full_name: str) -> tuple[bool, str | None]:
    result = run(
        ["gh", "repo", "view", full_name, "--json", "visibility", "--jq", ".visibility"],
        allow_failure=True,
    )
    if result.returncode == 0:
        return True, result.stdout.strip().upper()
    combined = (result.stdout + result.stderr).lower()
    if "could not resolve to a repository" in combined or "not found" in combined:
        return False, None
    raise PublishError(
        f"unable to determine whether {full_name} exists:\n"
        + (result.stderr or result.stdout).strip()
    )


def origin_url(repo: Path) -> str | None:
    result = run(
        ["git", "remote", "get-url", "origin"],
        cwd=repo,
        allow_failure=True,
    )
    return result.stdout.strip() if result.returncode == 0 else None


def matches_origin(origin: str, owner: str, repo_name: str) -> bool:
    normalized = origin.removesuffix(".git").rstrip("/")
    return normalized.endswith(f"github.com:{owner}/{repo_name}") or normalized.endswith(
        f"github.com/{owner}/{repo_name}"
    )


def publish_repo(
    local: Path,
    owner: str,
    repo_name: str,
    visibility: str,
) -> str:
    full_name = f"{owner}/{repo_name}"
    exists, actual_visibility = remote_exists(full_name)
    current_origin = origin_url(local)

    if exists:
        if actual_visibility != visibility.upper():
            raise PublishError(
                f"{full_name} already exists with visibility {actual_visibility}; "
                f"expected {visibility.upper()}"
            )
        if current_origin is None or not matches_origin(current_origin, owner, repo_name):
            raise PublishError(
                f"{full_name} already exists but is not the expected origin of {local}; "
                "refusing to adopt it"
            )
        run(["git", "push", "-u", "origin", "main"], cwd=local)
        return "resumed"

    if current_origin is not None:
        raise PublishError(
            f"{local} already has origin {current_origin}; refusing to create {full_name}"
        )
    run(
        [
            "gh",
            "repo",
            "create",
            full_name,
            f"--{visibility}",
            "--source",
            str(local),
            "--remote",
            "origin",
            "--push",
        ]
    )
    return "created"


def enable_pages(owner: str, repo_name: str) -> str:
    endpoint = f"repos/{owner}/{repo_name}/pages"
    existing = run(
        ["gh", "api", endpoint, "--jq", ".html_url"],
        allow_failure=True,
    )
    if existing.returncode == 0:
        return existing.stdout.strip()

    payload = json.dumps(
        {
            "build_type": "legacy",
            "source": {"branch": "main", "path": "/"},
        }
    )
    run(
        [
            "gh",
            "api",
            "--method",
            "POST",
            endpoint,
            "--input",
            "-",
            "--jq",
            ".html_url",
        ],
        input_text=payload,
    )
    created = run(["gh", "api", endpoint, "--jq", ".html_url"])
    return created.stdout.strip()


def main() -> int:
    try:
        args = parse_args()
        workspace = Path(args.workspace).expanduser().resolve()
        spec, app_root, legal_root = load_workspace(workspace)
        owner = spec["github"]["owner"]
        app_name = spec["repositories"]["android"]
        legal_name = spec["repositories"]["legal"]

        validate_local_repo(app_root)
        validate_local_repo(legal_root)

        plan = {
            "workspace": str(workspace),
            "androidRepository": {
                "local": str(app_root),
                "remote": f"{owner}/{app_name}",
                "visibility": "private",
            },
            "legalRepository": {
                "local": str(legal_root),
                "remote": f"{owner}/{legal_name}",
                "visibility": "public",
                "pagesSource": "main:/",
            },
            "apply": args.apply,
        }
        if not args.apply:
            print(json.dumps(plan, indent=2))
            return 0

        run(["gh", "auth", "status"])
        app_result = publish_repo(app_root, owner, app_name, "private")
        legal_result = publish_repo(legal_root, owner, legal_name, "public")
        pages_url = enable_pages(owner, legal_name)

        plan["results"] = {
            "android": app_result,
            "legal": legal_result,
            "pagesUrl": pages_url,
        }
        print(json.dumps(plan, indent=2))
        return 0
    except (PublishError, KeyError, json.JSONDecodeError) as error:
        print(f"android-app-factory publish failed: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
