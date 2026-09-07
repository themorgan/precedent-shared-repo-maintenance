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
**Deduplicated the same day it was written, 2026-09-07.** BestPractice landed this rule at universal level under the same slug hours after this copy was created, so the rule is in force there and a second statement of it here is what `no-duplication` says to drop. The record stays rather than being deleted, because the enforcement arrangement below is not obvious from the status alone.

**The check script in this set is deliberately kept**, even though the practice is not in force here. [`tools/checks/check_catalogue_stories.py`](../tools/checks/check_catalogue_stories.py) is the only thing that actually enforces this rule inside a practice set: universal's own check lives in `precedent_check.py`, which is in neither `ENGINE_FILES` nor `CONSUMER_ENGINE_FILES`, so it has never run in a set at all. Deleting the script to match the status would trade a working check for a tidy record. Retire it once `precedent_check.py` is vendored.

Written 2026-09-07, from a gap this set had been sitting in since it was created.

Thirty-four of this set's practices, and two of the individual set's, carried an empty `## Story`. The rules were all there and enforceable; the incidents that justified them had stayed behind in the personal rule set they were migrated out of, reachable only by knowing where to look. A rule whose reason nobody can see is the first one somebody deletes as arbitrary, which makes this a slow-acting failure rather than a cosmetic one.

The migration tool was not at fault, and the record should say so. It declines to populate Story deliberately, and documents the reason: separating an incident from its reasoning is editorial judgment, and doing it unreviewed for a whole catalogue in one pass risked mischaracterizing exactly the content the migration existed to preserve. It left `## Story` present and empty as a declared gap rather than a silent one.

The actual defect was that nothing ever came back for the declared gap, and nothing could. The universal check that demands a Story lives in a tool that is not in the vendored engine's file list at all, so it has never run inside a practice set -- the same shape as a status-contract check that turned out to be unreachable here for the same reason. A gap declared in a repo that cannot check for it is indistinguishable from one nobody declared. Hence a check owned by this set, over its own whole tree, rather than a note asking the next session to remember.

## Install
Checked mechanically by [`tools/checks/check_catalogue_stories.py`](../tools/checks/check_catalogue_stories.py), scope `tree`: it reads every `practices/*.md`, skips any whose `status:` is not `active`, and fails on an empty or whitespace-only `## Story`, naming each one. It skips any practice a committed `MANIFEST.json` attributes to another source, so it stays silent in a consuming repo on text that repo cannot fix, and checks everything in a source repo, which has no such manifest. It deliberately does not judge whether a Story is a *good* incident -- that is not a property a script can test -- only that the section says something. Two-direction tested in [`tools/checks/tests/test_catalogue_stories.sh`](../tools/checks/tests/test_catalogue_stories.sh).
