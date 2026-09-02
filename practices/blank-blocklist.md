---
slug:        blank-blocklist
title:       A public check-in scrub blocklist stays blank at install, never asked for
tier:        on-demand
severity:    default
applies_to:  ["**"]
occasion:    "installing a vendored practice layer that could check in upstream"
gates:       []
index_clause: "leave a check-in blocklist blank at install; don't ask, don't remind"
checked_by:  null
defines:     []
status:      active
supersedes:  []
overrides:   null
added:       2026-08-31
approved_by: "Morgan F, migrated from RepoPersonalPreferences by the private-set migration session"
---
## Rule
Where a repo's install procedure asks for private vocabulary to seed a scrub blocklist before any check-in to a public upstream repo, and this team doesn't use that check-in path today, installing the vendored layer never asks for blocklist content and never volunteers a seeded draft on its own -- write the file with just its explanatory header and no entries, and move on. No follow-up reminder, ever, in that session or a later one.

## Detail
This is a rule about the install-time default for a repo that genuinely doesn't check practices upstream. It doesn't reach back to reopen or blank out a blocklist a repo already has populated and is actively relying on -- a repo that does check practices in upstream (this team's own promotions to universal, for instance) keeps its populated blocklist doing real work, and this rule never touches it.

## Why
If the feature is ever wanted, someone will say so; a session asking for it unprompted, or seeding a draft from repo context on its own, has happened before and is exactly the friction this rule prevents.

## Story


## Install
No mechanical check: the rule governs a moment in a *target* repo's install procedure -- what an installing session does or doesn't ask for -- not a property this repo's own tree ever holds (this repo isn't itself being installed into anywhere, and has no check-in-upstream blocklist of its own to have left blank or populated).

