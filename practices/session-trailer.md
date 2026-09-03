---
slug:        session-trailer
title:       Commit messages link the session where the change was planned
tier:        on-demand
severity:    default
applies_to:  ["**"]
occasion:    "committing anything"
gates:       []
index_clause: "a Session: <url> trailer on every commit"
checked_by:  tools/checks/check_session_trailer.py
defines:     []
status:      active
supersedes:  []
overrides:   null
added:       2026-08-31
approved_by: "Morgan F, migrated from RepoPersonalPreferences by the private-set migration session"
---
## Rule
A `Session: <url>` trailer on every commit -- for Claude Code, `https://claude.ai/code/session_<ID>`. `Claude-Session: <url>` is also accepted -- the key Claude Code Remote's own harness actually emits as of 2026-09, functionally the same trailer under a different name. For unattended automation with no chat session behind it, the workflow run's own URL stands in. If a tool has no shareable link at all, the trailer says so explicitly (`Session: none available (<tool>)`) rather than being silently omitted.

## Detail


## Why
So a reviewer can tell "considered and skipped" from "forgotten" at a glance, and can trace a change back to the conversation that reasoned it through.

## Story


## Install
Checked mechanically by [`tools/checks/check_session_trailer.py`](../tools/checks/check_session_trailer.py), scope `tree`: every non-merge commit reachable from HEAD in this repo must carry a session trailer line -- `Session:` or `Claude-Session:` (the key Claude Code Remote's own harness actually emits as of 2026-09; the check accepts either), a URL or the explicit `none available (<tool>)` form. It doesn't verify the URL actually resolves to a real session -- only that the trailer, in one of its valid shapes, is present, which is the "considered and skipped" vs. "forgotten" distinction this practice's own Why section names. Merge commits are excluded (GitHub's own merge-via-API/UI commits never carry a custom trailer, and a merge isn't new planned work of its own); merge detection reads the raw commit object rather than `git log --format=%P`, which silently loses a shallow clone's boundary commit's real parents -- see the check's own `_is_merge` docstring. One pre-existing, non-merge commit from before this check existed is exempted by SHA (`GRANDFATHERED_SHAS` in the script) rather than rewritten, per `no-rewrite-for-warnings`. Two-direction tested in [`tools/checks/tests/test_session_trailer.sh`](../tools/checks/tests/test_session_trailer.sh).

