"""Offline repository context inventory; no host launches, config reads or installs."""
from pathlib import Path
import argparse
import collections
import hashlib
import json
import re
import subprocess

ROOT = Path(__file__).resolve().parents[3]
BASE = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
PLUGIN_DIRTY = bool(subprocess.check_output(
    ['git', 'status', '--porcelain', '--', 'plugins'], cwd=ROOT, text=True).strip())


def parts(text):
    match = re.match(r'\A---\n(.*?)\n---\n', text, re.S)
    return (match.group(1), text[match.end():]) if match else ('', text)


def examples(text):
    prose, fenced = [], []
    fence = None
    for line in text.splitlines(keepends=True):
        mark = re.match(r'^\s*(`{3,}|~{3,})', line)
        if fence:
            if mark and mark[1][0] == fence[0] and len(mark[1]) >= len(fence):
                fence = None
            else:
                fenced.append(line)
        elif mark:
            fence = mark[1]
        else:
            prose.append(line)
    return ''.join(prose), ''.join(fenced)


def field(frontmatter, name):
    found = re.search(r'^' + name + r':\s*(.+)$', frontmatter, re.M)
    if not found:
        return None
    value = found[1]
    return json.loads(value) if value.startswith('"') else value


rows = []
repeated = collections.defaultdict(list)
files = sorted(str(path.relative_to(ROOT)) for path in (ROOT / 'plugins').rglob('*')
               if path.is_file() and '__pycache__' not in path.parts)
for relative in files:
    path = ROOT / relative
    text = path.read_text()
    frontmatter, body = parts(text)
    if path.name == 'SKILL.md':
        kind = 'skill'
    elif '/rules/' in relative:
        kind = 'rule'
    elif '/agents/' in relative:
        kind = 'agent-adapter'
    elif '/commands/' in relative:
        kind = 'command-adapter'
    elif '/resources/' in relative:
        kind = 'resource'
    elif path.name == 'plugin.json':
        kind = 'manifest'
    elif '/skills/' in relative and path.suffix == '.md':
        kind = 'reference'
    else:
        kind = 'readme-or-script'
    prose, fenced = examples(body)
    name, description = field(frontmatter, 'name'), field(frontmatter, 'description')
    row = {
        'path': relative, 'plugin': relative.split('/')[1],
        'kind': kind, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
        'bytes': len(text.encode()), 'characters': len(text), 'lines': len(text.splitlines()),
        'body_characters': len(body), 'fenced_example_characters': len(fenced),
        'prose_words': len(prose.split()),
        'rough_body_tokens': round(len(prose.split()) * 1.3 + len(fenced) / 4),
        'name': name, 'description': description,
        'catalog_characters': len(name + ': ' + description) if kind == 'skill' else 0,
        'links': re.findall(r'\]\(([^)]+)\)', body),
    }
    rows.append(row)
    if kind == 'skill':
        for paragraph in re.split(r'\n\s*\n', body):
            normalized = ' '.join(paragraph.split())
            if len(normalized) > 220:
                repeated[normalized].append(relative)

plugins = []
for plugin in sorted({row['plugin'] for row in rows}):
    members = [row for row in rows if row['plugin'] == plugin]
    plugins.append({
        'plugin': plugin, 'file_count': len(members),
        'skills': sum(row['kind'] == 'skill' for row in members),
        'skill_file_bytes': sum(row['bytes'] for row in members if row['kind'] == 'skill'),
        'rules': sum(row['kind'] == 'rule' for row in members),
        'rule_file_bytes': sum(row['bytes'] for row in members if row['kind'] == 'rule'),
        'catalog_characters': sum(row['catalog_characters'] for row in members),
    })

metadata = '\n'.join(row['name'] + ': ' + row['description'] for row in rows if row['kind'] == 'skill')
result = {
    'audit_date': '2026-10-30', 'source_revision': BASE,
    'plugin_source_dirty': PLUGIN_DIRTY,
    'known_merged_pr37_revision': 'ae10c049c4e0d1667d7544199a980854d96794c3',
    'scope': 'Plugin source including new local references; no private host configuration, runtime schemas or model usage.',
    'method': 'Exact UTF-8 bytes/characters; rough prose words * 1.3 + fenced-example characters / 4. No matching model tokenizer or host context counter available. No total is an actual session usage measurement.',
    'skill_count': sum(row['kind'] == 'skill' for row in rows),
    'skill_file_bytes': sum(row['bytes'] for row in rows if row['kind'] == 'skill'),
    'catalog_characters': len(metadata) - metadata.count('\n'),
    'catalog_words': len(metadata.split()), 'catalog_rough_tokens': round(len(metadata.split()) * 1.3),
    'plugins': plugins, 'files': rows,
    'repeated_skill_paragraphs': [
        {'normalized_characters': len(text), 'copies': len(paths),
         'redundant_source_characters': len(text) * (len(paths) - 1),
         'sample': text[:180], 'paths': paths}
        for text, paths in sorted(repeated.items(), key=lambda item: len(item[0]) * (len(item[1]) - 1), reverse=True)
        if len(paths) > 1
    ],
}
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output', type=Path, required=True,
                    help='Write a new measurement, preserving the audit baseline.')
target = parser.parse_args().output
target.write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n')
print(f'{len(rows)} files; {len(plugins)} plugins; {result["skill_count"]} skills; {result["skill_file_bytes"]} skill-file bytes')
print(f'Catalog text: {result["catalog_characters"]} characters; ~{result["catalog_rough_tokens"]} rough tokens, excluding host formatting')
