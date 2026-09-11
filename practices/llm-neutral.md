---
slug:        llm-neutral
title:       LLM integrations stay platform-neutral; OpenRouter is the default assumption
tier:        on-demand
severity:    default
applies_to:  ["**"]
occasion:    "building or setting up a system that talks to an LLM"
gates:       []
index_clause: "build LLM integrations provider-neutral; assume an OpenRouter token"
checked_by:  null
defines:     []
status:      retired
in_force_at: none
supersedes:  []
overrides:   null
added:       2026-08-31
approved_by: "Morgan F, migrated from RepoPersonalPreferences by the private-set migration session"
---
## Rule
Whenever a system needs to talk to an LLM, build it against a provider-neutral interface -- model name, API key/token, and base URL as swappable configuration, not hard-wired to one vendor's SDK, auth header shape, or response schema. Absent a specific instruction otherwise, assume the credential in hand is an OpenRouter token, not a given vendor's own key.

## Detail
OpenRouter's own API is itself OpenAI-request-shaped and fronts most major model providers behind one key and one endpoint *(verified 2026-08-22)* -- re-verify this if OpenRouter's API shape is ever the reason a piece of code built against this rule breaks.

## Why
That keeps swapping providers, or dropping in whichever token happens to be on hand, a config change rather than a rewrite chasing call sites through the codebase.

## Story
**Retired 2026-09-11, by Morgan**, `strength: decided` -- his own words,
*"okay I think we can retire these"*, going further than the proposal on
the table, which was to move them into a subject set for engineering
craft. Reviewing this set after the 2026-09-09
subject split, this was one of two rules left in it that are not about
maintaining a repository at all: it governs how you build an integration
against a model provider, which is engineering craft. The split's own test
-- *who breaks if this is wrong?* -- puts it with everyone who writes that
kind of code, not with the people who run a vendoring repo, and reaching it
required declaring twenty-odd rules about syncs, gates and branch setup.

No subject set exists for engineering craft, and inventing one to hold two
practices was not the call made. Morgan retired it outright rather than move
it. Nothing in this repository's ecosystem calls a model API today
(BestPractice's own pre-launch audit already recorded this rule as *not
applicable* there for exactly that reason), so nothing loses a rule it was
relying on.

**What is given up, said plainly:** the OpenRouter default assumption is now
written down nowhere in force, and a future session building an LLM
integration will pick a provider's own SDK unless told otherwise. If that
ever costs something, this file is the argument, still readable.

Migrated here from RepoPersonalPreferences by the phase-3 private-set
migration. No originating incident was recorded, and this Story does not
supply one.

The reasoning is about the cost of the alternative: hard-wiring one vendor's
SDK, auth header shape or response schema turns swapping providers into a
rewrite that chases call sites through the codebase, where a neutral
interface makes it a config change. Model name, token and base URL are the
three things that actually vary.

The OpenRouter default is an assumption with a date on it, not a
preference: it is the provider actually in day-to-day use, so it is the
safer thing to design and test against, and its API is OpenAI-request-shaped
while fronting most major providers behind one key and one endpoint
(*verified 2026-08-22*). That makes it double as a sensible default shape
for the neutral interface itself. The date is on the claim deliberately --
if code built against this rule ever breaks because of the API's shape, that
claim is the thing to re-verify first.

## Install
No mechanical check: "provider-neutral" is a property of a whole integration's design (is the model name, key, and base URL actually swappable configuration, or hard-wired), not something a grep for a vendor's name can classify -- a comment or a config default mentioning a provider isn't itself a violation, and a real violation (a response schema parsed assuming one vendor's shape) has no fixed textual signature.

