# Native metadata verification — 2026-10-27

## Scope and outcome

The user explicitly authorized CLI Claude/Codex installation and discovery tests
following merged T11 PR #19. Model turns, additional agents, non-SOLO actor trials,
runtime, consumer edits, commit/push/PR and release remain outside this instruction.
This is DEEP + SOLO with metadata processes only.

- Base/plugin SHA: `5d3703739ffff207cdc98f606a32c260794bc6f8`; Linux x86_64.
- Branch/worktree: `test/hybrid-ai-workflow-native-verification`,
  `/workspaces/claude-plugins/.worktrees/test/hybrid-ai-workflow-native-verification`.
- Installed CLI versions: Claude Code `2.1.312`; Codex CLI `0.164.0`.
- Runtime/tools: Python 3.15.0; local git/jq as recorded in the preceding T11 run.
- Source manifest versions remain lifecycle 1.2.6, git-workflows 1.3.4, toolkit 1.1.4.
- Strict native suite: Claude validation/install checks PASS; Codex discovery FAIL.
- Canonical content and actual remove/reinstall checks: PASS for both hosts.
  Actual Codex discovery contains all canonical identities at expected paths.
- Release remains BLOCKED by the Codex mismatch and remaining live/platform/rollback
  gates. This is not a full workflow conformance or model-behavior PASS.

[Structured observations](2026-10-27-native-metadata.json) contain all 20 phase
records. PASS in their content field concerns canonical source bytes and identities,
not generated aliases or overall native acceptance. Temporary host config is set
explicitly per case; HOME is unchanged. No real user plugin is removed.

## Failures found and bounded correction

Initial execution of the prepared suite used:

```sh
WORKFLOW_NATIVE_TESTS=1 python3 -B -m unittest discover -s tests -p test_host_discovery.py -v
```

Two Claude methods passed. All five Codex case configurations failed before
installation because the test set CODEX_HOME to a nonexistent directory:

```text
Error: failed to resolve CODEX_HOME
CODEX_HOME points to "<temporary-case>/config", but that path does not exist
```

The sole test change creates that temporary config directory before invoking
Codex. No source plugin, host adapter, manifest, wrapper or user config is edited.
After this correction a fail-fast rerun reached actual discovery: Claude's two
methods passed, Codex's first lifecycle case failed the strict identity comparison.
All 22 expected lifecycle skills and their paths were present; ten extra aliases
were observed. The original discovery equality assertion is retained, not relaxed.

## Codex generated aliases and link failure

At this pinned version the installed lifecycle contains host-generated skills at:

```text
<installPath>/.codex-plugin/migrated-command-skills/source-command-spec/SKILL.md
```

The inspected file contains:

```markdown
# source-command-spec

Use this skill when the user asks to run the migrated source command `spec`.

## Command Template

Read [the shared spec workflow](../skills/spec/SKILL.md) and follow it for this task.
```

Resolving that link relative to the generated Markdown file yields a missing
file. `plugin_link_errors` reports `missing-target`; it is not a failed canonical
skill link. All ten lifecycle command aliases have this pattern. Full-catalog
installation adds `personal-essentials:source-command-personal-setup`, also with
a missing relative target: **11 distinct extra aliases** in the complete catalog.
No command aliases were discovered for standalone git-workflows or agent-toolkit
in these trials; no inference about other host versions is made.

Canonical skills, resources and wrappers still pass byte/containment checks;
all 70 canonical skills are discovered and enabled. The host-created alias files
are additional to that source inventory. Diagnostic assertions permit only
observed aliases matching the frozen command-derived names and exact generated
paths, then record their link errors separately. They do not label those errors
PASS or change the strict prepared suite's failure. No alias was invoked and no
claim about a model's eventual interpretation of that link is established.

## Actual fresh and remove/reinstall trials

Each host used fresh temporary config and workspace per selection. The marketplace
and all plugin sources were copied into that same temporary case for removal
trials: Claude can load a local marketplace source in place through readFromFolder.
An early diagnostic correctly stopped when that source pointed outside the trial
root, before any uninstall; a disposable marketplace copy resolved this isolation
precondition. Source plugins in the real worktree remain untouched.

For each selection, commands installed only selected entries, checked enabled
registration and content, uninstalled/removed them, asserted the installed list
was empty, and installed/checks again. All 20 phase records completed. Codex
metadata RPCs were restricted to initialize, initialized and skills/list; no
thread or turn was created. The local diagnostic script's success exit refers
to these bounded assertions; generated-link failure remains explicitly FAIL.

| Host | Selection | Phase | Canonical skills | Content / selected registration | Extra aliases |
| --- | --- | --- | --- | --- | --- |
| claude | development-lifecycle | fresh | 22 | PASS | not applicable |
| claude | development-lifecycle | remove-reinstall | 22 | PASS | not applicable |
| claude | git-workflows | fresh | 5 | PASS | not applicable |
| claude | git-workflows | remove-reinstall | 5 | PASS | not applicable |
| claude | agent-toolkit | fresh | 14 | PASS | not applicable |
| claude | agent-toolkit | remove-reinstall | 14 | PASS | not applicable |
| claude | owners combined | fresh | 41 | PASS | not applicable |
| claude | owners combined | remove-reinstall | 41 | PASS | not applicable |
| claude | all 12 catalog plugins | fresh | 70 | PASS | not applicable |
| claude | all 12 catalog plugins | remove-reinstall | 70 | PASS | not applicable |
| codex | development-lifecycle | fresh | 22 | PASS | 10 |
| codex | development-lifecycle | remove-reinstall | 22 | PASS | 10 |
| codex | git-workflows | fresh | 5 | PASS | 0 |
| codex | git-workflows | remove-reinstall | 5 | PASS | 0 |
| codex | agent-toolkit | fresh | 14 | PASS | 0 |
| codex | agent-toolkit | remove-reinstall | 14 | PASS | 0 |
| codex | owners combined | fresh | 41 | PASS | 10 |
| codex | owners combined | remove-reinstall | 41 | PASS | 10 |
| codex | all 12 catalog plugins | fresh | 70 | PASS | 11 |
| codex | all 12 catalog plugins | remove-reinstall | 70 | PASS | 11 |

Claude metadata validation included the marketplace and all 12 plugins. Its
prepared repeat-install requests also passed. Actual remove/reinstall is separate
from those repeat requests. Codex actual remove/reinstall and canonical discovery
passed in all five configurations; discovery remains incomplete for strict
acceptance due to the generated aliases. Full catalog has 70 canonical + 11
additional generated skills in Codex for this version.

## Reproduction and evidence limits

Official interface references checked alongside actual local --help:
[Codex developer commands](https://learn.chatgpt.com/docs/developer-commands),
[metadata RPCs](https://learn.chatgpt.com/docs/app-server),
[Claude plugin commands](https://code.claude.com/docs/en/plugins/cli-reference).
The empirical results above are tied to installed versions, not inferred from docs.

The equivalent diagnostic loop below runs from this repository root only in a
metadata-authorized session. It uses the existing assertion/RPC helpers and never
reads scenario JSON as executable instructions. The exploratory run resumed Codex
separately after preserving Claude results; structured observations consolidate
both. The code below runs the same checks serially for both hosts. Its diagnostic
alias assertions intentionally describe this known version's failure, not a general
acceptance policy: after an alias fix, update them and rerun the strict suite.

```python
from pathlib import Path
import os,sys,json,tempfile,subprocess,hashlib,shutil
sys.path.insert(0,str(Path.cwd()/'tests'))
from test_host_discovery import HostDiscoveryTest,ROOT,MARKETPLACE,OWNER_CASES,FROZEN_T01_CATALOG,FROZEN_T01_WRAPPERS,plugin_link_errors
check=HostDiscoveryTest('test_codex_discovers_shared_skills_after_direct_install')
log=[]
def cli(host,args,env,workspace):
 out=check.cli(host,args,env,workspace)
 log.append({'host':host,'args':args,'exit':0,'stdout':out})
 return out
results=[]
for host in ('claude','codex'):
 for selected in (*OWNER_CASES,tuple(FROZEN_T01_CATALOG)):
  with tempfile.TemporaryDirectory(prefix=f'workflow-{host}-reinstall-') as temporary:
   root=Path(temporary);config=root/'config';config.mkdir();workspace=root/'workspace';workspace.mkdir()
   env=dict(os.environ,**{('CLAUDE_CONFIG_DIR' if host=='claude' else 'CODEX_HOME'):str(config)})
   snapshot=root/'marketplace'
   snapshot.mkdir()
   shutil.copytree(ROOT/'.claude-plugin',snapshot/'.claude-plugin')
   shutil.copytree(ROOT/'plugins',snapshot/'plugins')
   cli(host,['plugin','marketplace','add',str(snapshot)],env,workspace)
   for phase in ('fresh','remove-reinstall'):
    if phase=='remove-reinstall':
     for name in selected:
      args=['plugin','uninstall',f'{name}@{MARKETPLACE}','--scope','user','--json'] if host=='claude' else ['plugin','remove',f'{name}@{MARKETPLACE}','--json']
      cli(host,args,env,workspace)
     records=json.loads(cli(host,['plugin','list','--json'],env,workspace))
     check.assertEqual(records if host=='claude' else records['installed'],[])
    paths={}
    for name in selected:
     if host=='claude':
      cli(host,['plugin','install',f'{name}@{MARKETPLACE}','--scope','user','--json'],env,workspace)
     else:
      item=json.loads(cli(host,['plugin','add',f'{name}@{MARKETPLACE}','--json'],env,workspace));paths[name]=Path(item['installedPath'])
    records=json.loads(cli(host,['plugin','list','--json'],env,workspace))
    if host=='claude':
     check.assertEqual({item['id'] for item in records},{f'{name}@{MARKETPLACE}' for name in selected})
     for item in records:
      check.assertTrue(item['enabled']);check.assertFalse(item.get('errors'))
      paths[item['id'].split('@',1)[0]]=Path(item.get('readFromFolder') or item['installPath'])
    else:
     check.assertEqual({item['name'] for item in records['installed']},set(selected))
     for item in records['installed']:check.assertTrue(item['enabled'])
    expected={}
    for name,path in paths.items():
     check.assertTrue(path.resolve().is_relative_to(root.resolve()),path)
     expected.update(check.assert_installed_content(name,path))
    row={'host':host,'plugins':list(selected),'phase':phase,'canonical_skills':len(expected),'content':'PASS'}
    if host=='codex':
     rpc=check.codex_skill_list(env,workspace)
     actual={skill['name']:skill['path'] for entry in rpc['data'] for skill in entry['skills'] if any(skill['name'].startswith(f'{name}:') for name in selected)}
     for entry in rpc['data']:
      check.assertFalse(entry.get('errors'))
      for skill in entry['skills']:
       check.assertNotIn('superpowers:',skill['name'].lower())
       if skill['name'] in actual:check.assertTrue(skill['enabled'])
     check.assertEqual({name:path for name,path in actual.items() if name in expected},expected)
     alias_expected={}
     for source,target in FROZEN_T01_WRAPPERS.items():
      parts=Path(source).parts
      if parts[1] in selected and parts[2]=='commands':
       name=parts[1];alias=f'{name}:source-command-{Path(source).stem}'
       alias_expected[alias]=str(paths[name]/'.codex-plugin/migrated-command-skills'/f'source-command-{Path(source).stem}'/'SKILL.md')
     extras={name:path for name,path in actual.items() if name not in expected}
     check.assertTrue(set(extras)<=set(alias_expected))
     check.assertEqual(extras,{name:alias_expected[name] for name in extras})
     errors={alias:plugin_link_errors(Path(path),paths[alias.split(':')[0]]) for alias,path in extras.items()}
     row.update(canonical_discovery='PASS',host_alias_count=len(extras),alias_link_errors=errors)
     check.assertTrue(all(err and all(kind=='missing-target' for kind,link in err) for err in errors.values()))
     log.append({'host':host,'rpc':'initialize; initialized; skills/list','model_turns':0,'canonical':len(expected),'extra_aliases':len(extras)})
    results.append(row);print(json.dumps(row),flush=True)
Path('/tmp/hybrid-native-reinstall-results.json').write_text(json.dumps(results,indent=2)+'\n')
Path('/tmp/hybrid-native-reinstall-commands.json').write_text(json.dumps(log,indent=2)+'\n')
print('PASS: canonical content/fresh/remove-reinstall checks; generated Codex alias links remain FAIL',flush=True)
```

Raw exploratory logs are ephemeral under `/tmp/hybrid-native-*`; the structured
observations and explicit errors above are the durable redacted summary, not a
full archived stdout transcript of every CLI call. Do not substitute this record
for live S01–S16, Bash 3.2, previous-revision rollback or Git-backed marketplace
install verification. These trials used local marketplaces and the same candidate
revision for reinstall, not a release rollback. No plugin invocation/model trial,
real runtime mutation, home-ops/dotfiles edit, PR or release occurred.

## Next action and rollback

Review the host-generated alias mismatch and decide the supported command adapter
behavior before changing production packaging or weakening strict discovery gates.
Rerun native tests after an accepted fix and keep prior failure evidence. Live actor
trials, Bash 3.2 and actual prior-version rollback remain separately scoped work.
The local CODEX_HOME test fixture fix and evidence can be reverted together; preserve
user settings, providers and existing worktrees. No runtime rollback is implied.
