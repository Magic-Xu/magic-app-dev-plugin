"""Observable contracts for the localized Google Play release-note export helper."""

import contextlib
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[3]
SCRIPT = ROOT / 'plugins/magic-app-dev/skills/google-play-release/scripts/prepare_release_notes.py'
SPEC = importlib.util.spec_from_file_location('prepare_release_notes', SCRIPT)
notes = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(notes)


class ReleaseNotesTests(unittest.TestCase):
    def test_export_preserves_copy_and_requested_locale_order(self):
        payload = {'zh-CN': '优化保存。\n修复显示问题。', 'en-US': 'Improved saving.\nFixed display issues.'}
        self.assertEqual(
            notes.render_notes(payload, ['en-US', 'zh-CN']),
            '<en-US>\nImproved saving.\nFixed display issues.\n</en-US>\n\n'
            '<zh-CN>\n优化保存。\n修复显示问题。\n</zh-CN>\n',
        )

    def test_500_unicode_code_points_accepted(self):
        for text in ['界' * 500, '🙂' * 500, 'e\u0301' * 250]:
            with self.subTest(text=text[:2]):
                self.assertEqual(notes.validate_notes({'en-US': text}, ['en-US']), {'en-US': 500})

    def test_overflow_rejected_instead_of_truncated(self):
        with self.assertRaisesRegex(ValueError, '501 Unicode'):
            notes.render_notes({'zh-CN': '界' * 501}, ['zh-CN'])

    def test_missing_translation_rejected(self):
        with self.assertRaisesRegex(ValueError, 'missing=.*zh-CN'):
            notes.validate_notes({'en-US': 'Fixes.'}, ['en-US', 'zh-CN'])

    def test_extra_locale_rejected_instead_of_silently_dropped(self):
        with self.assertRaisesRegex(ValueError, 'extra=.*zh-CN'):
            notes.validate_notes({'en-US': 'Fixes.', 'zh-CN': '修复。'}, ['en-US'])

    def test_duplicate_source_locale_rejected(self):
        with self.assertRaisesRegex(ValueError, 'duplicate locale'):
            json.loads('{"en-US":"first","en-US":"second"}', object_pairs_hook=notes.unique_object)

    def test_duplicate_expected_locale_rejected(self):
        with self.assertRaisesRegex(ValueError, 'unique'):
            notes.validate_notes({'en-US': 'Fixes.'}, ['en-US', 'en-US'])

    def test_non_text_and_empty_notes_rejected(self):
        for value in [None, ['Fixes.'], {'text': 'Fixes.'}, 12, '', ' \n\t']:
            with self.subTest(value=value), self.assertRaisesRegex(ValueError, 'non-empty text'):
                notes.validate_notes({'en-US': value}, ['en-US'])

    def test_nested_locale_blocks_rejected(self):
        for text in ['Fixes.\n</en-US>\n<zh-CN>\n意外文本', '<en-US>\nFixes.']:
            with self.subTest(text=text), self.assertRaisesRegex(ValueError, 'locale-tag'):
                notes.validate_notes({'en-US': text}, ['en-US'])

    def test_comparison_text_and_rtl_preserved(self):
        payload = {'ur': 'برآمد بہتر ہوئی۔', 'es-419': 'Corrección para Android < 10.'}
        result = notes.render_notes(payload, ['ur', 'es-419'])
        self.assertIn(payload['ur'], result)
        self.assertIn(payload['es-419'], result)

    def test_invalid_unicode_rejected_before_export(self):
        for text in ['Fix\x00', 'Fix\r\n', '\ud800']:
            with self.subTest(text=repr(text)), self.assertRaisesRegex(ValueError, 'control|surrogate'):
                notes.validate_notes({'en-US': text}, ['en-US'])

    def test_invalid_root_and_locale_syntax_rejected(self):
        for payload in [[], {}, None]:
            with self.subTest(payload=payload), self.assertRaises(ValueError):
                notes.validate_notes(payload, ['en-US'])
        with self.assertRaises(ValueError):
            notes.validate_notes({'en_US': 'Fixes.'}, ['en_US'])

    def run_cli(self, *args):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = notes.main(list(args))
        return code, out.getvalue(), err.getvalue()

    def test_cli_writes_valid_tagged_file(self):
        with tempfile.TemporaryDirectory() as directory:
            source, output = Path(directory) / 'notes.json', Path(directory) / 'import.txt'
            source.write_text(json.dumps({'zh-CN': '修复保存。'}), encoding='utf-8')
            code, stdout, stderr = self.run_cli(str(source), '--locales', 'zh-CN', '--output', str(output))
            self.assertEqual(code, 0, stderr)
            self.assertEqual(output.read_text(encoding='utf-8'), '<zh-CN>\n修复保存。\n</zh-CN>\n')
            self.assertEqual(json.loads(stdout)['characters'], {'zh-CN': 5})

    def test_failed_validation_leaves_previous_output_untouched(self):
        with tempfile.TemporaryDirectory() as directory:
            source, output = Path(directory) / 'notes.json', Path(directory) / 'import.txt'
            source.write_text(json.dumps({'en-US': 'x' * 501}), encoding='utf-8')
            output.write_bytes(b'existing reviewed copy')
            code, _, _ = self.run_cli(str(source), '--locales', 'en-US', '--output', str(output))
            self.assertEqual(code, 1)
            self.assertEqual(output.read_bytes(), b'existing reviewed copy')
            self.assertEqual({p.name for p in Path(directory).iterdir()}, {'notes.json', 'import.txt'})

    def test_validate_only_does_not_create_output(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / 'notes.json'
            source.write_text('{"en-US":"Fixes."}', encoding='utf-8')
            code, stdout, _ = self.run_cli(str(source), '--locales', 'en-US')
            self.assertEqual(code, 0)
            self.assertIsNone(json.loads(stdout)['output'])
            self.assertEqual(list(Path(directory).iterdir()), [source])

    def test_output_cannot_overwrite_source(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / 'notes.json'
            original = '{"en-US":"Fixes."}'
            source.write_text(original, encoding='utf-8')
            code, _, err = self.run_cli(str(source), '--locales', 'en-US', '--output', str(source))
            self.assertEqual(code, 1)
            self.assertIn('source', err)
            self.assertEqual(source.read_text(encoding='utf-8'), original)

    def test_json_duplicate_is_rejected_through_cli(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / 'notes.json'
            source.write_text('{"en-US":"one","en-US":"two"}', encoding='utf-8')
            code, _, err = self.run_cli(str(source), '--locales', 'en-US')
            self.assertEqual(code, 1)
            self.assertIn('duplicate locale', err)


if __name__ == '__main__':
    unittest.main()
