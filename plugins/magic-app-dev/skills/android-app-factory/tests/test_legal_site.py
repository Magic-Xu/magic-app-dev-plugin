from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


SITE = load("site_validator", ROOT / "assets/legal-site/validate_site.py")
APP = load("app_validator", ROOT / "assets/legal-site/validate_legal_site.py")
FACTORY = load("workspace_validator", ROOT / "scripts/validate_workspace.py")


class LegalSiteTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.site = self.root / "sample-legal"
        self.site.mkdir()
        (self.site / "site.json").write_text(json.dumps({
            "baseUrl": "https://example.github.io/sample-legal/",
            "requiredPages": ["index.html", "zh-CN/privacy.html"],
        }))
        (self.site / "zh-CN").mkdir()
        (self.site / "index.html").write_text(
            '<title>Home</title><h1>Home</h1><a href="zh-CN/privacy.html#app-view">Policy</a>'
        )
        (self.site / "zh-CN/privacy.html").write_text(
            '<title>Policy</title><h1 id="app-view">Policy</h1><a href="../index.html">Home</a>'
        )

    def hashes(self):
        return {str(p.relative_to(self.site)): hashlib.sha256(p.read_bytes()).hexdigest()
                for p in self.site.rglob("*") if p.is_file()}

    def test_validates_without_writing_and_accepts_app_fragment(self):
        before = self.hashes()
        self.assertEqual([], SITE.validate(self.site, [
            "https://example.github.io/sample-legal/zh-CN/privacy.html#app-view"
        ]))
        self.assertEqual(before, self.hashes())

    def test_missing_language_page_fails(self):
        (self.site / "zh-CN/privacy.html").unlink()
        self.assertTrue(any("required page" in x for x in SITE.validate(self.site)))

    def test_broken_link_and_app_fragment_fail(self):
        with (self.site / "index.html").open("a") as f:
            f.write('<a href="missing.html">Missing</a>')
        errors = SITE.validate(self.site, [
            "https://example.github.io/sample-legal/zh-CN/privacy.html#missing"
        ])
        self.assertTrue(any("broken local link" in x for x in errors))
        self.assertTrue(any("missing fragment" in x for x in errors))

    def test_other_site_and_path_escape_fail(self):
        errors = SITE.validate(self.site, [
            "https://other.github.io/sample-legal/index.html",
            "https://example.github.io/sample-legal/%2e%2e/private.html",
        ])
        self.assertTrue(any("another site" in x for x in errors))
        self.assertTrue(any("escapes site" in x for x in errors))

    def test_app_urls_are_collected_from_all_locales(self):
        for locale, suffix in [("values", "index.html"), ("values-zh-rCN", "zh-CN/privacy.html#app-view")]:
            p = self.root / "app/src/main/res" / locale / "strings.xml"
            p.parent.mkdir(parents=True)
            p.write_text(f'<resources><string name="legal_privacy_policy_url">https://example.github.io/sample-legal/{suffix}</string></resources>')
        self.assertEqual(2, len(APP.app_legal_urls(self.root)))

    def test_default_site_resolution_uses_primary_checkout_from_worktree(self):
        app = self.root / "sample-android"
        def git(*args):
            return subprocess.run(["git", *args], check=True, capture_output=True, text=True)
        git("init", "-b", "main", str(app))
        (app / "README.md").write_text("App")
        git("-C", str(app), "add", ".")
        git("-C", str(app), "-c", "user.name=Test", "-c", "user.email=test@example.com", "commit", "-m", "initial")
        worktree = self.root / "worktrees/feature"
        git("-C", str(app), "worktree", "add", "-b", "feature", str(worktree))
        previous = APP.LEGAL_REPOSITORY
        try:
            APP.LEGAL_REPOSITORY = "sample-legal"
            self.assertEqual(self.site, APP.resolve_legal_root(worktree))
            self.assertEqual(self.root / "candidate", APP.resolve_legal_root(worktree, self.root / "candidate"))
        finally:
            APP.LEGAL_REPOSITORY = previous

    def test_new_workspace_has_one_editable_site_and_rejects_duplicate(self):
        subprocess.run([
            sys.executable, "-B", str(ROOT / "scripts/create_workspace.py"),
            "--app-name", "Example", "--slug", "example", "--application-id", "com.example.app",
            "--github-owner", "example", "--product-sentence-en", "Example app.",
            "--product-sentence-zh", "示例应用。", "--parent-dir", str(self.root), "--no-git",
        ], check=True, capture_output=True, text=True)
        app = self.root / "example/example-android"
        site = self.root / "example/example-legal"
        self.assertFalse((app / "publishing/legal").exists())
        self.assertFalse((app / "tools/publishing/legal").exists())
        policy = site / "privacy-policy.html"
        policy.write_text(policy.read_text().replace("Privacy Policy", "Updated Privacy Policy"))
        FACTORY.validate_public_boundary(app, site)
        subprocess.run([
            sys.executable, "-B", str(app / "tools/release/validate_legal_site.py"),
            "--legal-root", str(site),
        ], check=True, capture_output=True, text=True)
        (app / "publishing/legal").mkdir()
        with self.assertRaises(FACTORY.ValidationError):
            FACTORY.validate_public_boundary(app, site)


if __name__ == "__main__":
    unittest.main()
