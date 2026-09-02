---
slug:        no-duplication
title:       Don't duplicate a lower-precedence source
tier:        on-demand
severity:    default
applies_to:  ["**"]
occasion:    "adding or reviewing a team-set rule"
gates:       []
index_clause: "a rule that only restates universal gets dropped"
checked_by:  null
defines:     []
status:      active
supersedes:  []
overrides:   null
added:       2026-08-31
approved_by: "Morgan F, migrated from RepoPersonalPreferences by the private-set migration session"
---
## Rule
This set exists to add to the universal catalogue or override it, not to restate it. A rule here that only repeats something universal already establishes on its own -- same substance, no actual change in outcome -- gets dropped the next time it's touched: a restated rule is a second place for the same idea to drift out of sync with the first, for no benefit over leaving the universal text to stand alone.

## Detail


## Why
Precedence already lets a team rule override a universal one by slug; there is no separate need to also copy the universal rule's own text into the team set just to have it nearby.

## Story


## Install
No mechanical check: telling "only repeats something universal, same substance, no actual change in outcome" apart from a legitimate override or a genuinely additional rule requires comparing this set's rules against the universal catalogue's own semantics -- the universal catalogue lives in the public Precedent repo, not vendored here, and even with it in reach, substance-equivalence between two rules is a reading judgment, not a text match.

