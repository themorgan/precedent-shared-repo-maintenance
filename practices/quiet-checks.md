---
slug:        quiet-checks
title:       Don't repeat the same backlog explanation every run
tier:        on-demand
severity:    default
applies_to:  ["**"]
occasion:    "reporting a check's outcome that includes a known pre-existing backlog"
gates:       []
index_clause: "\"checks passed\" is fine; don't re-explain the same old backlog"
checked_by:  null
defines:     []
status:      active
supersedes:  []
overrides:   null
added:       2026-08-31
approved_by: "Morgan F, migrated from RepoPersonalPreferences by the private-set migration session"
---
## Rule
A repo's own mechanical checks can report a real, pre-existing backlog unrelated to the current edit. A session that explains away that same unchanging backlog with the same sentence every single commit -- "pre-existing warnings only, unrelated to my edit," or an equivalent -- is repeating a disclaimer that never changes and never informs the next step. Drop that specific recurring explanation.

## Detail
This does not mean staying silent about checks in general: a plain "checks passed" (or "checks failed, here's why") is normal and often exactly what's wanted, wherever reporting an outcome is the natural thing to do. The distinction is between reporting an outcome, which is fine, and re-explaining the same known, static backlog every time as though it were new information, which isn't. A run that actually failed, or a warning the current edit newly introduced, is always worth flagging.

## Why
The runbook already moves on to checking branch state and committing regardless of what that recurring sentence says, so it is pure repetition with no informational payoff.

## Story


## Install
No mechanical check: it governs how a session narrates a check's outcome in its own reply across turns of a conversation -- whether the same static-backlog disclaimer got repeated -- which isn't content this repo's tree, or any single commit, holds a record of.

