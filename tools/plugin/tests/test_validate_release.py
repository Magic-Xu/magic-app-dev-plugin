from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "validate_release.py"
SPEC = importlib.util.spec_from_file_location("validate_release", MODULE_PATH)
assert SPEC and SPEC.loader
VALIDATOR = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = VALIDATOR
SPEC.loader.exec_module(VALIDATOR)


class PluginReleaseValidatorTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self.plugin = self.root / "plugins" / "magic-app-dev"
        (self.plugin / ".codex-plugin").mkdir(parents=True)
        (self.plugin / "skills" / "sample").mkdir(parents=True)
        (self.plugin / "skills" / "sample" / "SKILL.md").write_text(
            "---\nname: sample\ndescription: Sample.\n---\n", encoding="utf-8"
        )
        self._write_manifest("0.1.2+codex.initial")
        self._git("init", "-b", "main")
        self._git("config", "user.name", "plugin-release-test")
        self._git("config", "user.email", "plugin-release-test@example.com")
        self._commit("initial")
        self.base = self._git("rev-parse", "HEAD").stdout.strip()

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def _git(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["git", *args],
            cwd=self.root,
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

    def _write_manifest(self, version: str, prompt_count: int = 3) -> None:
        payload = {
            "name": "magic-app-dev",
            "version": version,
            "description": "Reusable app development workflows.",
            "author": {"name": "Magic Xu"},
            "skills": "./skills/",
            "interface": {
                "displayName": "Magic App Dev",
                "shortDescription": "App workflows.",
                "longDescription": "Reusable app development workflows.",
                "developerName": "Magic Xu",
                "category": "Productivity",
                "capabilities": ["Skills"],
                "defaultPrompt": ["Deliver this app requirement."] * prompt_count,
            },
        }
        path = self.plugin / ".codex-plugin" / "plugin.json"
        path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    def _commit(self, message: str) -> None:
        self._git("add", ".")
        self._git("commit", "-m", message)

    def test_accepts_increased_semver_for_plugin_change(self) -> None:
        self._write_manifest("0.2.0+codex.next")
        self._commit("release")

        errors = VALIDATOR.validate_release(self.root, self.plugin, self.base)

        self.assertEqual([], errors)

    def test_rejects_cachebuster_only_for_plugin_change(self) -> None:
        self._write_manifest("0.1.2+codex.next")
        self._commit("cachebuster only")

        errors = VALIDATOR.validate_release(self.root, self.plugin, self.base)

        self.assertTrue(any("without increasing SemVer" in error for error in errors))

    def test_allows_non_plugin_change_without_version_change(self) -> None:
        (self.root / "README.md").write_text("# Updated\n", encoding="utf-8")
        self._commit("readme")

        errors = VALIDATOR.validate_release(self.root, self.plugin, self.base)

        self.assertEqual([], errors)

    def test_rejects_more_than_three_default_prompts(self) -> None:
        self._write_manifest("0.2.0+codex.next", prompt_count=4)

        errors = VALIDATOR.validate_release(self.root, self.plugin)

        self.assertTrue(any("1 to 3 prompts" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
