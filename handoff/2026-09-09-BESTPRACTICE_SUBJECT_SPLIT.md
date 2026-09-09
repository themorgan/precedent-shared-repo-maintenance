<!-- Last updated: 2026-09-09 10:52:00 (Buenos Aires) by Morgan F, to version 1 -->

# BestPractice changes for the subject split — apply from a BestPractice-rooted session

**Status: not applied upstream.** Four commits against
`precedent-beta-v01`, exported as
[`2026-09-09-bestpractice-subject-split.patch`](2026-09-09-bestpractice-subject-split.patch).
Same shape as [`NOT_BINDING_FINDINGS.md`](../NOT_BINDING_FINDINGS.md) and
[`LEAK_SCRUB_FINDINGS.md`](../LEAK_SCRUB_FINDINGS.md): output produced here
because this is where the work happened, for a later session that can
actually push there to act on.

## Why it is here and not upstream

The session that did the split was rooted at a `themorgan/` repo, because
that is the only way to hold all five private sets at once. `add_repo` then
refused `alex137/BestPractice` — *"cross-tier adds are not supported in v1:
requested `alex137/bestpractice` but session already has repos from owner(s)
`[themorgan]`"* — so the clone had no credential and the push returned 403.
This is the condition Precedent's own `AGENTS.md` gotcha describes, and it
is why work spanning both owners is split across two sessions. The private
half of the split is fully landed and pushed; only this public half is
waiting.

## What the patch does

| File | Change |
|---|---|
| `INSTALL.md` | A repo declares as many team sets as its work needs. Adds the table answering *which* ones from the kind of work the repo is for, and the pattern under it. |
| `templates/nontechnical-document-project/AGENTS.md` | The session-start `add_repo` instruction named one set outright; it now reads the names out of `precedent.json`, so declaring another set is one edit rather than two files kept in agreement by hand. |
| `templates/nontechnical-document-project/precedent.json` | Declares the two new subject-scoped sets; says why the repo-mechanics set is deliberately not declared; corrects this file's own description of that set as "code-repo conventions", which was never true. |
| `TODO.md` | Closes `split-team-sets-by-subject` with what the sort found and the migration path repos on the old declaration follow. |

## To apply

```
git checkout -b claude/split-team-sets-by-subject origin/precedent-beta-v01
git am handoff/2026-09-09-bestpractice-subject-split.patch
```

Then the deep check, and a pull request **against `precedent-beta-v01`,
never `main`**.

## Deep check already run, in the session that wrote it

Against the same tree, with the private sets resolved and
`PRECEDENT_LEAK_BLOCKLIST` exported:

- `verify_harness.py` — **138 passed, 0 failed**, 1 not yet applicable
- `doc_lint.py` — **exit 0, zero errors**; 179 unlinked-reference warnings, all pre-existing, none on a line this patch adds
- `leak_gate.py` — **OK**, private half live, 926 units clean
- `precedent_check.py` — **0 violated**
- `doc_sync.py` — **OK**

Two modules had to be installed by hand first (`pip install cmarkgfm
markdown`) because a repo attached mid-session never runs its own
SessionStart hook. Without them `verify_harness` reported 3 failures and
`doc_lint` silently skipped its strikethrough check — both are the gotcha
already recorded upstream, not new.

**Re-run the deep check after applying anyway**: these results are from a
tree that had not yet been rebased onto whatever `precedent-beta-v01` has
moved to since.
