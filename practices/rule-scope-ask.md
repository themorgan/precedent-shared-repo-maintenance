---
slug:        rule-scope-ask
title:       When a proposed rule's scope is ambiguous, ask which layer it belongs to
tier:        on-demand
severity:    default
applies_to:  ["**"]
occasion:    "a new rule is proposed and its scope isn't obvious"
gates:       []
index_clause: "unclear if a new rule is repo-wide or one document? ask once"
checked_by:  null
defines:     []
status:      active
supersedes:  []
overrides:   null
added:       2026-08-31
approved_by: "Morgan F, migrated from RepoPersonalPreferences by the private-set migration session"
---
## Rule
When a rule is proposed and it's genuinely unclear whether it governs one document or the whole repo, ask -- once, in the moment, with a guess and the reason for it, so confirming costs a word rather than a paragraph.

## Detail
This is a carve-out from deciding small calls yourself: by that rule's own test (how hard a call is to undo), filing a newly proposed rule at the wrong layer looks cheap. It isn't -- the cost that matters is not undoing the mistake but noticing it. Both misfilings are silent: a rule that's really general, filed onto one document, ends up restated across several places in several phrasings, drifting; a rule that's really local, filed as a repo convention, quietly constrains every document in the repo.

The test: would the rule's own text still make sense applied to a different document? "Only short paragraphs" would, so ask. "Keep the Series A section under one page" names this document's own structure and is local on its face. "Use em dashes, not semicolons" is plainly house style and goes to the repo's conventions. Only the first case warrants stopping -- asking on all three trains the person proposing rules to wave the question through.

## Why
The ask is nearly free while the rule is still in front of the person proposing it; the same question weeks later costs a full reload of the context that produced it.

## Story


## Install
No mechanical check: this is a live judgment call made while a rule is being proposed -- whether its scope is genuinely ambiguous by the rule's own test ("would the rule's own text still make sense applied to a different document?"). Nothing in committed content records whether that ask happened, or should have.

