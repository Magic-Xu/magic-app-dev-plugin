#!/usr/bin/env python3
"""Validate localized Google Play notes and optionally export Console tag blocks."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import sys
import tempfile

MAX_CHARACTERS = 500
LOCALE = re.compile(r"[A-Za-z]{2,3}(?:-[A-Za-z0-9]{2,8})*\Z")
TAG_LINE = re.compile(r"^\s*</?[A-Za-z][A-Za-z0-9-]*>\s*$", re.MULTILINE)


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate locale: {key}")
        result[key] = value
    return result


def validate_notes(payload, locales):
    if not isinstance(payload, dict) or not payload:
        raise ValueError("notes must be a non-empty JSON object mapping locales to text")
    if not locales or len(locales) != len(set(locales)):
        raise ValueError("expected locales must be non-empty and unique")
    if any(not LOCALE.fullmatch(locale) for locale in locales):
        raise ValueError("invalid expected locale syntax; use the exact Console locale codes")
    missing = set(locales) - payload.keys()
    extra = payload.keys() - set(locales)
    if missing or extra:
        raise ValueError(f"locale coverage mismatch; missing={sorted(missing)}, extra={sorted(extra)}")
    for locale in locales:
        note = payload[locale]
        if not isinstance(note, str) or not note.strip():
            raise ValueError(f"{locale}: notes must be non-empty text")
        if len(note) > MAX_CHARACTERS:
            raise ValueError(f"{locale}: {len(note)} Unicode characters exceeds {MAX_CHARACTERS}")
        if any((ord(c) < 32 and c not in '\n\t') or 0xD800 <= ord(c) <= 0xDFFF for c in note):
            raise ValueError(f"{locale}: unsupported control character or unpaired Unicode surrogate")
        if TAG_LINE.search(note):
            raise ValueError(f"{locale}: notes must not contain standalone locale-tag lines")
    return {locale: len(payload[locale]) for locale in locales}


def render_notes(payload, locales):
    validate_notes(payload, locales)
    return '\n\n'.join(f'<{locale}>\n{payload[locale]}\n</{locale}>' for locale in locales) + '\n'


def write_atomic(path, content):
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', newline='\n',
                                         dir=path.parent, delete=False) as stream:
            temporary = Path(stream.name)
            stream.write(content)
        os.replace(temporary, path)
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('notes', type=Path, help='JSON object of locale -> complete note')
    parser.add_argument('--locales', nargs='+', required=True, help='Exact target Console locale set, in output order')
    parser.add_argument('--output', type=Path, help='Optional tagged text output; parent directory must exist')
    args = parser.parse_args(argv)
    try:
        if args.output is not None and args.notes.resolve() == args.output.resolve():
            raise ValueError('output must not overwrite the notes source')
        payload = json.loads(args.notes.read_text(encoding='utf-8'), object_pairs_hook=unique_object)
        counts = validate_notes(payload, args.locales)
        if args.output is not None:
            write_atomic(args.output, render_notes(payload, args.locales))
    except (OSError, UnicodeError, ValueError) as error:
        print(f'ERROR: {error}', file=sys.stderr)
        return 1
    print(json.dumps({'valid': True, 'characters': counts,
                      'output': str(args.output) if args.output else None}, ensure_ascii=False))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
