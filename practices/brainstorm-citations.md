---
slug:        brainstorm-citations
title:       A formal document cites another formal document, never a specific point in the brainstorm
tier:        on-demand
severity:    default
applies_to:  ["**/*.md"]
occasion:    "citing support for a claim in a formal document"
gates:       []
index_clause: "cite a formal document for support, never a raw brainstorm entry"
checked_by:  null
defines:     []
status:      active
supersedes:  []
overrides:   null
added:       2026-08-31
approved_by: "Morgan F, migrated from RepoPersonalPreferences by the private-set migration session"
---
## Rule
Some repos keep an explicit brainstorm document -- a running, loosely organized dump of raw ideas, explicitly not vetted prose. A formal document -- an essay, a reasons write-up, a rules-in-force checklist, anything meant to state a settled or settling claim -- links another formal document for a substantive point, never a specific entry inside a brainstorm document. If the idea hasn't been promoted into some formal document's own text yet, add it there first, then link there instead.

## Detail
What this doesn't reach: a document's own provenance note ("promoted out of the brainstorm") states a true fact about history, not a citation used as support, and stays fine linking to the brainstorm directly. Linking the brainstorm document itself as an object -- pointing a reader there to browse it -- isn't the pattern this catches either; only a specific interior point cited as justification is.

## Why
Citing a specific brainstorm entry as a claim's own support borrows a credibility the entry never earned -- it's raw material precisely because nobody has argued it through yet.

## Story


## Install
No mechanical check: catching a violation requires classifying a document as "formal" versus "brainstorm" and telling a citation used as substantive support apart from a provenance note or a link to the brainstorm document as a whole -- both genuinely allowed by the rule's own Detail section. Nothing in a link's syntax carries that distinction; it's a judgment about what the link is doing in context.

