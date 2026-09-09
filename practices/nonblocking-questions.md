---
slug:        nonblocking-questions
title:       A question that isn't a blocker doesn't pause the work
tier:        resident
severity:    default
applies_to:  ["**"]
occasion:    "a question worth asking has come up mid-task"
gates:       []
index_clause: "do the independent work first, ask early, keep going"
checked_by:  null
defines:     []
status:      deduplicated
in_force_at: nonblocking-questions
supersedes:  []
overrides:   null
added:       2026-08-31
approved_by: "Morgan F, migrated from RepoPersonalPreferences by the private-set migration session"
---
## Rule
Once a question is worth asking at all, asking is not itself a stopping point. A session holding a queue of work and an open question doesn't go idle waiting for the answer -- it keeps going on everything the answer doesn't touch.

## Detail
Sort pending questions into blockers and everything else. A blocker is one where proceeding under any assumption would be unsafe, spend real money or touch production the wrong way, or make the delivered work useless if the guess is wrong -- only those justify stopping with nothing delivered. Everything else is non-blocking: do the work that doesn't depend on the answer and the work that comes out the same either way, then ask, then carry on with whatever's still independent.

Ask early, not at the end -- put the question in front of the person as soon as it's formed rather than saving it for a summary, since they're often away when the answer would be most useful. Where the answer would change work already done, say so plainly when asking, so the cost of each option is visible.

## Why
The point is that the answer can arrive while work is still in flight, so a question asked only at the end of a session has nowhere useful to land.

## Story
Migrated here from RepoPersonalPreferences by the phase-3 private-set
migration. No dated incident was recorded; the rule states a working cadence
and its reason, and this Story keeps to that.

It picks up exactly where `small-calls` stops. That rule settles which
judgment calls are worth asking about at all; this one settles what happens
after -- and the answer is that asking is not itself a stopping point. A
session holding both a queue of work and an open question does not go idle
waiting for a reply.

The sorting rule is what makes it safe. A blocker is a question where
proceeding under any assumption would be unsafe, spend real money, touch
production the wrong way, or make the delivered work useless if the guess is
wrong -- those, and only those, justify stopping with nothing delivered.
Everything else gets the same order: do the independent work, do the work
that comes out the same either way, ask, carry on.

Asking early rather than at the end is the part with a practical reason
behind it. The point is for the answer to arrive while work is still in
flight, and a question saved for a closing summary has nowhere to land --
particularly when the person being asked is often away from the computer.

**Deduplicated on 2026-09-09**: now in force from `precedent-team-working-style`, a subject-scoped set. This set is named for the people who happened to write its rules, not for a subject, and this rule was never about maintaining a repository -- it was unreachable from a document project that needed it without also taking twenty-odd rules about syncs and gates. See Precedent's `TODO.md#split-team-sets-by-subject`; `spec/MOVING_PRACTICES.md` for why this is a deduplication and not a retirement -- the rule is fully in force, only the redundant copy went.

## Install
No mechanical check: this is a rule about how a session paces its own work against an open question -- whether it kept moving on independent work instead of going idle. That's a property of session conduct across a conversation, not of any file this repo's tree holds.

