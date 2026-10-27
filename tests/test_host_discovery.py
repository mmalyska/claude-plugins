"""Opt-in native CLI checks; temporary host configuration, no model turns.

WORKFLOW_NATIVE_TESTS=1 is required in addition to the target CLI. A session that
forbids other harness processes must leave these checks NOT RUN. Source/metadata
checks alone never satisfy this native gate.
"""

import json
import os
from pathlib import Path
import queue
import shutil
import subprocess
import tempfile
import threading
import time
import unittest

from test_codex_manifests import FROZEN_T01_CATALOG, FROZEN_T01_SKILLS, FROZEN_T01_WRAPPERS, plugin_link_errors

ROOT = Path(__file__).resolve().parents[1]
NATIVE_ENABLED = os.environ.get('WORKFLOW_NATIVE_TESTS') == '1'
OWNERS = ('development-lifecycle', 'git-workflows', 'agent-toolkit')
OWNER_CASES = tuple((name,) for name in OWNERS) + (OWNERS,)
MARKETPLACE = 'mmalyska-claude-plugins'


class HostDiscoveryTest(unittest.TestCase):
    def cli(self, host, arguments, environment, workspace):
        result = subprocess.run([host, *arguments], env=environment, cwd=workspace,
                                capture_output=True, text=True, timeout=30)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return result.stdout

    def assert_installed_content(self, name, installed):
        source = ROOT / FROZEN_T01_CATALOG[name]
        self.assertTrue(installed.is_dir(), installed)
        expected = {identity: installed / Path(path).relative_to(f'plugins/{name}')
                    for identity, path in FROZEN_T01_SKILLS.items()
                    if identity.startswith(f'{name}:')}
        actual = {f'{name}:{path.parent.name}': path
                  for path in installed.glob('skills/*/SKILL.md')}
        self.assertEqual(actual, expected)
        for identity, path in expected.items():
            self.assertEqual(path.read_bytes(), (ROOT / FROZEN_T01_SKILLS[identity]).read_bytes())
        expected_wrappers = {path: target for path, target in FROZEN_T01_WRAPPERS.items()
                             if path.startswith(f'plugins/{name}/')}
        actual_wrappers = {str(Path(f'plugins/{name}') / path.relative_to(installed))
                           for kind in ('commands', 'agents')
                           for path in (installed / kind).glob('*.md')}
        self.assertEqual(actual_wrappers, set(expected_wrappers))
        for path, target in expected_wrappers.items():
            relative = Path(path).relative_to(f'plugins/{name}')
            self.assertEqual((installed / relative).read_bytes(), (ROOT / path).read_bytes())
            self.assertTrue((installed / Path(target).relative_to(f'plugins/{name}')).is_file())
        for kind in ('rules', 'resources'):
            expected_files = {path.relative_to(source) for path in source.glob(f'{kind}/**/*.md')}
            actual_files = {path.relative_to(installed) for path in installed.glob(f'{kind}/**/*.md')}
            self.assertEqual(actual_files, expected_files)
            for relative in expected_files:
                self.assertEqual((installed / relative).read_bytes(), (source / relative).read_bytes())
        for kind in ('skills', 'commands', 'agents', 'rules', 'resources'):
            for document in installed.glob(f'{kind}/**/*.md'):
                self.assertEqual(plugin_link_errors(document, installed), [])
        for host in ('.claude-plugin', '.codex-plugin'):
            manifest = json.loads((installed / host / 'plugin.json').read_text())
            self.assertEqual(manifest, json.loads((source / host / 'plugin.json').read_text()))
        return {identity: str(path) for identity, path in expected.items()}

    @unittest.skipUnless(NATIVE_ENABLED and shutil.which('claude'),
                         'NOT RUN: opt in with WORKFLOW_NATIVE_TESTS=1 and install Claude CLI')
    def test_claude_accepts_marketplace_and_plugin_contents(self):
        catalog = json.loads((ROOT / '.claude-plugin/marketplace.json').read_text())
        with tempfile.TemporaryDirectory(prefix='claude-validation-') as temporary:
            environment = dict(os.environ, CLAUDE_CONFIG_DIR=str(Path(temporary) / 'config'))
            for path in [ROOT, *(ROOT / entry['source'] for entry in catalog['plugins'])]:
                with self.subTest(path=path):
                    output = self.cli('claude', ['plugin', 'validate', str(path), '--json'],
                                      environment, temporary)
                    self.assertTrue(json.loads(output)['success'])

    @unittest.skipUnless(NATIVE_ENABLED and shutil.which('claude'),
                         'NOT RUN: opt in with WORKFLOW_NATIVE_TESTS=1 and install Claude CLI')
    def test_claude_installs_owners_without_external_workflow_provider(self):
        # CLI/config contracts: https://code.claude.com/docs/en/plugins/cli-reference
        # and https://code.claude.com/docs/en/settings (CLAUDE_CONFIG_DIR).
        for selected in OWNER_CASES:
            with self.subTest(plugins=selected), tempfile.TemporaryDirectory(prefix='claude-owners-') as temporary:
                root = Path(temporary)
                workspace = root / 'workspace'
                workspace.mkdir()
                environment = dict(os.environ, CLAUDE_CONFIG_DIR=str(root / 'config'))
                self.cli('claude', ['plugin', 'marketplace', 'add', str(ROOT)], environment, workspace)
                for name in selected:
                    self.cli('claude', ['plugin', 'install', f'{name}@{MARKETPLACE}', '--scope', 'user'],
                             environment, workspace)
                records = json.loads(self.cli('claude', ['plugin', 'list', '--json'], environment, workspace))
                self.assertIsInstance(records, list)
                self.assertEqual({item['id'] for item in records},
                                 {f'{name}@{MARKETPLACE}' for name in selected})
                for item in records:
                    self.assertTrue(item['enabled'])
                    self.assertFalse(item.get('errors'), item.get('errors'))
                    name = item['id'].split('@', 1)[0]
                    installed = Path(item.get('readFromFolder') or item['installPath'])
                    self.assertTrue(installed.resolve().is_relative_to(root.resolve()) or
                                    installed.resolve() == (ROOT / FROZEN_T01_CATALOG[name]).resolve())
                    self.assert_installed_content(name, installed)

    def codex_skill_list(self, environment, workspace):
        """Use only metadata RPCs; never issue a turn/model/delegation request."""
        with tempfile.TemporaryFile(mode='w+') as log:
            process = subprocess.Popen(['codex', 'app-server', '--stdio'], env=environment,
                                       cwd=workspace, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                       stderr=log, text=True)
            messages = queue.Queue()

            def read_messages():
                for line in process.stdout:
                    try:
                        messages.put(json.loads(line))
                    except ValueError:
                        continue

            reader = threading.Thread(target=read_messages, daemon=True)
            reader.start()

            def request(method, params, identifier):
                process.stdin.write(json.dumps({'jsonrpc': '2.0', 'id': identifier,
                                                'method': method, 'params': params}) + '\n')
                process.stdin.flush()
                deadline = time.monotonic() + 25
                while time.monotonic() < deadline:
                    message = messages.get(timeout=max(0.01, deadline - time.monotonic()))
                    if message.get('id') == identifier:
                        self.assertNotIn('error', message, message)
                        return message['result']
                self.fail(f'No response to metadata RPC {method}')

            try:
                request('initialize', {'clientInfo': {'name': 'shared-workflow-check', 'version': '1.0.0'},
                                       'capabilities': {'experimentalApi': True}}, 1)
                process.stdin.write('{"jsonrpc":"2.0","method":"initialized"}\n')
                process.stdin.flush()
                return request('skills/list', {'cwds': [str(workspace)], 'forceReload': True}, 2)
            finally:
                process.terminate()
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait(timeout=5)
                process.stdin.close()
                reader.join(timeout=2)
                process.stdout.close()

    @unittest.skipUnless(NATIVE_ENABLED and shutil.which('codex'),
                         'NOT RUN: opt in with WORKFLOW_NATIVE_TESTS=1 and install Codex CLI')
    def test_codex_discovers_shared_skills_after_direct_install(self):
        for selected in (*OWNER_CASES, tuple(FROZEN_T01_CATALOG)):
            with self.subTest(plugins=selected), tempfile.TemporaryDirectory(prefix='codex-owners-') as temporary:
                root = Path(temporary)
                workspace = root / 'workspace'
                workspace.mkdir()
                environment = dict(os.environ, CODEX_HOME=str(root / 'config'))
                self.cli('codex', ['plugin', 'marketplace', 'add', str(ROOT)], environment, workspace)
                expected = {}
                for name in selected:
                    output = self.cli('codex', ['plugin', 'add', f'{name}@{MARKETPLACE}', '--json'],
                                      environment, workspace)
                    installed = Path(json.loads(output)['installedPath'])
                    self.assertTrue(installed.resolve().is_relative_to(root.resolve()) or
                                    installed.resolve() == (ROOT / FROZEN_T01_CATALOG[name]).resolve())
                    expected.update(self.assert_installed_content(name, installed))
                actual = {}
                result = self.codex_skill_list(environment, workspace)
                for item in result['data']:
                    self.assertFalse(item.get('errors'), item.get('errors'))
                    for skill in item['skills']:
                        self.assertNotIn('superpowers:', skill['name'].lower())
                        if any(skill['name'].startswith(f'{name}:') for name in selected):
                            self.assertTrue(skill['enabled'])
                            actual[skill['name']] = skill['path']
                self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
