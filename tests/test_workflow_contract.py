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

from test_codex_manifests import frontmatter, links

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
UNCHANGED_WORKTREE_HOOKS = {'guard-main-checkout.sh': 'af5510df0aa35479f8dfda41b21bffbdeffd93c31a28fa8c9f59660f445e8c51',
 'hooks.json': '501056f7d13da344b80ba6a49c687b9a45bb74ee8187eebbcd4d84827f4ff5bf',
 'inject-worktree-rule.sh': '2ed8e409b89e0b19c250ca7862b284091621bedfae4d417e6e1242f0f40a187f',
 'test-guard.sh': '0259c27e6320a2494ab6660f119693b21644dbece528cadaff51aca5f2c0ee52'}


def isolation_creation_errors(document):
    prose = active_prose(document)
    required = {
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


if __name__ == '__main__':
    unittest.main()
