# OpenCode metadata verification — 2026-10-27

## Scope and result

After authorizing Claude/Codex metadata checks, the user explicitly suggested
including locally available OpenCode. This extends the CLI/metadata scope only;
no model turn, new actor, production adapter or runtime operation is authorized.
DEEP + SOLO remains in effect.

- Installed binary: `opencode v2.2.0`, Linux x86_64.
- Source/base: `5d3703739ffff207cdc98f606a32c260794bc6f8` (merged T11).
- Branch: `test/hybrid-ai-workflow-native-verification`; primary stays clean on main.
- Result: **PASS for explicit-source skill metadata**, with 70/70 canonical skill
  IDs, expected copied-source paths, matching bodies and valid plugin-local links.
- Each owner alone, combined owners and all 12 catalog plugins passed configured,
  detached and reattached source checks: 15 records. No session or model turn was
  created. No Claude/Codex/OpenCode production plugin source was edited.
- This is a temporary manual source configuration, not native marketplace install,
  native adapter, hook enforcement, actor behavior or full workflow acceptance.

See [structured observations](2026-10-27-opencode-metadata.json) for all selected
IDs and counts, and [Claude/Codex evidence](2026-10-27-native-metadata.md) for the
independent strict Codex failure. That failure still blocks release.

## Version-specific discovery and isolation

Actual local --help confirmed v2 syntax. The v1 `debug skill` interface is absent;
using v1 commands/schema here would not establish v2 compatibility. Interface
references checked: [v2 CLI](https://dev.opencode.ai/v2/docs/cli),
[v2 skills](https://dev.opencode.ai/v2/docs/skills),
[v2 API](https://dev.opencode.ai/v2/docs/api) and
[v2 config](https://dev.opencode.ai/v2/docs/config).

Each case supplies temporary XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_CACHE_HOME and
XDG_STATE_HOME; HOME is unchanged. `debug paths` confirmed those directory roots;
the host's general temporary root remains `/tmp/opencode`. The test uses a fresh
workspace and a disposable full plugin-tree copy, preserving resource-relative
paths. Only that workspace gets an `opencode.json` with explicit local `skills`
roots; no installed source is renamed, flattened or adapted in this repository.
Warming and snapshots are disabled in the trial config.

Metadata queries use a private foreground loopback server that is always terminated
in finally; the user's shared background service is neither reused nor reconfigured.
Requests are GET `/api/skill`, `/api/config` and `/api/session`. Server-generated
credentials stay transient and are excluded/redacted from saved observations.
API keys are removed from the child environment. No message, generation, session
creation, tool execution or agent launch endpoint is called.

OpenCode can also read global Claude-compatible skill metadata despite the fresh
XDG roots. Trial assertions filter by the disposable source path and verify exact
expected project IDs/paths/content, not a count of unrelated global/builtin skills.
No user-global file is edited, and unrelated metadata is excluded from evidence.
Thus this is write-isolated configuration with selected-source assertions, not a
claim that OpenCode reads no user-global metadata.

## Probe failures and asynchronous readiness

- In the sandbox, the private-server CLI exited before readiness. The same bounded
  test was retried through normal escalated execution and the server started.
- A one-shot `api --standalone skill.list` returned an empty list immediately,
  including with a correctly loaded explicit skills source. This is not treated
  as proof of incompatibility or as successful discovery.
- A persistent private server showed that skills appear asynchronously. Trials
  now poll until a known harmless local metadata sentinel and the full expected
  source-ID set are present, under a 20-second deadline. A timeout is a failure;
  no early empty response is accepted. Removing v1-only environment assumptions
  did not change the need to wait for registration.
- A direct HTTP probe without the private server's generated credential returned
  401; authenticated metadata requests subsequently succeeded. The transient
  server was terminated after each attempt and no live credential is published.

## Actual observations

| Selection | Source state | Canonical skills | Result | Readiness polls |
| --- | --- | --- | --- | --- |
| development-lifecycle | configured | 22 | PASS | 6 |
| development-lifecycle | detached | 0 | PASS | 6 |
| development-lifecycle | reattached | 22 | PASS | 6 |
| git-workflows | configured | 5 | PASS | 6 |
| git-workflows | detached | 0 | PASS | 6 |
| git-workflows | reattached | 5 | PASS | 6 |
| agent-toolkit | configured | 14 | PASS | 6 |
| agent-toolkit | detached | 0 | PASS | 6 |
| agent-toolkit | reattached | 14 | PASS | 6 |
| owners combined | configured | 41 | PASS | 6 |
| owners combined | detached | 0 | PASS | 6 |
| owners combined | reattached | 41 | PASS | 6 |
| all 12 plugins | configured | 70 | PASS | 6 |
| all 12 plugins | detached | 0 | PASS | 6 |
| all 12 plugins | reattached | 70 | PASS | 6 |

Configured and reattached phases check discovered path and frontmatter-stripped
body against source, plus links with the existing plugin-contained checker. Each
copied plugin also passes source manifest/resource/wrapper assertions. Detached
means an empty explicit `skills` array and no selected-source skill registrations;
reattached means restoring the source roots and starting a new private process.
This is source discovery/reload smoke, **not package uninstall/reinstall**.

V2 IDs here are unqualified directory IDs such as `spec`, not Codex's
`development-lifecycle:spec` namespace. No alias/namespace adapter is generated.
Existing source IDs are globally unique in the frozen 70-skill inventory, so no
selected-source collision was observed. Agent definitions and Claude hooks were
not registered or exercised; profile/topology obedience is NOT RUN.

## Equivalent reproduction

Run only in a metadata-authorized session from repository root, with installed
OpenCode 2.2.0. The script is bounded metadata code, not an automatic release gate
or a scenario/model runner. It does not invoke skills as model tasks.

```python
from pathlib import Path
import os,sys,json,tempfile,subprocess,shutil,socket,time,urllib.request,urllib.parse,re,base64
sys.path.insert(0,str(Path.cwd()/'tests'))
from test_host_discovery import ROOT,OWNER_CASES,FROZEN_T01_CATALOG,FROZEN_T01_SKILLS,HostDiscoveryTest
from test_codex_manifests import frontmatter,plugin_link_errors
check=HostDiscoveryTest('test_claude_accepts_marketplace_and_plugin_contents')
results=[]
for selected in (*OWNER_CASES,tuple(FROZEN_T01_CATALOG)):
 with tempfile.TemporaryDirectory(prefix='workflow-opencode-skills-') as temporary:
  root=Path(temporary);env={k:v for k,v in os.environ.items() if not k.startswith('OPENCODE_') and not k.endswith('_API_KEY')}
  for kind in ('CONFIG','DATA','CACHE','STATE'):
   p=root/kind.lower();p.mkdir();env[f'XDG_{kind}_HOME']=str(p)
  env.update(OPENCODE_DISABLE_AUTOUPDATE='true',OPENCODE_DISABLE_MODELS_FETCH='true')
  workspace=root/'workspace';workspace.mkdir();snapshot=root/'source';snapshot.mkdir();shutil.copytree(ROOT/'plugins',snapshot/'plugins')
  sentinel=workspace/'.opencode/skills/metadata-probe';sentinel.mkdir(parents=True)
  (sentinel/'SKILL.md').write_text('---\nname: metadata-probe\ndescription: Metadata-only fixture.\n---\nNo model invocation.\n')
  expected={identity.split(':',1)[1]:snapshot/path for identity,path in FROZEN_T01_SKILLS.items() if identity.split(':',1)[0] in selected}
  for name in selected:check.assert_installed_content(name,snapshot/FROZEN_T01_CATALOG[name])
  for phase in ('configured','detached','reattached'):
   paths=[] if phase=='detached' else [str(snapshot/'plugins'/name/'skills') for name in selected if (snapshot/'plugins'/name/'skills').is_dir()]
   config={'skills':paths,'warming':False,'snapshots':False}
   (workspace/'opencode.json').write_text(json.dumps(config))
   with socket.socket() as sock:sock.bind(('127.0.0.1',0));port=sock.getsockname()[1]
   with tempfile.TemporaryFile(mode='w+') as log:
    server=subprocess.Popen(['opencode','serve','--hostname','127.0.0.1','--port',str(port)],env=env,cwd=workspace,stdout=log,stderr=log,text=True)
    try:
     query=urllib.parse.urlencode({'location[directory]':str(workspace)})
     def request(route):
      log.seek(0);text=log.read();password=re.search(r'^server password (.+)$',text,re.M)
      if not password:raise RuntimeError('Waiting for private-server readiness')
      headers={'Authorization':'Basic '+base64.b64encode(('opencode:'+password[1]).encode()).decode()}
      req=urllib.request.Request(f'http://127.0.0.1:{port}{route}?{query}',headers=headers)
      with urllib.request.urlopen(req,timeout=3) as response:return json.load(response)
     wanted={} if phase=='detached' else expected
     deadline=time.monotonic()+20;polls=0
     while True:
      polls+=1
      try:
       payload=request('/api/skill');skills=payload['data']
       own={item['id']:item for item in skills if item.get('path') and Path(item['path']).is_relative_to(snapshot)}
       if 'metadata-probe' in {item['id'] for item in skills} and set(own)==set(wanted):break
      except (OSError,RuntimeError):pass
      if server.poll() is not None or time.monotonic()>deadline:raise AssertionError('Metadata discovery did not reach the expected set')
      time.sleep(.15)
     for name,path in wanted.items():
      check.assertEqual(Path(own[name]['path']),path)
      header,body=frontmatter(path)
      check.assertEqual(own[name]['content'].strip(),body.strip())
      plugin=snapshot/'plugins'/next(identity.split(':',1)[0] for identity in FROZEN_T01_SKILLS if identity.split(':',1)[1]==name)
      check.assertEqual(plugin_link_errors(path,plugin),[])
     cfg=request('/api/config');check.assertTrue(any(item.get('info',{}).get('skills')==paths for item in cfg))
     sessions=request('/api/session');check.assertEqual(sessions.get('data',[]),[])
     row={'host':'opencode','version':'2.2.0','plugins':list(selected),'phase':phase,'canonical_skills':len(wanted),'result':'PASS','ids':sorted(wanted),'polls':polls,'session_count':0,'model_turns':0,'source_mode':'explicit local skills config; no production adapter'}
     results.append(row);print(json.dumps({k:v for k,v in row.items() if k!='ids'}),flush=True)
    finally:
     server.terminate()
     try:server.wait(timeout=5)
     except subprocess.TimeoutExpired:server.kill();server.wait(timeout=5)
Path('/tmp/hybrid-opencode-smoke-results.json').write_text(json.dumps(results,indent=2)+'\n')
print('PASS: explicit-source metadata only; no native plugin adapter or live behavior acceptance',flush=True)
```

## Acceptance and next work

This closes a bounded part of the pinned-version OpenCode spike: CLI shape,
configuration isolation and existing shared-skill metadata/body discovery. It does
not complete instruction precedence, permission mapping, worktree behavior,
QUICK + SOLO / HANDOFF / REVIEW live trials, native packaging, fresh package
install/reinstall, cross-host handoff or runtime refusal acceptance. Those remain
NOT RUN or deferred and need their own accepted scope. No additional actor, PR,
release, consumer migration or production adapter is created here.
