---
slug:        sensitive-characterization-scrub
title:       Scrub sensitive characterizations of real people, unless told otherwise
tier:        on-demand
severity:    blocking
applies_to:  ["**"]
occasion:    "about to commit a document that characterizes a real, identifiable person"
index_clause: "soften or ask before committing a blunt description of a real person"
checked_by:  null
defines:     []
status:      active
supersedes:  []
overrides:   null
added:       2026-08-31
approved_by: "Morgan F, migrated from RepoPersonalPreferences by the private-set migration session"
---
## Rule
Assume whoever is driving a session talks about real people -- colleagues, collaborators, anyone the work touches -- as candidly and directly as with a trusted collaborator, and that candor is not, on its own, safe to carry into anything committed. Before anything actually gets committed -- a document, a brainstorm entry, a code comment, a commit message -- assume the specific, identifiable real people it describes may eventually read it themselves. Where a description is unusually direct, strong, negative, or otherwise sensitive enough that the person might wince reading it, don't commit it as given: soften it, or ask first.

## Detail
Default to a euphemism that keeps the substance, not the edge -- a blunt personal trait restated as an indirect institutional or situational one usually does the job. Ask, don't guess, when no softened phrasing preserves what the point needs. This isn't a ban on describing real people, and it doesn't reach the conversation itself -- it only gates what actually gets written down; ordinary, neutral, complimentary, or already-public description needs none of this.

## Why
Marked blocking because it guards against a real information harm -- a description said only for the conversation, read back by the person it describes, more bluntly than intended -- that no personal preference for candor should be able to switch off.

## Story
Found the hard way in a dependent repo's own brainstorm notes: a direct, off-the-cuff description of a real, named acquaintance made it into a committed document, was then shown to that person, and read back more bluntly than intended.

## Install

