---
slug:        small-calls
title:       Decide small calls yourself; only stop for big ones
tier:        resident
severity:    default
applies_to:  ["**"]
occasion:    "a judgment call is needed to keep work moving"
gates:       []
index_clause: "make small calls yourself; note them; stop only for big ones"
checked_by:  null
defines:     []
status:      active
supersedes:  []
overrides:   null
added:       2026-08-31
approved_by: "Morgan F, migrated from RepoPersonalPreferences by the private-set migration session"
---
## Rule
Default to continuing, not asking. When a judgment call is needed to keep the work moving -- filling in a default, picking between two reasonable implementations, resolving an ambiguity that doesn't change the shape of what gets delivered -- make the call and note it, rather than stopping to ask first. Reserve stopping and asking for calls that are genuinely big: hard or costly to undo, change what gets delivered or to whom, spend real money, touch credentials or production, or are the kind of toss-up where two reasonable people would clearly land in different places.

## Detail
A small or moderate call made this way still gets surfaced, just not as an interruption: note it in both the normal end-of-work reply that already lists files touched, and the commit message itself, under a "Judgment calls made:" heading. The chat reply is easy to miss once a thread scrolls on; the commit message is the one copy that survives into `git log` and the PR diff, where it stays visible for as long as the repo does. Skip the heading only when a commit truly made no judgment calls -- don't pad it with "none" noise on every commit, but never omit it when a call was actually made.

## Why
Most calls in day-to-day work (a wording choice, which of two valid layouts to use, a template's exact phrasing) are small enough to just make; stopping for each one trades a session's own judgment for round-trip latency on decisions that don't need a second opinion.

## Story


## Install
No mechanical check: a commit either has a "Judgment calls made:" heading or doesn't, and that presence alone is trivially greppable -- but the actual rule is about which calls were correctly sized as small enough to just make versus which should have stopped and asked, and that sizing (hard/costly to undo, touches production, a real two-reasonable-people toss-up) is the judgment itself, not observable after the fact from the commit alone.

