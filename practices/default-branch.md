---
slug:        default-branch
title:       A new repo's default branch is main, set once
tier:        on-demand
severity:    default
applies_to:  ["**"]
occasion:    "setting up a new repo, or installing into an existing one"
gates:       []
index_clause: "check or set the default branch to main, once, at install"
checked_by:  tools/checks/check_default_branch.py
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
Migrated here from RepoPersonalPreferences by the phase-3 private-set
migration; the Story is backfilled from that pack's own text, and there are
two real incidents behind it -- one per branch of the rule.

The first: RepoPersonalPreferences itself sat on a default branch that was
not `main` until it was corrected by hand on 2026-08-21. The host only
defaults a *freshly created* repository to `main`; a repo that predates that
default, or arrived by an import, a mirror, or an organization policy, can
sit on something else indefinitely with nothing to flag it. That is why the
rule says to check at install rather than assume.

The second is the reason the brand-new-repo case is written as a separate
branch rather than folded into the first. An install session treated a
blank repo as though it were an existing one, went looking for a default
branch to check, discovered partway through that the repo had no `main` at
all, and then created one through the host's API from a planning branch's
tip after the fact. Every step of that was avoidable: a blank repo has
nothing to check and nothing to set, because the host adopts the first
branch ever pushed to it as the default automatically. Making the first
commit directly on `main` satisfies the rule outright.

One-time per repo either way. Once set, every later clone, pull request and
automation run already targets `main` on its own.

## Install
Checked mechanically by [`tools/checks/check_default_branch.py`](../tools/checks/check_default_branch.py), scope `tree`, via the one cheap remote query this file's own Install text already names: `git ls-remote --symref origin HEAD` asks the remote which branch it actually points at, no clone required. If the remote can't be reached at all (no network, no credential), the check reports SKIPPED rather than a silent pass -- a check that can't observe the property says so, per the NotApplicable convention. Two-direction tested in [`tools/checks/tests/test_default_branch.sh`](../tools/checks/tests/test_default_branch.sh) against a local bare repo standing in for a misconfigured remote.

