#!/usr/bin/env python3
"""Validate the generated repository's information architecture."""

from __future__ import annotations

import argparse
import os
import re
from collections.abc import Iterator
from pathlib import Path
from urllib.parse import unquote, urlsplit


DOC_SECTIONS = {"decisions", "engineering", "operations", "product"}

REQUIRED_PATHS = (
    "README.md",
    "docs/README.md",
    "docs/product/product-requirements.md",
    "docs/engineering/architecture.md",
    "docs/engineering/testing.md",
    "docs/operations/README.md",
    "docs/decisions/README.md",
    "tools/README.md",
    "tools/repository/validate_layout.py",
    "publishing/README.md",
    "publishing/legal/README.md",
)

DISALLOWED_DOC_DIRECTORY_NAMES = {
    "archive",
    "archives",
    "backup",
    "backups",
    "draft",
    "drafts",
    "old",
    "obsolete",
    "temp",
    "tmp",
}
DISALLOWED_STATE_COPY_NAME = re.compile(
    r"(?:^|[-_])(final|draft|copy|backup|old|v\d+|\d{4}-\d{2}-\d{2})(?:[-_.]|$)",
    re.IGNORECASE,
)

MARKDOWN_AREAS = (
    "README.md",
    "docs",
    "design",
    "tools",
    "publishing",
    "releases/README.md",
    ".agents/skills",
)
MARKDOWN_LINK = re.compile(r"!?\[[^\]]*\]\(([^)\n]+)\)")


def _relative(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def _markdown_sources(root: Path) -> Iterator[Path]:
    seen: set[Path] = set()
    for relative in MARKDOWN_AREAS:
        area = root / relative
        if area.is_file():
            candidates = [area]
        elif area.is_dir():
            candidates = area.rglob("*.md")
        else:
            continue
        for candidate in candidates:
            if candidate.is_symlink() or candidate in seen:
                continue
            seen.add(candidate)
            yield candidate


def _local_link_target(raw_destination: str) -> str | None:
    destination = raw_destination.strip()
    if destination.startswith("<") and ">" in destination:
        destination = destination[1 : destination.index(">")]
    else:
        destination = destination.split(maxsplit=1)[0]
    if not destination or destination.startswith("#"):
        return None
    parsed = urlsplit(destination)
    if parsed.scheme or parsed.netloc or destination.startswith("/"):
        return None
    return unquote(parsed.path)


def _validate_markdown_links(root: Path) -> list[str]:
    errors: list[str] = []
    for source in _markdown_sources(root):
        for line_number, line in enumerate(
            source.read_text(encoding="utf-8").splitlines(), start=1
        ):
            for match in MARKDOWN_LINK.finditer(line):
                local_target = _local_link_target(match.group(1))
                if local_target is None:
                    continue
                target = source.parent / local_target
                if not target.exists():
                    errors.append(
                        f"broken local Markdown link: {_relative(source, root)}:"
                        f"{line_number} -> {local_target}"
                    )
    return errors


def validate(repo_root: Path) -> list[str]:
    root = repo_root.resolve()
    docs = root / "docs"
    errors: list[str] = []

    for relative in REQUIRED_PATHS:
        if not (root / relative).exists():
            errors.append(f"missing required repository entry: {relative}")

    if not docs.is_dir():
        errors.append("missing required repository entry: docs")
        return errors

    for child in docs.iterdir():
        if child.name == "README.md":
            continue
        if child.is_dir() and child.name in DOC_SECTIONS:
            continue
        errors.append(
            f"unsupported docs/ entry: {_relative(child, root)}; "
            "choose a documented section"
        )

    for directory, dirnames, filenames in os.walk(docs, followlinks=False):
        current = Path(directory)
        for name in tuple(dirnames):
            path = current / name
            if name.lower() in DISALLOWED_DOC_DIRECTORY_NAMES:
                errors.append(
                    f"state-copy directory inside docs/: {_relative(path, root)}; "
                    "update the current source or use Git history"
                )
                dirnames.remove(name)
            elif path.is_symlink():
                errors.append(f"unexpected symlink inside docs/: {_relative(path, root)}")
                dirnames.remove(name)

        for filename in filenames:
            path = current / filename
            relative = _relative(path, root)
            if DISALLOWED_STATE_COPY_NAME.search(path.stem):
                errors.append(
                    f"state-copy filename inside docs/: {relative}; "
                    "update the current source instead of adding a versioned copy"
                )
            if path.is_symlink():
                errors.append(f"unexpected symlink inside docs/: {relative}")
            elif path.suffix.lower() != ".md":
                errors.append(
                    f"non-document artifact inside docs/: {relative}; "
                    "move executable, media, publishing, or generated content "
                    "to its owning top-level directory"
                )

    errors.extend(_validate_markdown_links(root))
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check repository artifact placement and documentation links."
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path(__file__).resolve().parents[2],
        help="repository root (defaults to the root containing tools/)",
    )
    args = parser.parse_args()

    errors = validate(args.repo_root)
    if errors:
        print("Repository layout check failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Repository layout check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
