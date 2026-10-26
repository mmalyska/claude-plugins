"""Optional maintainer checks; plugin installation has no Python dependency."""

import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]


class CodexManifestTest(unittest.TestCase):
    def test_static_plugins_are_self_contained_and_cover_shared_workflows(self):
        catalog = json.loads((ROOT / ".claude-plugin/marketplace.json").read_text())
        for entry in catalog["plugins"]:
            with self.subTest(plugin=entry["name"]):
                plugin = (ROOT / entry["source"]).resolve()
                claude = json.loads((plugin / ".claude-plugin/plugin.json").read_text())
                codex = json.loads((plugin / ".codex-plugin/plugin.json").read_text())
                self.assertEqual(codex["name"], claude["name"])
                self.assertEqual(codex["version"], claude["version"])
                self.assertEqual(codex["hooks"], [])
                if entry["name"] == "android":
                    self.assertNotIn("skills", codex)
                    continue
                directory = plugin / codex["skills"]
                self.assertTrue(directory.is_dir())
                referenced = set()
                for skill in directory.glob("*/SKILL.md"):
                    text = skill.read_text()
                    self.assertIn(f"name: {skill.parent.name}\n", text)
                    self.assertRegex(text, r"(?m)^description: .+")
                    for relative in re.findall(r"\]\(([^)]+)\)", text):
                        target = (skill.parent / relative).resolve()
                        self.assertTrue(target.is_relative_to(plugin), target)
                        self.assertTrue(target.is_file(), target)
                        referenced.add(target)
                if entry["name"] == "personal-essentials":
                    setup = (directory / "personal-setup/SKILL.md").read_text()
                    for other in catalog["plugins"]:
                        if other["name"] not in ("personal-essentials", "android"):
                            self.assertIn(f'codex plugin add {other["name"]}@{catalog["name"]}', setup)
                    self.assertNotIn("claude plugin install", setup)
                    continue
                expected = set(plugin.glob("skills/*/SKILL.md"))
                expected.update(plugin.glob("commands/*.md"))
                expected.update(plugin.glob("agents/*.md"))
                expected.update(plugin.glob("rules/**/*.md"))
                self.assertTrue(expected.issubset(referenced), expected - referenced)


if __name__ == "__main__":
    unittest.main()
