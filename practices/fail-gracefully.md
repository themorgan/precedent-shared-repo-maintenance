---
slug:        fail-gracefully
title:       Always fail gracefully
tier:        on-demand
severity:    default
applies_to:  ["**"]
occasion:    "writing code that depends on something outside its own control, or handling a part that could not run"
gates:       []
index_clause: "keep going on a missing config, file, call or credential — and tell the session's human"
checked_by:  null
defines:     []
status:      active
supersedes:  []
overrides:   null
added:       2026-08-31
approved_by: "Morgan F, migrated from RepoPersonalPreferences by the private-set migration session"
---
## Rule
Any code written or set up here anticipates its own common failure modes rather than letting them surface as an unhandled crash. Failing gracefully means **two** things, and one without the other is still a violation:

1. **Keep going.** The work continues. A part that cannot run does not stop the session, abort the surrounding task, or take the rest of the system down with it: check for the absence or failure case on purpose and carry on with a documented fallback, a reduced scope, or that one part skipped -- never a raw stack trace, a hang, or an abort of work that did not depend on the thing that failed.
2. **Say so, to the person in the session.** Every degraded path announces itself where the human running the session will see it, naming what could not run, what that means for the result they are about to trust, and what would fix it. Silence is not grace. A quiet fallback, an empty result reported as a clean one, a swallowed exception -- each of these is a *worse* failure than the crash, because the crash at least told someone.

The failure mode this rule forbids is not "an error happened." It is **a result that looks complete and is not**, or **a stop that did not have to happen**.

## Detail
Three shapes recur, all of them "graceful" by the narrow reading and violations by this one:

- **The silent fallback.** A missing optional dependency, a config that did not load, a network call that failed -- handled, defaulted, and never mentioned. The next reader has no way to know the result is partial.
- **The empty scan reported as clean.** A check whose input did not exist, whose parser is not installed, or whose history was too shallow to reach what it walks, printing the same "OK" it prints when it genuinely looked and found nothing. "Could not check" and "checked, nothing wrong" must never render identically.
- **The stop that need not be one.** One part failing takes down a whole run that had many independent parts, when the honest outcome was to skip that part, say which, and finish the rest.

Where a tool has an exit status, "keep going" applies to the *work*, not to the status: a run that could not check something still reports that honestly rather than exiting 0, and a run whose one purpose could not be served at all may still exit non-zero -- as long as it says why, in words naming the fix.

## Why
The three sanctioned degradations look like a list of options and are really one property: **the caller can act on the result.** A clear message naming what is missing and how to fix it, a documented fallback, and a clean non-zero exit all pass that test. The three failures named opposite them do not — and the last two fail it worst, because neither announces that anything happened at all.

The rule targets dependencies outside the program's own control specifically, because that is where the assumption is invisible. Code that assumes a file exists reads exactly like code that has checked, right up until the environment differs. Nothing in the source distinguishes them, so the check has to be written on purpose rather than noticed in review.

## Story
Migrated here from RepoPersonalPreferences by the phase-3 private-set
migration. That pack recorded no originating incident, and this Story says
so rather than inventing one.

It is also the odd rule out by kind: almost everything around it is a
repository-process rule, and this is a coding-quality rule about what gets
built. It was kept at this level rather than raised to the universal
catalogue for a stated reason -- general enough to want in every project,
but simple enough that a persuasive, attributed upstream submission was not
judged worth the effort yet. That remains the outlet if it changes.

The substance is a list of things outside a program's own control -- a
required config or environment variable, a file assumed to exist, a network
call, a third-party credential -- each of which fails in production and none
of which fails usefully by default. The three sanctioned degradations all
share one property: the caller can act on them. A clear message naming what
is missing and how to fix it, a documented fallback, or a clean non-zero
exit. A raw stack trace, a silent wrong answer, and a hang all fail that
test, the last two worst, because neither announces that anything happened.

## Install
No mechanical check, and this is the second attempt rather than an
assumption (practice `checkable-gets-checked`).

**Clause 1** -- whether code "anticipates its own common failure modes" and
keeps going -- is a judgment about error-handling adequacy across arbitrary
code in any language, not a fixed syntactic pattern: a bare `except:` is
sometimes exactly wrong and sometimes a deliberate, documented catch-all. At
this scope (`applies_to: ["**"]`, no language or shape specified) no static
rule is both broad enough to catch real violations and narrow enough not to
flood.

**Clause 2** -- the silent degrade -- looked more promising, because it has a
shape: an `except` handler whose body neither raises, nor prints or logs, nor
exits, but returns a default. Measured 2026-09-06 against Precedent's own
`tools/` (37 scripts, the most heavily audited Python in this project): **67
hits**, the large majority of them legitimate -- a narrow `except ValueError:
continue` inside a parser loop is correct and has nothing to announce. At that
signal-to-noise ratio the check would be turned off within a week, which is
worse than not having it, so this stays advisory and the measurement is
recorded here rather than re-derived by the next session that has the same
idea.

What IS enforceable is the specific case, not the general one. Where a
particular family of scripts must distinguish "could not check" from "checked,
nothing wrong," that family's own check can assert it -- `check_deep_check.py`
does exactly this for the check scripts in this set, and Precedent's own
harness asserts it for its gates. The general rule stays a review judgment;
each place it actually bites gets its own narrow check.
