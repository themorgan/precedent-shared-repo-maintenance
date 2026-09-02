---
slug: resolved-issue-note-updates
title: A resolved 'known issue' note is updated in the same commit that resolves it
date: 2026-09-02
status: promoted
signal: review-found-defect
raised_by: "Claude Code deep-check session, https://claude.ai/code/session_01EvcumpW3WguJ6qMWtTjqgp"
recurrence_count: 1
cost_if_once: "A reader (or the next session) trusts the document's own claim over the code: they either re-fix something already fixed, or budget time worrying about a gap that no longer exists -- wasted effort from a document silently diverging from the code the moment a fix lands, exactly the failure drift-notice and no-stale-counts already guard against for other kinds of staleness."
tier_requested: on-demand
proposed_checked_by: null
proposed_applies_to: ["**"]
proposed_occasion: "When a commit fixes, closes, or resolves something a document names in prose as a known, open issue"
proposed_gates: []
---
## Observed
BestPractice's spec/PHASE5_BRIEF.md named a real bug in prose: 'A known bug, found while writing this brief, not yet fixed' (precedent_candidate.py create's same-day recurrence collision). This deep-check session fixed the bug in tools/precedent_candidate.py, but the brief's own 'not yet fixed' sentence would have kept reading that way indefinitely if the session hadn't gone back to it on purpose -- nothing flags a stale not-yet-fixed claim once the code it describes has actually changed. The same shape recurs with any 'known issue' or 'open gap' note written into a spec, README, or backlog document: the note and the code drift apart the moment one of them moves without the other.

## Proposed Rule
When a commit fixes a bug, closes a gap, or resolves a limitation that some document names in prose as known-and-open ('not yet fixed', 'a real gap', 'currently unsupported'), update that document in the same commit -- mark it resolved with what changed, or remove the stale claim. Never leave a fixed issue described in prose as still open.
