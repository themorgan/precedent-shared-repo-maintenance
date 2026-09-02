---
slug:        rule-links
title:       A mentioned rule, item, or destination is always a link
tier:        on-demand
severity:    default
applies_to:  ["**"]
occasion:    "naming anything that has a destination, in a document or a reply"
gates:       []
index_clause: "link anything mentioned that has a destination, on first use"
checked_by:  null
defines:     []
status:      active
supersedes:  []
overrides:   doc-references-are-links
added:       2026-08-31
approved_by: "Morgan F, migrated from RepoPersonalPreferences by the private-set migration session"
---
## Rule
Anything mentioned that has a destination gets a link to that destination, the first time it's mentioned -- in any document in the repo, a commit message, a PR description, and a reply in chat, which is the one people forget. Naming a thing and leaving the reader to go find it costs the writer a few seconds and the reader a search every single time.

## Detail
What has a destination: a file in the repo (a relative markdown link, never a bare backticked name); a named rule of this or another practice set (its permanent slug and anchor, never a positional number, which moves whenever the document is reorganized); a git branch (its tree view, per the branch-links practice); a commit (the commit page, short SHA as the link text); a pull request or issue (its page -- not every host auto-links a bare `#43` inside repo markdown); a service, tool, spec, or documentation page named in prose (its canonical page).

Link a thing the first time a given document or reply names it, then use the plain name after that -- this is about the reader being able to get there, not about maximizing link density. A URL, path, or filename inside a code span or code block is a value, not a reference, and stays unlinked.

A rule of any practice set has one canonical citation form: the slug, linked to its anchor. A positional number ("rule 14") is never a citation -- it names where a rule sits today, not which rule it is.

## Why
A reply that says "fixed in the header rule, see the backlog item" is exactly as unhelpful as a document that says it -- a reply is usually more disposable, which is why it needs the links more, not less. This is stricter than a plain doc-references-are-links convention about where the link lands and what counts as mentionable, so it replaces that practice rather than sitting beside it.

## Story


## Install
No mechanical check: it's the general case of `branch-links` and `file-mention-links`, one level broader (any file, rule, branch, commit, PR, issue, tool, or spec named in a document or a reply), and inherits the same limit -- recognizing that something was "mentioned" in free-form prose, as opposed to a coincidentally similar word, has no reliable syntactic signature to key a check off.

