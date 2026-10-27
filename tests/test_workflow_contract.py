"""Static checks for packaged workflow guidance, not a policy execution engine.

Negative samples mutate the actual document so a newly unreachable contract,
missing stage/default or deleted authorization boundary cannot silently pass.
These checks do not establish live harness behavior or independent review.
"""

from pathlib import Path
import re
import unittest

from test_codex_manifests import links

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / 'plugins/development-lifecycle'
CONTRACT = PLUGIN / 'rules/common/workflow.md'
STAGES = ('Spec', 'Plan', 'Build', 'Test', 'Review', 'Simplify', 'Ship')
TOPOLOGIES = ('SOLO', 'HANDOFF', 'PARALLEL', 'REVIEW')
SECTIONS = (
    'Lifecycle', 'Selection and defaults', 'Execution profiles',
    'Execution topologies', 'Authorization and capabilities',
    'Safety and worktree-first', 'Artifacts and evidence',
    'Stage and delivery boundaries', 'Loading and host limitations',
)


def sections(document):
    """Read level-two sections of this Markdown document, without executing it."""
    parts = re.split(r'^## (.+)\n', document, flags=re.MULTILINE)
    return dict(zip(parts[1::2], parts[2::2]))


def table_rows(section):
    return [tuple(cell.strip() for cell in line.strip('|').split('|'))
            for line in section.splitlines() if line.startswith('|')]


def contract_errors(document):
    """Check the reviewable document shape and critical declarative boundaries."""
    content = sections(document)
    errors = {f'section:{name}' for name in SECTIONS
              if not content.get(name, '').strip()}
    lifecycle = re.findall(r'^Spec → .+$', content.get('Lifecycle', ''), re.MULTILINE)
    if lifecycle != [' → '.join(STAGES)]:
        errors.add('lifecycle')

    defaults = content.get('Selection and defaults', '')
    if not re.search(r'^defaults:\n  profile: standard\n  topology: solo$',
                     defaults, re.MULTILINE):
        errors.add('defaults')
    for name, expected, width in (
        ('Execution profiles', STAGES, 4),
        ('Execution topologies', TOPOLOGIES, 2),
    ):
        rows = table_rows(content.get(name, ''))
        data = rows[2:]  # header and separator
        if tuple(row[0] for row in data) != expected:
            errors.add(f'table:{name}')
        if not data or any(len(row) != width or not all(row) for row in data):
            errors.add(f'cells:{name}')
    profile_rows = table_rows(content.get('Execution profiles', ''))
    if not profile_rows or profile_rows[0] != ('Stage', 'QUICK', 'STANDARD', 'DEEP'):
        errors.add('profiles')

    # Key authority declarations must survive refactors of surrounding examples.
    boundaries = {
        'topology-authorization': (
            'Authorization and capabilities',
            'HANDOFF, PARALLEL and REVIEW require explicit user authorization'),
        'authority-before-capability': (
            'Authorization and capabilities', 'Check authority before capability.'),
        'isolation': (
            'Safety and worktree-first',
            'never silently fall back to editing primary'),
        'stage-scope': (
            'Stage and delivery boundaries', 'Stop after the requested stage;'),
        'runtime-permission': (
            'Stage and delivery boundaries',
            'Runtime and destructive mutations need separate fresh explicit permission'),
        'loading-limit': (
            'Loading and host limitations', 'Rules load on demand.'),
    }
    for code, (section, declaration) in boundaries.items():
        if declaration not in ' '.join(content.get(section, '').split()):
            errors.add(code)
    return errors


class WorkflowContractTest(unittest.TestCase):
    def setUp(self):
        self.document = CONTRACT.read_text()

    def test_packaged_contract_structure_and_boundaries(self):
        self.assertEqual(contract_errors(self.document), set())

    def test_missing_or_invalid_contract_data_is_detected(self):
        cases = [
            ('missing stage', self.document.replace('Build → ', '', 1), 'lifecycle'),
            ('reordered stages', self.document.replace('Build → Test', 'Test → Build', 1),
             'lifecycle'),
            ('missing profile default', self.document.replace('  profile: standard\n', '', 1),
             'defaults'),
            ('missing topology default', self.document.replace('  topology: solo\n', '', 1),
             'defaults'),
            ('non-solo default', self.document.replace('  topology: solo', '  topology: parallel', 1),
             'defaults'),
            ('missing profile', self.document.replace('| QUICK | STANDARD | DEEP |',
                                                       '| QUICK | STANDARD |', 1), 'profiles'),
            ('missing profile stage', re.sub(r'^\| Plan \|.*\n', '', self.document,
                                             count=1, flags=re.MULTILINE),
             'table:Execution profiles'),
            ('missing topology', re.sub(r'^\| HANDOFF \|.*\n', '', self.document,
                                        count=1, flags=re.MULTILINE),
             'table:Execution topologies'),
            ('empty profile cell', self.document.replace('Session goal, scope and success', '', 1),
             'cells:Execution profiles'),
            ('missing authorization', self.document.replace('explicit user authorization',
                                                            'implicit approval', 1),
             'topology-authorization'),
            ('missing stage boundary', self.document.replace('Stop after\nthe requested stage;',
                                                             'Continue automatically;', 1),
             'stage-scope'),
            ('empty document', '', 'section:Lifecycle'),
        ]
        for name, sample, expected in cases:
            with self.subTest(case=name):
                self.assertNotEqual(sample, self.document)
                self.assertIn(expected, contract_errors(sample))

    def test_each_required_section_is_checked(self):
        for name in SECTIONS:
            with self.subTest(section=name):
                sample = re.sub(r'^## ' + re.escape(name) + r'\n.*?(?=^## |\Z)', '',
                                self.document, count=1, flags=re.MULTILINE | re.DOTALL)
                self.assertIn(f'section:{name}', contract_errors(sample))

    def test_existing_rule_skill_reaches_plugin_local_contract(self):
        index = PLUGIN / 'skills/development-lifecycle-rules/SKILL.md'
        targets = [(index.parent / link.split('#')[0]).resolve()
                   for link in links(index.read_text()) if '://' not in link]
        self.assertIn(CONTRACT.resolve(), targets)
        for target in targets:
            with self.subTest(target=target):
                self.assertTrue(target.is_relative_to(PLUGIN.resolve()))
                self.assertTrue(target.is_file())
        self.assertIn('Read [the workflow contract]', index.read_text())
        # No speculative Plan/Build entrypoints are introduced.
        for kind, suffix in (('skills', '/SKILL.md'), ('commands', '.md')):
            for name in ('plan', 'build'):
                self.assertFalse((PLUGIN / kind / (name + suffix)).exists())

    def test_readme_summaries_point_to_the_contract_and_disclose_increment(self):
        for document in (ROOT / 'README.md', PLUGIN / 'README.md'):
            with self.subTest(document=document):
                targets = [(document.parent / link.split('#')[0]).resolve()
                           for link in links(document.read_text()) if '://' not in link]
                self.assertIn(CONTRACT.resolve(), targets)
        readme = (PLUGIN / 'README.md').read_text()
        self.assertIn('STANDARD + SOLO', readme)
        self.assertIn('T03–T08', readme)
        self.assertIn('full workflow conformance is not claimed yet',
                      ' '.join(readme.split()))


if __name__ == '__main__':
    unittest.main()
