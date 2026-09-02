---
slug:        durable-list-anchors
title:       A durable numbered list gets a permanent slug and anchor per entry
tier:        on-demand
severity:    default
applies_to:  ["**/*.md"]
occasion:    "a numbered list's entries are durable content likely to be cited by position"
gates:       []
index_clause: "anchor and slug each entry of a durable numbered list, not just its number"
checked_by:  null
defines:     []
status:      active
supersedes:  []
overrides:   null
added:       2026-08-31
approved_by: "Morgan F, migrated from RepoPersonalPreferences by the private-set migration session"
---
## Rule
A numbered list whose entries hold real, durable content -- standing rules, named ideas, arguments meant to last -- likely to be cited elsewhere as "item N" or "rule N," gets the same treatment a rules document's own rules get: each entry an `<a id="slug"></a>` anchor, every citation using the slug form, the visible number left as pure reading-order furniture nobody actually cites.

## Detail
Doesn't reach a short bullet list -- three or four quick options, a set of open questions -- that nothing outside it is likely to reference by position. Stops at the edge of anything vendored: a numbered list inside a tree that must stay byte-identical to its upstream source is not ours to renumber or re-anchor; cite it by its own file-qualified form instead (`SOMEFILE.md §17`) and raise any real need for slugs upstream. Even a list that already uses real headings needs an explicit anchor -- a host's auto-generated heading anchor bakes the visible number into the slug, so it still breaks on renumbering without one.

## Why
Position-only numbering makes every future insertion a choice between distorting the list's own logical order or paying for a repo-wide citation sweep; a slug removes that choice entirely.

## Story


## Install
No mechanical check: whether a given numbered list holds "durable content likely to be cited by position" versus a short, disposable set of options is exactly the judgment the rule turns on, and the Detail section's own carve-outs (a short bullet list; a list vendored byte-identical from upstream) need the same judgment to apply correctly. A check that flagged every unanchored numbered list would misfire on most of them.

