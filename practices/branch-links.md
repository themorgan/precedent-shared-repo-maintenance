---
slug:        branch-links
title:       A mentioned branch is always a link
tier:        on-demand
severity:    default
applies_to:  ["**"]
occasion:    "naming a git branch in a document, reply, or status update"
gates:       []
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
No mechanical check: it governs free-form prose (chat replies, status updates, any document) naming a branch, which has no reliable syntactic signature distinguishing "a git branch was named here" from any other backticked or plain-text token (a filename, a variable, a package name). A static scan would either miss real mentions or misfire constantly on lookalikes.

