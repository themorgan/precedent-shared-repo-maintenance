---
slug:        file-mention-links
title:       In chat and PR/commit text, every file mention is a clickable link
tier:        on-demand
severity:    default
applies_to:  ["**"]
occasion:    "mentioning a repo file in a chat reply, PR description, or commit message"
gates:       ["reply"]
index_clause: "every file mention in chat or PR/commit text is a live GitHub link"
checked_by:  null
defines:     []
status:      active
supersedes:  []
overrides:   null
added:       2026-08-31
approved_by: "Morgan F, migrated from RepoPersonalPreferences by the private-set migration session"
---
## Rule
A file gets linked the first time it's mentioned inside a document actually committed to the repo, using a relative link, leaving a filename inside a code span alone. Neither default holds on two other surfaces -- a chat reply, and a PR description, issue, or commit message aimed straight at the host -- since neither is part of the repo tree and a relative link doesn't resolve there. On those two surfaces only: every mention of a specific file is a clickable, absolute URL to that file, staying inside its code span rather than growing a separate marker.

## Detail
Which branch to link: an open PR's own head branch while it's still open, the default branch once merged or when the reply isn't tied to a particular PR. Where a harness offers a blocking turn-end hook, this is the one part of the documentation-link conventions worth enforcing mechanically -- reading the closing reply before a turn ends and blocking on an unlinked mention of a real, tracked file. Only the final contiguous run of text needs checking, not the whole turn: progress narration written between tool calls earlier in a turn was never meant as a citable deliverable the way the closing reply is.

## Why
A reader skimming a long reply or PR body has no "first mention" to scroll back to -- they want whichever mention is in front of them to work.

## Story


## Install
No mechanical check: the surfaces this rule governs -- a chat reply, a PR description, an issue, a commit message -- aren't content this repo's own tree contains, so there's nothing here to scan. The practice's own Detail section names the one place this is worth enforcing mechanically: a harness's blocking turn-end hook reading the closing reply, which is a property of the harness, not of this repo.

