#!/usr/bin/env python3
"""Bump a plugin's version in both manifests and refresh the protected-file hashes.

usage: scripts/bump_version.py <plugin> [patch|minor|major]

A plugin's version lives in plugins/<plugin>/.claude-plugin/plugin.json and
plugins/<plugin>/.codex-plugin/plugin.json; they must match. The context-layout
fixture records a sha256 for a few protected files; any that changed are refreshed
so the tests keep passing. Edits are textual so the files keep their formatting.
"""
import hashlib
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / 'tests/fixtures/context-layout/manifest.json'
VERSION = re.compile(r'("version"\s*:\s*")(\d+)\.(\d+)\.(\d+)(")')


def bump(version, part):
    major, minor, patch = version
    if part == 'major':
        return major + 1, 0, 0
    if part == 'minor':
        return major, minor + 1, 0
    return major, minor, patch + 1


def main(argv):
    if len(argv) not in (2, 3) or (len(argv) == 3 and argv[2] not in ('patch', 'minor', 'major')):
        sys.exit(__doc__)
    plugin, part = argv[1], argv[2] if len(argv) == 3 else 'patch'
    manifests = [ROOT / 'plugins' / plugin / host / 'plugin.json'
                 for host in ('.claude-plugin', '.codex-plugin')]
    missing = [str(m) for m in manifests if not m.is_file()]
    if missing:
        sys.exit('no such manifest: ' + ', '.join(missing))
    current = {json.loads(m.read_text())['version'] for m in manifests}
    if len(current) != 1:
        sys.exit(f'{plugin}: the two manifests disagree on the version: {sorted(current)}')
    old = current.pop()
    new = '.'.join(map(str, bump(tuple(map(int, old.split('.'))), part)))
    for manifest in manifests:
        text = manifest.read_text()
        text, count = VERSION.subn(lambda m: f'{m[1]}{new}{m[5]}', text, count=1)
        if count != 1:
            sys.exit(f'{manifest}: no version field found')
        manifest.write_text(text)
    refreshed = []
    fixture = FIXTURE.read_text()
    for relative, recorded in json.loads(fixture)['protected_files'].items():
        path = ROOT / relative
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != recorded:
            fixture = fixture.replace(recorded, actual)
            refreshed.append(relative)
    if refreshed:
        FIXTURE.write_text(fixture)
    print(f'{plugin}: {old} -> {new}')
    for relative in refreshed:
        print(f'refreshed fixture hash: {relative}')


if __name__ == '__main__':
    main(sys.argv)
