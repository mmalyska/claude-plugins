"""Offline content and standalone-reference guarantees for context optimization."""
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import shutil
import tempfile
import unittest

from test_codex_manifests import plugin_link_errors

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / 'tests/fixtures/context-layout/manifest.json'


def digest(text):
    return hashlib.sha256(text.encode()).hexdigest()


def example_hashes(text):
    blocks, block, fence = [], [], None
    for line in text.splitlines(keepends=True):
        mark = re.match(r'^\s*(`{3,}|~{3,})', line)
        if fence:
            if mark and mark[1][0] == fence[0] and len(mark[1]) >= len(fence):
                blocks.append(digest(''.join(block)))
                block, fence = [], None
            else:
                block.append(line)
        elif mark:
            fence = mark[1]
    return Counter(blocks)


def preservation_errors(root, manifest):
    errors = []
    for relative, record in manifest['skills'].items():
        path = root / relative
        actual = example_hashes(path.read_text())
        for reference in record['references']:
            actual.update(example_hashes((root / reference).read_text()))
        expected = Counter(record['example_hashes'])
        for revision in record.get('example_revisions', []):
            expected[revision['before']] -= 1
            expected[revision['after']] += 1
        missing = expected - actual
        if missing:
            errors.append(('missing-example', relative))
    for section in manifest['relocated_sections']:
        text = (root / section['destination']).read_text()
        start = text.find(section['prefix'])
        if start < 0 or digest(text[start:start + section['characters']]) != section['sha256']:
            errors.append(('changed-relocated-section', section['destination']))
    return errors


def selected_section(text, title):
    headings, fence, offset = [], None, 0
    for line in text.splitlines(keepends=True):
        mark = re.match(r'^\s*(`{3,}|~{3,})', line)
        if fence:
            if mark and mark[1][0] == fence[0] and len(mark[1]) >= len(fence):
                fence = None
        elif mark:
            fence = mark[1]
        else:
            match = re.match(r'^(#{1,6}) (.+?)\s*$', line)
            if match:
                headings.append((offset, len(match[1]), match[2]))
        offset += len(line)
    index = next(i for i, item in enumerate(headings) if item[2] == title)
    start, level, _ = headings[index]
    end = next((item[0] for item in headings[index + 1:] if item[1] <= level), len(text))
    return text[start:end]


class ContextLayoutTest(unittest.TestCase):
    def setUp(self):
        self.manifest = json.loads(MANIFEST.read_text())

    def test_original_examples_and_relocated_sections_survive(self):
        self.assertEqual(preservation_errors(ROOT, self.manifest), [])

    def test_core_policies_and_guard_bytes_are_unchanged(self):
        for relative, expected in self.manifest['protected_files'].items():
            self.assertEqual(digest((ROOT / relative).read_text()), expected, relative)

    def test_single_topic_reads_are_smaller_and_do_not_read_all_references(self):
        for case in self.manifest['read_sets']:
            record = self.manifest['skills'][case['skill']]
            paths = case['paths']
            cost = sum(len(selected_section((ROOT / p).read_text(), case['sections'][p]))
                       if p in case.get('sections', {}) else len((ROOT / p).read_text())
                       for p in paths)
            self.assertLess(cost, record['baseline_characters'], case['name'])
            if len(record['references']) > 1:
                self.assertLess(len(set(paths) & set(record['references'])),
                                len(record['references']), case['name'])

    def test_references_work_in_standalone_install_path_with_spaces(self):
        owners = {Path(p).parts[1] for p, item in self.manifest['skills'].items()
                  if item['references']}
        with tempfile.TemporaryDirectory(prefix='context layout ') as temporary:
            for owner in owners:
                plugin = Path(temporary) / owner
                shutil.copytree(ROOT / 'plugins' / owner, plugin)
                for document in plugin.rglob('*.md'):
                    self.assertEqual(plugin_link_errors(document, plugin), [], str(document))

    def test_deleted_example_is_rejected(self):
        with tempfile.TemporaryDirectory(prefix='context missing example ') as temporary:
            root = Path(temporary)
            (root / 'sample.md').write_text('# Sample\n')
            fixture = {'skills': {'sample.md': {'references': [],
                       'example_hashes': {digest('required example\n'): 1}}},
                       'relocated_sections': []}
            self.assertIn(('missing-example', 'sample.md'), preservation_errors(root, fixture))

    def test_missing_and_escaping_reference_is_rejected(self):
        with tempfile.TemporaryDirectory(prefix='context broken pointer ') as temporary:
            root = Path(temporary)
            path = root / 'SKILL.md'
            path.write_text('[missing](references/missing.md)\n[escape](../outside.md)\n')
            errors = plugin_link_errors(path, root)
            self.assertIn(('missing-target', 'references/missing.md'), errors)
            self.assertIn(('outside-plugin', '../outside.md'), errors)

    def test_section_selection_does_not_load_neighboring_topics(self):
        text = '# Reference\n\n## First\nneeded\n\n## Second\nunrelated\n'
        self.assertEqual(selected_section(text, 'First'), '## First\nneeded\n\n')
