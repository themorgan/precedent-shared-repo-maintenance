---
slug:        catalogue-carries-stories
title:       Every active practice in this set carries a non-empty Story
tier:        on-demand
severity:    default
applies_to:  ["practices/*.md"]
occasion:    "landing practices in bulk -- a migration, an import, or a move from another set"
gates:       ["merge"]
index_clause: "no active practice in this set sits with an empty ## Story"
checked_by:  null
defines:     []
status:      deduplicated
in_force_at: catalogue-carries-stories
supersedes:  []
overrides:   null
added:       2026-09-07
approved_by: "Morgan F, 2026-09-07"
---
## Rule
Every practice in this set with `status: active` carries a non-empty `## Story`. This is a standing invariant over the whole catalogue, checked across the entire tree rather than only across the files a branch happens to touch -- so a practice that arrives with an empty Story is red immediately, and stays red until somebody writes the incident down.

## Detail
Where the incident genuinely does not exist -- a practice written as a stated preference, or one carried over from a set whose own text recorded reasoning rather than a failure -- the Story says *that*, plainly, and that satisfies this rule. An honest "no originating incident was recorded, and this Story does not invent one" is a real Story. What this rule refuses is silence, not the absence of drama.

A practice that is not `status: active` is out of scope: a deduplicated record points at whichever practice is actually in force, and that one carries the Story.

**Only practices this repo authors are in scope.** In a repo that consumes this set, `practices/` is materialized output rewritten from every declared source on each sync, so a Story missing from another source's practice cannot be written there and would be overwritten if it were. The rule binds a source repo about its own catalogue.

## Why
The universal catalogue already asks an author to record the failure a rule prevents, and enforces it at authorship time on changed files. That is the right gate for writing one practice and the wrong one for receiving thirty-four at once, which is exactly how this set acquired its own catalogue. An authorship-time check on changed files also cannot see a gap that is already sitting in the tree: once the landing commit is behind you, nothing looks at those files again.

A standing invariant sees both. It fires on the landing commit, and it keeps firing every day the gap stays open, which is the property that actually makes the backlog get paid down instead of noticed once and deferred.

## Story
**Deduplicated a second time, 2026-09-13**, once `binds_publishers` removed the mechanism the 2026-09-07 re-activation existed to work around.

BestPractice PR #261 (2026-09-12) added that flag to `precedent_check.py`: a check carrying it binds any repo that PUBLISHES a practices/ tree, whether or not the practice's own text is vendored there. `catalogue-carries-stories` carries it, so the universal check now runs on this set's catalogue off universal's text, with no local declaration switching it on. Verified in this tree the same day, on the refreshed engine: with this file `status: deduplicated`, `--only catalogue-carries-stories` still reports `1 passed`, not `1 skipped`. The rule did not stop binding; only this copy of it went away. Upstream's `precedent_check.py` names this set by description as the one that "re-declared this practice locally purely to defeat the gate", and asked for the copy back once the flag landed.

**Deduplicated and then re-activated the same day, 2026-09-07, and the round trip is the point.** BestPractice landed this rule at universal level under the same slug hours after this copy was written, so it was marked deduplicated as `no-duplication` asks. That turned out to be wrong for a mechanical reason nobody had written down: **a source repo consumes no catalogue**, so universal's copy never reaches this set, and `precedent_check.py` gates every check on its practice actually being in force *here*. Deduplicating it did not defer enforcement to universal — it switched enforcement off.

So this file is not a restatement of the universal rule; it is the mechanism by which a source set puts that rule in force on its own catalogue. `checked_by` stays `null` because the check itself is universal's, now vendored in `ENGINE_FILES` and running here.

**The local check script was retired in the same commit.** `tools/checks/check_catalogue_stories.py` existed only because `precedent_check.py` was in `CONSUMER_ENGINE_FILES` but not `ENGINE_FILES` — a consuming repo got the universal checks and a source set never did. (Corrected 2026-09-07: an earlier note here said *neither* list, which was wrong about consumers and right about sources.) With that fixed upstream and the engine refreshed, the universal check runs here and the local copy was two implementations of one rule.

Written 2026-09-07, from a gap this set had been sitting in since it was created.

Thirty-four of this set's practices, and two of the individual set's, carried an empty `## Story`. The rules were all there and enforceable; the incidents that justified them had stayed behind in the personal rule set they were migrated out of, reachable only by knowing where to look. A rule whose reason nobody can see is the first one somebody deletes as arbitrary, which makes this a slow-acting failure rather than a cosmetic one.

The migration tool was not at fault, and the record should say so. It declines to populate Story deliberately, and documents the reason: separating an incident from its reasoning is editorial judgment, and doing it unreviewed for a whole catalogue in one pass risked mischaracterizing exactly the content the migration existed to preserve. It left `## Story` present and empty as a declared gap rather than a silent one.

The actual defect was that nothing ever came back for the declared gap, and nothing could. The universal check that demands a Story lives in a tool that is not in the vendored engine's file list at all, so it has never run inside a practice set -- the same shape as a status-contract check that turned out to be unreachable here for the same reason. A gap declared in a repo that cannot check for it is indistinguishable from one nobody declared. Hence a check owned by this set, over its own whole tree, rather than a note asking the next session to remember.

## Install
Checked mechanically by the universal catalogue's own `precedent_check.py`, vendored here in `ENGINE_FILES`, scope `tree`: every `practices/*.md` whose frontmatter `status:` is `active` must carry a non-empty `## Story`. `status:` is read from the frontmatter block only, never searched for anywhere in the file, since several practices here discuss the status vocabulary in their own prose. A practice a committed `MANIFEST.json` attributes to another source is skipped. It tests that the incident was recorded, never that it was the right incident.

`checked_by` is `null` and always was, because the check has never been this set's to own: it is universal's, vendored here in `ENGINE_FILES`. What changed on 2026-09-13 is that it no longer needs this file to reach the catalogue -- `binds_publishers` does that -- so `checked_by: null` on a `deduplicated` file now says exactly what is true, where on an `active` one it had come to read as though this declaration were the coverage. **Nothing here is to be copied into another source set.** A set on an engine carrying `binds_publishers` needs no local declaration; a set on an older engine should refresh rather than re-declare. This set carried its own `tools/checks/check_catalogue_stories.py` until 2026-09-07, retired once the universal check reached source sets -- two implementations of one rule, which is the state `engine-plus-host-shims` exists to prevent, and a local re-declaration was the third.
