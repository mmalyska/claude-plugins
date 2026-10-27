# Specyfikacja techniczna: hybrydowy, harness-agnostic AI Engineering Workflow

**Repozytoria:** `mmalyska/claude-plugins`, `mmalyska/dotfiles`, `mmalyska/home-ops`  
**Harnessy:** Claude Code, Codex, przyszły OpenCode  
**Status:** propozycja do wdrożenia, bez zmian w repozytoriach  
**Stan źródeł:** 2026-10-27 (Europe/Warsaw)  
**Decyzja architektoniczna:** Hybrid — wspólny kontrakt i artefakty, natywne możliwości harnessów, opcjonalna orkiestracja

## 1. Cel

Celem jest jeden przewidywalny workflow inżynierski, który:

- działa z jednym agentem i z wieloma agentami;
- nie wymaga konkretnego modelu, CLI, pluginu ani usługi orkiestrującej;
- pozwala zmieniać harness w trakcie zadania bez utraty stanu;
- zachowuje worktree-first, istniejące skills oraz historię `.plans`;
- traktuje Superpowers jako opcjonalny dostawca procedur, a nie warstwę sterującą;
- respektuje szczególne ryzyko `home-ops`: GitOps, Talos, ArgoCD, Terraform, Kubernetes i sekrety.

Poza zakresem pierwszej wersji są: własny scheduler, daemon wieloagentowy, ujednolicanie API narzędzi poszczególnych harnessów oraz automatyczne wykonywanie operacji na klastrze.

## 2. Stan zastany i wnioski z przeglądu

### 2.1 `claude-plugins`

Stan głównej gałęzi odpowiada commitowi `8396c61` z 2026-10-26. Repozytorium jest już kolekcją dla Claude Code **i Codex**, nie tylko Claude:

- `.claude-plugin/marketplace.json` publikuje 12 pluginów, m.in. `git-workflows`, `development-lifecycle`, `agent-toolkit`, `devops` i `security`;
- wspólne procedury są w `plugins/*/skills/*/SKILL.md` i są czytane bezpośrednio przez oba harnessy;
- Claude zachowuje natywne commands, agents i hooks jako cienkie entrypointy;
- Codex używa `.codex-plugin/plugin.json`, namespaced skills `$<plugin>:<skill>` i jawnie pustego `hooks: []`;
- `development-lifecycle` dostarcza m.in. `spec`, `test`, `review`, `code-review`, `simplify`, `ship` i role;
- `agent-toolkit` dostarcza m.in. blueprint, team-builder, safety-guard, eval-harness i verification-loop;
- `git-workflows` definiuje invariant: primary checkout nie jest workspace; zapis odbywa się w `.worktrees/<type>/<slug>`;
- Claude ma `PreToolUse` guard i wstrzyknięcie reguły przy `SessionStart`; Codex stosuje tę samą zasadę proceduralnie, bez interceptora.

Wniosek: nie należy budować drugiego katalogu adapterów Codex. Obecny model „shared skill body + cienkie natywne entrypointy” jest właściwym rdzeniem rozwiązania. Kanonicznym lifecycle pozostaje istniejący proces `Spec → Plan → Build → Test → Review → Simplify → Ship`. Brakuje przede wszystkim formalnego kontraktu profili QUICK/STANDARD/DEEP, topologii wykonania, kontraktu artefaktów i adaptera OpenCode.

### 2.2 `dotfiles`

Stan głównej gałęzi odpowiada commitowi `96a0802` z 2026-10-10. Repo jest warstwą dystrybucji środowiska przez chezmoi:

- `home/run_once_install-claude-plugins.sh` rejestruje prywatny i oficjalny marketplace oraz instaluje własny zestaw pluginów;
- ten sam skrypt nadal instaluje Superpowers oraz inne oficjalne pluginy Claude;
- `home/dot_claude/settings.json.tmpl` włącza agent teams, hooki powiadomień, własne pluginy i Superpowers;
- konfiguracja uwzględnia różne systemy oraz devcontainery.

Wniosek: `dotfiles` ma instalować i konfigurować harnessy, lecz nie być źródłem workflow. Superpowers powinien pozostać instalowalnym profilem opcjonalnym. Instalacja musi być idempotentna i nie może powodować, że brak jednego harnessu blokuje pozostałe.

### 2.3 `home-ops`

Stan głównej gałęzi odpowiada commitowi `24024f1` z 2026-10-27. Repo ma:

- rozbudowany, wyłącznie Claude-centryczny `CLAUDE.md`; brak `AGENTS.md`;
- project skills w `.claude/skills/`, np. `add-app` i `dev-workflow`;
- aktywne plany w `.plans/` i archiwum w `.archive/.plans/`;
- dwa historyczne formaty planów: foldery `plan.md` + `tasks.md` oraz Superpowers `specs/`/`plans/`/`artifacts/`;
- pusty obecnie rejestr aktywnych planów i obszerne archiwum; historii nie wolno przepisywać;
- twarde reguły: brak sekretów, brak zapisu do klastra bez jawnej zgody, brak push do `main`, brak attribution;
- automatyczny skutek po merge: zmiany Terraform Cloudflare na `main` mogą uruchomić auto-apply HCP Terraform;
- specyficzne walidacje Helm/Kustomize i pułapkę cache dla lokalnych chartów `file://`.

Wniosek: `home-ops` jest właściwym pilotem, ale polityki bezpieczeństwa muszą być wspólne dla wszystkich harnessów i zapisane w `AGENTS.md`. `CLAUDE.md` powinien stać się adapterem, nie równoległym źródłem prawdy.

## 3. Zasady architektoniczne

1. **Lifecycle ≠ profil ≠ topologia ≠ skill ≠ harness.** Lifecycle definiuje etapy; profil ich głębokość; topologia rozdział odpowiedzialności; skill sposób wykonania; harness udostępnia narzędzia.
2. **Jedno źródło prawdy.** Wspólne zasady projektu są w `AGENTS.md`, a wspólne procedury globalne w `claude-plugins`.
3. **Cienkie adaptery.** Pliki Claude/Codex/OpenCode zawierają wyłącznie mechanikę odkrywania, metadane narzędzi i różnice capability.
4. **Artefakty ponad pamięć sesji.** Plan, status, decyzje, wyniki testów i handoff są przenośnymi plikami Markdown.
5. **Capability detection, nie emulacja.** Gdy brak subagentów, hooków lub schedulera, proces ma mieć ścieżkę sekwencyjną/manualną.
6. **Jeden właściciel zadania.** Multi-agent nie rozmywa odpowiedzialności za integrację i końcową weryfikację.
7. **Worktree-first.** Primary checkout pozostaje czysty na domyślnej gałęzi. Wyjątek wymaga świadomej decyzji, nie cichego fallbacku.
8. **No implicit production mutation.** Operacje odczytu, render i plan są inne niż apply/sync/merge; każda mutacja środowiska wymaga osobnej autoryzacji.

## 4. Architektura docelowa

```text
                    VS Code / terminal
                            |
          +-----------------+------------------+
          |                 |                  |
     Claude Code          Codex           OpenCode
          |                 |                  |
          +--------- thin harness adapters ----+
                            |
                 Shared workflow contract
       Spec -> Plan -> Build -> Test -> Review
                    -> Simplify -> Ship
          profile: QUICK / STANDARD / DEEP
     topology: SOLO / HANDOFF / PARALLEL / REVIEW
                            |
     +----------------------+----------------------+
     |                      |                      |
 AGENTS.md          portable skills          artifacts
 policy/invariants  claude-plugins            .plans/.ai
     |                      |                      |
     +----------------------+----------------------+
                            |
                   project quality gates
                            |
                  commit / PR / GitOps merge
                            |
                 separately authorized runtime
                  ArgoCD / Talos / Kubernetes
```

### 4.1 Odpowiedzialność repozytoriów

| Repozytorium | Rola | Jest źródłem prawdy dla | Nie powinno zawierać |
| --- | --- | --- | --- |
| `claude-plugins` | AI Engineering Kit | przenośne skills, workflow modes, szablony, testy kompatybilności, adaptery dystrybucyjne | polityk konkretnego klastra, sekretów, globalnej instalacji stacji roboczej |
| `dotfiles` | Bootstrap i konfiguracja użytkownika | instalacja CLI/pluginów, profile harnessów, ścieżki, feature flags | kopii skills i reguł projektowych |
| `home-ops` | Projekt pilotowy i polityka domenowa | architektura projektu, quality gates, uprawnienia, plany i handoffy | globalnych instrukcji instalacji i skopiowanych procedur lifecycle |

### 4.2 Proponowana struktura w `home-ops`

```text
AGENTS.md                         # wspólny kontrakt projektu
CLAUDE.md                         # cienki adapter Claude -> AGENTS.md
.ai/
  workflow.md                     # wybór trybu i state machine
  capabilities.md                 # oczekiwane zachowanie przy brakach harnessu
  permissions.md                  # macierz read/render/write/apply
  quality-gates.md                # komendy i warunki zaliczenia
  templates/
    plan.md
    handoff.md
    decision.md
.agents/skills/                   # kanoniczne project skills
  add-app/SKILL.md
  dev-workflow/SKILL.md
.claude/skills/                   # adapter: link/copy generowana lub krótkie delegatory
.plans/                           # zachowany aktywny rejestr i formaty
.archive/.plans/                  # nienaruszone archiwum
```

Nie należy przenosić istniejących wpisów `.archive/.plans`. Nowe dokumenty mogą otrzymać neutralny format, ale stare linki i indeksy pozostają ważne.

## 5. Kontrakt wykonania: trzy niezależne wymiary

Architektura ma dokładnie jeden lifecycle oraz dwa niezależne parametry wykonania. Profile i topologie nie dodają alternatywnych sekwencji etapów.

### 5.1 Lifecycle — co się dzieje

Kanoniczny lifecycle pochodzi z istniejącego pluginu `development-lifecycle`:

```text
Spec → Plan → Build → Test → Review → Simplify → Ship
```

Wszystkie siedem etapów jest zawsze konceptualnie obecnych. Profil może zmniejszyć ich zakres, połączyć czynności lub zrezygnować z osobnego dokumentu, lecz nie zmienia kolejności ani znaczenia etapów. `Ship` oznacza ocenę gotowości i wykonanie wyłącznie autoryzowanych czynności dostarczenia; nie oznacza automatycznie commit, push, utworzenia PR, merge ani deploymentu.

### 5.2 Execution Profile — jak dokładnie

| Etap lifecycle | QUICK | STANDARD | DEEP |
| --- | --- | --- | --- |
| **Spec** | krótko/implicit: potwierdź cel, zakres i kryterium sukcesu w kontekście sesji | zwięzłe wymagania, zakres, non-goals i kryteria akceptacji; dokument, gdy zadanie nie jest oczywiste | pełna specyfikacja repo-grounded, ograniczenia, ryzyka i mierzalne kryteria |
| **Plan** | mentalny lub krótka lista kroków; bez obowiązkowego pliku | zwięzły plan implementacji, dotknięte obszary i quality gates; plik dla pracy wielosesyjnej | szczegółowy plan etapowy, decyzje/ADR, ownership, rollout, rollback i permission gates |
| **Build** | najmniejsza lokalna zmiana, bez refaktoryzacji poza zakresem | kompletna implementacja z rozsądnym podziałem zmian | implementacja etapowa, kontrakty między komponentami i kontrola blast radius |
| **Test** | najmniejszy miarodajny test/regresja lub udokumentowane sprawdzenie; ryzyko może wymusić silniejsze testy | odpowiednie testy automatyczne i project gates dla zmiany | pełne testy warstwowe/scenariuszowe, negatywne przypadki i dowody weryfikacji |
| **Review** | focused self-review diffu pod kątem regresji i zakresu | pełny self-review lub osobny review pass; oddzielny agent tylko po autoryzacji | niezależny review pass; oddzielny agent tylko w autoryzowanej topologii REVIEW/PARALLEL |
| **Simplify** | usuń oczywistą zbędną złożoność bez poszerzania zakresu | oceń, czy rozwiązanie można uprościć i zachować czytelność | jawna analiza alternatyw, długu, kosztu operacyjnego i maintainability |
| **Ship** | podsumuj wynik i gotowość; wykonaj tylko jawnie autoryzowaną czynność | sprawdź kompletność gates i w dozwolonym zakresie wykonaj delivery | readiness review, rollout/rollback i osobne potwierdzenia dla operacji mutujących |

Dobór profilu:

- `QUICK`: mała, lokalna i odwracalna zmiana o niskim ryzyku;
- `STANDARD`: normalna praca programistyczna — profil domyślny;
- `DEEP`: architektura, migracja, wysoki blast radius lub praca wieloetapowa.

Profil nigdy nie obniża obowiązkowych zasad bezpieczeństwa, uprawnień, worktree ani project quality gates. Dla zmian Talos bootstrap/PKI/dysków, polityk sekretów, ArgoCD bootstrap, Terraform z auto-apply i destrukcyjnych migracji agent powinien rekomendować `DEEP`; jeżeli użytkownik pozostaje przy innym profilu, obowiązkowe zabezpieczenia i tak pozostają wiążące.

### 5.3 Execution Topology — kto wykonuje

| Topologia | Kontrakt |
| --- | --- |
| SOLO | jeden właściciel wykonuje cały lifecycle; brak delegacji do innego agenta lub harnessu |
| HANDOFF | odpowiedzialność przechodzi między agentami przez jawny artefakt handoff |
| PARALLEL | autoryzowane, niezależne zakresy są rozdzielone; każdy writer ma osobny worktree/branch; istnieje jawny integrator |
| REVIEW | oddzielny, autoryzowany agent recenzuje implementację; domyślnie ma zakres read-only i raportuje findings z dowodem |

`HANDOFF`, `PARALLEL` i `REVIEW` wymagają jawnego polecenia lub akceptacji użytkownika. Agent może je rekomendować, lecz nie może samodzielnie uruchomić innego harnessu, subagenta ani zewnętrznego orkiestratora. Brak capability nie powoduje ukrytej zmiany topologii: agent zgłasza ograniczenie i kontynuuje `SOLO` tylko wtedy, gdy jest to zgodne z intencją użytkownika.

### 5.4 Globalny default

```yaml
defaults:
  profile: standard
  topology: solo
```

Default jest identyczny w Claude Code, Codex i OpenCode. Normalne polecenie deweloperskie oznacza `STANDARD + SOLO`; bieżący agent odpowiada za cały lifecycle. Instrukcja `quick` lub `deep` zmienia profil, ale nie topologię. Instrukcja wskazująca przekazanie, równoległość lub osobnego recenzenta zmienia topologię w podanym zakresie. Jawne polecenie użytkownika ma pierwszeństwo z zastrzeżeniem reguł bezpieczeństwa i uprawnień.

| Przykład polecenia | Profil | Topologia |
| --- | --- | --- |
| Fix the validation bug | STANDARD | SOLO |
| Quick: fix this typo | QUICK | SOLO |
| Deep: redesign the authentication module | DEEP | SOLO |
| Ask Codex to implement the approved plan | STANDARD | HANDOFF |
| Have Claude and Codex implement independent components | STANDARD | PARALLEL |
| Deep + Parallel: redesign monitoring | DEEP | PARALLEL |

## 6. Worktree-first

Kontrakt z `git-workflows` pozostaje obowiązujący:

- primary checkout: default branch, czysty, nieużywany jako workspace;
- branch: `<type>/<slug>`;
- worktree: `.worktrees/<type>/<slug>`;
- `.worktrees/` w `.git/info/exclude`, nie w `.gitignore`;
- read-only explorer/reviewer może dzielić worktree właściciela;
- każdy równoległy writer dostaje osobny worktree;
- integrator scala i uruchamia testy w swoim worktree.

Adapter Claude zachowuje obecny hook jako best-effort backstop. Adapter Codex nie obiecuje hooka, którego nie ma: wymusza check preflight w skillu. Adapter OpenCode ma użyć natywnego hooka tylko po potwierdzeniu jego stabilnego API; do tego czasu także preflight proceduralny.

Minimalny preflight przed pierwszym zapisem:

1. ustal root repo i default branch;
2. porównaj `GIT_DIR` z `GIT_COMMON_DIR`;
3. sprawdź bieżący branch oraz status;
4. jeśli primary checkout — utwórz/przełącz na worktree;
5. zapisz ścieżkę i branch w planie lub handoffie.

## 7. Wspólne instrukcje `AGENTS.md` i `CLAUDE.md`

### 7.1 `AGENTS.md`

Powinien zawierać tylko reguły istotne w każdej sesji:

- zwięzły opis architektury `home-ops`;
- kanoniczny siedmioetapowy lifecycle, default `STANDARD + SOLO` i worktree-first;
- quality gates;
- politykę planów i archiwum;
- granice uprawnień i sekretów;
- branch/PR/no-attribution;
- wskazanie project skills i `.ai/*` po szczegóły.

Nie powinien kopiować pełnych template’ów Kubernetes, list wszystkich tasków ani szczegółów pojedynczych usług. Te pozostają w skills i dokumentacji ładowanej na żądanie.

### 7.2 `CLAUDE.md`

Docelowo cienki adapter:

```md
# Claude Code adapter

@AGENTS.md

Claude-specific behavior:
- Load project skills from `.claude/skills/` adapters.
- The installed `git-workflows` hook is a backstop; `AGENTS.md` remains authoritative.
- Native agent teams are optional and must follow the collaboration/worktree contract.
```

Jeśli import `@AGENTS.md` okaże się niestabilny w używanej wersji Claude, adapter może zawierać krótki obowiązek odczytu pliku, ale nie duplikat reguł.

## 8. Skills i Superpowers

### 8.1 Klasyfikacja

| Typ | Lokalizacja | Przykłady |
| --- | --- | --- |
| przenośne, globalne | `claude-plugins/plugins/*/skills/` | lifecycle, review, worktrees, verification, safety |
| projektowe | `home-ops/.agents/skills/` | add-app, dev-workflow, Talos/GitOps conventions |
| natywne adaptery | `commands/`, `agents/`, `.claude/skills/`, przyszłe OpenCode entrypoints | host metadata, tool list, model hint |

### 8.2 Zasada migracji

Każdy skill przechodzi audit portability:

- nie zakłada nazw narzędzi jednego harnessu w treści kanonicznej;
- wykrywa dostępne możliwości przed delegacją, schedulowaniem lub external service;
- ma ścieżkę SOLO/sequential;
- nie deklaruje sukcesu, jeżeli capability jest nieobecne;
- host-specific metadata zostają w entrypoincie, nie w skill body.

Project skills `add-app` i `dev-workflow` należy przenieść kanonicznie do `.agents/skills/`. Adapter Claude może być dowiązaniem tam, gdzie działa przenośnie, albo krótkim plikiem wskazującym kanoniczny skill. Preferowane jest generowanie/validation przeciw kopiowaniu ręcznemu.

### 8.3 Superpowers

Superpowers pozostaje opcjonalnie zainstalowany dla Claude, ale:

- nie jest wymagany do wejścia w żaden tryb;
- nie jest domyślnym formatem nowych planów;
- jego TDD, debugging, brainstorming i verification mogą zostać wywołane jako implementacja etapu;
- workflow nie może odwoływać się do nieobecnego prefixu `superpowers:*` bez fallbacku;
- stare plany Superpowers pozostają w miejscu i są nadal czytelne.

W `dotfiles` rekomendowane są profile: `core` (własne pluginy), `claude-extended` (Superpowers i dodatki), `minimal`, z profilem wybieranym w chezmoi data.

## 9. Adaptery harnessów

### 9.1 Wspólny kontrakt capability

Adapter raportuje logicznie:

```yaml
capabilities:
  shared_skills: true|false
  native_agents: true|false
  parallel_delegation: true|false
  tool_hooks: true|false
  worktree_isolation: native|manual|none
  scheduling: true|false
  persistent_memory: true|false
```

Nie jest wymagany konkretny plik YAML w v1; ważne jest jednak, by tabela była testowalnym kontraktem w dokumentacji i testach scenariuszowych.

### 9.2 Claude Code

- marketplace i pluginy pozostają bez zmian;
- commands/agents linkują do wspólnych skills;
- hook worktree pozostaje Claude-only;
- agent teams są opcjonalnym wykonaniem PARALLEL/REVIEW;
- Superpowers nie może automatycznie nadpisywać wybranego trybu workflow.

### 9.3 Codex

- używa istniejących `.codex-plugin/plugin.json` i `$plugin:skill`;
- `hooks: []` jest prawdziwą deklaracją ograniczenia;
- worktree enforcement = preflight + instrukcja + kontrola integratora;
- brak delegacji oznacza role sekwencyjne;
- nie powstaje drugi katalog kopii skills.

### 9.4 OpenCode

Adapter jest projektowany dopiero po spike’u kompatybilności. Minimalny wynik spike’u:

- sposób ładowania `AGENTS.md`/instrukcji;
- sposób odkrywania lub wywoływania skills;
- mapping permissions i hooks;
- obsługa subagentów i worktrees;
- instalacja przez `dotfiles`;
- trzy scenariusze testowe: QUICK+SOLO, STANDARD+HANDOFF, REVIEW.

Do tego czasu OpenCode korzysta z `AGENTS.md`, artefaktów Markdown i ręcznego wywołania procedur; brak natywnego pluginu nie blokuje workflow.

## 10. Granice uprawnień `home-ops`

### 10.1 Macierz operacji

| Klasa | Przykłady | Domyślna decyzja |
| --- | --- | --- |
| READ | `git diff`, odczyt YAML, `kubectl get`, `argocd app get`, `talosctl get` | dozwolone, o ile nie ujawniają sekretów |
| LOCAL_RENDER | `helm template`, `kubectl kustomize`, lint, format, Terraform validate/plan po sprawdzeniu outputu | dozwolone; artefakty należy zredagować z sekretów |
| REPO_WRITE | edycja plików w worktree, testy generujące pliki | dozwolone w przydzielonym zakresie |
| DELIVERY | commit, push, utworzenie PR | tylko gdy wynika z polecenia/zaakceptowanego etapu; nigdy push do `main` |
| GITOPS_TRIGGER | merge PR, zmiana auto-sync/auto-apply, Argo refresh/sync | osobna jawna zgoda, bo może zmienić runtime |
| RUNTIME_MUTATION | `kubectl apply/delete/annotate/patch/scale`, `talosctl apply-config/upgrade/reset`, Terraform apply | każdorazowa jawna zgoda z opisem blast radius |
| DESTRUCTIVE | wipe dysków/Rook, usunięcie namespace/PVC, reset node, rotacja PKI/secrets | DEEP + plan rollback/backup + preflight + jawna zgoda bezpośrednio przed akcją |

Samo zatwierdzenie planu nie jest zgodą na runtime mutation. Zgoda na jeden krok nie obejmuje kolejnych kroków.

### 10.2 Sekrety

- nigdy nie umieszczać wartości w promptach, planach, logach, test fixtures ani PR;
- preferować nazwy/UUID/referencje, nigdy wartości;
- zachować rozdział: ExternalSecret dla `Secret data/stringData`, `cluster-secrets` dla tokenów w innych polach;
- przed commit uruchomić gitleaks/pre-commit;
- output `terraform plan`, `helm template` i komend klastra traktować jako potencjalnie poufny;
- agent nie może sam pobierać sekretu, jeśli do zadania wystarcza referencja lub schema.

### 10.3 GitOps i pośrednie skutki

Review musi oznaczać pliki, których merge wywołuje automatyczny efekt. Szczególnie `provision/terraform/cloudflare/**` może uruchomić HCP Terraform auto-apply. Dla takich PR wymagane są: plan, jawna sekcja impact, plan rollback i potwierdzenie, że merge jest operacją mutującą.

## 11. Artefakty i handoff

### 11.1 Nowy neutralny plan

Nowe plany zalecane są jako `.plans/<slug>/plan.md` + `tasks.md`. `plan.md` zawiera:

- cel i non-goals;
- `profile: QUICK|STANDARD|DEEP` i `topology: SOLO|HANDOFF|PARALLEL|REVIEW`;
- owner/integrator;
- base SHA, branch, worktree;
- architekturę i decyzje;
- scope i file ownership;
- quality gates;
- permissions/runtime impact;
- rollout i rollback;
- status oraz next action.

### 11.2 Handoff

Handoff jest snapshotem, nie pamiętnikiem rozmowy:

```yaml
task: <id/slug>
from: <harness/agent>
to: <harness/agent or unassigned>
base_sha: <sha>
branch: <branch>
worktree: <path>
profile: standard
topology: handoff
status: planned|in_progress|review|blocked
```

Treść: wykonane zmiany, ważne decyzje, pliki dotknięte, testy z wynikami, znane ryzyka, brakujące zgody, dokładny następny krok.

## 12. Opcjonalny orkiestrator

Orkiestrator nie jest częścią correctness boundary ani zależnością zwykłej pracy. Może zostać uruchomiony wyłącznie po jawnej autoryzacji topologii innej niż SOLO. Jest klientem tego samego kontraktu i może:

- utworzyć task graph;
- przydzielić właścicieli i worktrees;
- uruchomić niezależne work units;
- zebrać handoffy i wyniki testów;
- poprosić integratora o merge/review.

Nie może:

- omijać permission gates;
- samodzielnie scalać zmian wywołujących runtime bez zgody;
- przekazywać sekretów między agentami;
- uznać zadania za ukończone bez project quality gates;
- wymagać konkretnego modelu do odczytu artefaktów.

Warunek wdrożenia orkiestratora: co najmniej trzy zakończone ręcznie zadania HANDOFF/PARALLEL, z których wynika stabilny schemat, oraz test awarii częściowego wykonania.

## 13. Plan migracji i kolejność PR

### Faza 0 — baseline (bez zmian funkcjonalnych)

1. Zablokować referencyjne SHA z tej specyfikacji.
2. Uruchomić obecne testy `claude-plugins` i smoke instalacji.
3. Spisać aktualne wersje Claude/Codex/chezmoi i capability matrix.
4. Zrobić backup dotfiles state oraz listy aktywnych pluginów.

### PR 1 — `claude-plugins`: rozszerzenie kanonicznego lifecycle

- zachować `Spec → Plan → Build → Test → Review → Simplify → Ship` jako jedyny lifecycle;
- dodać profile QUICK/STANDARD/DEEP oraz topologie SOLO/HANDOFF/PARALLEL/REVIEW jako niezależne parametry;
- ustawić i przetestować globalny default `STANDARD + SOLO`;
- dodać neutralne szablony plan/handoff/decision;
- rozszerzyć istniejące lifecycle skills zamiast tworzyć konkurencyjne;
- zinwentaryzować i skorygować reguły wymuszające nadmierne planowanie, research lub TDD niezależnie od profilu i ryzyka;
- dodać testy linków, manifest parity i scenariuszy degradacji;
- udokumentować Superpowers jako optional provider;
- bez OpenCode adaptera produkcyjnego — tylko interfejs i spike checklist.

### PR 2 — `dotfiles`: profile i instalacja wielu harnessów

- rozbić pojedynczy Claude installer na idempotentne funkcje/profile;
- dodać instalację/rejestrację Codex pluginów;
- udostępnić ten sam default `STANDARD + SOLO` bez kopiowania definicji lifecycle do konfiguracji każdego harnessu;
- pozostawić Superpowers w profilu `claude-extended`, nie jako dependency core;
- dodać feature flag OpenCode bez domyślnej aktywacji;
- dodać smoke test świeżego HOME/devcontainera i ponownego apply chezmoi.

### PR 3 — `home-ops`: shared policy bez przenoszenia historii

- utworzyć `AGENTS.md` z regułami wspólnymi;
- zapisać w nim jeden lifecycle i default `STANDARD + SOLO`, bez automatycznej delegacji;
- odchudzić `CLAUDE.md` do adaptera;
- dodać `.ai/{workflow,permissions,quality-gates,capabilities}.md` i templates;
- przenieść kanoniczne project skills do `.agents/skills/` z kompatybilnymi adapterami Claude;
- zachować `.plans` i `.archive/.plans` bez masowego rename/move;
- dodać link checker i test zgodności instrukcji.

### PR 4 — `claude-plugins`: OpenCode spike/adapter

- wykonać spike na pinned wersji OpenCode;
- wybrać natywną integrację albo udokumentowany adapter manualny;
- dodać testy instalacji i trzy scenariusze behawioralne;
- nie deklarować parity capabilities bez dowodu.

### PR 5 — opcjonalnie: pilot orchestratora

- dopiero po stabilizacji ręcznych HANDOFF/PARALLEL;
- ograniczony do repo/worktrees/artifacts;
- bez credentials do klastra i bez merge permission w pilocie.

Każdy PR musi być niezależnie odwracalny. `home-ops` nie może zależeć od niewydanej zmiany `dotfiles`; najpierw release/tag `claude-plugins`, potem konsument.

## 14. Testy

### 14.1 `claude-plugins`

- `python3 -m unittest discover -s tests`;
- `claude plugin validate . --json` i walidacja każdego pluginu;
- `bash plugins/git-workflows/hooks/test-guard.sh` na Bash 3.2 i 5+;
- test parity identity/version manifestów Claude/Codex;
- test wszystkich links/resources pozostających w granicy pluginu;
- scenariusze obu harnessów: spec, TDD bugfix, review, ship, worktree;
- scenariusze negatywne: brak delegacji, scheduler, scanner, DevFleet, jq;
- oczekiwany rezultat braku capability: manual path albo jasny prerequisite, nigdy pozorny sukces.

### 14.2 `dotfiles`

- `chezmoi execute-template`/diff na Windows, Linux, macOS i devcontainer fixtures;
- świeża instalacja oraz drugie uruchomienie bez błędu;
- host z tylko Claude, tylko Codex, oboma, bez żadnego;
- profil core nie instaluje Superpowers;
- profil extended instaluje go, ale workflow działa po wyłączeniu pluginu;
- brak tokenów lub wartości prywatnych w renderowanych konfiguracjach.

### 14.3 `home-ops`

- parser/link checker dla `AGENTS.md`, `CLAUDE.md`, `.ai/`, `.plans/list.md` i archiwum;
- oba harnessy odpowiadają tak samo na test polityk (worktree, secrets, runtime mutation, main push, attribution);
- smoke: QUICK+SOLO dokumentacyjny;
- smoke z jawną autoryzacją: STANDARD+HANDOFF dla manifestu Helm;
- smoke z jawną autoryzacją: DEEP+REVIEW dla zmiany Talos — plan/render tylko, bez apply;
- `helm template`, `kubectl kustomize`, `task lint:all`, pre-commit/gitleaks według zakresu;
- test local `file://` chart: zmiana wymaga bump wersji chartu i parent dependency;
- test Terraform impact: PR dotykający Cloudflare musi oznaczyć auto-apply i rollback.

### 14.4 Test przenośności

Ten sam fixture task jest wykonany w Claude i Codex; porównywane są nie sformułowania, lecz invariants:

- wybrany tryb;
- brak zapisu w primary checkout;
- kompletność planu/handoffu;
- te same permission gates;
- te same quality gates;
- brak fałszywej deklaracji wykonania.
- nieokreślone polecenie deweloperskie daje `STANDARD + SOLO` w każdym harnessie;
- QUICK, STANDARD i DEEP raportują ten sam siedmioetapowy lifecycle;
- SOLO nie uruchamia subagenta, innego harnessu ani orkiestratora;
- HANDOFF i PARALLEL bez jawnej autoryzacji są odrzucane lub przedstawiane jako propozycja;

## 15. Kryteria akceptacji

1. Nieokreślone polecenie deweloperskie daje `STANDARD + SOLO` w Claude Code, Codex i OpenCode.
2. QUICK, STANDARD i DEEP używają tego samego lifecycle `Spec → Plan → Build → Test → Review → Simplify → Ship`.
3. SOLO nie uruchamia cross-harness delegation, subagenta ani zewnętrznego orkiestratora.
4. HANDOFF i PARALLEL wymagają jawnej autoryzacji; REVIEW z oddzielnym agentem również nie uruchamia się automatycznie.
5. QUICK nie omija polityk bezpieczeństwa, permission gates, worktree ani wymaganych project quality gates.
6. Wszystkie harnessy interpretują ten sam kontrakt, a różnice hooks, agents, plugins i orchestration są jawnie obsłużone adapterami.
7. Istniejące skills, `.plans`, `.archive/.plans` i konwencje worktree pozostają kompatybilne.
8. Workflow działa z tylko jednym zainstalowanym harness-em i nie wymaga delegacji.
9. Zewnętrzna orkiestracja jest opcjonalna i nie jest zależnością zwykłych zadań.
10. HANDOFF między harnessami nie wymaga historii czatu.
11. PARALLEL nie dopuszcza dwóch writerów w jednym worktree.
12. `home-ops` ma jedno kanoniczne źródło zasad wspólnych w `AGENTS.md`.
13. Wyłączenie Superpowers nie blokuje żadnego etapu kanonicznego lifecycle.
14. Project skills są dostępne w Claude i Codex bez ręcznie rozbieżnych treści.
15. Brak hooka Codex/OpenCode jest jawny i pokryty proceduralnym preflightem.
16. Żaden harness nie wykonuje runtime mutation bez świeżej, jawnej zgody.
17. Merge o skutku GitOps/HCP jest klasyfikowany jako mutacja, nie zwykła operacja Git.
18. Fresh install i ponowne `chezmoi apply` są idempotentne.
19. OpenCode ma udokumentowaną minimalną ścieżkę nawet przed natywnym adapterem.
20. Każdy PR ma sprawdzony rollback.

## 16. Rollback

### `claude-plugins`

- przypiąć marketplace do ostatniego działającego tagu/SHA;
- odinstalować wadliwą wersję i ponownie zainstalować poprzednią;
- przywrócić wcześniejsze manifesty jako jeden atomowy revert;
- brak migracji user data oznacza niski koszt rollbacku.

### `dotfiles`

- revert PR i `chezmoi apply` z poprzedniej rewizji;
- profiles domyślnie zachowują poprzedni Claude setup w pierwszym wydaniu;
- uninstall nie może być automatycznym skutkiem zmiany profilu; najpierw disable, usuwanie osobno.

### `home-ops`

- pierwszy PR nie usuwa treści starego `CLAUDE.md`, dopóki oba harnessy nie przejdą testów;
- adaptery skills można cofnąć do `.claude/skills/` bez ruszania archiwum;
- `.plans` i `.archive/.plans` są poza migracją treści;
- rollback dokumentacji/policy nie obejmuje runtime; jeśli merge uruchomił GitOps, potrzebny jest osobny runtime rollback zgodny z impact planem.

Stop condition: regresja permission gate, utrata discovery skills, zapis do primary checkout, uszkodzenie linków archiwum albo różne zasady bezpieczeństwa między harnessami blokują dalsze PR-y.

## 17. Otwarte decyzje

| ID | Decyzja | Rekomendacja |
| --- | --- | --- |
| D1 | kanoniczny format nowych planów | `.plans/<slug>/plan.md + tasks.md`; czytać oba stare formaty |
| D2 | adapter `.claude/skills` | symlink, jeśli działa na Windows/devcontainer; w przeciwnym razie generowany delegator z testem driftu |
| D3 | domyślny profil dotfiles | `core` dla nowych hostów, zachowanie `claude-extended` dla istniejących do świadomej migracji |
| D4 | wersjonowanie pluginów | release/tag po PR 1, zanim dotfiles/home-ops zaczną polegać na kontrakcie |
| D5 | OpenCode packaging | zdecydować dopiero po spike’u na konkretnej wersji; nie zakładać zgodności z Claude/Codex |
| D6 | lokalizacja handoffów | w aktywnym folderze planu; `.ai/handoffs/` tylko dla zadań bez planu |
| D7 | wymuszanie worktree w Codex | preflight proceduralny teraz; natywny hook tylko jeśli oficjalnie wspierany i testowalny |
| D8 | niezależność review w DEEP | wymagany osobny review pass; cross-model/oddzielny agent tylko po autoryzacji topologii REVIEW |
| D9 | orkiestrator | odłożyć do zebrania co najmniej 3 realnych handoffów i 1 parallel pilot |
| D10 | język dokumentów | instrukcje techniczne po angielsku dla przenośności narzędzi; opisy/PR według preferencji repo |

## 18. Źródła przeglądu

- [`claude-plugins` README](https://github.com/mmalyska/claude-plugins/blob/8396c61df25fb0e2f57ebaa46beb1dbe1db88a8e/README.md)
- [Shared Claude Code and Codex workflows](https://github.com/mmalyska/claude-plugins/blob/8396c61df25fb0e2f57ebaa46beb1dbe1db88a8e/docs/codex.md)
- [Worktree workflow](https://github.com/mmalyska/claude-plugins/blob/8396c61df25fb0e2f57ebaa46beb1dbe1db88a8e/plugins/git-workflows/rules/worktree-workflow.md)
- [`development-lifecycle` README](https://github.com/mmalyska/claude-plugins/blob/8396c61df25fb0e2f57ebaa46beb1dbe1db88a8e/plugins/development-lifecycle/README.md)
- [`agent-toolkit` README](https://github.com/mmalyska/claude-plugins/blob/8396c61df25fb0e2f57ebaa46beb1dbe1db88a8e/plugins/agent-toolkit/README.md)
- [`dotfiles` Claude installer](https://github.com/mmalyska/dotfiles/blob/96a0802425b5eaf6d9bd59b9e0a06cf8cde5702c/home/run_once_install-claude-plugins.sh)
- [`dotfiles` Claude settings](https://github.com/mmalyska/dotfiles/blob/96a0802425b5eaf6d9bd59b9e0a06cf8cde5702c/home/dot_claude/settings.json.tmpl)
- [`home-ops` CLAUDE.md](https://github.com/mmalyska/home-ops/blob/24024f1dcb24e0eca1cb9c18ebbbf7a887772f30/CLAUDE.md)
- [`home-ops` dev-workflow skill](https://github.com/mmalyska/home-ops/blob/24024f1dcb24e0eca1cb9c18ebbbf7a887772f30/.claude/skills/dev-workflow/SKILL.md)
- [`home-ops` archived plans index](https://github.com/mmalyska/home-ops/blob/24024f1dcb24e0eca1cb9c18ebbbf7a887772f30/.archive/.plans/list.md)

## 19. Rekomendacja wykonawcza

Rozpocząć od PR 1 w `claude-plugins`, ale ograniczyć go do formalizacji już istniejącej architektury, a nie przebudowy katalogów. Następnie dostarczyć idempotentną instalację Codex w `dotfiles`, a dopiero potem zrobić pilot `home-ops` z `AGENTS.md` i neutralnymi project skills. OpenCode i orkiestrator powinny być osobnymi, późniejszymi decyzjami opartymi na testach, nie warunkiem wejścia w nowy workflow.
