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
status:      retired
in_force_at: none
supersedes:  []
overrides:   null
added:       2026-08-31
approved_by: "Morgan F, migrated from RepoPersonalPreferences by the private-set migration session"
---
## Rule
A project repo that vendors this team's practices runs a scheduled workflow against this team's own source repo: compare the recorded source commit against the source's actual head, and -- if it moved -- merge each changed file through its recorded adaptation, re-run every gate, commit with the judgment calls spelled out under a "Judgment calls to review:" heading, open a pull request, and merge it once checks pass.

## Detail
The one real difference: this team's own source repo is private, so both the comparison and the update need their own repository credential to reach it, in addition to whatever model credential the update step itself needs. No workflow, and no session, can mint or install that credential on a repo's behalf -- an administrator has to generate and add it themselves. A run that skips the update because that credential is missing still reports that it skipped, every time, so a credential that was never set or later revoked gets noticed rather than silently degrading the sync forever.

## Why
A private source needs its own credential precisely because it is private -- a public source needs none, which is the whole difference from the universal-set sync.

## Story
**Retired 2026-09-11, by Morgan**, `strength: decided`, hours after its
sibling and for the same reason -- *"let's get rid of pack-sync"*, once the
question was put to him that the day's earlier decision had deliberately not
answered.

The reasoning is `bestpractice-sync`'s, unchanged: this rule required an
unattended workflow that merged an update through its recorded adaptations,
re-ran the gates, opened a pull request and **merged it once checks passed**.
An unattended merge is a merge nobody read. Pointing it at a private source
made that worse rather than better, because the auto-merged pull request is
one nobody outside this team can even see.

**What replaces it is the same thing that replaced its sibling**, and it
already covers a team set explicitly: the universal `vendor-update-runbook`,
triggered by saying *Update Vendors*, which is the person-initiated version
of this exact sequence. `drift-notice` -- still in force here -- compares
every vendored source's recorded commit against its head at session start
and says so in the first turn, so nobody has to remember to check. The
update still happens on the day it matters. It happens because somebody
asked for it.

**What genuinely goes with it, and is worth naming rather than glossing.**
This rule carried one thing its sibling did not: the private source needs
its own repository credential, and the design decision recorded above -- a
missing credential **skips** the update rather than failing the workflow,
but raises a tracked issue every time it skips, so a token never set or
later revoked is noticed the same day rather than by chance. That pattern
was the interesting part of this practice and it does not belong only to a
sync, so it was **carried into `automation-issues` the same day** rather
than left to be inferred from a retired file. That rule already required a
blocked job to open a tracked issue; the skip-rather-than-fail half was only
ever written here, and is written there now. Nothing else here is
load-bearing elsewhere.

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


**For a few hours on 2026-09-11 this practice was in force and its sibling
was not**, and the paragraph here said so -- that the reasoning did not stop
at the repository boundary, that this was the harder half to review after
the fact, and that it survived only because the instruction that retired
`bestpractice-sync` named `bestpractice-sync`. That was the right state to
write down and the wrong one to leave standing, so it was put to Morgan the
same afternoon and answered in one line. Kept here in past tense because a
practice file that only ever shows its end state teaches nothing about how
the decision was actually reached.

This practice's Rule and Install had also defined themselves by pointing at
`bestpractice-sync` as their sibling -- "same shape as", "same reason as" --
and were rewritten to say it in their own words while both were still in
force. A rule in force must not be readable only through a retired one. That
is no longer this file's problem, and it is exactly what was done for
`automation-issues` when this one went.

## Install
No mechanical check: the workflow this rule requires runs in a repo that vendors this team's set, comparing against this team's own private source with its own credential. This repo is that private source, not a consumer of it -- there is no such workflow here to check.

