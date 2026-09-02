---
slug:        install
title:       Installing a vendored practice set into a repo
tier:        on-demand
severity:    default
applies_to:  ["**"]
occasion:    "bringing a vendored practice layer into a new or existing repo"
gates:       []
index_clause: "vendor the tree, weave conventions into AGENTS.md, wire checks and manifest"
checked_by:  null
defines:     []
status:      active
supersedes:  []
overrides:   null
added:       2026-08-31
approved_by: "Morgan F, migrated from RepoPersonalPreferences by the private-set migration session"
---
## Rule
Vendor the practice set's tree into the target repo under a tracked path, the same way an upstream practice layer gets vendored. Weave its documentation conventions into the target repo's `AGENTS.md`, in reading-order position. Install its mechanical checks (a light check, any CI workflow it ships) and add its wiring to the repo's own bootstrap/session-start step. Record every installed file in a tracking manifest, with the source repo and the commit it was installed from, so a later sync has something real to compare against. Run the vendored layer's own audits with `--update-baseline` once, so future runs check against this install rather than failing on day one.

## Detail
This procedure applies exactly the same way when the target repo already has some of these pieces present because they arrived indirectly -- a fork, a copy, a chain-vendor -- rather than fresh from the canonical source. Do the missing pieces; don't skip any of them just because something is already present, since presence of the tree is not evidence the sync workflows or the `AGENTS.md` sections came with it.

Where the person working in the target repo has their own individual set, this install also wires that up -- a distinct step from vendoring universal and team, since an individual set is never vendored into the target repo at all (that's the privacy boundary). Concretely, for a Claude Code Web session: copy that person's individual repo's own bootstrap script (a worked example of this pattern exists in the individual-set practice for it) into the target repo as a tracked `SessionStart` hook, so the individual source clones and configures itself before the session's first tool call -- no command run by hand, on any machine, by anyone whether or not they're a developer. Skip this step only if the person has no individual set, or explicitly doesn't want one wired into this particular project.

## Why
Copying gets a repo the files but not the tracked provenance (source, commit, per-file record) that makes a vendored set auditable and syncable later -- an install that skips the manifest is not really an install.

## Story


## Install
No mechanical check: this rule describes a procedure a *target* repo's install session follows (vendor the tree, weave `AGENTS.md`, wire checks, write the tracking manifest). This repo is the source being vendored, not a target -- there's no install here to verify the outcome of. A target repo could check its own manifest for completeness (light-check's own Detail section already covers exactly that), but that check would live there, not here.

