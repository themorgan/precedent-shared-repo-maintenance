---
slug:        default-branch
title:       A new repo's default branch is main, set once
tier:        on-demand
severity:    default
applies_to:  ["**"]
occasion:    "setting up a new repo, or installing into an existing one"
index_clause: "check or set the default branch to main, once, at install"
checked_by:  null
defines:     []
status:      active
supersedes:  []
overrides:   null
added:       2026-08-31
approved_by: "Morgan F, migrated from RepoPersonalPreferences by the private-set migration session"
---
## Rule
For an existing repo whose default branch isn't already `main`: check it at install time, and if it isn't `main`, set it once -- via a host API where the session's tools reach that far, otherwise as a one-click administrator item, disclosed in the repo's own onboarding document. For a brand-new, blank repo with no branches yet, there is nothing to check or set: make the very first commit directly on a branch literally named `main` and push that first, not a feature or planning branch -- the host adopts the first branch ever pushed to an empty repo as its default automatically.

## Detail
One-time per repo either way -- once set, every subsequent clone, PR, and CI run already targets `main` on its own, nothing to repeat.

## Why
A host only defaults a freshly-created repo to `main` on its own; plenty of repos predate that default or arrived some other way (an import, a mirror, an org policy) and still sit on `master` or something else.

## Story


## Install

