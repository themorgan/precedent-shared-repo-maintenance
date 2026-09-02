---
slug:        automation-issues
title:       Unattended automation reports its own blockers as a tracked issue
tier:        on-demand
severity:    default
applies_to:  ["**"]
occasion:    "an unattended scheduled job hits something blocking its normal work"
gates:       []
index_clause: "a blocked scheduled job opens or updates an issue, not just a log line"
checked_by:  null
defines:     []
status:      active
supersedes:  []
overrides:   null
added:       2026-08-31
approved_by: "Morgan F, migrated from RepoPersonalPreferences by the private-set migration session"
---
## Rule
Any unattended job -- a scheduled sync, or any future one a team's own automation adds -- that hits something blocking it from finishing its normal work (a missing or revoked credential, an unexpected failure) reports that blocker by opening or updating a tracked issue, not only a CI annotation or a job-summary line. Keep the annotation too -- it's free and some readers will still see it -- but treat it as a backup, not the primary channel.

## Detail
Idempotent by design: one open issue per blocker, not one per run -- a second occurrence of the same blocker comments on the existing open issue (with a "recurred: `<date>`" stamp) instead of opening a duplicate, so a blocker that fires every week for months reads as one ongoing problem with a comment thread, not fifty separate issues. Fails gracefully if the reporting mechanism itself can't reach the host or authenticate: prints a warning, exits cleanly, never turns a failure to report a blocker into a second, more confusing blocker.

## Why
A CI annotation lives inside one workflow run; nobody sees it unless they already know to go check that run. A tracked issue persists in the repo itself and rides the host's own notification system for free.

## Story


## Install
No mechanical check: this repo runs no unattended scheduled job itself, so there is no run history here to check the idempotent-issue-per-blocker behavior against. A repo that adds such automation could check it directly (does a recurrence comment on the existing open issue rather than opening a duplicate) but that's a property of that automation's own run history, not of this repo's tree.

