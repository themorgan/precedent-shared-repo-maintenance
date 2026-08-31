---
slug:        session-trailer
title:       Commit messages link the session where the change was planned
tier:        on-demand
severity:    default
applies_to:  ["**"]
occasion:    "committing anything"
index_clause: "a Session: <url> trailer on every commit"
checked_by:  null
defines:     []
status:      active
supersedes:  []
overrides:   null
added:       2026-08-31
approved_by: "Morgan F, migrated from RepoPersonalPreferences by the private-set migration session"
---
## Rule
A `Session: <url>` trailer on every commit -- for Claude Code, `https://claude.ai/code/session_<ID>`. For unattended automation with no chat session behind it, the workflow run's own URL stands in. If a tool has no shareable link at all, the trailer says so explicitly (`Session: none available (<tool>)`) rather than being silently omitted.

## Detail


## Why
So a reviewer can tell "considered and skipped" from "forgotten" at a glance, and can trace a change back to the conversation that reasoned it through.

## Story


## Install

