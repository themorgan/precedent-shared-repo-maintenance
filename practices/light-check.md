---
slug:        light-check
title:       A light check runs on every commit path
tier:        on-demand
severity:    default
applies_to:  ["**"]
occasion:    "about to commit"
index_clause: "a cheap mechanical audit runs before every commit, not just merges"
checked_by:  null
defines:     []
status:      active
supersedes:  []
overrides:   null
added:       2026-08-31
approved_by: "Morgan F, migrated from RepoPersonalPreferences by the private-set migration session"
---
## Rule
A repo maintains one cheap, mechanical audit script that runs before every commit: conflict markers, invalid JSON/YAML syntax, secret-shaped strings (an AWS-style key ID, a private-key PEM header, a token), and broken relative doc links, at minimum. Run it yourself before every commit; wire it into CI too, so it binds every push even when a session forgets to run it by hand.

## Detail
Where this team set (or any vendored practice set) is installed into a project repo, extend the same check to verify the install is real, not a plain copy: the tracking manifest exists, parses, has at least one entry, and every entry's recorded path exists on disk. A style-oriented linter (accidental strikethrough, unlinked references, unglossed acronyms) is a separate, complementary tool -- this is the broader, cheaper net for "something obviously went wrong" that isn't a style question.

## Why
A required CI check catches an install-time or commit-time mistake the moment it happens, rather than relying on every session remembering a runbook step.

## Story


## Install

