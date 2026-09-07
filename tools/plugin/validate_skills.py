#!/usr/bin/env python3
"""Lint packaged Magic skills: metadata, local links and named skill references.

This is deterministic package validation, not a model-routing evaluation. Markdown
checks cover inline links and reference-link definitions outside fenced examples.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit

import yaml


class UniqueKeyLoader(yaml.SafeLoader):
    """Reject duplicate keys instead of silently keeping the final YAML value."""


def unique_mapping(loader, node, deep=False):
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if not isinstance(key, str):
            raise ValueError('mapping keys must be strings')
        if key in result:
            raise ValueError(f'duplicate YAML key: {key}')
        result[key] = loader.construct_object(value_node, deep=deep)
    return result


UniqueKeyLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping)
SKILL_ID = re.compile(r'[a-z0-9]+(?:-[a-z0-9]+)*')
SKILL_CALL = re.compile(r'\$(?:magic-app-dev:)?([a-z][a-z0-9]*(?:-[a-z0-9]+)+)\b')
INLINE_LINK = re.compile(r'\[[^\]\n]*\]\(\s*(?:<([^>\n]+)>|([^\s)]+))(?:\s+["\'][^\n]*?["\'])?\s*\)')
LINK_DEFINITION = re.compile(r'^\s{0,3}\[[^\]\n]+\]:\s*(?:<([^>\n]+)>|(\S+))', re.M)
# These are optional, environment-owned capabilities; report-delivery.md documents
# their availability check and fallback. They are not bundled plugin dependencies.
EXTERNAL_SKILLS = {'lark-doc', 'artifact-boundary-review'}


def unfenced(source: str) -> str:
    result = []
    fence = None
    for line in source.splitlines():
        marker = re.match(r'^\s{0,3}(`{3,}|~{3,})(.*)$', line)
        if fence is None and marker:
            fence = marker.group(1)
        elif fence and marker and marker.group(1)[0] == fence[0] and len(marker.group(1)) >= len(fence) and not marker.group(2).strip():
            fence = None
        elif fence is None:
            result.append(line)
    return '\n'.join(result)


def load_mapping(source: str) -> dict:
    data = yaml.load(source, Loader=UniqueKeyLoader)
    if not isinstance(data, dict):
        raise ValueError('expected a YAML mapping')
    return data


def nonempty(data: dict, key: str) -> bool:
    return isinstance(data.get(key), str) and bool(data[key].strip())


def link_errors(path: Path, source: str, package: Path) -> list[str]:
    errors = []
    content = unfenced(source)
    for pattern in (INLINE_LINK, LINK_DEFINITION):
        for match in pattern.finditer(content):
            target = match.group(1) or match.group(2)
            parsed = urlsplit(target)
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            resolved = (path.parent / unquote(parsed.path)).resolve()
            if not resolved.is_relative_to(package.resolve()):
                errors.append(f'{path}: link leaves package: {target}')
            elif not resolved.exists():
                errors.append(f'{path}: missing link target: {target}')
    return errors


def validate_skills(plugin_root: Path) -> list[str]:
    root = plugin_root.resolve()
    skills_root = root / 'skills'
    if not skills_root.is_dir():
        return [f'{root}: missing skills directory']
    folders = sorted(p for p in skills_root.iterdir() if p.is_dir() and not p.name.startswith('.'))
    if not folders:
        return [f'{skills_root}: no skills found']
    known = {p.name for p in folders}
    errors = []
    display_names = set()
    for folder in folders:
        if not folder.resolve().is_relative_to(root):
            errors.append(f'{folder}: skill directory leaves package')
            continue
        entry = folder / 'SKILL.md'
        if not entry.is_file():
            errors.append(f'{entry}: missing skill entrypoint')
            continue
        try:
            source = entry.read_text(encoding='utf-8')
            frontmatter = re.match(r'\A---\r?\n(.*?)\r?\n---(?:\r?\n|$)', source, re.S)
            if frontmatter is None:
                raise ValueError('missing YAML frontmatter')
            data = load_mapping(frontmatter.group(1))
            allowed = {'name', 'description', 'license', 'allowed-tools', 'metadata'}
            if set(data) - allowed:
                errors.append(f'{entry}: unsupported frontmatter fields: {sorted(set(data) - allowed)}')
            name = data.get('name')
            if not isinstance(name, str) or len(name) > 64 or not SKILL_ID.fullmatch(name) or name != folder.name:
                errors.append(f'{entry}: name must be a valid skill ID matching the directory')
            if not nonempty(data, 'description'):
                errors.append(f'{entry}: description must be a non-empty string')
            elif len(data['description']) > 1024 or '<' in data['description'] or '>' in data['description']:
                errors.append(f'{entry}: description must be at most 1024 characters without angle brackets')
        except (OSError, UnicodeError, yaml.YAMLError, ValueError) as error:
            errors.append(f'{entry}: {error}')

        metadata = folder / 'agents/openai.yaml'
        try:
            agent = load_mapping(metadata.read_text(encoding='utf-8'))
            interface = agent.get('interface')
            if not isinstance(interface, dict):
                raise ValueError('interface must be a mapping')
            display = interface.get('display_name')
            if not isinstance(display, str) or not display.startswith('Magic · ') or not display[8:].strip():
                errors.append(f'{metadata}: display_name must use Magic · <task name>')
            elif display in display_names:
                errors.append(f'{metadata}: duplicate display_name: {display}')
            else:
                display_names.add(display)
            short = interface.get('short_description')
            if not isinstance(short, str) or not 25 <= len(short.strip()) <= 64:
                errors.append(f'{metadata}: short_description must contain 25–64 characters')
            prompt = interface.get('default_prompt')
            if not isinstance(prompt, str) or folder.name not in SKILL_CALL.findall(prompt):
                errors.append(f'{metadata}: default_prompt must invoke ${folder.name}')
            policy = agent.get('policy', {})
            if not isinstance(policy, dict) or ('allow_implicit_invocation' in policy and type(policy['allow_implicit_invocation']) is not bool):
                errors.append(f'{metadata}: allow_implicit_invocation must be a boolean')
            if folder.name == 'android-device-keep-awake' and (not isinstance(policy, dict) or policy.get('allow_implicit_invocation') is not False):
                errors.append(f'{metadata}: device keep-awake must remain explicit-only')
            for field in ('icon_small', 'icon_large'):
                if field in interface:
                    value = interface[field]
                    if not isinstance(value, str) or not value:
                        errors.append(f'{metadata}: {field} must be a non-empty path')
                    elif not (folder / value).resolve().is_relative_to(root) or not (folder / value).is_file():
                        errors.append(f'{metadata}: invalid {field} asset path')
        except (OSError, UnicodeError, yaml.YAMLError, ValueError) as error:
            errors.append(f'{metadata}: {error}')

        docs = [entry, *sorted((folder / 'references').rglob('*.md'))]
        for doc in docs:
            if not doc.resolve().is_relative_to(root):
                errors.append(f'{doc}: reference file leaves package')
                continue
            try:
                content = doc.read_text(encoding='utf-8')
                errors.extend(link_errors(doc, content, root))
                for call in sorted(set(SKILL_CALL.findall(unfenced(content)))):
                    if call not in known | EXTERNAL_SKILLS:
                        errors.append(f'{doc}: unknown skill reference: ${call}')
            except (OSError, UnicodeError, ValueError) as error:
                errors.append(f'{doc}: {error}')
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('plugin_root', type=Path)
    args = parser.parse_args()
    errors = validate_skills(args.plugin_root)
    if errors:
        print('\n'.join(errors))
        return 1
    print('Skill metadata, local links and named references passed.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
