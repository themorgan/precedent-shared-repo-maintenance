---
slug:        no-stale-counts
title:       Don't state a count that will drift -- describe it instead
tier:        on-demand
severity:    default
applies_to:  ["**/*.md"]
occasion:    "writing a sentence that cites an exact, changeable count"
gates:       []
index_clause: "drop a count that will go stale; say \"several\", not the number"
checked_by:  tools/checks/check_no_stale_counts.py
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
Checked mechanically, but only half of it: [`tools/checks/check_no_stale_counts.py`](../tools/checks/check_no_stale_counts.py), scope `tree`, catches the one shape of violation that needs no writer intent to judge -- a sentence stating "`<N> practices`" is a claim about this repo's own `practices/` directory, and that claim is either currently true or it isn't, independent of intent. It's deliberately narrow: it does not (and, per this file's own Detail section, cannot) tell a "genuinely maintained" count apart from one that merely happens to be accurate today, and it doesn't push toward the Rule's preferred fix of dropping the number outright -- it only catches a count that has already gone stale, which is the concrete harm the Rule names. A general digit-plus-noun scan across arbitrary count types stays a judgment call, for the reason already given. Two-direction tested in [`tools/checks/tests/test_no_stale_counts.sh`](../tools/checks/tests/test_no_stale_counts.sh).

