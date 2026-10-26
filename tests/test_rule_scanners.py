"""Run the bundled scanner scripts against disposable host directories."""

import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

SCRIPTS = Path(__file__).resolve().parents[1] / 'plugins/agent-toolkit/skills/rules-distill/scripts'


@unittest.skipUnless(shutil.which('bash') and shutil.which('jq'), 'Bash and jq required')
class RuleScannerTest(unittest.TestCase):
    def run_script(self, name, *args, env=None, expected=0):
        clean = {key: value for key, value in os.environ.items() if not key.startswith('RULES_DISTILL_')}
        clean.update(env or {})
        result = subprocess.run(['bash', str(SCRIPTS / name), *map(str, args)],
                                env=clean, capture_output=True, text=True)
        self.assertEqual(result.returncode, expected, result.stderr)
        return result

    def test_both_host_skill_directories_and_environment_overrides(self):
        with tempfile.TemporaryDirectory(prefix='shared skills ') as temporary:
            root = Path(temporary)
            project = root / '.agents/skills'
            global_dir = root / '.claude/skills'
            for directory, name in ((project, 'project-example'), (global_dir, 'global-example')):
                skill = directory / name / 'SKILL.md'
                skill.parent.mkdir(parents=True)
                skill.touch()
            # Use a real JSON-quoted YAML scalar, including escapes and Unicode.
            for skill in root.rglob('SKILL.md'):
                name = skill.parent.name
                skill.write_text(f'---\nname: {name}\ndescription: '+json.dumps('Handle "quoted" paths — safely')+'\n---\n\nBody\n')
            result = self.run_script('scan-skills.sh', project, global_dir)
            data = json.loads(result.stdout)
            self.assertEqual(data['scan_summary']['project']['count'], 1)
            self.assertEqual(data['scan_summary']['global']['count'], 1)
            self.assertEqual({item['name'] for item in data['skills']}, {'project-example', 'global-example'})
            self.assertTrue(all(item['description'] == 'Handle "quoted" paths — safely' for item in data['skills']))
            overridden = self.run_script('scan-skills.sh', root / 'absent', root / 'absent',
                                         env={'RULES_DISTILL_PROJECT_DIR': str(project), 'RULES_DISTILL_GLOBAL_DIR': str(global_dir)})
            self.assertEqual(json.loads(overridden.stdout), data)
            missing = json.loads(self.run_script('scan-skills.sh', root / 'absent', root / 'absent').stdout)
            self.assertEqual(missing['skills'], [])

    def test_rules_directory_instruction_file_empty_and_missing(self):
        with tempfile.TemporaryDirectory(prefix='shared rules ') as temporary:
            root = Path(temporary)
            directory = root / '.claude/rules'
            directory.mkdir(parents=True)
            (directory / 'conventions.md').write_text('# Rules\n\n## Testing\nRun tests\n')
            (directory / '_archived').mkdir()
            (directory / '_archived/old.md').write_text('## Obsolete\n')
            result = json.loads(self.run_script('scan-rules.sh', directory).stdout)
            self.assertEqual(result['total'], 1)
            self.assertEqual(result['rules'][0]['headings'], ['Testing'])
            self.assertEqual(result['rules'][0]['path'], str(directory / 'conventions.md'))
            instruction = root / 'AGENTS.md'
            instruction.write_text('# Instructions\n\n## Code review\nReview changes\n')
            result = json.loads(self.run_script('scan-rules.sh', instruction).stdout)
            self.assertEqual(result['total'], 1)
            self.assertEqual(result['rules'][0]['file'], 'AGENTS.md')
            empty = root / 'empty'
            empty.mkdir()
            self.assertEqual(json.loads(self.run_script('scan-rules.sh', empty).stdout)['rules'], [])
            missing = self.run_script('scan-rules.sh', root / 'missing', expected=1)
            self.assertIn('rules source not found', json.loads(missing.stderr)['error'])


if __name__ == '__main__':
    unittest.main()
