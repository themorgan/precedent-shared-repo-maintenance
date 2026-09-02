---
slug:        trim-prose
title:       Trim iteratively-edited prose on two state-free triggers
tier:        on-demand
severity:    default
applies_to:  ["**/*.md"]
occasion:    "a paragraph just got a substantial edit, or the piece is done"
gates:       []
index_clause: "trim a paragraph right after editing it, and before calling it done"
checked_by:  null
defines:     []
status:      active
supersedes:  []
overrides:   null
added:       2026-08-31
approved_by: "Morgan F, migrated from RepoPersonalPreferences by the private-set migration session"
---
## Rule
Prose revised repeatedly in the same conversation tends to only grow -- each pass adds a clause without removing what the new wording made redundant. Fix it with two cheap, state-free triggers rather than a running count: trim a paragraph immediately after any substantial edit to it (a rewritten sentence, or roughly a sentence or more added), and give the whole piece a final trim pass before calling it done, independent of edit size, for any paragraph that's grown noticeably longer than the point it's making warrants.

## Detail


## Why
Both triggers fire at a checkpoint that already exists -- making an edit, declaring the piece finished -- rather than a mechanical count needing counters or stored baselines.

## Story


## Install
No mechanical check: whether a paragraph has "grown noticeably longer than the point it's making warrants" is a judgment about proportion between content and substance -- word or sentence count alone can't distinguish a legitimately long, dense point from one padded by iterative edits, so a length-based trigger would flag exactly the paragraphs this rule doesn't target as often as the ones it does.

