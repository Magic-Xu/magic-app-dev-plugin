#!/usr/bin/env python3
"""Validate the independent legal checkout and the App's legal URL resources."""

from __future__ import annotations

import argparse
from pathlib import Path
import subprocess
import sys
import xml.etree.ElementTree as ET


LEGAL_REPOSITORY = "__LEGAL_REPOSITORY__"


def resolve_legal_root(app_root: Path, explicit: Path | None = None) -> Path:
    if explicit is not None:
        return explicit.expanduser().resolve()
    result = subprocess.run(
        ["git", "-C", str(app_root), "rev-parse", "--path-format=absolute", "--git-common-dir"],
        text=True, capture_output=True, check=True,
    )
    return Path(result.stdout.strip()).parent.parent / LEGAL_REPOSITORY


def app_legal_urls(app_root: Path) -> list[str]:
    urls: set[str] = set()
    for path in (app_root / "app/src/main/res").glob("values*/strings.xml"):
        for element in ET.parse(path).getroot().findall("string"):
            name = element.get("name", "")
            if name.startswith("legal_") and name.endswith("_url") and element.text:
                urls.add(element.text.strip())
    return sorted(urls)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--legal-root", type=Path)
    args = parser.parse_args()
    app_root = Path(__file__).resolve().parents[2]
    try:
        root = resolve_legal_root(app_root, args.legal_root)
        validator = root / "tools/validate_site.py"
        if not validator.is_file():
            raise ValueError(f"Legal checkout/validator missing: {root}; clone {LEGAL_REPOSITORY} or pass --legal-root")
        command = [sys.executable, "-B", str(validator), "--site-root", str(root)]
        for url in app_legal_urls(app_root):
            command.extend(["--url", url])
        return subprocess.run(command, check=False).returncode
    except (OSError, ValueError, ET.ParseError, subprocess.CalledProcessError) as error:
        print(f"Legal validation failed: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
