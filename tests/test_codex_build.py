"""Packaging invariants for the generated Codex distribution."""

import importlib.util
import json
from pathlib import Path
import re
import tempfile
import unittest

spec = importlib.util.spec_from_file_location("build_codex", Path(__file__).resolve().parents[1] / "scripts/build_codex.py")
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


class CodexBuildTest(unittest.TestCase):
    def test_self_contained_marketplace_and_aggregate(self):
        with tempfile.TemporaryDirectory() as temporary:
            original = builder.OUTPUT
            builder.OUTPUT = Path(temporary) / "codex"
            try:
                root = builder.build()
                catalog = json.loads((root / ".agents/plugins/marketplace.json").read_text())
                individual = set()
                for entry in catalog["plugins"]:
                    plugin = root / entry["source"]["path"]
                    manifest = json.loads((plugin / ".codex-plugin/plugin.json").read_text())
                    self.assertEqual(manifest["name"], entry["name"])
                    self.assertNotIn("hooks", manifest)
                    self.assertFalse(list(plugin.rglob("hooks.json")))
                    names = set()
                    for skill in plugin.glob("skills/*/SKILL.md"):
                        names.add(skill.parent.name)
                        text = skill.read_text()
                        self.assertIn(f"name: {skill.parent.name}\n", text)
                        reference = re.search(r"\[the shared workflow\]\(([^)]+)\)", text)[1]
                        target = (skill.parent / reference).resolve()
                        self.assertTrue(target.is_relative_to(plugin.resolve()))
                        self.assertTrue(target.is_file(), target)
                    if entry["name"] == "personal-essentials":
                        aggregate = names
                    else:
                        individual.update(names)
                self.assertEqual(individual, aggregate)
                # Rebuilding removes stale generated files and is reproducible.
                before = {str(p.relative_to(root)): p.read_bytes() for p in root.rglob("*") if p.is_file()}
                (root / "stale").write_text("obsolete")
                builder.build()
                after = {str(p.relative_to(root)): p.read_bytes() for p in root.rglob("*") if p.is_file()}
                self.assertEqual(before, after)
            finally:
                builder.OUTPUT = original


if __name__ == "__main__":
    unittest.main()
