"""Optional maintainer checks; installing plugins needs no Python dependency."""

import json
import shutil
import tempfile
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit
import unittest

ROOT = Path(__file__).resolve().parents[1]


# Frozen T01 inventory at 2194b9ad587963dd75a8d6b4fa320b963ee88f9a.
# Source: docs/plans/hybrid-ai-workflow/audit.md, T01 catalog/skill/wrapper tables.
FROZEN_T01_CATALOG = {'agent-toolkit': './plugins/agent-toolkit',
 'android': './plugins/android',
 'backend': './plugins/backend',
 'devcontainer': './plugins/devcontainer',
 'development-lifecycle': './plugins/development-lifecycle',
 'devops': './plugins/devops',
 'dotnet': './plugins/dotnet',
 'frontend': './plugins/frontend',
 'git-workflows': './plugins/git-workflows',
 'personal-essentials': './plugins/personal-essentials',
 'renovate': './plugins/renovate',
 'security': './plugins/security'}
FROZEN_T01_SKILLS = {'agent-toolkit:autonomous-agent-harness': 'plugins/agent-toolkit/skills/autonomous-agent-harness/SKILL.md',
 'agent-toolkit:blueprint': 'plugins/agent-toolkit/skills/blueprint/SKILL.md',
 'agent-toolkit:context-budget': 'plugins/agent-toolkit/skills/context-budget/SKILL.md',
 'agent-toolkit:continuous-agent-loop': 'plugins/agent-toolkit/skills/continuous-agent-loop/SKILL.md',
 'agent-toolkit:eval-harness': 'plugins/agent-toolkit/skills/eval-harness/SKILL.md',
 'agent-toolkit:iterative-retrieval': 'plugins/agent-toolkit/skills/iterative-retrieval/SKILL.md',
 'agent-toolkit:rules-distill': 'plugins/agent-toolkit/skills/rules-distill/SKILL.md',
 'agent-toolkit:safety-guard': 'plugins/agent-toolkit/skills/safety-guard/SKILL.md',
 'agent-toolkit:search-first': 'plugins/agent-toolkit/skills/search-first/SKILL.md',
 'agent-toolkit:subagent-driven-development': 'plugins/agent-toolkit/skills/subagent-driven-development/SKILL.md',
 'agent-toolkit:team-builder': 'plugins/agent-toolkit/skills/team-builder/SKILL.md',
 'agent-toolkit:verification-loop': 'plugins/agent-toolkit/skills/verification-loop/SKILL.md',
 'agent-toolkit:workspace-surface-audit': 'plugins/agent-toolkit/skills/workspace-surface-audit/SKILL.md',
 'agent-toolkit:writing-skills': 'plugins/agent-toolkit/skills/writing-skills/SKILL.md',
 'backend:api-design': 'plugins/backend/skills/api-design/SKILL.md',
 'backend:backend-patterns': 'plugins/backend/skills/backend-patterns/SKILL.md',
 'backend:database-migrations': 'plugins/backend/skills/database-migrations/SKILL.md',
 'backend:database-reviewer': 'plugins/backend/skills/database-reviewer/SKILL.md',
 'backend:hexagonal-architecture': 'plugins/backend/skills/hexagonal-architecture/SKILL.md',
 'backend:mcp-server-patterns': 'plugins/backend/skills/mcp-server-patterns/SKILL.md',
 'backend:nestjs-patterns': 'plugins/backend/skills/nestjs-patterns/SKILL.md',
 'backend:postgres-patterns': 'plugins/backend/skills/postgres-patterns/SKILL.md',
 'devcontainer:devcontainer-auditor': 'plugins/devcontainer/skills/devcontainer-auditor/SKILL.md',
 'devcontainer:devcontainer-ghcr-image-pipeline': 'plugins/devcontainer/skills/devcontainer-ghcr-image-pipeline/SKILL.md',
 'devcontainer:devcontainer-renovate-digest-pinning': 'plugins/devcontainer/skills/devcontainer-renovate-digest-pinning/SKILL.md',
 'devcontainer:devcontainer-secrets-injection': 'plugins/devcontainer/skills/devcontainer-secrets-injection/SKILL.md',
 'development-lifecycle:ai-regression-testing': 'plugins/development-lifecycle/skills/ai-regression-testing/SKILL.md',
 'development-lifecycle:architect': 'plugins/development-lifecycle/skills/architect/SKILL.md',
 'development-lifecycle:architecture-decision-records': 'plugins/development-lifecycle/skills/architecture-decision-records/SKILL.md',
 'development-lifecycle:aside': 'plugins/development-lifecycle/skills/aside/SKILL.md',
 'development-lifecycle:build-error-resolver': 'plugins/development-lifecycle/skills/build-error-resolver/SKILL.md',
 'development-lifecycle:claude-devfleet': 'plugins/development-lifecycle/skills/claude-devfleet/SKILL.md',
 'development-lifecycle:code-review': 'plugins/development-lifecycle/skills/code-review/SKILL.md',
 'development-lifecycle:code-reviewer': 'plugins/development-lifecycle/skills/code-reviewer/SKILL.md',
 'development-lifecycle:development-lifecycle-rules': 'plugins/development-lifecycle/skills/development-lifecycle-rules/SKILL.md',
 'development-lifecycle:doc-updater': 'plugins/development-lifecycle/skills/doc-updater/SKILL.md',
 'development-lifecycle:docs-lookup': 'plugins/development-lifecycle/skills/docs-lookup/SKILL.md',
 'development-lifecycle:e2e-testing': 'plugins/development-lifecycle/skills/e2e-testing/SKILL.md',
 'development-lifecycle:learn-eval': 'plugins/development-lifecycle/skills/learn-eval/SKILL.md',
 'development-lifecycle:review': 'plugins/development-lifecycle/skills/review/SKILL.md',
 'development-lifecycle:ship': 'plugins/development-lifecycle/skills/ship/SKILL.md',
 'development-lifecycle:simplify': 'plugins/development-lifecycle/skills/simplify/SKILL.md',
 'development-lifecycle:skill-create': 'plugins/development-lifecycle/skills/skill-create/SKILL.md',
 'development-lifecycle:spec': 'plugins/development-lifecycle/skills/spec/SKILL.md',
 'development-lifecycle:tdd-guide': 'plugins/development-lifecycle/skills/tdd-guide/SKILL.md',
 'development-lifecycle:test': 'plugins/development-lifecycle/skills/test/SKILL.md',
 'development-lifecycle:update-codemaps': 'plugins/development-lifecycle/skills/update-codemaps/SKILL.md',
 'development-lifecycle:update-docs': 'plugins/development-lifecycle/skills/update-docs/SKILL.md',
 'devops:deployment-patterns': 'plugins/devops/skills/deployment-patterns/SKILL.md',
 'devops:docker-patterns': 'plugins/devops/skills/docker-patterns/SKILL.md',
 'dotnet:csharp-reviewer': 'plugins/dotnet/skills/csharp-reviewer/SKILL.md',
 'dotnet:csharp-testing': 'plugins/dotnet/skills/csharp-testing/SKILL.md',
 'dotnet:dotnet-patterns': 'plugins/dotnet/skills/dotnet-patterns/SKILL.md',
 'dotnet:dotnet-rules': 'plugins/dotnet/skills/dotnet-rules/SKILL.md',
 'frontend:design-system': 'plugins/frontend/skills/design-system/SKILL.md',
 'frontend:frontend-patterns': 'plugins/frontend/skills/frontend-patterns/SKILL.md',
 'frontend:frontend-rules': 'plugins/frontend/skills/frontend-rules/SKILL.md',
 'frontend:nextjs-turbopack': 'plugins/frontend/skills/nextjs-turbopack/SKILL.md',
 'git-workflows:commit': 'plugins/git-workflows/skills/commit/SKILL.md',
 'git-workflows:finishing-a-development-branch': 'plugins/git-workflows/skills/finishing-a-development-branch/SKILL.md',
 'git-workflows:git-workflows-rules': 'plugins/git-workflows/skills/git-workflows-rules/SKILL.md',
 'git-workflows:pr': 'plugins/git-workflows/skills/pr/SKILL.md',
 'git-workflows:using-git-worktrees': 'plugins/git-workflows/skills/using-git-worktrees/SKILL.md',
 'personal-essentials:personal-setup': 'plugins/personal-essentials/skills/personal-setup/SKILL.md',
 'renovate:renovate-auditor': 'plugins/renovate/skills/renovate-auditor/SKILL.md',
 'renovate:renovate-automerge-rules': 'plugins/renovate/skills/renovate-automerge-rules/SKILL.md',
 'renovate:renovate-custom-regex-managers': 'plugins/renovate/skills/renovate-custom-regex-managers/SKILL.md',
 'renovate:renovate-extending-presets': 'plugins/renovate/skills/renovate-extending-presets/SKILL.md',
 'security:security-review': 'plugins/security/skills/security-review/SKILL.md',
 'security:security-scan': 'plugins/security/skills/security-scan/SKILL.md'}
FROZEN_T01_WRAPPERS = {'plugins/backend/agents/database-reviewer.md': 'plugins/backend/skills/database-reviewer/SKILL.md',
 'plugins/devcontainer/agents/devcontainer-auditor.md': 'plugins/devcontainer/skills/devcontainer-auditor/SKILL.md',
 'plugins/development-lifecycle/agents/architect.md': 'plugins/development-lifecycle/skills/architect/SKILL.md',
 'plugins/development-lifecycle/agents/build-error-resolver.md': 'plugins/development-lifecycle/skills/build-error-resolver/SKILL.md',
 'plugins/development-lifecycle/agents/code-reviewer.md': 'plugins/development-lifecycle/skills/code-reviewer/SKILL.md',
 'plugins/development-lifecycle/agents/doc-updater.md': 'plugins/development-lifecycle/skills/doc-updater/SKILL.md',
 'plugins/development-lifecycle/agents/docs-lookup.md': 'plugins/development-lifecycle/skills/docs-lookup/SKILL.md',
 'plugins/development-lifecycle/agents/tdd-guide.md': 'plugins/development-lifecycle/skills/tdd-guide/SKILL.md',
 'plugins/development-lifecycle/commands/aside.md': 'plugins/development-lifecycle/skills/aside/SKILL.md',
 'plugins/development-lifecycle/commands/code-review.md': 'plugins/development-lifecycle/skills/code-review/SKILL.md',
 'plugins/development-lifecycle/commands/learn-eval.md': 'plugins/development-lifecycle/skills/learn-eval/SKILL.md',
 'plugins/development-lifecycle/commands/review.md': 'plugins/development-lifecycle/skills/review/SKILL.md',
 'plugins/development-lifecycle/commands/ship.md': 'plugins/development-lifecycle/skills/ship/SKILL.md',
 'plugins/development-lifecycle/commands/skill-create.md': 'plugins/development-lifecycle/skills/skill-create/SKILL.md',
 'plugins/development-lifecycle/commands/spec.md': 'plugins/development-lifecycle/skills/spec/SKILL.md',
 'plugins/development-lifecycle/commands/test.md': 'plugins/development-lifecycle/skills/test/SKILL.md',
 'plugins/development-lifecycle/commands/update-codemaps.md': 'plugins/development-lifecycle/skills/update-codemaps/SKILL.md',
 'plugins/development-lifecycle/commands/update-docs.md': 'plugins/development-lifecycle/skills/update-docs/SKILL.md',
 'plugins/dotnet/agents/csharp-reviewer.md': 'plugins/dotnet/skills/csharp-reviewer/SKILL.md',
 'plugins/git-workflows/commands/commit.md': 'plugins/git-workflows/skills/commit/SKILL.md',
 'plugins/git-workflows/commands/pr.md': 'plugins/git-workflows/skills/pr/SKILL.md',
 'plugins/personal-essentials/commands/personal-setup.md': 'plugins/personal-essentials/skills/personal-setup/SKILL.md',
 'plugins/renovate/agents/renovate-auditor.md': 'plugins/renovate/skills/renovate-auditor/SKILL.md'}

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


def markdown_anchors(text):
    """GitHub-style heading fragments, ignoring fenced examples."""
    anchors, counts = set(), {}
    fence = None
    for line in text.splitlines():
        match = re.match(r'^\s*(`{3,}|~{3,})', line)
        if match:
            marker = match[1]
            if fence is None:
                fence = marker
            elif marker[0] == fence[0] and len(marker) >= len(fence):
                fence = None
            continue
        if fence is not None:
            continue
        heading = re.match(r'^#{1,6}\s+(.+?)\s*#*$', line)
        if heading:
            slug = re.sub(r'[^\w\- ]', '', heading[1].lower()).replace(' ', '-')
            number = counts.get(slug, 0)
            counts[slug] = number + 1
            anchors.add(f'{slug}-{number}' if number else slug)
    return anchors


def plugin_link_errors(document, plugin):
    """Resolve local resource links/fragments within an installed plugin root."""
    errors = []
    for raw in links(document.read_text()):
        relative = raw.strip('<>')
        parsed = urlsplit(relative)
        if parsed.scheme or parsed.netloc:
            continue
        target = (document.parent / unquote(parsed.path)).resolve() if parsed.path else document.resolve()
        if not target.is_relative_to(plugin.resolve()):
            errors.append(('outside-plugin', raw))
        elif not target.is_file():
            errors.append(('missing-target', raw))
        elif parsed.fragment and (target.suffix != '.md' or
                                  unquote(parsed.fragment) not in markdown_anchors(target.read_text())):
            errors.append(('missing-fragment', raw))
    return errors


def hard_workflow_provider(manifest):
    """Inspect declared dependencies only, not optional prose/keywords/history."""
    return bool(re.search(r'(?i)superpowers', json.dumps(manifest.get('dependencies', []))))


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
            documents += list(plugin.glob('resources/**/*.md'))
            for document in documents:
                with self.subTest(document=document):
                    self.assertEqual(plugin_link_errors(document, plugin), [])
                for relative in links(document.read_text()):
                    parsed = urlsplit(relative.strip('<>'))
                    if not parsed.scheme and not parsed.netloc:
                        referenced.add((document.parent / unquote(parsed.path)).resolve()
                                       if parsed.path else document.resolve())
            for entrypoint in list(plugin.glob('commands/*.md')) + list(plugin.glob('agents/*.md')):
                expected = plugin / 'skills' / entrypoint.stem / 'SKILL.md'
                self.assertIn(expected.resolve(), referenced)
                self.assertIn(f'../skills/{entrypoint.stem}/SKILL.md', entrypoint.read_text())
            for rule in plugin.glob('rules/**/*.md'):
                self.assertIn(rule.resolve(), referenced)

    def test_disposable_copy_preserves_catalog_content_and_detects_corruption(self):
        # Filesystem smoke only: no CLI installation/discovery claim.
        from test_host_discovery import HostDiscoveryTest
        check = HostDiscoveryTest('test_claude_accepts_marketplace_and_plugin_contents')
        with tempfile.TemporaryDirectory() as temporary:
            for name, source in FROZEN_T01_CATALOG.items():
                with self.subTest(plugin=name):
                    installed = Path(temporary) / name
                    shutil.copytree(ROOT / source, installed)
                    check.assert_installed_content(name, installed)
            lifecycle = Path(temporary) / 'development-lifecycle'
            manifest = lifecycle / '.codex-plugin/plugin.json'
            content = manifest.read_text()
            altered = json.loads(content)
            altered['version'] = '0.0.0'
            manifest.write_text(json.dumps(altered))
            with self.assertRaises(AssertionError):
                check.assert_installed_content('development-lifecycle', lifecycle)
            manifest.write_text(content)
            resource = lifecycle / 'resources/workflow/plan.md'
            resource.write_text(resource.read_text() + '\n[broken](missing.md)\n')
            with self.assertRaises(AssertionError):
                check.assert_installed_content('development-lifecycle', lifecycle)

    def test_codex_command_wrappers_do_not_generate_a_second_skill_catalog(self):
        owners = {Path(path).parts[1] for path in FROZEN_T01_WRAPPERS if '/commands/' in path}
        self.assertEqual(owners, {'development-lifecycle', 'git-workflows', 'personal-essentials'})
        for owner in owners:
            with self.subTest(plugin=owner):
                plugin = ROOT / 'plugins' / owner
                codex = json.loads((plugin / '.codex-plugin/plugin.json').read_text())
                claude = json.loads((plugin / '.claude-plugin/plugin.json').read_text())
                self.assertEqual(codex.get('commands'), [])
                self.assertNotIn('commands', claude)  # Retain Claude's default entrypoint scan.
                self.assertTrue(list(plugin.glob('commands/*.md')))
                self.assertEqual(codex['skills'], './skills/')
                self.assertEqual(codex['hooks'], [])

    def test_personal_setup_contains_both_host_installations(self):
        catalog = json.loads((ROOT / '.claude-plugin/marketplace.json').read_text())
        setup = (ROOT / 'plugins/personal-essentials/skills/personal-setup/SKILL.md').read_text()
        for entry in catalog['plugins']:
            if entry['name'] not in ('personal-essentials', 'android'):
                selector = f"{entry['name']}@{catalog['name']}"
                self.assertIn(f'codex plugin add {selector}', setup)
                self.assertIn(f'claude plugin install {selector}', setup)


    def test_t01_catalog_and_shared_identities_are_preserved(self):
        catalog = json.loads((ROOT / '.claude-plugin/marketplace.json').read_text())
        self.assertEqual(catalog['name'], 'mmalyska-claude-plugins')
        self.assertEqual({entry['name']: entry['source'] for entry in catalog['plugins']},
                         FROZEN_T01_CATALOG)
        actual = {}
        for plugin in (ROOT / 'plugins').iterdir():
            for path in plugin.glob('skills/*/SKILL.md'):
                fields, _ = frontmatter(path)
                actual[f"{plugin.name}:{fields['name']}"] = str(path.relative_to(ROOT))
        self.assertEqual(len(FROZEN_T01_SKILLS), 70)
        self.assertEqual(actual, FROZEN_T01_SKILLS)

    def test_t01_wrapper_set_links_and_descriptions_are_preserved(self):
        actual = {}
        for kind in ('commands', 'agents'):
            for source in (ROOT / 'plugins').glob(f'*/{kind}/*.md'):
                target = source.parent.parent / 'skills' / source.stem / 'SKILL.md'
                fields, body = frontmatter(source)
                shared_fields, _ = frontmatter(target)
                actual[str(source.relative_to(ROOT))] = str(target.relative_to(ROOT))
                self.assertIn(f'../skills/{source.stem}/SKILL.md', body)
                def value(raw):
                    return json.loads(raw) if raw.startswith('"') else raw
                self.assertEqual(value(fields['description']), value(shared_fields['description']))
        self.assertEqual(len(FROZEN_T01_WRAPPERS), 23)
        self.assertEqual(actual, FROZEN_T01_WRAPPERS)

    def test_external_workflow_provider_is_optional_in_both_manifests(self):
        for plugin in (ROOT / 'plugins').iterdir():
            for host in ('.claude-plugin', '.codex-plugin'):
                with self.subTest(plugin=plugin.name, host=host):
                    manifest = json.loads((plugin / host / 'plugin.json').read_text())
                    self.assertFalse(hard_workflow_provider(manifest))
        for dependency in ('superpowers@claude-plugins-official', 'SUPERPOWERS@other'):
            with self.subTest(reintroduced_dependency=dependency):
                sample = {'dependencies': [dependency]}
                self.assertTrue(hard_workflow_provider(sample))
        self.assertFalse(hard_workflow_provider({'keywords': ['optional superpowers']}))


if __name__ == '__main__':
    unittest.main()
