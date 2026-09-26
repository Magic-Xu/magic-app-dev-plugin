#!/usr/bin/env python3
"""Read-only checks for published routes, local links, and App URL fragments."""

from __future__ import annotations

import argparse
import json
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit


class Page(HTMLParser):
    def __init__(self, text: str) -> None:
        super().__init__()
        self.ids: set[str] = set()
        self.links: list[str] = []
        self.has_title = False
        self.has_heading = False
        self.feed(text)

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        self.has_title |= tag == "title"
        self.has_heading |= tag == "h1"
        if values.get("id"):
            self.ids.add(values["id"])
        if tag == "a" and values.get("name"):
            self.ids.add(values["name"])
        for key in ("href", "src"):
            if values.get(key):
                self.links.append(values[key])


def validate(root: Path, app_urls: list[str] | None = None) -> list[str]:
    root = root.resolve()
    errors: list[str] = []
    try:
        config = json.loads((root / "site.json").read_text(encoding="utf-8"))
        base = config["baseUrl"].rstrip("/") + "/"
        required = config["requiredPages"]
        origin = urlsplit(base)
        if origin.scheme != "https" or not origin.netloc or not required:
            raise ValueError("baseUrl must be HTTPS and requiredPages must not be empty")
    except (OSError, ValueError, KeyError, TypeError) as error:
        return [f"invalid site.json: {error}"]

    pages: dict[Path, Page] = {}
    for relative in required:
        path = (root / relative).resolve()
        if not path.is_relative_to(root) or not path.is_file():
            errors.append(f"missing or out-of-site required page: {relative}")
    for path in root.rglob("*.html"):
        if any(part.startswith(".") or part in {"node_modules", "_site", "build"}
               for part in path.relative_to(root).parts):
            continue
        resolved = path.resolve()
        if not resolved.is_relative_to(root):
            errors.append(f"page escapes site: {path.relative_to(root)}")
            continue
        page = Page(path.read_text(encoding="utf-8"))
        pages[resolved] = page
        if not page.has_title or not page.has_heading:
            errors.append(f"missing title or main heading: {path.relative_to(root)}")

    def check(url: str, source: str, required_url: bool = False) -> None:
        parsed = urlsplit(url)
        same_origin = parsed.scheme == origin.scheme and parsed.netloc == origin.netloc
        if not same_origin:
            if required_url:
                errors.append(f"App URL uses another site: {url}")
            return
        decoded_path = unquote(parsed.path)
        prefix = unquote(origin.path)
        if not decoded_path.startswith(prefix):
            errors.append(f"link leaves site base path: {source} -> {url}")
            return
        target = (root / decoded_path[len(prefix):]).resolve()
        if not target.is_relative_to(root):
            errors.append(f"link escapes site: {source} -> {url}")
            return
        if target.is_dir():
            target = (target / "index.html").resolve()
        if not target.is_relative_to(root):
            errors.append(f"link escapes site: {source} -> {url}")
            return
        if not target.is_file():
            errors.append(f"broken local link: {source} -> {url}")
        elif parsed.fragment and target.suffix == ".html":
            page = pages.get(target)
            if page is None or unquote(parsed.fragment) not in page.ids:
                errors.append(f"missing fragment: {source} -> {url}")

    for path, page in pages.items():
        relative = path.relative_to(root).as_posix()
        for link in page.links:
            check(urljoin(base + relative, link), relative)
    for url in app_urls or []:
        check(url, "App", required_url=True)
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--site-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--url", action="append", default=[])
    args = parser.parse_args()
    try:
        errors = validate(args.site_root, args.url)
    except (OSError, ValueError, TypeError) as error:
        errors = [str(error)]
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print("Legal site routes, local links, and App URL fragments passed (read-only).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
