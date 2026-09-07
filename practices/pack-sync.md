---
slug:        pack-sync
title:       A sync keeps a vendored team set current, the same way, against a private source
tier:        on-demand
severity:    default
applies_to:  ["**"]
occasion:    "a project repo vendors this team's own practice set, and it has moved"
gates:       []
index_clause: "the team-set sync is the universal sync's sibling, against a private repo"
checked_by:  null
defines:     []
status:      active
supersedes:  []
overrides:   null
added:       2026-08-31
approved_by: "Morgan F, migrated from RepoPersonalPreferences by the private-set migration session"
---
## Rule
Same shape as the scheduled sync that keeps a vendored universal set current, pointed at this team's own set instead: a project repo that vendors this team's practices runs the same compare-then-update workflow against this team's own source repo.

## Detail
The one real difference: this team's own source repo is private, so both the comparison and the update need their own repository credential to reach it, in addition to whatever model credential the update step itself needs. No workflow, and no session, can mint or install that credential on a repo's behalf -- an administrator has to generate and add it themselves. A run that skips the update because that credential is missing still reports that it skipped, every time, so a credential that was never set or later revoked gets noticed rather than silently degrading the sync forever.

## Why
A private source needs its own credential precisely because it is private -- a public source needs none, which is the whole difference from the universal-set sync.

## Story
Migrated here from RepoPersonalPreferences by the phase-3 private-set
migration; the Story is backfilled from that pack's own text.

The trigger was a threshold rather than a failure: copying the pack once at
install is sufficient right up until rules start being added often enough
that every dependent repo is quietly running an old copy. This sync is the
sibling of the universal one -- same compare-then-update shape, separate
workflow, separate concern -- pointed at the private source instead of the
public upstream.

The one real difference from its sibling is that the source is private, so
both jobs need a repository secret to reach it at all, on top of the model
credential the universal sync already needs. Nothing automated can mint or
install that token on the owner's behalf; an administrator has to generate
it and add it themselves. The design decision that followed is the
interesting one: a missing token skips the update rather than failing the
workflow, because a private-repo credential should not block an otherwise
successful install -- but a skip that is silent is indistinguishable from a
sync that is working, so every such run also raises a tracked issue. That is
what turns a token never set, or later revoked, into something noticed the
same day rather than by chance.

The schedule is set deliberately outside working hours, so an unattended
self-merging run is skimmed as a finished thing the next morning rather than
landing mid-workday, and offset from the universal sync so the two never
race over the same working tree.

## Install
No mechanical check, same reason as its sibling `bestpractice-sync`: the workflow this rule requires runs in a repo that vendors this team's set, comparing against this team's own private source with its own credential. This repo is that private source, not a consumer of it -- there is no such workflow here to check.

