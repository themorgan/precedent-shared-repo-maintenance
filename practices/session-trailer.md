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
A commit GitHub makes with its own buttons -- a merge, squash or revert button, an edit made on the website -- needs no trailer: no session wrote it, and there is nowhere to put one. Where the working-style set's `revert-needs-no-trailer` practice is in force, a revert needs none either.

## Why
So a reviewer can tell "considered and skipped" from "forgotten" at a glance, and can trace a change back to the conversation that reasoned it through.

## Story
Migrated here from RepoPersonalPreferences by the phase-3 private-set
migration. No incident was recorded, and none is invented here.

The one design detail with a stated reason is the explicit
no-link-available form. A trailer that is simply omitted when a tool has no
shareable session link is indistinguishable from one that was forgotten, so
the rule requires saying so in the trailer itself -- which lets a reviewer
tell "considered and skipped" from "forgotten" at a glance. The same
reasoning covers unattended automation, where the workflow run's own URL
stands in rather than the field going blank.

**Drafted into the universal catalogue on 2026-09-28**, as the universal practice `session-trailer`, on Morgan's approval of a session's recommendation to move it together with four others that apply to any repository rather than to maintaining practice sets (strength: assented; this rule's own recorded strength is unchanged). His framing, said about `dont-race-another-window`: *"From the name it sounds like a fundamental rule, so it should be in precedent universal. Repo-maintenance is just for things to help maintain the practices etc."* The universal copy was rewritten to be public-safe -- general terms in place of this account's private repositories and people -- so its wording differs from this one. **This copy stays active until that pull request has merged and every repository consuming this set has taken the new universal catalogue**; then `precedent_move.py --dedupe-only` marks it `deduplicated` with `in_force_at: session-trailer` ([spec/MOVING_PRACTICES.md](https://github.com/alex137/BestPractice/blob/staging/spec/MOVING_PRACTICES.md) in BestPractice). Until then THIS copy is the one in force wherever this set is declared (shared outranks universal), so an edit goes into both copies. **Its check did not move.** [`tools/checks/check_session_trailer.py`](../tools/checks/check_session_trailer.py) walks every non-merge commit reachable from HEAD; shipped from universal it would run in every consuming repository, and in BestPractice itself, against histories that predate the rule. Decide at the deduplication step whether it stays here under a set-specific practice or is retired -- a deduplicated practice claims no check, so materialization stops copying it to consumers the moment this copy is withdrawn.

**2026-09-29: judged on what a push carries** (Morgan, strength: decided). The check walked every commit reachable from HEAD, so a consumer's Promote was refused over one trailer-less commit already on its `main`, which nothing short of rewriting published history could clear. It now judges only commits origin does not have yet -- each at the first push that carries it, Booked into pre-staging included -- so nothing already on origin needs grandfathering. The same day it stopped flagging commits GitHub makes with its own buttons, and reverts where the working-style set says they need no trailer (Morgan: *"maybe Alex or others don't want to include that"*, which is why that part lives in a set a team can choose not to declare).

## Install
Checked mechanically by [`tools/checks/check_session_trailer.py`](../tools/checks/check_session_trailer.py), scope `tree`, judged on what a push carries: every non-merge commit reachable from HEAD that origin does not have yet (`HEAD --not --remotes=origin`) must carry a session trailer line -- `Session:` or `Claude-Session:` (the key Claude Code Remote's own harness actually emits as of 2026-09; the check accepts either), a URL or the explicit `none available (<tool>)` form. `--range A..B` judges a named range instead, and `--all-history` walks every commit for a deliberate audit. The engine's push check runs it at every push, Booked into pre-staging included, and a full sweep runs it the same way. It doesn't verify the URL actually resolves to a real session -- only that the trailer, in one of its valid shapes, is present, which is the "considered and skipped" vs. "forgotten" distinction this practice's own Why section names. Merge commits are excluded (a merge isn't new planned work of its own); merge detection reads the raw commit object rather than `git log --format=%P`, which silently loses a shallow clone's boundary commit's real parents -- see the check's own `_is_merge` docstring. Commits GitHub made with its own buttons (committer `noreply@github.com`) are excluded, and so are reverts where `revert-needs-no-trailer` resolves in force, asked through the engine's own resolver. One pre-existing, non-merge commit from before this check existed is exempted by SHA (`GRANDFATHERED_SHAS` in the script) rather than rewritten, per `no-rewrite-for-warnings`; `--all-history` still honours it. Tested in both directions, and for each exemption, in [`tools/checks/tests/test_session_trailer.sh`](../tools/checks/tests/test_session_trailer.sh).
