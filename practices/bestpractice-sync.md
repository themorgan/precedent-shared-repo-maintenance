---
slug:        bestpractice-sync
title:       A scheduled sync keeps a vendored universal set current, unattended
tier:        on-demand
severity:    default
applies_to:  ["**"]
occasion:    "a repo vendors a universal or team practice set as tracked files"
gates:       []
index_clause: "a scheduled workflow keeps the vendored universal copy current"
checked_by:  null
defines:     []
status:      deduplicated
in_force_at: bestpractice-sync
supersedes:  []
overrides:   null
added:       2026-08-31
approved_by: "Morgan F, migrated from RepoPersonalPreferences by the private-set migration session; retired by Morgan F"
---
## Rule
A repo that vendors a universal or team practice set as tracked files runs a scheduled workflow that compares the recorded source commit against the source's actual head, and -- if it moved -- takes the update: merge each changed file through its recorded adaptation, re-run every gate, commit with every judgment call spelled out under a "Judgment calls to review:" heading, open a PR, and merge once checks pass.

## Detail
The comparison itself costs nothing -- a single remote query, no model call -- on a quiet run where nothing moved. If the run can't confidently resolve something, it leaves the PR open, unmerged, with a comment explaining exactly what it couldn't do; it never forces a merge past a failing check. If the workflow requires a model credential and none is configured when the source has moved, it skips the update rather than failing on an auth error, and reports that it skipped rather than looking like a quiet "nothing to sync" run.

## Why
Nothing is fetched from a remote when a working session starts -- the vendored copy is what's on disk -- so a background sync is what keeps that copy from silently going stale between sessions.

## Story
Migrated here by the original RepoPersonalPreferences split under that
migration's own "default everything ambiguous to team" rule, without a
separate check of whether it was actually team-appropriate. It wasn't:
unattended, auto-merging automation is a preference about how *one*
person's own projects behave, not a convention this team's second member
(Alex) separately agreed his own repos should run. Retired here and moved
to Morgan's own individual practice set on 2026-09-03, following
BestPractice's own
[spec/MOVING_PRACTICES.md](https://github.com/alex137/BestPractice/blob/precedent-beta-v01/spec/MOVING_PRACTICES.md)
pattern (landed there first, retired here second). Not ruled out for the
future: if a team genuinely wants this behavior and its approvers agree to
it as their own choice, it can move to a team set again — narrowest first,
same as any other practice.

## Install
No mechanical check: the workflow this practice requires runs in a *consuming* repo that vendors a universal or team set, comparing its recorded source commit against the source's actual head. This repo is a source, not a consumer of one -- there is no vendored copy and no such workflow to check here.

