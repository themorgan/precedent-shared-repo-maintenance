---
slug:        list-restraint
title:       Use a list only when the content is actually a list
tier:        on-demand
severity:    default
applies_to:  ["**/*.md"]
occasion:    "about to format connected prose as bullet points"
gates:       []
index_clause: "don't reformat connected reasoning as bullet fragments"
checked_by:  null
defines:     []
status:      active
supersedes:  []
overrides:   null
added:       2026-08-31
approved_by: "Morgan F, migrated from RepoPersonalPreferences by the private-set migration session"
---
## Rule
A bulleted or numbered list is sometimes reached for because it looks more organized than the same content written as connected sentences, not because the content is a set of discrete, parallel items. Ask: does this content name several parallel, roughly interchangeable items the reader will scan or reference individually (a list), or does it make one continuous point with reasoning tying it together (prose)? When genuinely unsure, prose is the safer default.

## Detail
A genuine enumeration a reader will scan or reference individually -- ingredients, steps in a procedure, a set of options, a checklist -- is never what this rule targets. What it catches: content with connective logic ("because," "so," one point building on the last) reformatted as bullet fragments that erase those connections. The tell: reading the bullets back as plain sentences joined by ordinary connectives loses nothing and reads more naturally.

## Why
A paragraph that could have been a list costs the reader little; a list that erases an argument's reasoning costs more.

## Story


## Install
No mechanical check: telling "connected reasoning reformatted as bullet fragments" apart from "a genuine enumeration a reader will scan individually" is precisely the semantic call the rule's own Detail section describes -- reading the bullets back as plain sentences and judging whether the connective logic survives. No syntax-level property of a markdown list captures that.

