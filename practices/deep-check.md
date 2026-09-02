---
slug:        deep-check
title:       "The deep check: every audit, plus an open-ended coherence review"
tier:        on-demand
severity:    default
applies_to:  ["**"]
occasion:    "asked for a \"deep check\" by name, or after drift-inviting work"
gates:       ["merge"]
index_clause: "every mechanical audit, plus a full read of the repo against itself"
checked_by:  tools/checks/check_deep_check.py
defines:     []
status:      active
supersedes:  []
overrides:   null
added:       2026-08-31
approved_by: "Morgan F, migrated from RepoPersonalPreferences by the private-set migration session"
---
## Rule
A deep check has two halves. The mechanical half is every audit script the repo maintains, run together -- the same set the merge runbook already runs on every merge, and all of it must pass before the merge commits. The review half is a read of the repo's own rules and documents against each other -- the audits catch broken links and bad syntax; they can't catch a rule that now contradicts another rule, or a section that stopped making sense a few edits ago.

## Detail
What to look for -- a starting point, not a specification: contradictions between rules; stale references (a slug, number, filename, or click-path that points at something moved or gone; a positional number cited as if it were a name; an orphaned name left over from a rename elsewhere); fragments left behind by an earlier edit; needless repetition of the same rule in several places; disproportion (paragraphs on a minor point, a rule buried where it no longer fits); process-cost disproportion (a minor rule that costs a disproportionate amount of tokens, time, or friction each time it applies, especially one re-researched from scratch instead of following a written-down answer); formatting and spacing drift (heading levels and capitalization, missing blank lines, ragged tables, a stale header); self-application (a rule this set asks of every project it's installed into that this set doesn't follow itself); and backlog-document drift (items already done or no longer relevant). Anything else the read turns up is still a finding -- report it, and if it will recur, add a bullet here.

Fix what the review turns up in the same pass, then re-run the mechanical half, since the fixes themselves can break a link. Anything deliberately left alone gets a line in the backlog document saying so.

When it runs: the mechanical half on every merge, per the runbook. The full deep check, both halves, whenever asked for by name, and after work that invites drift -- a batch of rules added or reordered, a rule that changed shape, an install into a new repo, or a merge that resolved conflicts across several shared files.

## Why
It is deliberately not a per-commit gate: the review half costs a careful read of the whole repo, which is exactly why the light check exists to carry the cheap checks on every commit instead.

## Story


## Install
Checked mechanically, but only half of it: [`tools/checks/check_deep_check.py`](../tools/checks/check_deep_check.py), scope `tree`, verifies the mechanical half's own claim is actually true -- that [`tools/checks/tests/run_all.sh`](../tools/checks/tests/run_all.sh) really does run every audit script the repo maintains. It catches a check script added with no matching test (so `run_all.sh`'s `test_*.sh` glob would silently never exercise it) and a stale test left behind after its check script was removed. The review half -- reading the repo's own rules against each other for contradiction, drift, or disproportion -- is explicitly the part no audit can catch (per this file's own Rule: "the audits catch broken links and bad syntax; they can't catch a rule that now contradicts another rule"); that's a judgment call by design, not a gap to close. Two-direction tested in [`tools/checks/tests/test_deep_check.sh`](../tools/checks/tests/test_deep_check.sh).

