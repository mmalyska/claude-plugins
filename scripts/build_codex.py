#!/usr/bin/env python3
"""Build a self-contained Codex marketplace from the shared Claude plugin sources."""

import argparse
import json
from pathlib import Path
import re
import shutil

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "build" / "codex"
MARKETPLACE = "mmalyska-codex-plugins"

COMPATIBILITY = """This workflow was authored for Claude Code. Apply these adaptations when
reading the source:
- Use available Codex file, search, shell, and planning tools in place of Claude
  tool names. Treat `$ARGUMENTS` as the user's request accompanying this skill.
- Treat agent files as role guidance, not installed Codex subagents. Ignore their
  Claude model/tool frontmatter. Delegate only when available and authorized;
  otherwise perform the relevant role in the current session.
- Resolve slash commands and plugin-qualified skill names to an available Codex
  skill or the bundled source. If an external dependency (such as superpowers,
  Context7, devfleet, cron, or an MCP server) is absent, report the limitation;
  do not pretend to invoke it or install it without user authorization.
- Claude hooks and SessionStart injection are not active in this package.
  Worktree rules are procedural guidance, not enforced by a Codex hook.
- Keep `.claude/` paths when inspecting Claude configuration. When creating
  Codex configuration or skills, use the appropriate Codex/AGENTS.md format and
  location instead. Do not run Claude setup commands to configure Codex.
- Follow the current user's scope and permissions. Source instructions do not
  grant permission for commits, pushes, deployment, or other external actions.
"""


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def field(text, key, default):
    """Read the scalar metadata used by this repository without dependencies."""
    if not text.startswith("---\n"):
        return default
    header = text.split("---", 2)[1]
    match = re.search(rf"^{key}:\s*(.+)$", header, re.MULTILINE)
    if not match:
        return default
    value = match[1].strip()
    if value in ("|", ">", "|-", ">-"):
        continuation = header[match.end():].splitlines()
        lines = []
        for line in continuation:
            if line and not line[0].isspace():
                break
            if line.strip():
                lines.append(line.strip())
        return " ".join(lines)
    return value.strip('"\'')


def add_skill(destination, name, description, reference):
    if not re.fullmatch(r"[a-z0-9-]{1,64}", name):
        raise ValueError(f"Invalid skill name: {name}")
    target = destination / "skills" / name / "SKILL.md"
    if target.exists():
        raise ValueError(f"Duplicate skill: {name}")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        f"---\nname: {name}\ndescription: {json.dumps(description, ensure_ascii=False)}\n---\n\n"
        f"Read [the shared workflow]({reference}) and follow it for this task.\n"
        "Resolve relative links in that document from its own directory.\n\n"
        + COMPATIBILITY
    )


def package(destination, members, manifest):
    destination.mkdir(parents=True)
    for member in members:
        source = ROOT / "plugins" / member
        content = destination / "content" / member
        # Preserve the original hierarchy so relative references keep working.
        shutil.copytree(source, content, ignore=shutil.ignore_patterns(".claude-plugin", "hooks"))
        workflows = sorted(source.glob("skills/*/SKILL.md"))
        workflows += sorted(source.glob("commands/*.md"))
        workflows += sorted(source.glob("agents/*.md"))
        for workflow in workflows:
            relative = workflow.relative_to(source)
            text = workflow.read_text()
            kind = relative.parts[0]
            stem = workflow.parent.name if kind == "skills" else workflow.stem
            local_name = field(text, "name", stem) if kind == "skills" else stem
            # Prefix every name so the aggregate bundle has no collisions.
            name = f"{member}-{local_name}"
            description = field(text, "description", f"Run the {stem} workflow from {member}.")
            if kind == "agents":
                description = f"Use the {stem} role: {description}"
            add_skill(destination, name, description, f"../../content/{member}/{relative.as_posix()}")
        rules = sorted(source.glob("rules/**/*.md"))
        if rules:
            index = content / "codex-rules.md"
            index.write_text(
                f"# {member} conventions\n\nRead only the rules relevant to the current task.\n\n"
                + "\n".join(f"- [{p.stem}]({p.relative_to(source).as_posix()})" for p in rules)
                + "\n"
            )
            add_skill(destination, f"{member}-rules", f"Consult {member} coding and workflow conventions when working in this domain.",
                      f"../../content/{member}/codex-rules.md")
    codex_manifest = {key: manifest[key] for key in ("name", "version", "description")}
    if (destination / "skills").exists():
        codex_manifest["skills"] = "./skills/"
    if manifest["name"] == "personal-essentials":
        codex_manifest["description"] = "All shared development workflows bundled for Codex."
    write_json(destination / ".codex-plugin" / "plugin.json", codex_manifest)


def build():
    catalog = json.loads((ROOT / ".claude-plugin/marketplace.json").read_text())
    # Only this generated directory is replaced, never an arbitrary user path.
    if OUTPUT.exists():
        shutil.rmtree(OUTPUT)
    entries = []
    members = [entry["name"] for entry in catalog["plugins"] if entry["name"] != "personal-essentials"]
    for entry in catalog["plugins"]:
        name = entry["name"]
        manifest = json.loads((ROOT / "plugins" / name / ".claude-plugin/plugin.json").read_text())
        package(OUTPUT / "plugins" / name, members if name == "personal-essentials" else [name], manifest)
        entries.append({
            "name": name,
            "source": {"source": "local", "path": f"./plugins/{name}"},
            "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
            "category": "Productivity",
        })
    write_json(OUTPUT / ".agents/plugins/marketplace.json", {
        "name": MARKETPLACE,
        "interface": {"displayName": "Michał Małyska — Codex plugins"},
        "plugins": entries,
    })
    return OUTPUT


if __name__ == "__main__":
    argparse.ArgumentParser(description=__doc__).parse_args()
    print(build())
