# RepoPersonalPreferences reference sweep — what every live repo turned out to hold

**Who this is for:** anyone who needs to know which repositories still
depend on the retired personal pack, and which are finished with it. The
list of repos left alone matters as much as the list that changed.

**What was asked**, Morgan, 2026-09-14: remove `RepoPersonalPreferences`
from any repo that references it **and** has been updated to Precedent. A
repo still running the old BestPractice-plus-personal-pack layout is left
exactly as it is — taking the pack out of a repo that still depends on it
removes its rules and replaces them with nothing.

Every live repository under `themorgan` was cloned and searched. The three
`DEPRECATED-`prefixed archived repos were not touched.

## The short answer

**Of 21 live repos, 3 needed work and got it. 5 must not be touched. 13
were already correct.** The pack itself — the vendored `process/personal/`
tree, `process/manifest_personal.json`, the `personal-pack-sync` workflow —
was **already gone from every migrated repo before this sweep started**.
What was left was dead wiring pointing at it, and in one repo a gate that
had been failing unnoticed.

## Left alone deliberately — still running the old layout (5)

These have the pack **and** no `precedent.json`, no vendored engine. They
are at step 0 of `RPP_RETIREMENT_MAP.md`'s procedure, not step 6. Removing
anything here would strip their rules.

| Repo | What it still has |
|---|---|
| [`WriteLike`](https://github.com/themorgan/WriteLike) | `process/personal/`, `manifest_personal.json`, 2 sync workflows, live `PERSONAL_PACK_TOKEN` |
| [`GetEmailsFromGmail`](https://github.com/themorgan/GetEmailsFromGmail) | same shape |
| [`duads`](https://github.com/themorgan/duads) | same shape |
| [`holiday-sync`](https://github.com/themorgan/holiday-sync) | same shape |
| [`RepoPersonalScaffold`](https://github.com/themorgan/RepoPersonalScaffold) | same shape |

**These five are the real outstanding work**, and it is a migration, not a
deletion. Each needs `precedent.json` declaring its sources *first* — 16 of
the pack's 22 rules live in the private team and individual sets, so a repo
that deletes the tree before declaring them silently stops carrying those
rules.

## Changed and merged (3)

| Repo | Pull request | What was actually wrong |
|---|---|---|
| [`SoundHuman`](https://github.com/themorgan/SoundHuman) | [#29](https://github.com/themorgan/SoundHuman/pull/29) | `tools/bootstrap.sh` called `process/personal/tools/pack_sync.py` three times; the tree went 2026-09-10 and every call had been failing silently behind `2>/dev/null \|\| true` |
| [`VoiceDefinitionMorgan`](https://github.com/themorgan/VoiceDefinitionMorgan) | [#53](https://github.com/themorgan/VoiceDefinitionMorgan/pull/53) | A wired Stop hook whose checker went with the pack; its own `[[ -f ... ]] \|\| exit 0` guard made it exit clean on every turn |
| [`TodoMorgan`](https://github.com/themorgan/TodoMorgan) | [#55](https://github.com/themorgan/TodoMorgan/pull/55) | `migration-scrubs-vocabulary` was **failing on eight findings**, hidden by a stale note in the repo's own declaration |

### The pattern worth naming

All three failures were **silent by construction**. A dead script call
wrapped in `|| true`, a hook that exits 0 when its checker is missing, and a
declaration asserting its own gate could not run. None produced an error;
each looked exactly like success. Four days passed in two of them and
eleven in the third.

**TodoMorgan's is the one to remember.** `process/retired_vocabulary.json`
carried a `VERIFICATION NOTE` saying `precedent_check.py` could not run
there — `ROOT` was hardcoded, and the repo vendored only the loader engine.
Both grounds had since become false (`ROOT` resolves via `git rev-parse
--show-toplevel`; `tools/` now vendors the whole engine), but the note
stayed and told every later reader to verify by hand. *A stale claim that a
gate cannot run is indistinguishable, to every later reader, from the gate
passing.*

## Already correct — nothing to do (13)

**Finished properly:** [`nomen-omen`](https://github.com/themorgan/nomen-omen)
(migrated 2026-09-07, pack decommissioned through the audit with a recorded
reason, remaining mentions exempted as historical records — this is the
model),
[`HavrutaBrainstorm`](https://github.com/themorgan/HavrutaBrainstorm) and
[`VoiceModelTemplateDefinition`](https://github.com/themorgan/VoiceModelTemplateDefinition)
(both declare retired vocabulary and pass the check).

**Correction to `RPP_RETIREMENT_MAP.md`:** it records `nomen-omen` as
carrying the tree with "**no `precedent.json`**, so it is at step 0". That
was true when written on 2026-09-07 and is **stale now** — `nomen-omen`
migrated that same day and is complete. It also names `HavrutaBrainstorm` as
a likely candidate "not inspected"; it has been inspected and is clean.

**No first-party references at all** — every hit is inside the vendored
engine (`tools/precedent_check.py`, `tools/precedent_decommission.py`, whose
own source comments discuss the pack) or a materialized `practices/`
directory carrying another source's verbatim text:
[`VoiceDefinitionCelia`](https://github.com/themorgan/VoiceDefinitionCelia),
[`CopyrightNewBrainstorming`](https://github.com/themorgan/CopyrightNewBrainstorming),
[`OnegAdsPlanning`](https://github.com/themorgan/OnegAdsPlanning),
[`precedent-team-writing`](https://github.com/themorgan/precedent-team-writing),
[`precedent-team-working-style`](https://github.com/themorgan/precedent-team-working-style).
**Never hand-edit these** — the engine is checksummed in
`tools/ENGINE_MANIFEST.json` and materialized directories are rewritten on
every sync.

**Provenance only, correctly kept:** this repo (`MAP.md` and `README.md`
record which practices came from the pack's 46 rules — `MAP.md` is
*generated* from the practices' own metadata) and
[`precedent-individual`](https://github.com/themorgan/precedent-individual)
(holds `RPP_RETIREMENT_MAP.md`, the migration record itself, plus deliberate
`leak-blocklist.txt` entries).

**No references whatsoever:**
[`GematriaPageCalculator`](https://github.com/themorgan/GematriaPageCalculator),
[`nolaunch`](https://github.com/themorgan/nolaunch).

## VoiceDefinitionOneg — referenced, migrated, and still correctly left alone

[`VoiceDefinitionOneg`](https://github.com/themorgan/VoiceDefinitionOneg) is
the one repo that meets both conditions and was still **not** changed. Its
remaining references are of two kinds, neither of them removable:

1. **`PERSONAL_PACK_TOKEN` is a live credential.** It authenticates the
   *voicedef* pack sync, which has nothing to do with the personal pack.
   `VoiceModelTemplateDefinition` had already reasoned this out and recorded
   the decision: *"do not delete it — narrow its scope to this repo
   instead."* Morgan confirmed on 2026-09-14 that this stands. Renaming it
   would need new GitHub secrets in four repos before the code change could
   land safely.
2. **Its `process/voicedef/` tree is vendored and stale.** The dangling
   `../personal/` links there were **already fixed at source** in
   `VoiceModelTemplateDefinition`; this copy simply has not taken the
   update. A vendored tree is never hand-edited — the fix arrives by sync.

### Why that sync has never worked — two wrong diagnoses before the right one

**All three scheduled runs** of `voicedef-pack-sync.yml` in
`VoiceDefinitionOneg` failed: 2026-08-31, 2026-09-07, 2026-09-14. This
section is worth reading for the diagnostic trap more than the bug.

**Wrong guess #1 — the pack token.** `VoiceDefinitionOneg` is absent from the
list of repos `VoiceModelTemplateDefinition`'s TODO says `PERSONAL_PACK_TOKEN`
was set on, so the token looked missing. It is not: the run log shows
`VOICEDEF_PACK_TOKEN` populated from it and the `check` job succeeding.

**Wrong guess #2 — the Claude credential.** The failing job's environment
dump shows `ANTHROPIC_API_KEY:` empty, which reads as "no credential, action
cannot run", and there is even a matching open TODO item upstream about
Claude credentials being unset. **That was reported as the answer and it was
also wrong.** Morgan pushed back — the credential should be there, and all
these repos name it `CLAUDE_CODE_OAUTH_TOKEN`, not `ANTHROPIC_API_KEY`.

**The actual cause.** The workflow's own gate accepts *either* name
(`if [ -n "$ANTHROPIC_API_KEY" ] || [ -n "$CLAUDE_CODE_OAUTH_TOKEN" ]`), and
`CLAUDE_CODE_OAUTH_TOKEN` was set the whole time. Reading the full log rather
than its tail gives the real error:

```
error: Unable to get ACTIONS_ID_TOKEN_REQUEST_URL env variable
Action failed: Could not fetch an OIDC token. Did you remember to add
`id-token: write` to your workflow permissions?
```

The `update` job declared `contents: write` and `pull-requests: write` but
not `id-token: write`. No `github_token` input is passed to
`anthropics/claude-code-action@v1`, so it mints one over OpenID Connect,
which needs that scope.

**Why both wrong guesses were so easy.** The failure lands *after* the
credential gate has already passed, and the empty `ANTHROPIC_API_KEY` sits
two lines above the stack trace in the log. Everything visible near the
error points at credentials; the actual cause is a permission, and it is
only named in the middle of the log, not at its end.

### This one is estate-wide

**Every workflow under `themorgan` that calls `claude-code-action` is missing
`id-token: write`** — 14 of them across 10 repos, `bestpractice-upstream-sync.yml`
in eight included. **No unattended sync's `update` job can ever have
succeeded anywhere.** Fixed in `VoiceDefinitionOneg` and in
`VoiceModelTemplateDefinition`'s template, so new installs and re-syncs carry
it. The rest still need it — most are the five repos still running the
retired pack, which are deliberately not being touched until they migrate.

### And the fix was verified, including what it did not fix

A real `workflow_dispatch` run after the fix merged
([34896563578](https://github.com/themorgan/VoiceDefinitionOneg/actions/runs/34896563578))
got much further: the OIDC error is gone, the GitHub App token mints and is
revoked cleanly, Claude Code v2.1.270 installs, and the session initialises
on `claude-sonnet-5`. **It still fails**, on a genuinely separate problem the
permission bug had been masking:

```json
{"type":"result","subtype":"success","is_error":true,
 "num_turns":1,"total_cost_usd":0,"modelUsage":{}}
```

One turn, zero cost, no model usage — nothing was billed, so no request was
ever answered. That is a credential **present and rejected**, not missing.

**Rotating the token did not fix it.** Morgan rotated
`CLAUDE_CODE_OAUTH_TOKEN` on 2026-09-14 and the next run failed identically —
same one turn, same zero cost, same empty `modelUsage`, same ~1.9s. So
"expired token" is the third diagnosis this failure has attracted and the
third that does not hold up on its own.

**The error cannot be read from a branch**, which is worth recording because
it is the obvious thing to try. Putting `show_full_output: true` on a test
branch and dispatching it produced:

```
Skipping action due to workflow validation: Workflow validation failed.
The workflow file must exist and have identical content to the version on
the repository's default branch.
```

`claude-code-action` refuses to run a modified workflow from a branch, and
reports **success** when it does so — a green run that executed nothing. That
same run did confirm `OIDC token successfully obtained`, so the `id-token`
fix is sound.

Reading the real error therefore needs one of: `show_full_output: true`
merged to `main` briefly, or the repository variable `ACTIONS_STEP_DEBUG=true`
with a re-run, which changes no tracked file and is the cheaper option.

## What governed the judgment calls

The brief for this sweep asked for prose references in `AGENTS.md`,
`README.md`, `GLOSSARY.md`, `TODO.md` and friends to be removed.
`RPP_RETIREMENT_MAP.md` step 7, Morgan's standing instruction of 2026-09-07,
said the opposite: *"Leave the mentions."* The sweep ran on the standing
instruction, then put the conflict to Morgan, who settled it on 2026-09-14:

> I think documentation should always be up to date, but historical
> mentions should not be changed like ledgers.

**Neither half of the brief was right on its own.** A ledger — a provenance
note, a decision record, a dated backlog entry, a manifest `notes` field —
keeps the name untouched; rewriting it to satisfy a checker falsifies the
history it exists to hold. But **documentation is the opposite case**: an
instructions file, a glossary, an onboarding page, a live workflow header, an
*open* backlog item describing current state all teach a reader what is true
*now*, and when they describe the pack, its sync or its secret's scope as
live, they are simply wrong.

The test is **what the sentence claims, not which file it sits in.** "This is
how it works" is documentation; "this is what we did on 2026-08-29" is a
ledger. One file usually holds both — `TODO.md`'s closed entries are ledger
and its open items are documentation. Step 7 now says all of this, with
Morgan quoted in place.

Applied: what went from the three changed repos is *uses* — code calling the
deleted tree, wiring pointing at it, and dead **paths** that resolve to
nothing. TodoMorgan's eight findings were **repointed rather than deleted**
for this reason: `"migrated from process/personal/README.md"` became
`"migrated from the retired personal pack"`, keeping the provenance and
dropping the dead path. Under the clarified rule a second pass then corrected
live documentation in `VoiceDefinitionOneg` and `VoiceModelTemplateDefinition`
that still described the retired pack's sync as a running mechanism and its
token as needing read access to the archived repo. A sweep of every other
migrated repo's `AGENTS.md`, `README.md`, `GLOSSARY.md`, `GETTING_STARTED.md`
and `MAP.md` found nothing else stale — their remaining mentions all state
correctly that the pack *is* retired.

**`PERSONAL_PACK_TOKEN` is itself being retired** (Morgan, 2026-09-14),
which reverses the "keep it, narrow its scope" decision recorded earlier in
`VoiceModelTemplateDefinition`. The replacement is a per-repo
`VOICEDEF_PACK_TOKEN` — already the name of the environment variable those
workflows read. **Order matters and is written into every document that
mentions it: create the new secret in each dependent repo first, then
repoint the workflows.** The code half alone breaks every dependent's sync
at once, which is why nothing was repointed in this sweep.

One correction to the brief's mechanics, for whoever writes the next one:
the audit tool is **`precedent_decommission.py`**, not `precedent_retire.py`.
The latter exists but only proposes a *practice* status change — the
`decommission-deletes-files` practice calls out this exact confusion as the
reason the practice was renamed.

## Pre-existing failures found along the way, not fixed here

Raised rather than acted on, since they are outside this sweep:

- **`TodoMorgan`'s `main` carries 12 other violations**, `VoiceDefinitionMorgan`'s
  12, `SoundHuman`'s 1. None relates to the personal pack. Nothing is
  currently tracking them as a set.
- **`VoiceDefinitionMorgan`'s `scrub-gate` fails on four leak-blocklist hits
  inside the vendored `process/upstream/` tree**, which also makes
  `practice_audit.py` exit non-zero.
- **`SoundHuman`'s `tools/bootstrap.sh` still hardcodes a name and email**
  in `git config`, which `.claude/hooks/commit-identity.sh` now resolves
  properly. Left alone: changing commit identity is its own decision.
- **A fired drift notice is no longer persisted into `TODO.md`** in
  `SoundHuman`. The recorder was the pack's `pack_sync.py`; nothing in
  `tools/` carries it today. Opened there as a migration follow-up.
- **Nothing enforces `file-mention-links` in `VoiceDefinitionMorgan`.**
  `tools/precedent_reply_check.py` is vendored but no hook calls it;
  `SoundHuman` wired `.claude/hooks/reply-gate.sh` to it. Opened there.
- **`id-token: write` is missing from all 14 `claude-code-action` workflows**
  under `themorgan`. Fixed in `VoiceDefinitionOneg` and in
  `VoiceModelTemplateDefinition`'s template; the rest still need it, and most
  of those are the five repos deliberately left alone.

## Retiring `PERSONAL_PACK_TOKEN` — every repo that depends on it

Morgan, 2026-09-14, on why it goes: *it was used to update RPP, which we're
no longer using.* **That is true of five of its six uses.** The sixth is the
one to handle deliberately, so here is the whole dependency list, measured
rather than remembered.

| Repo | What the token does there | What retiring it means |
|---|---|---|
| `WriteLike` | `personal-pack-sync.yml` → reads RPP | Dies with the pack when the repo migrates |
| `GetEmailsFromGmail` | same | same |
| `duads` | same | same |
| `holiday-sync` | same | same |
| `RepoPersonalScaffold` | same | same |
| **`VoiceDefinitionOneg`** | **`voicedef-pack-sync.yml` → reads `VoiceModelTemplateDefinition`** | **Breaks unless a replacement exists first** |

For the five, nothing needs doing: the token's only job there is the RPP
sync, and both go together when those repos migrate. **Deleting the secret
before they migrate would break their sync while they still depend on it**,
which is the same ordering trap step 1 of `RPP_RETIREMENT_MAP.md` exists for.

`VoiceDefinitionOneg` is the exception, and it is not an RPP use at all. The
secret was **repurposed on 2026-08-24** — per Morgan at the time, reuse the
token already in hand rather than mint a second one — to authenticate
`git ls-remote` and a clone against the *private* `VoiceModelTemplateDefinition`
for the **voicedef** pack. That pack is live. The replacement is
`VOICEDEF_PACK_TOKEN`, already the name of the environment variable both
jobs read, needing read access to `VoiceModelTemplateDefinition` only.

One simplification the sweep turned up: `VoiceModelTemplateDefinition`'s TODO
records the secret as also set on `VoiceDefinitionMorgan` and
`VoiceDefinitionCelia`. **Neither has a voicedef pack or names the secret in
any workflow**, so those two grants are unused and can simply go.

## Waiting on Morgan

1. **Diagnose `VoiceDefinitionOneg`'s Claude credential.** Rotating
   `CLAUDE_CODE_OAUTH_TOKEN` did not change the failure: still one turn, zero
   cost, empty `modelUsage` at ~1.9s, so no API request is ever answered.
   **The error cannot be read from a branch** — `claude-code-action` refuses
   to run when the workflow file differs from the default branch's copy
   ("Workflow validation failed"), which a test branch confirmed. Reading it
   needs either `show_full_output: true` merged to `main` briefly, or the
   repository variable `ACTIONS_STEP_DEBUG=true` and a re-run, which changes
   no tracked file.
2. **Migrate the five step-0 repos**, or decide not to. Until then they keep
   depending on an archived repository — and keep needing
   `PERSONAL_PACK_TOKEN`.
3. **Create `VOICEDEF_PACK_TOKEN` in `VoiceDefinitionOneg`** before
   `PERSONAL_PACK_TOKEN` is deleted. That is the only repo where the two
   steps cannot be done in either order.

## Two mistakes this sweep made, recorded on purpose

Both were caught by Morgan rather than by a check, and both are the kind
that repeat.

**Reporting a diagnosis from the tail of a log.** The `ANTHROPIC_API_KEY`
answer above was confidently wrong, and the evidence for it was real — an
empty variable, right next to the failure, with a matching open TODO
elsewhere. What was missing was the middle of the log, where the actual
error names itself. *Read the whole failing job, not its last screen.*

**Bumping a version header is part of editing the file.** A merged commit
here edited `VoiceDefinitionOneg`'s `TODO.md` without bumping its
`file-header` version, turning that check red on `main`. It passed on the
branch beforehand because `check_file_header.py` compares the **committed
parent**, not the working tree — so the violation only appears after the
commit exists. Fixed in a follow-up; worth knowing before testing a doc edit
against that gate.
