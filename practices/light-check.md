---
slug:        light-check
title:       A light check runs on every commit path
tier:        on-demand
severity:    default
applies_to:  ["**"]
occasion:    "about to commit"
gates:       ["push"]
index_clause: "a cheap mechanical audit runs before every commit, not just merges"
checked_by:  tools/checks/check_light_check.py
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
Writing this practice's own checked_by turned it into the actual audit script it describes: run against this repo's own tree, it found three practice files (`deep-check`, `header-caps`, `push-back`) with a `title:` frontmatter value containing an unquoted colon -- invalid YAML that a strict parser rejects. Fixed in the same commit that added the check.

## Install
[`tools/checks/check_light_check.py`](../tools/checks/check_light_check.py) IS the audit this practice describes, run against this repo, scope `tree`: conflict markers, invalid JSON/YAML (including every practice file's own frontmatter block), secret-shaped strings (an AWS-style key ID, a PEM private-key header, a GitHub or Slack token), and broken relative markdown links. The Detail section's second half -- verifying an *installed* copy's tracking manifest -- doesn't apply here, since this repo is the source of the set, not an installer of one; a repo that vendors this set would extend the check with that piece itself. Two-direction tested in [`tools/checks/tests/test_light_check.sh`](../tools/checks/tests/test_light_check.sh), one planted violation per audit.

