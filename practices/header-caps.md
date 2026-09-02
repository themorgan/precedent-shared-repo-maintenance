---
slug:        header-caps
title:       "Header capitalization: pick one consistent schema, NY Times headline style by default"
tier:        on-demand
severity:    default
applies_to:  ["**/*.md"]
occasion:    "writing or reviewing a document's headers"
gates:       []
index_clause: "one capitalization schema per document; default to headline style"
checked_by:  tools/checks/check_header_caps.py
defines:     []
status:      active
supersedes:  []
overrides:   null
added:       2026-08-31
approved_by: "Morgan F, migrated from RepoPersonalPreferences by the private-set migration session"
---
## Rule
Headers and subheaders at the same rank in a document must all follow one capitalization style, never mixed; sibling headers at the same rank also share the same heading level. Absent a documented reason to pick something else, use NY Times headline-style capitalization -- capitalize principal words (nouns, verbs, adjectives, adverbs, pronouns), lowercase minor words (articles, short prepositions, coordinating conjunctions) except at the very start or end of the header -- consistently across every header and subheader in the document.

## Detail
A repo is free to choose a different scheme and document that choice inline, the same way it documents any other repo-wide convention. A document whose sections mix capitalization schemes, or mix heading levels, at the same rank is the failure this rule exists to catch.

## Why


## Story


## Install
Checked mechanically, but only half of it: [`tools/checks/check_header_caps.py`](../tools/checks/check_header_caps.py), scope `tree`, over tracked markdown files, verifies the rule's first, unambiguous sentence -- headers at the same rank in one document never mix capitalization styles. It does this without needing a minor-word dictionary: if the same word (excluding each header's own first/last word) shows up capitalized one way in one same-rank header and differently in another, that word itself is direct evidence of a mixed scheme.

What it doesn't check: that the default scheme, absent a documented reason otherwise, is specifically NY Times headline style. Telling "principal word" from "minor word" for that judgment has enough real edge cases (a short verb doing the sentence's main work, a preposition used adjectivally) that a check built on a fixed word list would misclassify often enough to not actually be enforcing the rule -- exactly the kind of check phase 4 found silently broken elsewhere. That half stays a judgment call for review.

Two-direction tested in [`tools/checks/tests/test_header_caps.sh`](../tools/checks/tests/test_header_caps.sh).

