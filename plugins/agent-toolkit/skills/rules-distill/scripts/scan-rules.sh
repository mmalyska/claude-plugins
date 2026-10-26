#!/usr/bin/env bash
# scan-rules.sh — enumerate rule files and extract H2 heading index
# Usage: scan-rules.sh [RULES_DIR_OR_FILE]
# Output: JSON to stdout
#
# Environment:
#   RULES_DISTILL_DIR  Override the source path; accepts either host's Markdown rules

set -euo pipefail

RULES_DIR="${RULES_DISTILL_DIR:-${1:-$HOME/.claude/rules}}"

if [[ ! -d "$RULES_DIR" && ! -f "$RULES_DIR" ]]; then
  jq -n --arg path "$RULES_DIR" '{"error":"rules source not found","path":$path}' >&2
  exit 1
fi

# Collect all .md files (excluding _archived/)
files=()
total=0
while IFS= read -r f; do
  files+=("$f")
  total=$((total+1))
done < <(find "$RULES_DIR" -name '*.md' -not -path '*/_archived/*' -type f -print | sort)

tmpdir=$(mktemp -d)
_rules_cleanup() { rm -rf "$tmpdir"; }
trap _rules_cleanup EXIT

for ((i=0; i<total; i++)); do
  file="${files[$i]}"
  rel_path="$file"
  if [[ "$file" == "$HOME/"* ]]; then
    rel_path="~/${file#"$HOME"/}"
  fi

  # Extract H2 headings (## Title) into a JSON array via jq
  headings_json=$({ grep -E '^## ' "$file" 2>/dev/null || true; } | sed 's/^## //' | jq -R . | jq -s '.')

  # Get line count
  line_count=$(wc -l < "$file" | tr -d ' ')

  jq -n \
    --arg path "$rel_path" \
    --arg file "$(basename "$file")" \
    --argjson lines "$line_count" \
    --argjson headings "$headings_json" \
    '{path:$path,file:$file,lines:$lines,headings:$headings}' \
    > "$tmpdir/$i.json"
done

if [[ $total -eq 0 ]]; then
  jq -n --arg dir "$RULES_DIR" '{rules_dir:$dir,total:0,rules:[]}'
else
  jq -n \
    --arg dir "$RULES_DIR" \
    --argjson total "$total" \
    --argjson rules "$(jq -s '.' "$tmpdir"/*.json)" \
    '{rules_dir:$dir,total:$total,rules:$rules}'
fi
