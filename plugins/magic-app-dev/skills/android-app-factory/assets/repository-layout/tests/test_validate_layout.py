from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "validate_layout.py"
SPEC = importlib.util.spec_from_file_location("validate_layout", MODULE_PATH)
assert SPEC and SPEC.loader
VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR)


class RepositoryLayoutValidatorTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self._create_valid_layout()

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def _write(self, relative: str, content: str = "# Current\n") -> None:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def _create_valid_layout(self) -> None:
        for relative in VALIDATOR.REQUIRED_PATHS:
            self._write(relative)
        for section in VALIDATOR.DOC_SECTIONS:
            (self.root / "docs" / section).mkdir(parents=True, exist_ok=True)

    def test_accepts_current_layout(self) -> None:
        self.assertEqual([], VALIDATOR.validate(self.root))

    def test_rejects_non_document_artifact_in_docs(self) -> None:
        self._write("docs/product/mockup.png", "not really a png")

        errors = VALIDATOR.validate(self.root)

        self.assertTrue(
            any("non-document artifact inside docs/" in error for error in errors)
        )

    def test_rejects_unsupported_docs_section(self) -> None:
        self._write("docs/misc/notes.md")

        errors = VALIDATOR.validate(self.root)

        self.assertTrue(any("unsupported docs/ entry" in error for error in errors))

    def test_rejects_file_at_docs_root(self) -> None:
        self._write("docs/notes.md")

        errors = VALIDATOR.validate(self.root)

        self.assertTrue(any("unsupported docs/ entry" in error for error in errors))

    def test_rejects_broken_local_markdown_link(self) -> None:
        self._write("docs/product/guide.md", "[Missing](missing.md)\n")

        errors = VALIDATOR.validate(self.root)

        self.assertTrue(
            any("broken local Markdown link" in error for error in errors)
        )

    def test_rejects_versioned_state_copy(self) -> None:
        self._write("docs/product/requirements-v2.md")

        errors = VALIDATOR.validate(self.root)

        self.assertTrue(any("state-copy filename" in error for error in errors))

    def test_rejects_archive_directory(self) -> None:
        self._write("docs/product/archive/old-requirements.md")

        errors = VALIDATOR.validate(self.root)

        self.assertTrue(any("state-copy directory" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
