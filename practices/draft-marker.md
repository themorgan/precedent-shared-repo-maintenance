---
slug:        draft-marker
title:       Temporary in-document notes get a marker loud enough to catch on a skim
tier:        on-demand
severity:    default
applies_to:  ["**"]
occasion:    "leaving a placeholder or fill-in-later note mid-draft"
index_clause: "wrap a draft placeholder in \u27a1\ufe0f TEXT \u2b05\ufe0f, bold and all caps"
checked_by:  null
defines:     []
status:      active
supersedes:  []
overrides:   null
added:       2026-08-31
approved_by: "Morgan F, migrated from RepoPersonalPreferences by the private-set migration session"
---
## Rule
A temporary note left mid-draft -- a placeholder to fill in later, a reminder to the future editor, an "insert X here" -- is only safe to leave in a document if whoever next looks at it actually notices it. Wrap it in a marker built to fail a skim on purpose: `**➡️ TEXT OF THE NOTE ⬅️**` -- bold, all caps, a directional arrow hugging the outer edge of the first and last word.

## Detail
Before showing or sharing any document, scan it for the marker specifically -- a text search for the arrow character confirms none remain, cheaper than rereading the whole document.

## Why
Plain caps alone isn't enough: an all-caps placeholder still reads as ordinary body text on a fast scan once the eye has adjusted to a document that already uses bold and caps for other things. Nothing else on the page looks like the arrow marker.

## Story


## Install

