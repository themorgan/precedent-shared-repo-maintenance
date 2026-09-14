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

### Why that sync has never worked — a finding with a corrected diagnosis

**All three runs** of `voicedef-pack-sync.yml` in `VoiceDefinitionOneg` have
failed: 2026-08-31, 2026-09-07, 2026-09-14.

The obvious guess was the token, since `VoiceDefinitionOneg` is absent from
the list of repos `VoiceModelTemplateDefinition`'s TODO says the secret was
set on. **That guess is wrong.** The run log shows `VOICEDEF_PACK_TOKEN`
populated and the `check` job succeeding. What fails is the *update* job:
`ANTHROPIC_API_KEY` is **empty**, so the Claude Code action cannot run.

That is already a known open item in `VoiceModelTemplateDefinition`'s TODO —
*"A Claude credential needs to exist in this repo, `VoiceDefinitionMorgan`,
and `VoiceDefinitionCelia`"* — but it does not name `VoiceDefinitionOneg`,
and nobody had connected it to that repo's pack being weeks out of date.
**Setting a Claude credential there is what unsticks it**, and it will pull
in the `../personal/` link fixes as a side effect.

## What governed the judgment calls

The brief for this sweep asked for prose references in `AGENTS.md`,
`README.md`, `GLOSSARY.md`, `TODO.md` and friends to be removed.
`RPP_RETIREMENT_MAP.md` step 7, which is Morgan's own standing instruction
of 2026-09-07, says the opposite: **"Leave the mentions. Provenance notes,
decision records and backlog entries keep the name; it is not private and
the history is worth having."**

Where they conflicted, the standing instruction won. So what went in all
three changed repos is *uses* — code that called the deleted tree, wiring
that pointed at it, and dead **paths** that resolve to nothing. What stayed
is every statement of where a rule came from. TodoMorgan's eight findings
were repointed rather than deleted for exactly this reason: `"migrated from
process/personal/README.md"` became `"migrated from the retired personal
pack"`, which keeps the provenance and drops the dead path.

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
