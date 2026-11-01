"""Static checks for docs/workflow/repository-adoption-guide.md.

These are static documentation assertions, not evidence of model behavior.
"""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GUIDE = ROOT / 'docs/workflow/repository-adoption-guide.md'
CONTRACT = ROOT / 'plugins/development-lifecycle/rules/common/workflow.md'

REQUIRED_SECTIONS = (
    '## 1. Purpose and ownership',
    '## 2. When to adopt, and how risk sets planning depth',
    '## 3. Instruction ownership model',
    '## 4. Repository audit before implementation',
    '## 5. Harness capability probes',
    '## 6. Choosing an adapter strategy',
    '## 7. Worktree-first enforcement and its limits',
    '## 8. Plan and archive conventions',
    '## 9. Permission boundaries and action classes',
    '## 10. Validation matrix',
    '## 11. CI patterns for instructions, plans and documentation',
    '## 12. Rollout as small, reversible PRs',
    '## 13. Migration, rollback and recovery',
    '## 14. Optional orchestration',
    '## 15. Lessons from the first adoptions',
    '## 16. Adoption checklist',
    '## 17. Templates',
)

TASK_FIELDS = (
    'Scope', 'Depends on', 'Tests', 'Expected result', 'Acceptance', 'Rollback',
    'Mutation consent',
)
PLAN_FRONT_MATTER = (
    'title', 'slug', 'status', 'profile', 'topology', 'owner', 'base_sha', 'branch',
    'worktree', 'workflow_ref', 'updated', 'next_action',
)
CANONICAL_LINKS = (
    '../../plugins/development-lifecycle/rules/common/workflow.md',
    'compatibility.md',
    '../../plugins/git-workflows/rules/worktree-workflow.md',
    '../../plugins/development-lifecycle/resources/workflow/plan.md',
    '../../plugins/development-lifecycle/resources/workflow/tasks.md',
)
LESSONS = (
    'Merge can be a production operation',
    'Build publishing documentation in the PR',
    'deterministic sync and drift tests',
    'stay NOT RUN',
    'No standing authorization',
)
PRIVATE_PATTERNS = {
    'ipv4': r'\b(?:\d{1,3}\.){3}\d{1,3}\b',
    'uuid': r'\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b',
    'private-tld': r'\b[\w-]+\.(?:local|lan|internal|home|corp|ts\.net)\b',
    'secret-assignment': r'(?i)\b(?:token|password|secret|api[_-]?key)\s*[:=]\s*\S+',
    'github-token': r'\bgh[pousr]_[A-Za-z0-9]{20,}\b',
}


def text():
    return GUIDE.read_text()


def fenced_blocks(source):
    """Return (info, body) for each fenced block, honoring longer outer fences."""
    blocks, lines, i = [], source.splitlines(), 0
    while i < len(lines):
        match = re.match(r'^(`{3,})(\S*)\s*$', lines[i])
        if match:
            fence, info, body, i = match.group(1), match.group(2), [], i + 1
            while i < len(lines) and lines[i].rstrip() != fence:
                body.append(lines[i])
                i += 1
            blocks.append((info, '\n'.join(body)))
        i += 1
    return blocks


class AdoptionGuideTests(unittest.TestCase):
    def test_required_sections_present_in_order(self):
        source = text()
        positions = [source.find(heading) for heading in REQUIRED_SECTIONS]
        for heading, position in zip(REQUIRED_SECTIONS, positions):
            self.assertNotEqual(position, -1, heading)
        self.assertEqual(positions, sorted(positions))

    def test_checklist_covers_every_phase(self):
        source = text()
        for heading in ('### A. Audit', '### B. Decisions', '### C. Implementation',
                        '### D. Verification', '### E. Unresolved items and NOT RUN'):
            self.assertIn(heading, source)
        self.assertGreaterEqual(len(re.findall(r'^- \[ \] ', source, re.M)), 40)

    def test_both_plan_templates_have_required_fields(self):
        blocks = [body for info, body in fenced_blocks(text()) if info == 'markdown']
        plan = next((b for b in blocks if b.startswith('---\ntitle:')), None)
        tasks = next((b for b in blocks if b.startswith('---\nplan:')), None)
        self.assertIsNotNone(plan, 'plan.md skeleton missing')
        self.assertIsNotNone(tasks, 'tasks.md skeleton missing')
        front = plan.split('---\n')[1]
        for key in PLAN_FRONT_MATTER:
            self.assertRegex(front, rf'(?m)^{key}:', key)
        for heading in ('Scope', 'Dependencies', 'Tests', 'Expected result',
                        'Acceptance criteria', 'Rollback', 'Mutation consent'):
            self.assertIn(f'## {heading}', plan)
        for field in TASK_FIELDS:
            self.assertIn(f'- {field}:', tasks, field)

    def test_templates_are_balanced_markdown(self):
        source = text()
        fence_lines = re.findall(r'^`{3,}', source, re.M)
        self.assertEqual(len(fence_lines) % 2, 0, 'unbalanced code fences')
        self.assertNotRegex(source, r'[ \t]+$', 'trailing whitespace')

    def test_links_resolve_and_canonical_links_present(self):
        source = text()
        for target in CANONICAL_LINKS:
            self.assertIn(f']({target}', source, target)
        stripped = re.sub(r'^(`{3,}).*?^\1\s*$', '', source, flags=re.M | re.S)
        for target in re.findall(r'\]\(([^)\s]+)\)', stripped):
            if re.match(r'[a-z]+:', target):
                continue
            path, _, anchor = target.partition('#')
            resolved = (GUIDE.parent / path).resolve() if path else GUIDE
            self.assertTrue(resolved.exists(), f'broken link: {target}')
            if anchor and resolved.suffix == '.md':
                self.assertIn(anchor, heading_anchors(resolved.read_text()), target)

    def test_definitions_are_linked_not_copied(self):
        source = text()
        contract = CONTRACT.read_text()
        self.assertNotIn('Spec → Plan → Build', source)
        self.assertNotIn('Spec -> Plan -> Build', source)
        for line in contract.splitlines():
            if line.startswith('| SOLO |') or line.startswith('| HANDOFF |') \
                    or line.startswith('| PARALLEL |') or line.startswith('| REVIEW |'):
                self.assertNotIn(line, source)
        self.assertNotRegex(source, r'(?m)^\| (?:Spec|Plan|Build|Test|Review|Simplify|Ship) \|')
        self.assertIn('never restate the lifecycle', source)

    def test_generalized_lessons_present(self):
        source = text()
        for lesson in LESSONS:
            self.assertIn(lesson, source)
        self.assertIn('PASS', source)
        self.assertIn('NOT RUN', source)

    def test_no_private_infrastructure_values(self):
        source = text()
        for name, pattern in PRIVATE_PATTERNS.items():
            self.assertIsNone(re.search(pattern, source), name)

    def test_indexed_from_readme_and_compatibility(self):
        self.assertIn('docs/workflow/repository-adoption-guide.md',
                      (ROOT / 'README.md').read_text())
        self.assertIn('repository-adoption-guide.md',
                      (ROOT / 'docs/workflow/compatibility.md').read_text())


def heading_anchors(markdown):
    anchors = set()
    for heading in re.findall(r'^#{1,6}\s+(.+?)\s*$', markdown, re.M):
        slug = re.sub(r'[^\w\- ]', '', heading.lower()).replace(' ', '-')
        anchors.add(slug)
    return anchors


if __name__ == '__main__':
    unittest.main()
