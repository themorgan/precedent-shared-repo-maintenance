---
slug:        fail-gracefully
title:       Always fail gracefully
tier:        on-demand
severity:    default
applies_to:  ["**"]
occasion:    "writing code that depends on something outside its own control"
index_clause: "degrade on a missing config, file, network call, or credential"
checked_by:  null
defines:     []
status:      active
supersedes:  []
overrides:   null
added:       2026-08-31
approved_by: "Morgan F, migrated from RepoPersonalPreferences by the private-set migration session"
---
## Rule
Any code written or set up here anticipates its own common failure modes rather than letting them surface as an unhandled crash. Before shipping code that depends on something outside its own control -- a required config or environment variable, a file that's supposed to exist, a network call, a third-party credential -- check for the absence or failure case on purpose and degrade in a way the caller can act on: a clear error message naming exactly what's missing and how to fix it, a documented fallback/default, or a clean non-zero exit -- never a raw stack trace, a silent wrong answer, or a hang.

## Detail


## Why


## Story


## Install

