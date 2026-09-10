# Source-Supplied Check Audit — Install-Model Assumptions

**This file is the record of an audit, not a practice and not a decision.**
It exists so the next person does not run this pass again. It covers the
audit clause of BestPractice's TODO item 52
(`source-checks-adopt-engine-helpers`), for the three team sets that item
does not itself name.

**Date:** 2026-09-10.
**Engine read at:** `alex137/BestPractice` `precedent-beta-v01`, commit
`680ee07` — the commit that added the two helpers this audit exists to
adopt.

## What Was Being Looked For

Three defects in source-supplied checks were found on 2026-09-10 by
installing `precedent-beta-v01` into a real private project via
INSTALL.md §0 — the first real-project install, after the design had only
ever been walked against scratch repositories. Every one of them was the
same shape: **a check re-deriving from private assumptions something that
is only true of one install model.** In the defect report's own words,
*"this one was found because it fired, not because anything looked for
it."* Nothing in any set distinguished "reads a §1 path" from "reads a
path", so this pass looked, deliberately, at all four classes:

1. a §1-only path (`process/upstream/...`, `process/manifest.json`)
   treated as universal — §0 step 5 says outright to skip the manifest,
   and a §0 install puts the engine at `tools/` and the vendored
   catalogue at whatever path `precedent.json` declares;
2. an absent optional file reported as a violation, where the honest
   answer is `NotApplicable`;
3. an unguarded import of an optional engine module — `precedent_resolve.py`,
   `doc_lint.py`, `doc_sync.py` and `title_case.py` are in upstream's
   `CONSUMER_ENGINE_FILES` but **not** its `ENGINE_FILES`, so they are
   absent inside a practice-set repo and a bare import there ERRORs;
4. a `scope: tree` check that walks `git log` and reads an empty result
   as clean.

## Scope Audited

| Set | Checks supplied | Verdict |
|---|---|---|
| `precedent-team-maintainers` (this repo) | 6 | 3 defects found and fixed, 3 open items recorded below |
| `precedent-team-tms` | **none** | Nothing to audit — see "The Two Sets With No Checks" |
| `precedent-team-working-style` | **none** | Nothing to audit — see "The Two Sets With No Checks" |

## The Two Sets With No Checks

Neither `precedent-team-tms` nor `precedent-team-working-style` has a
`tools/checks/` directory at all, and neither has a `check_*.py` anywhere
in its tree. This was confirmed two ways rather than assumed from a
missing directory: a `find` for `check_*.py` across each whole repo
returned nothing, and a grep of each `practices/` tree for `check_`
or `checks/` found no practice claiming a check that has gone missing.
Their `tools/` trees are the vendored engine only.

**That is a real result and not a gap.** A source set supplies checks only
for practices whose own `Install` names one; both of these sets are
prose-tier practice sets whose rules are about register and working style,
and `checked_by: null` is the honest and correct answer for a rule about
how to talk to somebody. Each set has been given its own copy of this
record so the next person does not re-derive the same emptiness.

## Verdict 1 — Fixed

Each of these is a defect in one of the four classes above, fixed in
`claude/source-checks-adopt-engine-helpers` and verified in both
directions (the state that should now pass, **and** the state that must
still fire, asserting the finding text and not merely a non-zero exit).

### `check_light_check.py` — class 1, a §1-only path treated as universal

`_link_check_exempt` was the literal `rel.startswith("process/upstream/")`.
That is §1's layout. A §0 install has no `process/upstream/` and no
`process/manifest.json`, so the exemption matched nothing and the
broken-relative-link scan walked straight back into the vendored
catalogue.

**Measured, not argued.** A §0 fixture built exactly as INSTALL.md §0
step 1 describes — upstream's `practices/` tree vendored to
`precedent/universal/practices/`, the consumer engine seeded with
`precedent_vendor_engine.py seed --kind consumer`, a `precedent.json`
declaring that source, and deliberately no `process/` directory at all —
produced **174 broken-relative-link findings inside the mirror**, not one
of them actionable: editing a mirror is forbidden and the next sync would
overwrite the edit anyway. This is the `no-stale-counts` failure exactly,
in a different check.

Now asks `precedent_resolve.mirrored_prefixes(ROOT)`. On that same
fixture: 174 → 0, and a broken link in the repo's own content still
fires with its own path named.

### `check_derived_file_marker.py` — class 1, the same assumption unstated

This walked every tracked file with **no** mirror exclusion at all. It had
never fired inside a mirror only because nothing in the vendored
catalogue happens to open with a `DERIVED from` line — luck, not scope.
Fixed with the same helper. Proved with one byte-identical planted file
placed inside the mirror (silent) and outside it (fires, and is the only
finding).

**How the helper is imported, and why it is not `NotApplicable`.** Both
checks carry the call as a marked `shared:mirrored-prefixes` block, so
`check_light_check.py`'s own `check_shared_blocks_agree` keeps the two
copies byte-identical — these are deliberate copies, since a check script
runs standalone and cannot import a sibling. The import of
`precedent_resolve` is guarded, and on failure falls back to the §1
literal rather than raising `NotApplicable`: that module is absent inside
a practice set by design, and the exclusion is a *refinement of where to
look*, not the check's subject. Skipping the whole check over it would
trade a false finding for a missing one. In a source set
`mirrored_prefixes()` returns `()` regardless, so nothing changes when
these run in place here.

### `check_session_trailer.py` — class 4, an empty walk read as clean

`Scope: tree`, walks `git log`, reported clean whenever it found nothing.
On a shallow clone the walk stops at the graft boundary, so "nothing to
report" and "could not look" produced the same green.

**Measured in this repo, on the clone this audit started from:** `git log`
saw 101 commits and the check said clean; after
`git fetch --depth=1000 origin main` it saw 114. Thirteen commits had
never been examined and nothing said so. None of the thirteen turned out
to violate — which is luck, and precisely why it is worth a guard.

It now exits 2 (`SKIPPED`, the could-not-run convention) when the history
is truncated **and** it found nothing, and still exits 1 when a violation
is visible inside the slice it can see. That ordering is deliberate: a
partial view can only cost findings, never invent them, so what it did
see is trustworthy. The one thing it must not do is call the repo clean.

Note this is a different hazard from the one `_is_merge` already
documented. That one is about how git *pretty-prints* a commit at the
boundary; this one is about which commits the traversal reaches at all.
Fixing the first in 2026-09-06 did not fix the second, and the check
carried both at once.

## Verdict 2 — Looked At, No Defect

- **`check_private_repo_scrub.py`** scans prose and excludes foreign
  practices, so it was the obvious candidate for class 1. It is correct:
  its attribution comes from `MANIFEST.json` at the repo root, which
  `precedent_materialize.py` writes at `out_dir` root in **both** install
  models — it is not `process/manifest.json` and does not inherit that
  file's §0 problem. It also does not need `mirrored_prefixes()`: it scans
  only `practices/*.md`, and the materialized `practices/` tree is
  deliberately *not* a mirrored prefix (the helper's own docstring says
  so), because that is where a consuming repo's practices actually live.
- **`check_default_branch.py`** already uses the `NotApplicable`
  convention correctly for all three of its could-not-run states.
- **Class 3 is absent from this set entirely.** No check here imports
  `precedent_resolve`, `doc_lint`, `doc_sync` or `title_case` — verified
  by reading every import in all six scripts. The two that now import
  `precedent_resolve` do so guarded, as described above.

## Verdict 3 — Open Items

Recorded rather than fixed, each with what it is blocked on. This repo has
no `TODO.md`; `todo-gate` says "`TODO.md` **or equivalent**", and these
belong with the audit that produced them rather than in a new file
carrying nothing else.

1. **`check_deep_check.py` reports an absent `tools/checks/` as a
   violation.** With `PRECEDENT_CHECK_ROOT` pointed at a repo that has no
   check directory at all — a sibling source set, for instance — it
   reports `tools/checks/tests/run_all.sh is missing -- there is no
   'every audit script, run together' entry point at all`. Confirmed by
   running it against `precedent-team-tms`. That is class 2 in shape: a
   repo shaped differently, not a repo that did the wrong thing.
   **Not fixed, and not currently reachable in a real install:**
   `precedent_sync_views.py` runs `precedent_materialize.py`, which
   *generates* `run_all.sh` rather than copying it, so every consuming
   repo has one. **Blocked on** a judgment that is the practice's to make
   and not an auditor's: whether "a repo with no materialized checks"
   is a `deep-check` violation or a `NotApplicable`. Deciding it here
   would be redesigning the practice under cover of a defect fix.
2. **`import yaml` at module scope in `check_light_check.py` is
   unguarded.** PyYAML is a third-party dependency rather than an engine
   module, so this is not the class-3 defect — but if it is absent the
   check ERRORs, which reads as a broken tool rather than an absent
   dependency. **Blocked on** knowing whether every environment that runs
   these checks is guaranteed PyYAML: this repo declares no dependency
   manifest (no `requirements.txt`, no `pyproject.toml`) and has no CI
   workflow at all, so there is nothing to read the answer off.
3. **`_is_merge`'s docstring in `check_session_trailer.py` cites
   "AGENTS.md's environment-gotchas", which `AGENTS.md` does not
   contain.** A dead cross-reference; confirmed by grep. Behaviourally
   harmless, and not caught by the link check because it is not a
   markdown link. **Blocked on** nothing but scope — this pass audited
   check behaviour, and rewriting comment prose was not part of it.

## What This Audit Could Not Do

TODO item 52 lives in `alex137/BestPractice`, a different owner. This
session could read that repo (it is public) but could not push to it, so
**item 52 is not closed** — this record is the evidence a later
BestPractice-rooted session needs to close it against something real
rather than against an assumption.
