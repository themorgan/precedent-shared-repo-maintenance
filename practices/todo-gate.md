---
slug:        todo-gate
title:       A backlog document gets reconciled before every push
tier:        on-demand
severity:    default
applies_to:  ["**"]
occasion:    "about to push after a thread of work"
gates:       ["push"]
index_clause: "add missed ideas, check off finished ones, before every push"
checked_by:  null
defines:     []
status:      active
supersedes:  []
overrides:   null
added:       2026-08-31
approved_by: "Morgan F, migrated from RepoPersonalPreferences by the private-set migration session"
---
## Rule
Before pushing, check the thread's discussion against the repo's own backlog document (`TODO.md` or equivalent): add any idea that came up but never got a line, remove or check off anything this branch just implemented.

## Detail


## Why
A backlog document drifting out of sync with what was actually decided is common enough in practice that it earns its own gate rather than staying an occasional "oh, I should update that" afterthought.

## Story


## Install
No mechanical check: reconciling the backlog document against "the thread's discussion" requires comparing a file to a conversation this repo's tree never records -- a check could confirm a `TODO.md` exists and was touched in the same commit, but that's a weak proxy that would pass on an unrelated edit to the file and fail on a push that genuinely needed no reconciliation.

