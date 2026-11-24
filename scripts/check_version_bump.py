#!/usr/bin/env python3
"""Fail when a plugin's files changed against a base revision without a version bump.

usage: scripts/check_version_bump.py <base-ref>

Installed copies are keyed by version, so a changed plugin that keeps its version
never reaches a workspace. Run scripts/bump_version.py <plugin> to fix a failure.
"""
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def git(*args):
    return subprocess.run(['git', *args], cwd=ROOT, check=True, capture_output=True, text=True).stdout


def version_at(ref, plugin):
    try:
        return json.loads(git('show', f'{ref}:plugins/{plugin}/.claude-plugin/plugin.json'))['version']
    except subprocess.CalledProcessError:
        return None  # plugin is new


def main(argv):
    if len(argv) != 2:
        sys.exit(__doc__)
    base = argv[1]
    changed = git('diff', '--name-only', f'{base}...HEAD', '--', 'plugins').splitlines()
    plugins = sorted({line.split('/')[1] for line in changed})
    failures = []
    for plugin in plugins:
        old = version_at(base, plugin)
        manifest = ROOT / 'plugins' / plugin / '.claude-plugin/plugin.json'
        if old is None:
            continue
        if not manifest.is_file():
            continue  # plugin removed
        new = json.loads(manifest.read_text())['version']
        if new == old:
            failures.append(plugin)
    for plugin in failures:
        print(f'plugins/{plugin} changed but its version is still {version_at(base, plugin)}: '
              f'run scripts/bump_version.py {plugin}')
    if not failures:
        print('version check: ok' + (f' ({", ".join(plugins)} changed)' if plugins else ' (no plugin changes)'))
    sys.exit(1 if failures else 0)


if __name__ == '__main__':
    main(sys.argv)
