---
slug:        quiet-checks
title:       Don't repeat the same backlog explanation every run
tier:        on-demand
severity:    default
applies_to:  ["**"]
occasion:    "reporting a check's outcome that includes a known pre-existing backlog"
gates:       []
index_clause: "\"checks passed\" is fine; don't re-explain the same old backlog"
checked_by:  null
defines:     []
status:      deduplicated
in_force_at: quiet-checks
supersedes:  []
overrides:   null
added:       2026-08-31
approved_by: "Morgan F, migrated from RepoPersonalPreferences by the private-set migration session"
---
## Rule
A repo's own mechanical checks can report a real, pre-existing backlog unrelated to the current edit. A session that explains away that same unchanging backlog with the same sentence every single commit -- "pre-existing warnings only, unrelated to my edit," or an equivalent -- is repeating a disclaimer that never changes and never informs the next step. Drop that specific recurring explanation.

## Detail
This does not mean staying silent about checks in general: a plain "checks passed" (or "checks failed, here's why") is normal and often exactly what's wanted, wherever reporting an outcome is the natural thing to do. The distinction is between reporting an outcome, which is fine, and re-explaining the same known, static backlog every time as though it were new information, which isn't. A run that actually failed, or a warning the current edit newly introduced, is always worth flagging.

## Why
The runbook already moves on to checking branch state and committing regardless of what that recurring sentence says, so it is pure repetition with no informational payoff.

## Story
Migrated here from RepoPersonalPreferences by the phase-3 private-set
migration; the Story is backfilled from that pack's own text, and it names
an observed habit rather than a single dated failure.

The setup is a real, static backlog. Running the doc linter across a whole
repo turns up a pile of unlinked-reference and unglossed-acronym warnings
that predate the current branch and are not gated -- the linter's own scope
is files changed against the default branch, on a fix-what-you-touch basis.
So the backlog is expected and is nobody's current problem.

The habit the rule targets is what sessions then did with it: explaining it
away with the same sentence before every single commit -- "pre-existing
warnings only, unrelated to my edit". That disclaimer never changes and
never informs the next step, since the runbook moves on to checking branch
state and committing regardless of what the sentence says. It is words spent
to produce no decision.

The rule is carefully bounded because the obvious overcorrection is worse.
It is not a rule about staying silent on checks: a plain "checks passed", or
a failure with its reason, is normal and often exactly what is wanted. The
distinction is between reporting an outcome, which is fine, and re-explaining
a known static backlog every time as though it were new information. A run
that actually failed, or a warning this edit introduced, is new information
every time and always worth flagging.

**Deduplicated on 2026-09-09**: now in force from `precedent-team-working-style`, a subject-scoped set. This set is named for the people who happened to write its rules, not for a subject, and this rule was never about maintaining a repository -- it was unreachable from a document project that needed it without also taking twenty-odd rules about syncs and gates. See Precedent's `TODO.md#split-team-sets-by-subject`; `spec/MOVING_PRACTICES.md` for why this is a deduplication and not a retirement -- the rule is fully in force, only the redundant copy went.

## Install
No mechanical check: it governs how a session narrates a check's outcome in its own reply across turns of a conversation -- whether the same static-backlog disclaimer got repeated -- which isn't content this repo's tree, or any single commit, holds a record of.

