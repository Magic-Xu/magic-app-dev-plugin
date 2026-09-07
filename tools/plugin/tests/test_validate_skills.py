from pathlib import Path
import importlib.util
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'validate_skills.py'
spec = importlib.util.spec_from_file_location('validate_skills', SCRIPT)
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


class SkillPackageValidationTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / 'plugin'
        self.skill = self.add_skill('sample-skill', '示例任务')

    def add_skill(self, name, title):
        folder = self.root / 'skills' / name
        (folder / 'agents').mkdir(parents=True)
        (folder / 'SKILL.md').write_text(f'---\nname: {name}\ndescription: Review the requested scope.\n---\n\n# Skill\n')
        (folder / 'agents/openai.yaml').write_text(f'''interface:
  display_name: "Magic · {title}"
  short_description: "Review the requested task with evidence."
  default_prompt: "Use ${name} for this task."
policy:
  allow_implicit_invocation: false
dependencies:
  tools:
    - type: "mcp"
      value: "example"
''')
        return folder

    def edit(self, relative, before, after):
        path = self.skill / relative
        path.write_text(path.read_text().replace(before, after))

    def assert_error(self, text):
        self.assertTrue(any(text in error for error in validator.validate_skills(self.root)), text)

    def test_accepts_unicode_metadata_and_preserves_extra_fields(self):
        self.assertEqual([], validator.validate_skills(self.root))

    def test_missing_skill_entrypoint_is_reported(self):
        (self.skill / 'SKILL.md').unlink()
        self.assert_error('missing skill entrypoint')

    def test_frontmatter_must_match_directory(self):
        self.edit('SKILL.md', 'name: sample-skill', 'name: other-skill')
        self.assert_error('matching the directory')

    def test_missing_frontmatter_and_empty_description(self):
        for content, expected in [('no metadata', 'missing YAML frontmatter'), ('---\nname: sample-skill\ndescription: ""\n---\n', 'description must')]:
            with self.subTest(content=content):
                (self.skill / 'SKILL.md').write_text(content)
                self.assert_error(expected)

    def test_unsupported_frontmatter_and_description_constraints(self):
        self.edit('SKILL.md', 'name: sample-skill', 'name: sample-skill\nunsupported: true')
        self.edit('SKILL.md', 'Review the requested scope.', 'Review <scope>.')
        self.assert_error('unsupported frontmatter')
        self.assert_error('without angle brackets')

    def test_keep_awake_remains_explicit_only(self):
        keep_awake = self.add_skill('android-device-keep-awake', '设备常亮')
        metadata = keep_awake / 'agents/openai.yaml'
        self.assertEqual([], validator.validate_skills(self.root))
        metadata.write_text(metadata.read_text().replace('false', 'true'))
        self.assert_error('must remain explicit-only')

    def test_duplicate_yaml_keys_fail_in_both_files(self):
        self.edit('SKILL.md', 'name: sample-skill', 'name: sample-skill\nname: sample-skill')
        self.edit('agents/openai.yaml', 'interface:', 'interface: {}\ninterface:')
        errors = validator.validate_skills(self.root)
        self.assertEqual(2, sum('duplicate YAML key' in error for error in errors))

    def test_missing_and_malformed_agent_metadata_fail(self):
        path = self.skill / 'agents/openai.yaml'
        path.unlink()
        self.assert_error('openai.yaml')
        path.write_text('interface: []')
        self.assert_error('interface must be a mapping')

    def test_prefix_duplicate_title_and_prompt_identity(self):
        self.add_skill('another-skill', '示例任务')
        self.assert_error('duplicate display_name')
        self.edit('agents/openai.yaml', 'Magic · 示例任务', '示例任务')
        self.edit('agents/openai.yaml', '$sample-skill', '$another-skill')
        self.assert_error('must use Magic')
        self.assert_error('must invoke $sample-skill')

    def test_description_length_and_boolean_policy(self):
        self.edit('agents/openai.yaml', 'Review the requested task with evidence.', 'short')
        self.edit('agents/openai.yaml', 'false', '"false"')
        self.assert_error('25–64')
        self.assert_error('must be a boolean')

    def test_checks_linked_files_and_reference_link_definitions(self):
        with (self.skill / 'SKILL.md').open('a') as out:
            out.write('\n[guide](references/missing.md)\n[other]: references/also-missing.md\n')
        self.assertEqual(2, sum('missing link target' in e for e in validator.validate_skills(self.root)))

    def test_accepts_cross_skill_links_fragments_urls_and_fenced_examples(self):
        self.add_skill('another-skill', '另一任务')
        references = self.skill / 'references'
        references.mkdir()
        (references / 'a guide.md').write_text('# Guide\n')
        with (self.skill / 'SKILL.md').open('a') as out:
            out.write('''
[other](../another-skill/SKILL.md#heading)
[guide](references/a%20guide.md "Title")
[dir](references/)
[anchor](#heading)
[remote](https://example.org/unavailable)
[named][ref]
[ref]: <references/a guide.md>
~~~md
[generated example](not-in-package.md)
~~~
```sh
echo $example-variable
```
''')
        self.assertEqual([], validator.validate_skills(self.root))

    def test_link_traversal_and_symlink_escape_fail(self):
        outside = Path(self.temp.name) / 'outside.md'
        outside.write_text('outside')
        (self.skill / 'outside.md').symlink_to(outside)
        with (self.skill / 'SKILL.md').open('a') as out:
            out.write('\n[escape](../../../outside.md)\n[symlink](outside.md)\n')
        self.assertEqual(2, sum('leaves package' in e for e in validator.validate_skills(self.root)))

    def test_missing_icon_and_unknown_skill_call_fail(self):
        self.edit('agents/openai.yaml', 'interface:', 'interface:\n  icon_small: "./assets/missing.png"')
        with (self.skill / 'SKILL.md').open('a') as out:
            out.write('\nUse `$unknown-skill`.\n')
        self.assert_error('invalid icon_small')
        self.assert_error('unknown skill reference')

    def test_empty_package_and_external_capability_names(self):
        self.assertTrue(validator.validate_skills(Path(self.temp.name) / 'absent'))
        with (self.skill / 'SKILL.md').open('a') as out:
            out.write('\nUse `$lark-doc` or `$artifact-boundary-review` when available.\n')
        self.assertEqual([], validator.validate_skills(self.root))


if __name__ == '__main__':
    unittest.main()
