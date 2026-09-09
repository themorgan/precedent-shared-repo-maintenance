---
slug:        bestpractice-sync
title:       A scheduled sync keeps a vendored universal set current, unattended
tier:        on-demand
severity:    default
applies_to:  ["**"]
occasion:    "a project of mine vendors a universal practice set as tracked files"
gates:       []
index_clause: "a scheduled workflow keeps the vendored universal copy current"
checked_by:  null
defines:     []
status:      active
supersedes:  []
overrides:   null
added:       2026-09-03
approved_by: "Morgan F"
---
## Rule
A project of mine that vendors a universal practice set as tracked files runs a scheduled workflow that compares the recorded source commit against the source's actual head, and -- if it moved -- takes the update: merge each changed file through its recorded adaptation, re-run every gate, commit with every judgment call spelled out under a "Judgment calls to review:" heading, open a PR, and merge once checks pass.

## Detail
The comparison itself costs nothing -- a single remote query, no model call -- on a quiet run where nothing moved. If the run can't confidently resolve something, it leaves the PR open, unmerged, with a comment explaining exactly what it couldn't do; it never forces a merge past a failing check. If the workflow requires a model credential and none is configured when the source has moved, it skips the update rather than failing on an auth error, and reports that it skipped rather than looking like a quiet "nothing to sync" run.

This is *my own* preference about how unattended automation behaves on *my own* projects -- merging without waiting for me to review each upstream update by hand. It is not something I've decided every project I touch should run this way by default; a project I work on with someone else adopts it only if they separately want it too.

## Why
Nothing is fetched from a remote when a working session starts -- the vendored copy is what's on disk -- so a background sync is what keeps that copy from silently going stale between sessions.

## Story
Migrated to `precedent-team-maintainers` in the original RepoPersonalPreferences split, by that migration's own "default everything ambiguous to team" rule. On reflection that default was wrong for this one: unattended, auto-merging automation is a preference about how *I* want *my own* projects to behave, not a convention I get to decide Alex's projects should run just because we share a team practice set -- adopting it as team policy would apply it to his repos without his own separate say-so on that specific behavior. Moved here on 2026-09-03, following [spec/MOVING_PRACTICES.md](https://github.com/alex137/BestPractice/blob/precedent-beta-v01/spec/MOVING_PRACTICES.md)'s pattern (landed here first, then retired in `precedent-team-maintainers` with a note pointing back). Nothing here rules out moving it to a *different* team's set later, if a future team I work with wants the same behavior and agrees to it as their own choice -- narrowest first, same as any other practice.

**Moved to `precedent-team-maintainers` on 2026-09-09**, from `precedent-individual`, in the subject split recorded at Precedent's `TODO.md#split-team-sets-by-subject`. It was written as one person's own default, but the thing that breaks when it is wrong is a repository the whole team works in -- a stale checkout, a practice file whose links die on materialization, a vendored engine nobody refreshes. That is the maintaining team's business, not one person's preference. The copy left behind in the individual set is `status: deduplicated` and points here.

## Install
No mechanical check: the workflow this practice requires runs in a *consuming* repo that vendors a universal set, comparing its recorded source commit against the source's actual head. This repo is a source, not a consumer of one -- there is no vendored copy and no such workflow to check here.
