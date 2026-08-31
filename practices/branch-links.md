---
slug:        branch-links
title:       A mentioned branch is always a link
tier:        on-demand
severity:    default
applies_to:  ["**"]
occasion:    "naming a git branch in a document, reply, or status update"
index_clause: "link every git branch mentioned to its tree view"
checked_by:  null
defines:     []
status:      active
supersedes:  []
overrides:   null
added:       2026-08-31
approved_by: "Morgan F, migrated from RepoPersonalPreferences by the private-set migration session"
---
## Rule
Any time a reply or document names a git branch -- not only in a files-touched footer, but anywhere in running text, a status update, a decision note -- link it, to that branch's tree view on whichever host the repo actually lives on. A bare branch name in backticks or plain prose is the failure mode this rule exists to catch.

## Detail


## Why
A doc-references-are-links convention covers files at the repo's current tree; it doesn't reach a branch, since a branch is a ref rather than a path at the current tree, so it needs its own explicit rule.

## Story


## Install

