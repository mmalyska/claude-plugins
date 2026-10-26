"""Optional native CLI checks. All installs use disposable configuration."""

import json
import os
from pathlib import Path
import queue
import shutil
import subprocess
import tempfile
import threading
import unittest

ROOT = Path(__file__).resolve().parents[1]


class HostDiscoveryTest(unittest.TestCase):
    @unittest.skipUnless(shutil.which('claude'), 'Claude CLI not installed')
    def test_claude_accepts_marketplace_and_plugin_contents(self):
        catalog = json.loads((ROOT / '.claude-plugin/marketplace.json').read_text())
        for path in [ROOT, *(ROOT / entry['source'] for entry in catalog['plugins'])]:
            with self.subTest(path=path):
                result = subprocess.run(['claude', 'plugin', 'validate', str(path), '--json'],
                                        capture_output=True, text=True, timeout=30)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertTrue(json.loads(result.stdout)['success'])

    @unittest.skipUnless(shutil.which('codex'), 'Codex CLI not installed')
    def test_codex_discovers_shared_skills_after_direct_install(self):
        catalog = json.loads((ROOT / '.claude-plugin/marketplace.json').read_text())
        with tempfile.TemporaryDirectory(prefix='shared-plugin-check-') as temporary:
            env = dict(os.environ, CODEX_HOME=temporary)

            def cli(*args):
                result = subprocess.run(['codex', *args], env=env, capture_output=True,
                                        text=True, timeout=30)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                return result.stdout

            cli('plugin', 'marketplace', 'add', str(ROOT))
            expected = {}
            for entry in catalog['plugins']:
                result = json.loads(cli('plugin', 'add', f"{entry['name']}@{catalog['name']}", '--json'))
                installed = Path(result['installedPath'])
                for skill in installed.glob('skills/*/SKILL.md'):
                    expected[f"{entry['name']}:{skill.parent.name}"] = str(skill)

            with tempfile.TemporaryFile(mode='w+') as log:
                process = subprocess.Popen(['codex', 'app-server', '--stdio'], env=env,
                                           stdin=subprocess.PIPE, stdout=subprocess.PIPE,
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
                    while True:
                        message = messages.get(timeout=25)
                        if message.get('id') == identifier:
                            self.assertNotIn('error', message, message)
                            return message['result']

                try:
                    request('initialize', {'clientInfo': {'name': 'shared-workflow-check', 'version': '1.0.0'},
                                           'capabilities': {'experimentalApi': True}}, 1)
                    process.stdin.write('{"jsonrpc":"2.0","method":"initialized"}\n')
                    process.stdin.flush()
                    result = request('skills/list', {'cwds': [str(ROOT)], 'forceReload': True}, 2)
                    actual = {}
                    for item in result['data']:
                        for error in item.get('errors', []):
                            if str(error.get('path', '')).startswith(temporary):
                                self.fail(str(error))
                        for skill in item['skills']:
                            if skill['name'] in expected:
                                self.assertTrue(skill['enabled'])
                                actual[skill['name']] = skill['path']
                    self.assertEqual(actual, expected)
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


if __name__ == '__main__':
    unittest.main()
