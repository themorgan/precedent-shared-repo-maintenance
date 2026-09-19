# The 2026-09-19 Actions Billing Spike — What It Was and What Changed

**Addressed to whoever next looks at this account's Actions minutes, or at
`precedent-check.yml` in any of the four practice sets, and wonders why it
has three jobs instead of one, or why `push:` names `branches: [main]`.**
Written the same day the spike was diagnosed and fixed, from all four
sets' actual workflow files as they stood that day, not from the templates
upstream. **See the ADDENDUM at the bottom, added the same day**: a second,
independent fix landed on `main` from a different session while this one
was still open as pull requests, and the two were combined rather than one
overwriting the other. Read the body below as the first half of that story.

**Date:** 2026-09-19.

## What Happened

Two days running, this account's GitHub Actions billing spiked: 183
minutes one day, 165 by noon the next. All four practice sets —
`precedent-individual`, `precedent-team-writing`,
`precedent-team-repo-maintenance`, `precedent-team-working-style` — carried
two workflows, `precedent-check.yml` and `views-drift.yml`, both triggered
on `push:` with no `branches:` or `paths:` filter, both dating that trigger
to 2026-09-14 (see either file's own header, before this fix, for why: a
session pushing straight to a source set's own branch — the normal way
work lands in a private, single-owner set — used to run no check
whatsoever). Measured against the real usage report: these four sets'
push-triggered workflows accounted for 142 of the 165 minutes billed on
2026-09-19 (86%), and did not appear in the billing data at all before
2026-09-11.

A debounce step (added 2026-09-16, alongside `concurrency:
cancel-in-progress`) already existed in both files, reading
`ci_debounce_minutes` from `identity.json` (default 360 = 6 hours) and
skipping the expensive steps when the workflow had already run recently on
that branch. It did not stop the spike, and the reason is a GitHub Actions
billing mechanic neither file's comments named at the time: **a step
skipped inside a job that already started still bills that job's full
runner-minute, rounded up — GitHub does not bill by the second, and a job
is not "cheap" just because most of its steps did nothing.** Only a *job*
whose own `if:` condition is false is reported skipped and never allocated
a runner at all, which is the one thing that actually costs zero.

With two separate push-triggered workflows, each running its own debounce
step inside its own single job, every push cost a minimum of **two**
billed minutes regardless of what either debounce window decided — one
minute for `precedent-check.yml`'s job to check out the tree and ask "have
we looked recently", one more for `views-drift.yml`'s job to do the same
thing independently. A session pushing to its own branch dozens of times
across a work session — which is exactly how work lands in these sets, per
each `AGENTS.md`'s own "before pushing" instructions — turns into dozens of
guaranteed two-minute charges no matter how generous the debounce window
is. Concurrency's `cancel-in-progress` only helps when a second push
arrives before the first run finishes; spaced-out pushes, the common case
in an interactive session, never overlap, so it never fires for them.
Raising the debounce window further would not have helped either: it
changes how often the *expensive* steps run, not how many jobs the *push
itself* unconditionally starts.

## The Fix

`precedent-check.yml` in all four sets now has three jobs instead of one,
and `views-drift.yml` no longer exists as a separate file:

1. **`debounce`** — runs on every push, checks out the tree (shallow; it
   only reads `identity.json`, never git history) and makes the "have we
   looked recently" decision exactly once, exposing it as a job output.
2. **`precedent-check`** — `needs: debounce`, `if:
   needs.debounce.outputs.skip != 'true'`. Unchanged from before: same
   four named refusal/run steps, same full-suite `precedent_check.py`
   invocation, same `fetch-depth: 0` checkout.
3. **`views-drift`** — same gating, folded in from the old `views-drift.yml`
   file with its steps otherwise untouched: same three-way layout
   decision, same `build_views.py --check` call, same refusal messages.

Because `precedent-check` and `views-drift` are gated at the **job** level
via `needs:` + `if:`, not a step inside a job that already ran, the common
(debounced-skip) case now bills exactly one job-minute per push — the
`debounce` job alone — instead of two. The rare case (first push in six
hours, or `ci_debounce_minutes: 0`) bills about what it always did: the
debounce job's own minute plus each check's own run, still in parallel.
Nothing about *what* either check verifies changed, and the push-on-every-
branch trigger, the missing `paths:`/`branches:` filter, and the whole-
suite (not `--strict`) run are all untouched — see each job's own header
comments in the merged file for why those stay as they are. Only how many
jobs a single push unconditionally pays the one-minute floor for changed.

All four sets carry the identical merged file, byte-identical (sha256
`237a77a6c360292decc01d61a266c5b2310e32977485e5cc6d2b17e2099eaebc` after
the ADDENDUM below folded in the `branches: [main]` restriction; it was
`3078a6aad65a064efa3cc885cc6d41a30e284975bc99ca6a5f2be0ffb6cd9d39` before
that), same as the two files it replaces were. `tools/ENGINE_MANIFEST.json`'s
`ci_workflow_files`/`ci_workflows_sha256` in each set was updated to drop
the now-nonexistent `views-drift.yml` entry and record the merged file's
hash — leaving the old entry in place would have had a future
`precedent_vendor_engine.py refresh` report the missing file as drift and
refuse to proceed.

## Tradeoff, Stated Explicitly

The two checks used to keep **independent** six-hour debounce clocks, one
per workflow name (`gh run list --workflow <name>`). They now share
**one**, keyed off the merged workflow's single name. Both are described,
in their own steps' comments, as whole-catalogue *advisory* checks over the
same tree rather than a security backstop, and in practice they drift
together (both changed on 2026-09-14 and 2026-09-16 for the same reasons,
on the same day, in lockstep) — so collapsing them to one clock is judged
to cost nothing anyone would notice. If that judgment turns out wrong —
if `views-drift` ever needs to run on a cadence `precedent-check` doesn't
— split them back into two debounce jobs sharing the same `debounce`
job's checkout, rather than reverting to two full workflow files; that
keeps the one-job-minute floor for the common case while giving each check
its own clock.

A second, smaller tradeoff: `views-drift`'s failure messages used to be
the *only* named check in the PR/commit status list calling out generated-
view drift by that name. It is now a job named `views-drift` inside the
single `Precedent checks` workflow rather than a separately-named
top-level check — still fully visible and still carrying its own step
names and messages, just one level deeper in the Actions UI than before.

## Do Not "Fix" These Back

- **No `paths:` filter was added, and none should be** — it would report
  nothing while looking green on an input it missed; see each job's own
  header for why. **A `branches: [main]` filter WAS added**, but not by
  this fix — see the ADDENDUM below. As originally written, this section
  argued against adding one at all; that argument held only until Morgan
  made the opposite call, deliberately, in a different session the same
  day. Don't re-litigate that call from this document's original text —
  read the ADDENDUM for what actually shipped and why.
- **`views-drift`'s coverage was not narrowed to "whatever
  `generated-artifact-provenance` already covers."** That check (part of
  `precedent-check`'s own suite, `binds_publishers` since BestPractice PR
  #261) covers `MAP.md` and `GLOSSARY.md` — whole generated files — but
  explicitly defers `AGENTS.md`'s generated loader-block drift to
  `verify_harness.py`, which is deliberately not vendored into a source
  set (see `precedent_vendor_engine.py`'s own docstring). Removing
  `views-drift` entirely, rather than folding it in, would have silently
  dropped the only thing in these repos that catches loader-block drift —
  this was checked directly (`tools/precedent_check.py`'s own
  `_generated_artifact_provenance` docstring) before deciding to fold
  rather than delete.
- **The debounce window itself was never the problem** — see "What
  Happened" above; the fix in this document's original text is the
  job-count restructuring, not a window change. Its default (`
  ci_debounce_minutes`) WAS separately tightened, 360 → 30, by the same
  other-session decision the branches:[main] restriction came from — see
  the ADDENDUM.

## Relationship to `CHECK_WORKFLOW_TEMPLATE_FINDINGS.md`

That file is a different, still-live comparison: four ways these sets'
copy of `precedent-check.yml` is *stronger* than the upstream BestPractice
template, written 2026-09-13 against a template read that same day. Its
recorded sha256 for the sets' file (`1df3d91f148a7728485a…`) already
predates the 2026-09-14 push-trigger change and the 2026-09-16
concurrency/debounce additions, so it was stale before this fix touched
anything — that document was not updated here, and shouldn't be conflated
with this one.

**UPDATE, same day, checked directly rather than assumed:** this file
originally claimed a fifth divergence from upstream here (the merged-file
design existing locally but not in BestPractice's own template) and said
nothing here had been applied upstream, on the reasoning that a session
rooted in a practice set can never gain push access to BestPractice. Both
claims turned out to be wrong, not because that reasoning was faulty, but
because a **different session had push access to BestPractice directly**
and used it: BestPractice's `templates/github-actions/precedent-check.yml.template`
already carries this exact design, merged there the same day via PR #476
("Template cost discipline: consolidate + pull_request trigger, all three
CI templates") — diffed directly against this repo's own merged file:
mechanically identical (same three jobs, same `branches:[main]` +
`pull_request` trigger, same 30-minute debounce default), differing only
in header prose (upstream cites its own `spec/CI_MINUTES_PLAN.md`; these
sets cite this document). `views-drift.yml.template` is gone upstream too.
So there is no fifth divergence to carry upstream: it converged there on
its own, concurrently, not because anything from these four sets was
pushed there. New repos bootstrapped from the template from here on get
this design automatically.

## ADDENDUM, Same Day: A Second Fix Landed Concurrently, and the Two Were Combined

While the job-count fix above sat open as four pull requests, a
**different session** (the one that originally diagnosed this spike,
`session_01UcMeVemrxF6xtCkKwP6z87`) pushed and merged a second, independent
fix straight to `main` in all four sets: `precedent-check.yml`'s (and, at
the time, `views-drift.yml`'s separate) `push:` trigger narrowed to
`branches: [main]`, and `ci_debounce_minutes` tightened from 360 to 30.
That session's own commit message states the tradeoff in as many words:
*"This reopens the exact gap 2026-09-14 closed... Morgan's call, 2026-09-19,
weighed against that gap and accepted it."*

That is a **different lever** from the one this document's original text
argues for, not a duplicate of it:

- The job-count fix (above) cuts the floor cost of a push this workflow
  still runs on. It changes nothing about which pushes trigger the
  workflow.
- The `branches: [main]` fix cuts how many pushes reach the workflow at
  all, by giving up automatic verification on a branch pushed to directly
  — the exact working-branch coverage this document's "Do Not Fix These
  Back" section (as originally written) argued should never be traded away.

Told about the conflict, Morgan's instruction was explicit: **combine
both, keep `branches: [main]`.** The two don't fight each other
mechanically — one is about job count per triggered run, the other is
about which pushes trigger a run at all — so the merged workflow file now
carries both: `push: branches: [main]` plus `ci_debounce_minutes` default
30, alongside the single-`debounce`-job structure from earlier in this
document. Combined sha256:
`237a77a6c360292decc01d61a266c5b2310e32977485e5cc6d2b17e2099eaebc`.

**What this means going forward, stated plainly because the rest of this
document argues the other way:** a working branch (any `claude/*` session
branch, the normal way work lands in these sets) again gets **zero**
automatic CI, same as before 2026-09-14. `python3 tools/precedent_check.py`
before pushing (already each `AGENTS.md`'s own instruction) is now the only
check a working branch gets; a violation is caught by CI only once that
branch reaches `main`. This is a deliberate, informed, twice-confirmed
tradeoff of Morgan's — not a regression, and not this document's original
author quietly losing the argument. If a future reader is tempted to
"fix" the coverage gap back by widening `push:` again, read `AGENTS.md`
first: this is the second time this exact tradeoff has been made in this
account's history (2026-09-14 → widen; 2026-09-19 → narrow again, on
purpose, for cost), and a third reversal should come from a new explicit
decision, not from rediscovering the 2026-09-14 incident and assuming
nobody already knew about it.

`AGENTS.md` and (in `precedent-individual`) `identity.json`'s own comments
were updated in each of the four sets to describe this combined, current
state accurately, rather than leaving them describing only the first half.
