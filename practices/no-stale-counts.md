---
slug:        no-stale-counts
title:       Don't state a count that will drift -- describe it instead
tier:        on-demand
severity:    default
applies_to:  ["**/*.md"]
occasion:    "writing a sentence that cites an exact, changeable count"
index_clause: "drop a count that will go stale; say \"several\", not the number"
checked_by:  null
defines:     []
status:      active
supersedes:  []
overrides:   null
added:       2026-08-31
approved_by: "Morgan F, migrated from RepoPersonalPreferences by the private-set migration session"
---
## Rule
Prose that cites an exact count of something that changes over time -- how many rules a document has, how many warnings a lint tool currently reports -- reads precisely today and goes stale the moment that thing changes, with nothing to flag it. When the exact count isn't the point being made, don't state it: rewrite to the qualitative form ("numbered sections" instead of "twenty-nine numbered sections"). Dropping the number outright is usually the right fix, not swapping it for a vaguer-but-still-numeric approximation that will just go stale on a slower clock.

## Detail
This isn't a rule against numbers in general -- a version number, a date, or a count genuinely maintained alongside the thing it counts all stay exact. The target is specifically a count that can change independent of the sentence stating it, where the number isn't actually the point.

## Why
No audit checks a sentence like "twenty-nine numbered sections" against the actual count, so it just sits there being wrong until a session happens to notice.

## Story


## Install
No mechanical check: distinguishing a count "genuinely maintained alongside the thing it counts" (explicitly fine, per the Detail section -- a version number, a date) from one that "will drift" (the violation) requires knowing the writer's intent behind the number, not just its presence. A digit-plus-noun pattern would flag exactly the counts this rule exempts as often as the ones it targets.

