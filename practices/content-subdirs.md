---
slug:        content-subdirs
title:       Content-oriented repos group deliverable content in a subdirectory
tier:        on-demand
severity:    default
applies_to:  ["**"]
occasion:    "root has accumulated three or more deliverable-content documents"
gates:       []
index_clause: "group deliverable content under a named subdirectory -- a recommendation"
checked_by:  null
defines:     []
status:      active
supersedes:  []
overrides:   null
added:       2026-08-31
approved_by: "Morgan F, migrated from RepoPersonalPreferences by the private-set migration session"
---
## Rule
In a content-oriented repo -- one whose deliverable is the writing itself, not software that runs -- once root accumulates three or more documents that are deliverable content rather than navigation, consider grouping that content under one or more named subdirectories (say `book/` and `brainstorm/`), while the navigation layer (a map, a glossary, a backlog document, a README, `AGENTS.md`, a getting-started guide) stays at root.

## Detail
A code-oriented repo doesn't get this recommendation at all -- its root-level clutter, if any, is a different problem with its own existing conventions. Not mechanically enforced, and not retroactive: raise it as a judgment call when a session actually notices root cluttered with deliverable content, never as a reason to force a restructure on its own.

## Why
Left alone, both kinds of root-level file pile up together, and enough deliverable content reads as cluttered even when the navigation layer is doing exactly what it should.

## Story


## Install
No mechanical check, and the practice says so itself: its own Detail section states it's "not mechanically enforced... raise it as a judgment call when a session actually notices," since telling deliverable content apart from navigation-layer files (and deciding whether root genuinely reads as cluttered) is exactly that kind of call.

