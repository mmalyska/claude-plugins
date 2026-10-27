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


# Explicit T03 audit scope; do not scan history or treat domain confidence
# percentages and project-specific coverage targets as global testing policy.
PROFILE_SKILLS = (
    'spec', 'architect', 'ai-regression-testing', 'test', 'tdd-guide',
    'review', 'code-review', 'code-reviewer', 'simplify',
)
PROFILE_DOCUMENTS = tuple(
    f'plugins/development-lifecycle/skills/{name}/SKILL.md' for name in PROFILE_SKILLS
) + (
    'plugins/development-lifecycle/rules/common/testing.md',
    'plugins/development-lifecycle/rules/common/code-review.md',
    'plugins/development-lifecycle/rules/common/patterns.md',
    'plugins/development-lifecycle/rules/common/performance.md',
    'plugins/git-workflows/rules/development-workflow.md',
    'plugins/agent-toolkit/skills/search-first/SKILL.md',
    'plugins/agent-toolkit/skills/verification-loop/SKILL.md',
)
PROJECT_GATE_DOCUMENTS = (
    'plugins/development-lifecycle/rules/common/testing.md',
    'plugins/development-lifecycle/rules/common/code-review.md',
    'plugins/development-lifecycle/skills/tdd-guide/SKILL.md',
    'plugins/agent-toolkit/skills/verification-loop/SKILL.md',
)


def active_prose(document):
    """Ignore frontmatter and fenced examples/history, keeping actual guidance."""
    if document.startswith('---\n'):
        document = document.split('\n---\n', 1)[1]
    output = []
    fence = None
    for line in document.splitlines():
        marker = re.match(r'^\s*(`{3,}|~{3,})', line)
        if marker:
            if fence is None:
                fence = marker[1]
            elif marker[1][0] == fence[0] and len(marker[1]) >= len(fence):
                fence = None
            continue
        if fence is None:
            output.append(line)
    return ' '.join(' '.join(output).split())


def profile_instruction_errors(path, document):
    """Find concrete audited regressions, not every mention of mandatory policy."""
    prose = active_prose(document)
    errors = set()
    forbidden = {
        'universal-tdd': r'MANDATORY workflow:|ensures all code is developed test-first',
        'universal-test-types': r'Test Types \(ALL required\)',
        'global-coverage': r'Minimum Test Coverage: 80%|coverage meets 80% minimum',
        'research-sweep': r'mandatory before any new implementation',
        'planning-dossier': r'Generate planning docs before coding: PRD',
        'mandatory-specialist': r'STOP and use security-reviewer agent',
    }
    for code, pattern in forbidden.items():
        if re.search(pattern, prose, re.IGNORECASE):
            errors.add(code)
    if path in PROJECT_GATE_DOCUMENTS:
        if 'Mandatory project gates remain binding in every profile.' not in prose:
            errors.add('project-policy')
        if 'A failed required security or coverage gate blocks readiness.' not in prose:
            errors.add('project-failure')
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


class ProfileGuidanceTest(unittest.TestCase):
    def test_audited_procedures_have_no_universal_technique_requirements(self):
        for path in PROFILE_DOCUMENTS:
            with self.subTest(path=path):
                self.assertEqual(profile_instruction_errors(path, (ROOT / path).read_text()), set())

    def test_concrete_old_directives_are_rejected_outside_examples(self):
        cases = (
            ('MANDATORY workflow: write test first', 'universal-tdd'),
            ('Ensures all code is developed test-first', 'universal-tdd'),
            ('Test Types (ALL required): unit, integration, E2E', 'universal-test-types'),
            ('Minimum Test Coverage: 80%', 'global-coverage'),
            ('Test coverage meets 80% minimum', 'global-coverage'),
            ('Research (mandatory before any new implementation)', 'research-sweep'),
            ('Generate planning docs before coding: PRD, architecture', 'planning-dossier'),
            ('STOP and use security-reviewer agent when handling input', 'mandatory-specialist'),
        )
        for directive, expected in cases:
            with self.subTest(directive=directive):
                self.assertIn(expected, profile_instruction_errors('example.md', directive))
        allowed = ('Use project-required TDD for this component. '
                   'The project requires 95% coverage and no exposed secrets. '
                   'Only report findings when more than 80% confident.')
        self.assertEqual(profile_instruction_errors('example.md', allowed), set())
        fenced = '# Example\n\n```text\nMinimum Test Coverage: 80%\n```\n'
        self.assertEqual(profile_instruction_errors('example.md', fenced), set())

    def test_quick_cannot_delete_project_coverage_or_security_gates(self):
        for path in PROJECT_GATE_DOCUMENTS:
            document = (ROOT / path).read_text()
            for declaration, error in (
                ('Mandatory project gates remain binding in every profile.', 'project-policy'),
                ('A failed required security or coverage gate blocks readiness.', 'project-failure'),
            ):
                with self.subTest(path=path, gate=error):
                    # Normalize wrapping before mutation so the negative sample
                    # really removes an active declaration, not just an example.
                    self.assertIn(declaration, active_prose(document))
                    sample = active_prose(document).replace(declaration,
                                                            'QUICK may skip project gates.', 1)
                    self.assertIn(error, profile_instruction_errors(path, sample))

    def test_stage_procedures_link_the_single_packaged_contract(self):
        for name in PROFILE_SKILLS:
            source = PLUGIN / f'skills/{name}/SKILL.md'
            with self.subTest(skill=name):
                targets = [(source.parent / link.split('#')[0]).resolve()
                           for link in links(source.read_text()) if '://' not in link]
                self.assertIn(CONTRACT.resolve(), targets)
                self.assertNotIn('/spec →', source.read_text())
                self.assertNotIn('/spec → /plan', source.read_text())

    def test_review_scope_includes_unstaged_staged_and_untracked_work(self):
        for name in ('review', 'code-review'):
            text = (PLUGIN / f'skills/{name}/SKILL.md').read_text()
            with self.subTest(skill=name):
                for command in ('git diff --name-only', 'git diff --cached --name-only',
                                'git ls-files --others --exclude-standard'):
                    self.assertIn(command, text)
                self.assertNotIn('HEAD~1', text)
        review = (PLUGIN / 'skills/review/SKILL.md').read_text()
        self.assertLess(review.index('git diff --name-only'), review.index('git diff <base>...HEAD'))
        simplify = (PLUGIN / 'skills/simplify/SKILL.md').read_text()
        self.assertIn('../review/SKILL.md', simplify)
        self.assertIn('undo only that edit', simplify)
        self.assertNotIn('HEAD~1', simplify)

    def test_selected_tdd_keeps_reproducer_without_phantom_provider(self):
        text = (PLUGIN / 'skills/test/SKILL.md').read_text()
        for phrase in ('Feature Mode', 'Bug Fix Mode', 'RED', 'GREEN',
                       'python3 -B -m unittest discover -s tests', 'verification-only'):
            self.assertIn(phrase, text)
        api = (PLUGIN / 'skills/ai-regression-testing/SKILL.md').read_text()
        self.assertNotIn('Store this as `skills/bug-check/SKILL.md`', api)
        self.assertNotIn('/bug-check', api)
        self.assertIn('../test/SKILL.md', api)
        self.assertIn('../review/SKILL.md', api)
        role = (PLUGIN / 'skills/tdd-guide/SKILL.md').read_text()
        self.assertNotIn('skill: tdd-workflow', role)

    def test_review_does_not_fetch_tools_or_publish_by_pr_number(self):
        text = (PLUGIN / 'skills/code-review/SKILL.md').read_text()
        self.assertNotIn('npx tsc', text)
        self.assertIn('shared `AGENTS.md` first in either host', text)
        self.assertIn('Only publish when the current user request explicitly authorizes', text)
        self.assertLess(text.index('Only publish when'), text.index('gh pr review'))


if __name__ == '__main__':
    unittest.main()
