#!/usr/bin/env bash
# Offline payload checks. Retain the fresh fixture for inspection; no cleanup.
set -eu

SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
python3 -B - "$SCRIPT_DIR" <<'PY'
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

hooks = Path(sys.argv[1])
fixture = Path(tempfile.mkdtemp(prefix='worktree-injector-test-'))
print(f'Retained offline fixture: {fixture}', flush=True)
repo = fixture / 'repo with spaces'
plain = fixture / 'plain'
repo.mkdir()
plain.mkdir()
subprocess.run(['git', 'init', '-q', '-b', 'main', str(repo)], check=True)
(repo / 'sentinel.txt').write_text('unrelated user state\n')
rule = (hooks.parent / 'rules/worktree-workflow.md').read_text()

def snapshot():
    return {str(p.relative_to(fixture)): p.read_bytes()
            for p in fixture.rglob('*') if p.is_file()}

before = snapshot()
env = os.environ.copy()
env.pop('CLAUDE_ALLOW_MAIN_EDITS', None)

def inject(cwd, disabled=False):
    child_env = env.copy()
    if disabled:
        child_env['CLAUDE_ALLOW_MAIN_EDITS'] = '1'
    result = subprocess.run(
        ['bash', str(hooks / 'inject-worktree-rule.sh')],
        input=json.dumps({'cwd': str(cwd)}), text=True,
        capture_output=True, env=child_env, cwd=plain, check=True)
    assert result.stderr == '', result.stderr
    return result.stdout

for disabled in (False, True):
    payload = json.loads(inject(repo, disabled))
    assert set(payload) == {'hookSpecificOutput'}
    output = payload['hookSpecificOutput']
    assert set(output) == {'hookEventName', 'additionalContext'}
    assert output['hookEventName'] == 'SessionStart'
    context = output['additionalContext']
    assert context.endswith('\n\n' + rule), 'injected rule was changed'
    preamble = context[:-len('\n\n' + rule)]
    assert 'best-effort backstop' in preamble
    assert 'Read the\nlinked worktree skill' in preamble
    assert 'does not replace other required guidance' in preamble
    assert 'without reading any further file' not in preamble
    assert ('hook is disabled' in preamble) == disabled
    assert 'permissionDecision' not in output
    print(f'PASS: repository payload, disabled={disabled}')

assert inject(plain) == '', 'non-repository session received context'
print('PASS: non-repository session emits no context')
assert snapshot() == before, 'injector mutated fixture files or Git metadata'
print('PASS: fixture files and Git metadata unchanged')
PY
