"""Static checks for packaged workflow guidance, not a policy execution engine.

Negative samples mutate the actual document so a newly unreachable contract,
missing stage/default or deleted authorization boundary cannot silently pass.
These checks do not establish live harness behavior or independent review.
"""

from pathlib import Path
import hashlib
import json
import os
import shutil
import subprocess
import tempfile
import re
import unittest

from test_codex_manifests import frontmatter, links, plugin_link_errors, markdown_anchors

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
        'reasoned-solo-assessment': (
            'Authorization and capabilities',
            'A reasoned SOLO conclusion is valid; do not invent specialist work for a small task.'),
        'conditional-specialist-proposal': (
            'Authorization and capabilities',
            'If recommending specialists, describe bounded candidate scopes, expected benefit '
            'and any missing actor authorization as a proposal only.'),
        'unknown-topology-no-substitution': (
            'Selection and defaults',
            'Do not substitute SOLO merely because it is the only permitted topology;'),
        'gate-conflict-blocks-edits': (
            'Safety and worktree-first',
            'An unresolved conflict over a required project gate blocks dependent edits.'),
        'deep-plan-review-status': (
            'Execution profiles',
            'If the pass is incomplete, record NOT RUN and keep the plan draft/incomplete.'),
        'deep-plan-output-paths': (
            'Execution profiles',
            'A task that records a decision or findings must name the durable output path;'),
        'authority-before-capability': (
            'Authorization and capabilities', 'Check authority before capability.'),
        'isolation': (
            'Safety and worktree-first',
            'never silently fall back to editing primary'),
        'first-write-preflight': (
            'Safety and worktree-first',
            'Each actor verifies current Git state before its first write, including a handoff snapshot:'),
        'evidence-without-narration': (
            'Safety and worktree-first',
            'no separate completion note is required.'),
        'direct-project-check': (
            'Artifacts and evidence',
            'Use the exact project check directly when its tool result captures the runner status;'),
        'denied-preflight-unresolved': (
            'Safety and worktree-first',
            'A denied or unexecuted prerequisite check remains unresolved;'),
        'denied-preflight-stop': (
            'Safety and worktree-first',
            'stop dependent writes and report the blocker;'),
        'actual-primary': (
            'Safety and worktree-first', 'primary branch/HEAD and clean status;'),
        'full-initial-load': (
            'Loading and host limitations', 'Load the complete contract on first use'),
        'missing-guidance-stop': (
            'Loading and host limitations',
            'If required guidance is unavailable, stop dependent work'),
        'test-runner-status': (
            'Artifacts and evidence',
            "Capture the test runner's exit code before another command can overwrite it."),
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
            ('forced specialist work', self.document.replace(
                'A reasoned SOLO conclusion is valid; do not invent specialist work for a small task.',
                'Always propose specialist work, including for trivial tasks.', 1),
             'reasoned-solo-assessment'),
            ('unbounded specialist recommendation', self.document.replace(
                'If recommending specialists, describe bounded candidate scopes, expected benefit\n'
                'and any missing actor authorization as a proposal only.',
                'Recommend specialists without scope or authority details.', 1),
             'conditional-specialist-proposal'),
            ('missing stage boundary', self.document.replace('Stop after\nthe requested stage;',
                                                             'Continue automatically;', 1),
             'stage-scope'),
            ('missing first-write preflight', self.document.replace(
                'Each actor verifies current Git state before its first write, including a handoff\nsnapshot:',
                'Directory names establish isolation', 1), 'first-write-preflight'),
            ('mandatory narration replaces factual evidence', self.document.replace(
                'no\nseparate completion note is required.',
                'A separate completion note is mandatory.', 1), 'evidence-without-narration'),
            ('direct check preference removed', self.document.replace(
                'Use the exact project check directly when its tool result captures the runner\nstatus;',
                'Always wrap checks;', 1), 'direct-project-check'),
            ('denied prerequisite treated as complete', self.document.replace(
                'A denied or unexecuted prerequisite check remains unresolved;',
                'A denied prerequisite counts as complete;', 1),
             'denied-preflight-unresolved'),
            ('unresolved preflight allows edits', self.document.replace(
                'stop dependent writes and report the blocker;',
                'continue editing without the remaining facts;', 1),
             'denied-preflight-stop'),
            ('missing actual primary check', self.document.replace(
                'primary branch/HEAD\nand clean status;', 'assume primary is clean;', 1),
             'actual-primary'),
            ('missing full initial load', self.document.replace(
                'Load the complete contract on first use', 'Read a short excerpt', 1),
             'full-initial-load'),
            ('missing loading blocker', self.document.replace(
                'If required guidance is unavailable, stop dependent work',
                'Use an invented fallback', 1), 'missing-guidance-stop'),
            ('missing runner status', self.document.replace(
                "Capture the test runner's exit code before another command can overwrite it.",
                'Only inspect the last shell command.', 1), 'test-runner-status'),
            ('unknown topology normalization', self.document.replace(
                'Do not substitute SOLO merely because it is the only permitted topology;',
                'Choose SOLO automatically when it is the only permitted topology;', 1),
             'unknown-topology-no-substitution'),
            ('gate conflict deferred until verification', self.document.replace(
                'An unresolved conflict over a required project gate blocks dependent edits.',
                'Implement first and reconcile the required gate before shipping.', 1),
             'gate-conflict-blocks-edits'),
            ('plan review asserted without execution', self.document.replace(
                'If the pass is incomplete, record NOT RUN and keep the plan draft/incomplete.',
                'A review completion sentence is sufficient.', 1), 'deep-plan-review-status'),
            ('missing durable task output', self.document.replace(
                'A task that records a decision or\nfindings must name the durable output path;',
                'Task output locations may remain unspecified;', 1), 'deep-plan-output-paths'),
            ('empty document', '', 'section:Lifecycle'),
        ]
        for name, sample, expected in cases:
            with self.subTest(case=name):
                self.assertNotEqual(sample, self.document)
                self.assertIn(expected, contract_errors(sample))

    def test_documented_default_queries_distinguish_missing_ref_from_no_remote(self):
        section = WORKTREE_CREATION.read_text().split(
            '### Verify base without silently changing primary', 1)[1]
        commands = re.search(r'```sh\n(.*?)```', section, re.DOTALL)[1].strip().splitlines()
        self.assertEqual(commands, ['git symbolic-ref refs/remotes/origin/HEAD', 'git remote'])
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            subprocess.run(['git', 'init', '-b', 'main', str(root)],
                           check=True, capture_output=True)

            def observations():
                return [subprocess.run(command.split(), cwd=root, capture_output=True,
                                       text=True) for command in commands]

            absent_ref, no_remotes = observations()
            self.assertNotEqual(absent_ref.returncode, 0)
            self.assertEqual(no_remotes.returncode, 0)
            self.assertEqual(no_remotes.stdout, '')
            subprocess.run(['git', 'remote', 'add', 'origin', str(root / 'not-fetched')],
                           cwd=root, check=True)
            absent_ref, configured_remote = observations()
            self.assertNotEqual(absent_ref.returncode, 0)
            self.assertEqual(configured_remote.returncode, 0)
            self.assertEqual(configured_remote.stdout, 'origin\n')

    def test_documented_runner_status_survives_reporting_and_errexit(self):
        section = self.document.split('### Check exit status\n', 1)[1]
        example = re.search(r'```sh\n(.*?)\n```', section, re.DOTALL)[1]
        # Execute the documented pattern against actual passing/failing unittest
        # fixtures. printf succeeds in both cases; it must not mask a RED exit.
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            tests = root / 'tests'
            tests.mkdir()
            for expected in (0, 1):
                (tests / 'test_sample.py').write_text(
                    'import unittest\nclass Sample(unittest.TestCase):\n'
                    f'    def test_result(self): self.assertEqual({expected}, 0)\n')
                for errexit in (False, True):
                    with self.subTest(test_exit=expected, errexit=errexit):
                        arguments = ['sh', *(['-e'] if errexit else []), '-c', example]
                        result = subprocess.run(arguments, cwd=root, capture_output=True,
                                                text=True, timeout=15)
                        self.assertEqual(result.returncode, expected, result.stderr)
                        self.assertIn(f'unittest exit: {expected}', result.stdout)
                        self.assertIn('Ran 1 test', result.stderr)

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


# Frozen from the merged T03 baseline: native names/tools/models and domain
# checklist suffixes. Descriptions and role guards are the only T04 changes.
NATIVE_ROLE_METADATA = {'backend/database-reviewer': {'model': 'sonnet',
                               'name': 'database-reviewer',
                               'tools': '["Read", "Write", "Edit", "Bash", "Grep", "Glob"]'},
 'devcontainer/devcontainer-auditor': {},
 'development-lifecycle/architect': {'model': 'opus',
                                     'name': 'architect',
                                     'tools': '["Read", "Grep", "Glob"]'},
 'development-lifecycle/build-error-resolver': {'model': 'sonnet',
                                                'name': 'build-error-resolver',
                                                'tools': '["Read", "Write", "Edit", "Bash", '
                                                         '"Grep", "Glob"]'},
 'development-lifecycle/code-reviewer': {'model': 'sonnet',
                                         'name': 'code-reviewer',
                                         'tools': '["Read", "Grep", "Glob", "Bash"]'},
 'development-lifecycle/doc-updater': {'model': 'haiku',
                                       'name': 'doc-updater',
                                       'tools': '["Read", "Write", "Edit", "Bash", "Grep", '
                                                '"Glob"]'},
 'development-lifecycle/docs-lookup': {'model': 'sonnet',
                                       'name': 'docs-lookup',
                                       'tools': '["Read", "Grep", "Glob", "WebSearch", "WebFetch", '
                                                '"mcp__context7__resolve-library-id", '
                                                '"mcp__context7__query-docs"]'},
 'development-lifecycle/tdd-guide': {'model': 'sonnet',
                                     'name': 'tdd-guide',
                                     'tools': '["Read", "Write", "Edit", "Bash", "Grep"]'},
 'dotnet/csharp-reviewer': {'model': 'sonnet',
                            'name': 'csharp-reviewer',
                            'tools': '["Read", "Grep", "Glob", "Bash"]'},
 'renovate/renovate-auditor': {}}
DOMAIN_CHECKLIST_HASHES = {'backend/database-reviewer': '4ea928c83e3a2e8ce93a16b5f914b8ae3ed7bbf6dcc34be68c2fdb77dd66cdde',
 'devcontainer/devcontainer-auditor': 'e7ddf4b91e77822f9c5d4622323f9fc7825b7b8c348598533e78cf16fb04be5c',
 'dotnet/csharp-reviewer': '89f572e3598d37d6b31776399f7ee5340e8791208cd2b7fa6fd5a38b134f88e7',
 'renovate/renovate-auditor': 'd39418706bb4f5d7f3e7458095e127dec10d6b626d5de32c7cce4cb328560716'}


def role_authorization_errors(document):
    prose = active_prose(document)
    boundaries = {
        'local-default': 'Use this role locally by default (STANDARD + SOLO)',
        'role-not-actor': 'Naming a role does not authorize another actor.',
        'actor-authorization':
            'HANDOFF, PARALLEL and REVIEW require explicit user authorization before delegation.',
        'authority-before-capability': 'Check authority before exposed capability;',
        'model-scope': 'Keep the configured model and task/tool/permission limits.',
        'no-bypass': 'Never launch another CLI to bypass a restriction.',
        'shared-policy': '`AGENTS.md` first, then host adapters and project policy;',
        'policy-conflict': 'report conflicts and pause dependent actions until reconciled.',
    }
    return {code for code, declaration in boundaries.items() if declaration not in prose}


def security_response_errors(document):
    prose = active_prose(document)
    boundaries = {
        'assessment-without-reviewer':
            'agent does not waive assessment or mandatory gates.',
        'required-gates': 'A failed required security or coverage gate blocks readiness.',
        'rotation-authority':
            'Credential rotation requires separate fresh explicit authorization with impact and rollback.',
        'scope': 'Review-only is not remediation or delivery permission.',
        'policy-conflict': 'report conflicts and pause dependent actions until reconciled.',
    }
    return {code for code, declaration in boundaries.items() if declaration not in prose}


class RoleAuthorizationTest(unittest.TestCase):
    def test_native_metadata_and_entrypoint_mapping_preserved(self):
        for identity, expected in NATIVE_ROLE_METADATA.items():
            plugin, role = identity.split('/')
            native = ROOT / f'plugins/{plugin}/agents/{role}.md'
            shared = ROOT / f'plugins/{plugin}/skills/{role}/SKILL.md'
            with self.subTest(role=identity):
                fields, body = frontmatter(native)
                metadata = {key: value for key, value in fields.items() if key != 'description'}
                self.assertEqual(metadata, expected)
                shared_fields, _ = frontmatter(shared)
                self.assertEqual(shared_fields['name'], role)
                self.assertEqual(json.loads(fields['description']),
                                 json.loads(shared_fields['description']))
                self.assertEqual(body.strip(),
                                 f'Read [the shared {role} workflow](../skills/{role}/SKILL.md) '
                                 'and follow it for this task.')

    def test_descriptions_cannot_mandate_an_actor_or_universal_tdd(self):
        for identity in NATIVE_ROLE_METADATA:
            plugin, role = identity.split('/')
            for relative in (f'agents/{role}.md', f'skills/{role}/SKILL.md'):
                path = ROOT / f'plugins/{plugin}' / relative
                fields, _ = frontmatter(path)
                description = json.loads(fields['description'])
                with self.subTest(path=path):
                    self.assertNotRegex(description, r'(?i)proactiv|must be used|use immediately|80%')
                    self.assertIn('Apply locally by default;', description)
                    self.assertIn('explicit user authorization', description)

    def test_each_shared_role_has_direct_entry_guards(self):
        for identity in NATIVE_ROLE_METADATA:
            plugin, role = identity.split('/')
            path = ROOT / f'plugins/{plugin}/skills/{role}/SKILL.md'
            with self.subTest(role=identity):
                self.assertEqual(role_authorization_errors(path.read_text()), set())
                if plugin == 'development-lifecycle':
                    targets = [(path.parent / link.split('#')[0]).resolve()
                               for link in links(path.read_text()) if '://' not in link]
                    self.assertIn(CONTRACT.resolve(), targets)

    def test_domain_checklists_unchanged_and_no_new_provider_dependency(self):
        for identity, expected_hash in DOMAIN_CHECKLIST_HASHES.items():
            plugin, role = identity.split('/')
            text = (ROOT / f'plugins/{plugin}/skills/{role}/SKILL.md').read_text()
            with self.subTest(role=identity):
                checklist = text.split('pause dependent actions until reconciled.', 1)[1]
                self.assertEqual(hashlib.sha256(checklist.encode()).hexdigest(), expected_hash)
                self.assertNotIn('../../rules/common/workflow.md', text)

    def test_missing_authority_and_policy_conflict_are_detected(self):
        text = active_prose((PLUGIN / 'skills/architect/SKILL.md').read_text())
        cases = (
            ('Naming a role does not authorize another actor.', 'role-not-actor'),
            ('explicit user authorization before delegation.', 'actor-authorization'),
            ('Check authority before exposed capability;', 'authority-before-capability'),
            ('report conflicts and pause dependent actions until reconciled.', 'policy-conflict'),
        )
        for declaration, error in cases:
            with self.subTest(boundary=error):
                self.assertIn(declaration, text)
                sample = text.replace(declaration, 'Proceed without checking.', 1)
                self.assertIn(error, role_authorization_errors(sample))

    def test_security_response_does_not_depend_on_a_reviewer(self):
        path = PLUGIN / 'rules/common/security.md'
        text = path.read_text()
        self.assertEqual(security_response_errors(text), set())
        prose = active_prose(text)
        cases = (
            ('agent does not waive assessment or mandatory gates.', 'assessment-without-reviewer'),
            ('A failed required security or coverage gate blocks readiness.', 'required-gates'),
            ('Credential rotation requires separate fresh explicit authorization with impact and rollback.',
             'rotation-authority'),
            ('report conflicts and pause dependent actions until reconciled.', 'policy-conflict'),
        )
        for declaration, error in cases:
            with self.subTest(boundary=error):
                self.assertIn(declaration, prose)
                self.assertIn(error, security_response_errors(
                    prose.replace(declaration, 'Reviewer unavailable: skip security.', 1)))

    def test_common_agent_rule_gates_parallel_work_and_has_no_cli_bypass(self):
        prose = active_prose((PLUGIN / 'rules/common/agents.md').read_text())
        for declaration in (
            'HANDOFF, PARALLEL and REVIEW require explicit user authorization',
            'Parallel read-only work requires explicit topology authorization',
            'Never launch another CLI, worker or orchestrator to bypass a restriction.',
            'report conflicting instructions and pause dependent actions until reconciled;',
        ):
            self.assertIn(declaration.lower(), prose.lower())


GIT_PLUGIN = ROOT / 'plugins/git-workflows'
WORKTREE_CREATION = GIT_PLUGIN / 'skills/using-git-worktrees/SKILL.md'
WORKTREE_FINISH = GIT_PLUGIN / 'skills/finishing-a-development-branch/SKILL.md'
# Startup-preamble repair intentionally changes only the injector hash;
# guard behavior and other frozen hook files remain unchanged.
UNCHANGED_WORKTREE_HOOKS = {'guard-main-checkout.sh': 'af5510df0aa35479f8dfda41b21bffbdeffd93c31a28fa8c9f59660f445e8c51',
 'hooks.json': '501056f7d13da344b80ba6a49c687b9a45bb74ee8187eebbcd4d84827f4ff5bf',
 'inject-worktree-rule.sh': '302b8209043e5807a7a74050080b8659171edcf0ea38a09175788e91b28bf2c7',
 'test-guard.sh': '0259c27e6320a2494ab6660f119693b21644dbece528cadaff51aca5f2c0ee52'}


def isolation_creation_errors(document):
    prose = active_prose(document)
    required = {
        'denied-preflight': 'A denied preflight query is not a missing ref or a successful check.',
        'unverified-preflight-stop': 'If verification remains unavailable, stop dependent writes and report the blocker.',
        'blocked-writes': 'If worktree creation fails, stop writes and report the permission prerequisite.',
        'no-primary-fallback': 'Never silently fall back to editing primary.',
        'normal-permissions': 'Use normal host permission escalation only when available and within scope;',
        'preserve-primary': 'Do not switch a dirty or non-default primary merely to satisfy a postcondition.',
        'no-second-harness': 'Do not start a second CLI session to imitate a missing tool or bypass a restriction.',
        'procedural-invariant': 'A missing jq or failed-open hook does not waive this procedural invariant;',
    }
    errors = {code for code, declaration in required.items() if declaration not in prose}
    if re.search(r"(?i)you're working in the current directory instead|permission error on create.*?\| Work in place", prose):
        errors.add('unsafe-fallback')
    return errors


def isolation_finish_errors(document):
    prose = active_prose(document)
    required = {
        'path-not-owner': 'Directory location alone is not proof of cleanup ownership.',
        'owned-target-authority': 'Cleanup requires explicit authorization for the verified owned target.',
        'preserve-external': 'Preserve external, unknown or active worktrees.',
        'no-automatic-cleanup': 'Successful merge does not itself authorize deleting a worktree or branch.',
        'primary-readonly': 'do not restore primary by switching, stashing, resetting, cleaning or merging to hide it.',
        'dirty-primary': 'Dirty/non-default primary: report and preserve it.',
        'runtime-scope': 'separate fresh runtime permission with impact and rollback before mutation.',
    }
    errors = {code for code, declaration in required.items() if declaration not in prose}
    if re.search(r'(?i)we own cleanup|runs for.*all four options', prose):
        errors.add('unsafe-cleanup')
    return errors


class WorktreeIsolationTest(unittest.TestCase):
    def test_creation_stops_on_permission_failure_without_primary_edits(self):
        text = WORKTREE_CREATION.read_text()
        self.assertEqual(isolation_creation_errors(text), set())
        for command in ('git rev-parse --absolute-git-dir', 'git rev-parse --git-common-dir',
                        'git rev-parse --show-superproject-working-tree',
                        'git worktree list --porcelain', 'git pull --ff-only'):
            self.assertIn(command, text)
        for state in ('Submodule', 'Detached', 'Existing suitable linked worktree', 'verified-base'):
            self.assertIn(state.lower(), text.lower())
        self.assertIn('.git/info/exclude', text)

    def test_finishing_preserves_provenance_primary_and_delivery_scope(self):
        text = WORKTREE_FINISH.read_text()
        self.assertEqual(isolation_finish_errors(text), set())
        self.assertIn('pull --ff-only', text)
        self.assertIn('merge --ff-only', text)
        self.assertNotIn('git checkout', text)
        self.assertNotIn('git worktree prune', text)
        self.assertNotIn('git branch -D', text)
        self.assertIn('Do not force removal.', text)
        self.assertIn('including untracked files', text)
        self.assertIn('active consumers', text)

    def test_removed_unsafe_fallbacks_are_detected(self):
        text = active_prose(WORKTREE_CREATION.read_text())
        cases = (
            ('A denied preflight query is not a missing ref or a successful check.',
             'denied-preflight'),
            ('If verification remains unavailable, stop dependent writes and report the blocker.',
             'unverified-preflight-stop'),
            ('If worktree creation fails, stop writes and report the permission prerequisite.',
             'blocked-writes'),
            ('Never silently fall back to editing primary.', 'no-primary-fallback'),
            ('Do not switch a dirty or non-default primary merely to satisfy a postcondition.',
             'preserve-primary'),
        )
        for declaration, expected in cases:
            with self.subTest(boundary=expected):
                self.assertIn(declaration, text)
                self.assertIn(expected, isolation_creation_errors(text.replace(declaration, '', 1)))
        self.assertIn('unsafe-fallback', isolation_creation_errors(
            text + " If sandbox fails, you're working in the current directory instead."))

    def test_ownership_and_readonly_boundaries_cannot_disappear(self):
        text = active_prose(WORKTREE_FINISH.read_text())
        cases = (
            ('Directory location alone is not proof of cleanup ownership.', 'path-not-owner'),
            ('Cleanup requires explicit authorization for the verified owned target.',
             'owned-target-authority'),
            ('Preserve external, unknown or active worktrees.', 'preserve-external'),
            ('Successful merge does not itself authorize deleting a worktree or branch.',
             'no-automatic-cleanup'),
            ('do not restore primary by switching, stashing, resetting, cleaning or merging to hide it.',
             'primary-readonly'),
        )
        for declaration, expected in cases:
            with self.subTest(boundary=expected):
                self.assertIn(declaration, text)
                self.assertIn(expected, isolation_finish_errors(text.replace(declaration, '', 1)))
        self.assertIn('unsafe-cleanup', isolation_finish_errors(text + ' If under .worktrees/, we own cleanup.'))

    def test_actor_isolation_permissions_are_not_delegation_authority(self):
        text = active_prose((GIT_PLUGIN / 'rules/worktree-workflow.md').read_text())
        for declaration in (
            'HANDOFF, PARALLEL and REVIEW require explicit user authorization',
            'Distinct branch/worktree for each writer and a named integrator',
            'These are isolation rules, not delegation permission.',
            'A missing jq or failed-open hook removes technical enforcement, not procedural requirements.',
        ):
            self.assertIn(declaration, text)
        readme = (GIT_PLUGIN / 'README.md').read_text()
        self.assertIn('stop writes rather than silently edit primary', readme)
        self.assertNotIn('always leaves the primary checkout on the default branch', readme)
        self.assertNotIn('research → worktree → plan → TDD → review → commit', readme)

    def test_existing_hook_sources_and_fixtures_unchanged(self):
        for name, expected_hash in UNCHANGED_WORKTREE_HOOKS.items():
            with self.subTest(path=name):
                self.assertEqual(hashlib.sha256((GIT_PLUGIN / 'hooks' / name).read_bytes()).hexdigest(),
                                 expected_hash)


    @unittest.skipUnless(os.name == 'posix' and all(shutil.which(tool)
                         for tool in ('bash', 'git', 'cat', 'jq')),
                         'POSIX Bash, git, cat and jq required')
    def test_missing_jq_keeps_fail_open_hook_and_procedural_requirement(self):
        with tempfile.TemporaryDirectory(prefix='workflow-missing-jq-') as temporary:
            root = Path(temporary)
            repository = root / 'repo'
            result = subprocess.run(['git', 'init', '-q', '-b', 'main', str(repository)],
                                    text=True, capture_output=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json.dumps({'tool_name': 'Write', 'cwd': str(repository),
                                  'permission_mode': 'auto',
                                  'tool_input': {'file_path': str(repository / 'probe.txt')}})
            guard = GIT_PLUGIN / 'hooks/guard-main-checkout.sh'
            environment = dict(os.environ)
            environment.pop('CLAUDE_ALLOW_MAIN_EDITS', None)
            control = subprocess.run([shutil.which('bash'), str(guard)], input=payload,
                                     env=environment, text=True, capture_output=True)
            self.assertEqual(control.returncode, 0, control.stderr)
            self.assertEqual(json.loads(control.stdout)['hookSpecificOutput']['permissionDecision'],
                             'deny')
            tools = root / 'tools'
            tools.mkdir()
            for tool in ('cat', 'git'):
                (tools / tool).symlink_to(shutil.which(tool))
            environment['PATH'] = str(tools)  # Real cat/git, deliberately no jq.
            missing = subprocess.run([shutil.which('bash'), str(guard)], input=payload,
                                     env=environment, text=True, capture_output=True)
            self.assertEqual(missing.returncode, 0)
            self.assertEqual(missing.stdout, '')
            self.assertFalse((repository / 'probe.txt').exists())
            self.assertEqual(isolation_creation_errors(WORKTREE_CREATION.read_text()), set())


DELIVERY_POLICIES = (
    'plugins/development-lifecycle/skills/ship/SKILL.md',
    'plugins/development-lifecycle/skills/code-review/SKILL.md',
    'plugins/git-workflows/rules/git-workflow.md',
    'plugins/agent-toolkit/skills/safety-guard/SKILL.md',
)
DELIVERY_BOUNDARIES = {
    'readiness': 'Readiness alone authorizes no commit, push, PR, review publication, merge or runtime mutation.',
    'required-gates': 'No blanket override may bypass mandatory safety or project gates.',
    'runtime': 'A GitOps/HCP auto-apply merge is runtime mutation and needs separate fresh explicit authorization with impact and rollback.',
}


def delivery_policy_errors(document):
    prose = active_prose(document)
    return {code for code, declaration in DELIVERY_BOUNDARIES.items() if declaration not in prose}


class DeliveryAuthorizationTest(unittest.TestCase):
    def test_delivery_owners_preserve_readiness_project_and_runtime_boundaries(self):
        for path in DELIVERY_POLICIES:
            with self.subTest(path=path):
                self.assertEqual(delivery_policy_errors((ROOT / path).read_text()), set())

    def test_missing_action_gate_or_runtime_authority_is_rejected(self):
        text = active_prose((GIT_PLUGIN / 'rules/git-workflow.md').read_text())
        for code, declaration in DELIVERY_BOUNDARIES.items():
            with self.subTest(boundary=code):
                self.assertIn(declaration, text)
                sample = text.replace(declaration, 'GO authorizes every delivery action.', 1)
                self.assertIn(code, delivery_policy_errors(sample))

    def test_commit_scope_preserves_unrelated_index_and_untracked_files(self):
        text = active_prose((GIT_PLUGIN / 'skills/commit/SKILL.md').read_text())
        for declaration in (
            "Empty input selects only the current task's verified changes, never all repository changes.",
            'Preserve unrelated staged and unstaged changes.',
            'Do not use git add -A by default.',
            'Never silently include untracked files.',
            'Commit-only stops after the commit;',
        ):
            self.assertIn(declaration, text)
        self.assertNotIn('Stage everything', text)

    def test_pr_divergence_does_not_authorize_rebase_or_force_push(self):
        text = active_prose((GIT_PLUGIN / 'skills/pr/SKILL.md').read_text())
        for declaration in (
            'Do not automatically rebase, reset, merge or force-push after divergence.',
            'A request to create a PR authorizes that PR and its necessary task-branch push.',
            'PR creation does not authorize merge, review publication, deployment or cleanup.',
            'If the branch contains unrelated commits, report the scope problem before push or PR;',
        ):
            self.assertIn(declaration, text)
        for name in ('commit', 'pr'):
            self.assertNotRegex((GIT_PLUGIN / f'skills/{name}/SKILL.md').read_text(), r'/prp-(?:commit|pr)')

    def test_git_entrypoints_reach_common_policy_without_cross_plugin_links(self):
        policy = (GIT_PLUGIN / 'rules/git-workflow.md').resolve()
        for name in ('commit', 'pr', 'finishing-a-development-branch'):
            path = GIT_PLUGIN / f'skills/{name}/SKILL.md'
            with self.subTest(entrypoint=name):
                targets = [(path.parent / link.split('#')[0]).resolve()
                           for link in links(path.read_text()) if '://' not in link]
                self.assertIn(policy, targets)
                self.assertTrue(all(target.is_relative_to(GIT_PLUGIN.resolve()) for target in targets))

    def test_ship_reuses_evidence_and_defaults_to_local_sequential_review(self):
        text = active_prose((PLUGIN / 'skills/ship/SKILL.md').read_text())
        for declaration in (
            'SOLO performs review passes sequentially in the current session.',
            'New changes invalidate affected evidence;',
            'do not ask again for an already authorized action.',
            'including a repository unittest suite',
            'Docs-only work may use Markdown/link checks;',
        ):
            self.assertIn(declaration, text)
        self.assertNotIn('dispatches three parallel review passes', text)
        review = (PLUGIN / 'skills/code-review/SKILL.md').read_text()
        self.assertLess(review.index('Only publish when'), review.index('gh pr review'))
        self.assertIn('--body-file', review)

    def test_readiness_commit_pr_publication_and_merge_have_distinct_rows(self):
        text = (GIT_PLUGIN / 'rules/git-workflow.md').read_text()
        rows = table_rows(sections(text)['Action authorization'])[2:]
        self.assertEqual(tuple(row[0] for row in rows),
                         ('Readiness', 'Commit', 'Push', 'PR', 'Review publication',
                          'Local/remote merge', 'Runtime/destructive mutation'))
        self.assertTrue(all(len(row) == 3 and all(row) for row in rows))
        self.assertIn('Push, PR', rows[1][2])
        self.assertIn('necessary task-branch push', rows[3][1])
        self.assertIn('merge', rows[3][2])
        self.assertIn('merge', rows[4][2])
        self.assertIn('Separate fresh permission', rows[6][1])


TOOLKIT_ENTRYPOINTS = (
    'blueprint', 'subagent-driven-development', 'team-builder',
    'autonomous-agent-harness', 'continuous-agent-loop', 'iterative-retrieval',
    'rules-distill', 'writing-skills',
)
TOOLKIT_AUTHORITY = {
    'authority-first': 'Check authority before capability.',
    'default': 'STANDARD + SOLO',
    'actor-scope': 'HANDOFF, PARALLEL and REVIEW require explicit user authorization',
    'no-bypass': 'Never launch another CLI, worker or orchestrator to bypass a restriction.',
}


def toolkit_authority_errors(document):
    prose = active_prose(document)
    return {code for code, declaration in TOOLKIT_AUTHORITY.items() if declaration not in prose}


def service_control_errors(document):
    prose = active_prose(document)
    required = {
        'inert-plan': 'Do not call `plan_project` until verified controls prevent unauthorized launch and merge.',
        'unsafe-service': 'If safe controls cannot be verified before the call, report incompatibility and use no service.',
        'failed-dependency': 'A failed worker blocks dependent integration and further dependent dispatch.',
    }
    return {code for code, declaration in required.items() if declaration not in prose}


class ToolkitAuthorizationTest(unittest.TestCase):
    def test_every_entrypoint_gates_authority_and_unsafe_examples(self):
        paths = [ROOT / f'plugins/agent-toolkit/skills/{name}/SKILL.md'
                 for name in TOOLKIT_ENTRYPOINTS]
        paths.append(PLUGIN / 'skills/claude-devfleet/SKILL.md')
        for host in ('.claude-plugin', '.codex-plugin'):
            manifest = json.loads((ROOT / 'plugins/agent-toolkit' / host / 'plugin.json').read_text())
            self.assertEqual(manifest.get('dependencies', []), [])
        for path in paths:
            text = path.read_text()
            with self.subTest(path=path):
                self.assertEqual(toolkit_authority_errors(text), set())
                # Include fenced examples/diagrams, not only opening prose.
                self.assertNotRegex(text, r'auto_dispatch\s*=\s*true')
                for old in ('executing-plans', 'Fresh subagent per task +',
                            'direct mode (edit-in-place', '[Subagent analysis:'):
                    self.assertNotIn(old, text)

    def test_deleting_authority_declarations_is_detected(self):
        path = ROOT / 'plugins/agent-toolkit/skills/blueprint/SKILL.md'
        prose = active_prose(path.read_text())
        for code, declaration in TOOLKIT_AUTHORITY.items():
            with self.subTest(boundary=code):
                self.assertIn(declaration, prose)
                self.assertIn(code, toolkit_authority_errors(prose.replace(declaration, '', 1)))

    def test_plan_and_execution_are_local_by_default_with_preserved_paths(self):
        blueprint = active_prose((ROOT / 'plugins/agent-toolkit/skills/blueprint/SKILL.md').read_text())
        for declaration in ('Preserve the existing artifact directory.',
                            'If isolation is blocked, stop writes',
                            'only if configured and within accepted write scope;',
                            '.plans/<slug>/plan.md'):
            self.assertIn(declaration, blueprint)
        executor = active_prose((ROOT / 'plugins/agent-toolkit/skills/subagent-driven-development/SKILL.md').read_text())
        for declaration in ('A plan is state, not authority to execute all its tasks.',
                            'A failed worker or required gate blocks dependent integration.',
                            'no automatic final reviewer dispatch.',
                            'TDD is selected when useful/requested or required by project policy'):
            self.assertIn(declaration, executor)

    def test_loops_carry_restrictions_bounds_and_compatible_fallback(self):
        for name in ('continuous-agent-loop', 'autonomous-agent-harness'):
            text = active_prose((ROOT / f'plugins/agent-toolkit/skills/{name}/SKILL.md').read_text())
            with self.subTest(skill=name):
                for field in ('profile/topology', 'permissions', 'revoked', 'attempt', 'scope'):
                    self.assertIn(field, text)
                self.assertIn('only when compatible with user intent', text)
                self.assertIn('blocks dependent integration', text)
        autonomous = active_prose((ROOT / 'plugins/agent-toolkit/skills/autonomous-agent-harness/SKILL.md').read_text())
        self.assertIn('report incompatibility and create nothing.', autonomous)
        self.assertIn('not a fallback for local SOLO work', autonomous)

    def test_service_controls_must_be_verified_before_side_effects(self):
        prose = active_prose((PLUGIN / 'skills/claude-devfleet/SKILL.md').read_text())
        boundaries = (
            'Do not call `plan_project` until verified controls prevent unauthorized launch and merge.',
            'If safe controls cannot be verified before the call, report incompatibility and use no service.',
            'A failed worker blocks dependent integration and further dependent dispatch.',
        )
        for declaration in boundaries:
            with self.subTest(boundary=declaration):
                self.assertIn(declaration, prose)
                self.assertEqual(service_control_errors(prose), set())
                self.assertTrue(service_control_errors(prose.replace(
                    declaration, 'Launch the chain anyway.', 1)))
        self.assertIn('at least three completed manual HANDOFF/PARALLEL tasks', prose)
        self.assertIn('partial-execution failure test', prose)
        self.assertIn('workers are Claude workers', prose)
        self.assertIn('fresh explicit permission with impact/rollback', prose)

    def test_retrieval_and_distillation_examples_stay_local(self):
        retrieval = (ROOT / 'plugins/agent-toolkit/skills/iterative-retrieval/SKILL.md').read_text()
        self.assertNotIn('DISPATCH', retrieval)
        self.assertIn('complete: false', retrieval)
        self.assertIn('critical missing context blocks dependent implementation', active_prose(retrieval))
        distill = (ROOT / 'plugins/agent-toolkit/skills/rules-distill/SKILL.md').read_text()
        # The worked example is conditional reference, while actor boundaries
        # remain in the core. Preserve the original example assertion there.
        distill_example = (ROOT / 'plugins/agent-toolkit/skills/rules-distill/'
                           'references/verdict-schema-and-examples.md').read_text()
        self.assertIn('[SOLO local role pass:', distill_example)
        self.assertIn('brief is not permission to add actors', distill)
        self.assertIn('reuse existing approval', active_prose(distill))

    def test_authoring_and_readme_cover_proposals_without_launch_permission(self):
        writing = active_prose((ROOT / 'plugins/agent-toolkit/skills/writing-skills/SKILL.md').read_text())
        for area in ('descriptions', 'diagrams', 'examples', 'prompts', 'final steps'):
            self.assertIn(area, writing)
        self.assertIn('Persist profile/topology/permissions', writing)
        readme = active_prose((ROOT / 'plugins/agent-toolkit/README.md').read_text())
        self.assertIn('not launch authority', readme)
        self.assertIn('without copying skills or requiring Superpowers', readme)


class OptionalProviderCompatibilityTest(unittest.TestCase):
    def test_local_paths_cover_every_stage_without_new_skills(self):
        prose = (ROOT / 'plugins/development-lifecycle/README.md').read_text()
        for stage in ('Spec', 'Plan', 'Build', 'Test', 'Review', 'Simplify', 'Ship'):
            self.assertIn(f'| {stage} |', prose)
        self.assertIn('not new commands/skills', prose)
        self.assertIn('does not uninstall or disable', prose)
        self.assertIn('not required for this plugin to work', prose)

    def test_host_limits_and_native_evidence_are_explicit(self):
        prose = (ROOT / 'docs/codex.md').read_text()
        for boundary in ('STANDARD + SOLO', 'hooks: []', 'No duplicate host adapter catalog',
                         'not PASS', 'WORKFLOW_NATIVE_TESTS=1', 'remain release gates',
                         'No provider is installed'):
            self.assertIn(boundary, prose)
        self.assertIn('full OpenCode/consumer strategy remain later work', prose)

    def test_native_tests_require_explicit_opt_in(self):
        import test_host_discovery as native
        self.assertEqual(len(native.OWNER_CASES), 4)
        if not native.NATIVE_ENABLED:
            names = unittest.defaultTestLoader.getTestCaseNames(native.HostDiscoveryTest)
            self.assertEqual(len(names), 3)
            for name in names:
                method = getattr(native.HostDiscoveryTest, name)
                self.assertTrue(method.__unittest_skip__)
                self.assertIn('NOT RUN', method.__unittest_skip_why__)


ARTIFACT_RESOURCES = PLUGIN / 'resources/workflow'
ARTIFACT_SECTIONS = {
    'plan': ('Resume state', 'Objective and non-goals', 'Architecture and decisions',
             'Scope and ownership', 'Tasks and dependencies', 'Quality gates and evidence',
             'Authorization and runtime impact', 'Rollout and rollback', 'Status and next action'),
    'tasks': ('Task TNN — bounded outcome',),
    'handoff': ('Transfer state', 'Completed changes and affected files', 'Decisions and context',
                'Tests and results', 'Risks and missing permissions', 'Exact next step', 'Receiver preflight'),
    'decision': ('Identity and status', 'Context', 'Options', 'Choice and rationale',
                 'Consequences', 'Revisit condition'),
}
TASK_FIELDS = ('Status', 'Exact files', 'Intended change', 'Dependencies', 'Owner / integrator',
               'Authority and missing permissions', 'Tests and checks', 'Expected result',
               'Actual evidence', 'Completion criterion', 'Risks', 'Rollback', 'Next action')


def artifact_shape_errors(kind, text):
    """Test-only template schema checks, not a runtime plan parser."""
    errors = {f'section:{name}' for name in ARTIFACT_SECTIONS[kind]
              if not sections(text).get(name, '').strip()}
    if kind in ('plan', 'handoff'):
        keys = ('task', 'profile', 'topology', 'base_sha', 'branch', 'worktree', 'status')
        keys += ('owner', 'integrator', 'next_action') if kind == 'plan' else ('from', 'to')
        for key in keys:
            if not re.search(rf'^{key}: \S.+$', text, re.MULTILINE):
                errors.add(f'field:{key}')
    if kind == 'tasks':
        for field in TASK_FIELDS:
            if f'- {field}: ' not in text:
                errors.add(f'field:{field}')
    return errors


def cold_resume_fixture_errors(snapshot, current):
    """S06/S13 static fixture assertions; never executes a next action or policy."""
    errors = set()
    for field in ('base_sha', 'branch', 'worktree'):
        if snapshot[field] != current[field]:
            errors.add(f'drift:{field}')
    if snapshot['to'] == 'unassigned' or snapshot['to'] != current['actor']:
        errors.add('receiver')
    if snapshot['authority'] != current['authority']:
        errors.add('authority')
    if snapshot['missing_permissions']:
        errors.add('missing-permission')
    if any(gate['required'] and gate['result'] != 'PASS' for gate in snapshot['gates']):
        errors.add('required-gate')
    return errors


class PortableArtifactTest(unittest.TestCase):
    def test_resource_schema_and_missing_field_mutations(self):
        self.assertEqual({p.stem for p in ARTIFACT_RESOURCES.glob('*.md')}, set(ARTIFACT_SECTIONS))
        for kind, required in ARTIFACT_SECTIONS.items():
            text = (ARTIFACT_RESOURCES / f'{kind}.md').read_text()
            with self.subTest(kind=kind):
                self.assertEqual(artifact_shape_errors(kind, text), set())
                for heading in required:
                    mutated = text.replace(f'## {heading}', '## Missing section', 1)
                    self.assertIn(f'section:{heading}', artifact_shape_errors(kind, mutated))
                if kind in ('plan', 'handoff'):
                    keys = ('task', 'profile', 'topology', 'base_sha', 'branch', 'worktree', 'status')
                    keys += ('owner', 'integrator', 'next_action') if kind == 'plan' else ('from', 'to')
                    for key in keys:
                        mutated = re.sub(rf'^{key}: .+\n', '', text, flags=re.MULTILINE)
                        self.assertIn(f'field:{key}', artifact_shape_errors(kind, mutated))
                if kind == 'tasks':
                    for field in TASK_FIELDS:
                        mutated = text.replace(f'- {field}: ', '- Missing: ', 1)
                        self.assertIn(f'field:{field}', artifact_shape_errors(kind, mutated))

    def test_resources_are_reachable_from_existing_entrypoints(self):
        seeds = [CONTRACT, PLUGIN / 'skills/spec/SKILL.md', PLUGIN / 'skills/architect/SKILL.md',
                 PLUGIN / 'skills/architecture-decision-records/SKILL.md']
        for seed in seeds:
            pending, visited = [seed.resolve()], set()
            while pending:
                document = pending.pop()
                if document in visited:
                    continue
                visited.add(document)
                self.assertEqual(plugin_link_errors(document, PLUGIN), [])
                for relative in links(document.read_text()):
                    if '://' not in relative:
                        target = (document.parent / relative.split('#')[0]).resolve()
                        if target.is_file() and target.suffix == '.md':
                            pending.append(target)
            self.assertTrue({p.resolve() for p in ARTIFACT_RESOURCES.glob('*.md')} <= visited, seed)

    def test_resource_links_reject_missing_fragment_path_and_plugin_escape(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            plugin = root / 'plugin'
            documents = plugin / 'resources/workflow'
            documents.mkdir(parents=True)
            target = documents / 'target.md'
            target.write_text('# Target\n\n## Receiver preflight\n\n## Receiver preflight\n')
            source = documents / 'source.md'
            for relative, error in (('target.md#receiver-preflight', None),
                                    ('target.md#receiver-preflight-1', None),
                                    ('target.md#missing', 'missing-fragment'),
                                    ('missing.md', 'missing-target'),
                                    ('../../../outside.md', 'outside-plugin'),
                                    ('../../../docs/plan.md', 'outside-plugin')):
                source.write_text(f'[link]({relative})\n')
                found = plugin_link_errors(source, plugin)
                self.assertEqual([kind for kind, _ in found], [error] if error else [])
            outside = root / 'outside.md'
            outside.write_text('# Outside\n')
            (documents / 'escape.md').symlink_to(outside)
            source.write_text('[escape](escape.md)\n')
            self.assertEqual(plugin_link_errors(source, plugin)[0][0], 'outside-plugin')
            self.assertEqual(markdown_anchors('```md\n# Phantom\n```\n# Actual\n'), {'actual'})

    def test_installed_resource_validation_without_launching_a_host(self):
        from test_host_discovery import HostDiscoveryTest
        check = HostDiscoveryTest('test_claude_accepts_marketplace_and_plugin_contents')
        with tempfile.TemporaryDirectory() as temporary:
            installed = Path(temporary) / 'development-lifecycle'
            shutil.copytree(PLUGIN, installed)
            expected = check.assert_installed_content('development-lifecycle', installed)
            self.assertTrue(expected)
            (installed / 'resources/workflow/handoff.md').unlink()
            with self.assertRaises(AssertionError):
                check.assert_installed_content('development-lifecycle', installed)
        # This is a filesystem fixture only, never evidence of a native install.

    def test_optional_blueprint_uses_discovery_without_copying_resources(self):
        toolkit = ROOT / 'plugins/agent-toolkit'
        text = (toolkit / 'skills/blueprint/SKILL.md').read_text()
        for boundary in ('development-lifecycle-rules', 'actual installed location',
                         'Do not\nclone', 'plain-plan', 'Unassigned receivers', 'NOT RUN'):
            self.assertIn(boundary, text)
        self.assertNotIn('../../resources/workflow/', text)
        self.assertFalse((toolkit / 'resources/workflow').exists())

    def test_templates_preserve_artifacts_and_do_not_grant_authority(self):
        for kind in ('plan', 'tasks', 'handoff'):
            text = (ARTIFACT_RESOURCES / f'{kind}.md').read_text()
            for declaration in ('existing project directories and formats', 'Superpowers/PRP',
                                'QUICK may', 'DEEP multi-session', 'PASS', 'NOT RUN'):
                self.assertIn(declaration, text)
        plan = (ARTIFACT_RESOURCES / 'plan.md').read_text()
        self.assertIn('not a new grant', plan)
        self.assertIn('STANDARD + SOLO', plan)
        handoff = (ARTIFACT_RESOURCES / 'handoff.md').read_text()
        self.assertIn('to: unassigned', handoff)
        self.assertIn('snapshot grants no permission', handoff)
        self.assertIn('no dispatch follows', handoff)
        self.assertIn('../../rules/common/workflow.md#safety-and-worktree-first',
                      sections(handoff)['Receiver preflight'])
        adr = (PLUGIN / 'skills/architecture-decision-records/SKILL.md').read_text()
        self.assertIn('reuse approval already covering the exact action', adr)

    def test_cold_resume_s06_stale_base_receiver_authority_and_not_run(self):
        snapshot = {'base_sha': 'a' * 40, 'branch': 'feat/example', 'worktree': '/tmp/example',
                    'to': 'authorized-receiver', 'authority': 'bounded-read-only-review',
                    'missing_permissions': [], 'gates': [{'required': True, 'result': 'PASS'}]}
        current = {**snapshot, 'actor': 'authorized-receiver'}
        self.assertEqual(cold_resume_fixture_errors(snapshot, current), set())
        for field, replacement in (('base_sha', 'b' * 40), ('branch', 'main'),
                                   ('worktree', '/tmp/other')):
            self.assertIn(f'drift:{field}', cold_resume_fixture_errors(snapshot, {**current, field: replacement}))
        self.assertIn('receiver', cold_resume_fixture_errors({**snapshot, 'to': 'unassigned'}, current))
        self.assertIn('authority', cold_resume_fixture_errors(snapshot, {**current, 'authority': 'revoked'}))
        self.assertIn('missing-permission', cold_resume_fixture_errors(
            {**snapshot, 'missing_permissions': ['delivery']}, current))
        for result in ('NOT RUN', 'FAIL', 'NOT APPLICABLE'):
            self.assertIn('required-gate', cold_resume_fixture_errors(
                {**snapshot, 'gates': [{'required': True, 'result': result}]}, current))
        # Simulated records only; real actor behavior remains a release gate.

    def test_cold_receiver_primary_status_cannot_be_inherited_from_snapshot(self):
        with tempfile.TemporaryDirectory() as temporary:
            primary = Path(temporary) / 'primary'
            writer = Path(temporary) / 'writer'

            def git(*args, cwd=primary):
                return subprocess.run(['git', *args], cwd=cwd, check=True,
                                      capture_output=True, text=True).stdout

            primary.mkdir()
            git('init', '-b', 'main')
            (primary / 'file.txt').write_text('baseline\n')
            git('add', 'file.txt')
            git('-c', 'user.name=Workflow Test', '-c', 'user.email=test@example.invalid',
                '-c', 'commit.gpgsign=false', 'commit', '-m', 'seed')
            git('worktree', 'add', '-b', 'feat/receiver', str(writer))
            sender_primary_status = git('status', '--porcelain')
            sender_worktrees = git('worktree', 'list', '--porcelain', cwd=writer)
            self.assertEqual(sender_primary_status, '')

            # State changes after the sender exits, without moving either HEAD.
            (primary / 'file.txt').write_text('unrelated user work\n')
            self.assertEqual(git('worktree', 'list', '--porcelain', cwd=writer),
                             sender_worktrees)
            self.assertEqual(git('status', '--porcelain', cwd=writer), '')
            self.assertNotEqual(git('-C', str(primary), 'status', '--porcelain',
                                    cwd=writer), sender_primary_status)

    def test_s13_cold_snapshot_roundtrip_preserves_established_paths(self):
        template = (ARTIFACT_RESOURCES / 'handoff.md').read_text()
        for folder in ('.plans/established', '.archive/.plans/old',
                       'docs/superpowers/plans', '.claude/prp-plans'):
            # Render a cold snapshot; source plan format is not transformed.
            snapshot = template.replace('<id/slug>', 'T13').replace('<verified full SHA>', 'a' * 40)
            snapshot = snapshot.replace('<actual branch>', 'feat/example')
            snapshot = snapshot.replace('<absolute verified path>', '/tmp/isolated')
            snapshot = snapshot.replace('to: unassigned', 'to: authorized-receiver')
            snapshot = snapshot.replace('topology: solo', 'topology: handoff')
            snapshot = snapshot.replace('profile: standard', 'profile: deep')
            snapshot = snapshot.replace('(plan.md)', f'({folder}/plan.md)')
            snapshot = snapshot.replace('(tasks.md)', f'({folder}/tasks.md)')
            with tempfile.TemporaryDirectory() as temporary:
                handoff = Path(temporary) / 'handoff.md'
                handoff.write_text(snapshot)
                resumed = handoff.read_text()
            fields = dict(re.findall(r'^(\w+): (.+)$', resumed, flags=re.MULTILINE))
            self.assertEqual(fields['base_sha'], 'a' * 40)
            self.assertEqual(fields['worktree'], '/tmp/isolated')
            self.assertEqual(fields['to'], 'authorized-receiver')
            self.assertEqual((fields['profile'], fields['topology']), ('deep', 'handoff'))
            self.assertIn(f'{folder}/plan.md', resumed)
            self.assertIn(f'{folder}/tasks.md', resumed)
            self.assertIn('NOT RUN', resumed)
            self.assertEqual(artifact_shape_errors('handoff', resumed), set())


SCENARIO_FIXTURE = ROOT / 'tests/fixtures/workflow/scenarios.json'
SCENARIO_CASES = {
    'S01': {'default', 'unknown-profile', 'unknown-topology', 'policy-conflict'},
    'S02': {'small-check'}, 'S03': {'reproducer'}, 'S04': {'plan-only'},
    'S05': {'proposal', 'revoked'}, 'S06': {'cold-resume', 'stale-base', 'unassigned'},
    'S07': {'isolated-writers', 'partial-failure'}, 'S08': {'read-only', 'sequential'},
    'S09': {'readiness-only', 'commit-only', 'pr-only', 'gate-failed'},
    'S10': {'missing-reviewer'}, 'S11': {'each-owner'},
    'S12': {'manual-git', 'denied', 'missing-jq'},
    'S13': {'existing-formats', 'new-convention'},
    'S14': {'missing-tools', 'unsafe-service'}, 'S15': {'gitops-merge', 'destructive'},
    'S16': {'dirty-primary', 'submodule', 'detached-external'},
}


def scenario_fixture_errors(data, read_document=None):
    """Validate data and source references only; never interpret/execute actions."""
    errors = set()
    read_document = read_document or (lambda relative: (ROOT / relative).read_text())
    if set(data) != {'schema_version', 'data_only', 'execution', 'description', 'scenarios'}:
        errors.add('fixture-fields')
    if data.get('schema_version') != 1 or data.get('data_only') is not True:
        errors.add('data-only')
    if data.get('execution') != 'manual-authorized-trials-only':
        errors.add('execution-boundary')
    scenarios = data.get('scenarios', [])
    if not isinstance(scenarios, list):
        return errors | {'scenarios'}
    if {item.get('id') for item in scenarios} != set(SCENARIO_CASES) or len(scenarios) != 16:
        errors.add('scenario-coverage')
    def fields(value, keys):
        return isinstance(value, dict) and set(value) == set(keys)
    def strings(value, empty=False):
        return isinstance(value, list) and (empty or bool(value)) and all(
            isinstance(item, str) and item.strip() for item in value)
    for scenario in scenarios:
        sid = scenario.get('id')
        if not fields(scenario, ('id', 'title', 'hosts', 'input', 'authority', 'capabilities', 'guidance', 'cases')):
            errors.add(f'{sid}:fields')
        if scenario.get('hosts') != ['claude', 'codex']:
            errors.add(f'{sid}:hosts')
        inp = scenario.get('input', {})
        if not fields(inp, ('request', 'profile', 'topology')) or not inp.get('request'):
            errors.add(f'{sid}:input')
        if inp.get('profile') not in (None, 'quick', 'standard', 'deep') or inp.get('topology') not in (
                None, 'solo', 'handoff', 'parallel', 'review'):
            errors.add(f'{sid}:selection')
        authority = scenario.get('authority', {})
        if not fields(authority, ('source', 'actors', 'actions', 'exclusions')) or not authority.get('source'):
            errors.add(f'{sid}:authority')
        for name in ('actors', 'actions', 'exclusions'):
            if not strings(authority.get(name)):
                errors.add(f'{sid}:authority:{name}')
        capability = scenario.get('capabilities', {})
        if not fields(capability, ('available', 'missing')) or any(
                not strings(capability.get(name), empty=True) for name in ('available', 'missing')):
            errors.add(f'{sid}:capabilities')
        refs = scenario.get('guidance', [])
        if not isinstance(refs, list) or not refs:
            errors.add(f'{sid}:guidance')
            refs = []
        for reference in refs:
            if not fields(reference, ('path', 'fragment', 'required_text')) or not all(reference.values()):
                errors.add(f'{sid}:reference-fields')
                continue
            path = (ROOT / reference['path']).resolve()
            if not path.is_relative_to((ROOT / 'plugins').resolve()) or not path.is_file():
                errors.add(f'{sid}:reference-path')
                continue
            document = read_document(reference['path'])
            if reference['fragment'] not in markdown_anchors(document):
                errors.add(f'{sid}:reference-fragment')
            if ' '.join(reference['required_text'].split()) not in ' '.join(document.split()):
                errors.add(f'{sid}:instruction')
        cases = scenario.get('cases', [])
        if not isinstance(cases, list):
            errors.add(f'{sid}:cases')
            continue
        if {case.get('id') for case in cases} != SCENARIO_CASES.get(sid, set()) or len(cases) != len(SCENARIO_CASES.get(sid, set())):
            errors.add(f'{sid}:case-coverage')
        for case in cases:
            if not fields(case, ('id', 'given', 'required_actions', 'forbidden_actions', 'artifact_expectations')):
                errors.add(f'{sid}:case-fields')
            for name in ('given', 'required_actions', 'forbidden_actions', 'artifact_expectations'):
                if not strings(case.get(name)):
                    errors.add(f'{sid}:case:{name}')
            if set(case.get('required_actions', [])) & set(case.get('forbidden_actions', [])):
                errors.add(f'{sid}:contradictory-actions')
    return errors


class WorkflowScenarioTest(unittest.TestCase):
    def fixture(self):
        return json.loads(SCENARIO_FIXTURE.read_text())

    def test_all_scenarios_and_negative_variants_have_complete_data(self):
        data = self.fixture()
        self.assertEqual(scenario_fixture_errors(data), set())
        self.assertEqual(sum(len(s['cases']) for s in data['scenarios']), 34)
        self.assertEqual(data['scenarios'][0]['input'], {
            'request': 'Fix a small validation defect.', 'profile': None, 'topology': None})

    def test_removed_scenario_host_or_required_fields_are_rejected(self):
        data = self.fixture()
        data['scenarios'].pop()
        self.assertIn('scenario-coverage', scenario_fixture_errors(data))
        for field in ('input', 'authority', 'capabilities', 'guidance', 'cases'):
            data = self.fixture()
            del data['scenarios'][0][field]
            self.assertTrue(scenario_fixture_errors(data), field)
        data = self.fixture()
        data['scenarios'][0]['hosts'] = ['claude']
        self.assertIn('S01:hosts', scenario_fixture_errors(data))
        for key in ('given', 'required_actions', 'forbidden_actions', 'artifact_expectations'):
            data = self.fixture()
            data['scenarios'][0]['cases'][0][key] = []
            self.assertIn(f'S01:case:{key}', scenario_fixture_errors(data))

    def test_action_conflict_case_loss_and_execution_fields_are_rejected(self):
        data = self.fixture()
        case = data['scenarios'][0]['cases'][0]
        case['forbidden_actions'].append(case['required_actions'][0])
        self.assertIn('S01:contradictory-actions', scenario_fixture_errors(data))
        data = self.fixture()
        data['scenarios'][0]['cases'].pop()
        self.assertIn('S01:case-coverage', scenario_fixture_errors(data))
        for mutation in ({'data_only': False}, {'execution': 'auto-run'}, {'command': 'do not execute'}):
            self.assertTrue(scenario_fixture_errors({**self.fixture(), **mutation}))

    def test_broken_or_escaping_guidance_and_fragments_are_rejected(self):
        for change, error in (({'path': 'plugins/missing.md'}, 'reference-path'),
                              ({'path': '../outside.md'}, 'reference-path'),
                              ({'fragment': 'missing'}, 'reference-fragment')):
            data = self.fixture()
            data['scenarios'][0]['guidance'][0].update(change)
            self.assertIn(f'S01:{error}', scenario_fixture_errors(data))

    def test_every_source_guard_deletion_is_detected_without_running_actions(self):
        for scenario in self.fixture()['scenarios']:
            for reference in scenario['guidance']:
                with self.subTest(scenario=scenario['id'], path=reference['path']):
                    target = reference['path']
                    def mutated_reader(relative):
                        text = ' '.join((ROOT / relative).read_text().split())
                        return text.replace(' '.join(reference['required_text'].split()),
                                            'Guard removed.', 1) if relative == target else (ROOT / relative).read_text()
                    self.assertIn(f"{scenario['id']}:instruction", scenario_fixture_errors(self.fixture(), mutated_reader))

    def test_guidance_is_reachable_from_existing_installed_entrypoints(self):
        referenced = {reference['path'] for scenario in self.fixture()['scenarios']
                      for reference in scenario['guidance']}
        for relative in referenced:
            target = ROOT / relative
            plugin = ROOT / '/'.join(Path(relative).parts[:2])
            pending = list(plugin.glob('skills/*/SKILL.md'))
            pending += list(plugin.glob('commands/*.md')) + list(plugin.glob('agents/*.md'))
            visited = set()
            while pending:
                document = pending.pop().resolve()
                if document in visited:
                    continue
                visited.add(document)
                for link in links(document.read_text()):
                    if '://' in link or link.startswith('mailto:'):
                        continue
                    linked = (document.parent / link.split('#')[0]).resolve()
                    if linked.is_relative_to(plugin.resolve()) and linked.is_file() and linked.suffix == '.md':
                        pending.append(linked)
            self.assertIn(target.resolve(), visited, relative)

    def test_missing_jq_and_denied_worktree_guards_have_direct_negative_checks(self):
        path = ROOT / 'plugins/git-workflows/skills/using-git-worktrees/SKILL.md'
        text = ' '.join(path.read_text().split())
        for declaration in (
                'If worktree creation fails, stop writes and report the permission prerequisite.',
                'A missing jq or failed-open hook does not waive this procedural invariant;'):
            self.assertIn(declaration, text)
            def removed(relative):
                content = ' '.join((ROOT / relative).read_text().split())
                return content.replace(declaration, 'Continue in primary.', 1) if ROOT / relative == path else (ROOT / relative).read_text()
            self.assertIn('S12:instruction', scenario_fixture_errors(self.fixture(), removed))


if __name__ == '__main__':
    unittest.main()
