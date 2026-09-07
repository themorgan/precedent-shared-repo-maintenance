---
slug:        drift-notice
title:       A session-start notice asks about drift immediately, not at the end
tier:        on-demand
severity:    default
applies_to:  ["**"]
occasion:    "a session starts in a repo that vendors a universal or team set"
gates:       []
index_clause: "check source freshness at session start; raise it right away, not later"
checked_by:  null
defines:     []
status:      active
supersedes:  []
overrides:   null
added:       2026-08-31
approved_by: "Morgan F, migrated from RepoPersonalPreferences by the private-set migration session"
---
## Rule
A scheduled sync closes the gap between sessions; this rule closes a narrower one: the scheduled run hasn't caught up yet, even though a session -- and the person who could approve an update -- is right here from the first turn. At session start, compare each vendored source's recorded commit against its actual head (one cheap remote query, no model call), and if either has moved, say so as part of catching the person up, not saved for the end of the session.

## Detail
A fired notice is also persisted, not just printed: write it into the repo's own backlog document under a standing "Pending Drift Reviews" heading, so it survives past the turn that first raised it and a mechanical check can warn on it staying open. Taking either update stays deliberate, whenever it's raised -- never without being asked. If a merge lands in the same session while a notice is still open, re-ask right there rather than waiting for the end of the session. Fallback: if no notice fired at session start (an incomplete install, an offline start), repeat the same cheap comparison at the end of the session, right after the merge runbook's own steps.

## Why
A purely printed notice competes for a session's attention against whatever concrete task the person actually opened the session to do, and can lose that fight silently -- read once, never acted on, and nothing forces it back into view.

## Story
Migrated here from RepoPersonalPreferences by the phase-3 private-set
migration; the Story is backfilled from that pack's own text. Two real
incidents shaped it.

The first, on 2026-08-27, is why a fired notice is persisted rather than
only printed. In a dependent repo a drift notice fired at session start, was
never raised to the user, and surfaced only when he asked directly a full
task later. Nothing had malfunctioned -- the notice was printed and is in the
transcript. It simply lost a priority fight against whatever concrete task
the session had been opened to do, and once the turn moved on nothing forced
it back into view. A notice that competes for attention and loses is
indistinguishable from one that never fired, so the notice now also writes
itself into the repo's own backlog document, where a per-commit check keeps
warning while the entry stays open.

The second is why the check verifies the install and not just the recorded
commit. A repo can carry a vendored tree without carrying the mechanisms
that keep it current -- through a fork, a template copy, or the case that
actually prompted it, a repo vendored from an already-dependent repo rather
than from canonical source. Comparing recorded commits there answers a
question nobody asked, because the wiring that would act on the answer is
missing. So a missing workflow, bootstrap snippet or woven-in section is
reported as an incomplete install rather than as drift, with an offer to
finish it from canonical source regardless of which repo the files on disk
arrived from.

Taking an update stays deliberate, which is the one deliberate difference
from the scheduled syncs that merge unattended: a human is already present
to answer, so there is no reason to skip the ask.

## Install
No mechanical check: this is a rule about when a session raises drift (immediately at session start, not saved for later) -- a property of session conduct and turn ordering, not of any file this repo's own tree holds. There is no artifact left behind that distinguishes a notice raised early from one raised late.

