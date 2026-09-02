---
slug:        new-rule-placement
title:       A new rule lands in reading-order position, never appended
tier:        on-demand
severity:    default
applies_to:  ["**"]
occasion:    "adding a new rule to a maintained rules document"
gates:       []
index_clause: "place a new rule by subject, slug it, renumber, mirror, re-check"
checked_by:  null
defines:     []
status:      active
supersedes:  []
overrides:   null
added:       2026-08-31
approved_by: "Morgan F, migrated from RepoPersonalPreferences by the private-set migration session"
---
## Rule
When adding a new rule to a maintained rules document: pick where it belongs by subject among the existing groups, not at the end of the file; assign it a permanent slug and anchor, never renumbered later; renumber every rule after the insertion point so the reading order stays one unbroken sequence; mirror the new rule everywhere else it's required to live, in the same reading-order position; then re-run the light check and record the addition in the backlog document.

## Detail
Enforced only in part: a mechanical check can catch a broken slug citation or a stray positional reference, but nothing mechanically checks that a new rule actually landed in the right group, or that every mirror picked it up -- that gap is exactly what the deep check's review exists to catch.

## Why
Related rules sitting together and everyday rules coming before rare ones is reasoning a session would otherwise have to reconstruct from scratch each time; this makes it an actual, repeatable checklist instead.

## Story


## Install
No mechanical check, and the practice says so itself: its own Detail section states "nothing mechanically checks that a new rule actually landed in the right group, or that every mirror picked it up -- that gap is exactly what the deep check's review exists to catch." A slug/anchor uniqueness check and a stray-positional-reference check are the parts it names as checkable in principle, but neither is what this rule is actually about.

