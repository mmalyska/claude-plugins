"""Optional maintainer checks; installing plugins needs no Python dependency."""

import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]


def frontmatter(path):
    text = path.read_text()
    if not text.startswith('---\n'):
        raise AssertionError(f'Missing frontmatter: {path}')
    header, body = text[4:].split('\n---\n', 1)
    fields = {}
    for line in header.splitlines():
        if line and not line[0].isspace():
            key, value = line.split(':', 1)
            fields[key] = value.strip()
    return fields, body


def links(text):
    """Ignore Markdown examples inside fenced code blocks."""
    fence = None
    lines = []
    for line in text.splitlines():
        match = re.match(r'^\s*(`{3,}|~{3,})', line)
        if match:
            marker = match[1]
            if fence is None:
                fence = marker
            elif marker[0] == fence[0] and len(marker) >= len(fence):
                fence = None
            continue
        if fence is None:
            lines.append(line)
    return re.findall(r'\]\(([^)\n]+)\)', '\n'.join(lines))


class SharedPluginTest(unittest.TestCase):
    def test_shared_skill_discovery_and_metadata(self):
        catalog = json.loads((ROOT / '.claude-plugin/marketplace.json').read_text())
        names = set()
        for entry in catalog['plugins']:
            plugin = ROOT / entry['source']
            with self.subTest(plugin=entry['name']):
                claude = json.loads((plugin / '.claude-plugin/plugin.json').read_text())
                codex = json.loads((plugin / '.codex-plugin/plugin.json').read_text())
                for key in ('name', 'version'):
                    self.assertEqual(codex[key], claude[key])
                self.assertEqual(codex['hooks'], [])
                self.assertFalse((plugin / 'codex-skills').exists())
                if entry['name'] == 'android':
                    self.assertNotIn('skills', codex)
                    continue
                self.assertEqual(codex['skills'], './skills/')
                skills = list((plugin / 'skills').glob('*/SKILL.md'))
                self.assertTrue(skills)
                for skill in skills:
                    fields, _ = frontmatter(skill)
                    self.assertRegex(fields['name'], r'^[a-z0-9]+(?:-[a-z0-9]+)*$')
                    self.assertLessEqual(len(fields['name']), 64)
                    self.assertEqual(fields['name'], skill.parent.name)
                    self.assertNotIn(fields['name'], names)
                    names.add(fields['name'])
                    raw = fields['description']
                    description = json.loads(raw) if raw.startswith('"') else raw
                    self.assertIsInstance(description, str)
                    self.assertTrue(description.strip())
                    self.assertLessEqual(len(description), 1024)
                    self.assertFalse(set(fields) - {'name', 'description', 'metadata'})

    def test_entrypoints_and_references_remain_inside_installed_plugin(self):
        for plugin in (ROOT / 'plugins').iterdir():
            resolved = plugin.resolve()
            referenced = set()
            documents = list(plugin.glob('skills/**/*.md'))
            documents += list(plugin.glob('commands/*.md')) + list(plugin.glob('agents/*.md'))
            documents += list(plugin.glob('rules/**/*.md'))
            for document in documents:
                for relative in links(document.read_text()):
                    relative = relative.strip('<>')
                    if relative.startswith(('#', '/', 'mailto:')) or '://' in relative:
                        continue
                    target = (document.parent / relative.split('#')[0]).resolve()
                    with self.subTest(source=document, link=relative):
                        self.assertTrue(target.is_relative_to(resolved))
                        self.assertTrue(target.is_file(), target)
                    referenced.add(target)
            for entrypoint in list(plugin.glob('commands/*.md')) + list(plugin.glob('agents/*.md')):
                expected = plugin / 'skills' / entrypoint.stem / 'SKILL.md'
                self.assertIn(expected.resolve(), referenced)
                self.assertIn(f'../skills/{entrypoint.stem}/SKILL.md', entrypoint.read_text())
            for rule in plugin.glob('rules/**/*.md'):
                self.assertIn(rule.resolve(), referenced)

    def test_personal_setup_contains_both_host_installations(self):
        catalog = json.loads((ROOT / '.claude-plugin/marketplace.json').read_text())
        setup = (ROOT / 'plugins/personal-essentials/skills/personal-setup/SKILL.md').read_text()
        for entry in catalog['plugins']:
            if entry['name'] not in ('personal-essentials', 'android'):
                selector = f"{entry['name']}@{catalog['name']}"
                self.assertIn(f'codex plugin add {selector}', setup)
                self.assertIn(f'claude plugin install {selector}', setup)


if __name__ == '__main__':
    unittest.main()
