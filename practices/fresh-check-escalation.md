---
slug:        fresh-check-escalation
title:       When the freshness check can't reach the source, say so -- then verify directly
tier:        on-demand
severity:    default
applies_to:  ["**"]
occasion:    "a session-start freshness check against a private source can't be reached"
gates:       []
index_clause: "tell \"could not verify\" apart from \"confirmed fresh\"; verify directly"
checked_by:  null
defines:     []
status:      active
supersedes:  []
overrides:   null
added:       2026-08-31
approved_by: "Morgan F, migrated from RepoPersonalPreferences by the private-set migration session"
---
## Rule
A freshness check against a private source is built deliberately silent on a transient failure -- offline, a timeout -- treating it the same as "nothing has moved," because a notice that turns out to mean only "the network hiccuped" would be worse than no notice at all. That silence assumption breaks for a standing gap rather than a blip: an environment with no credentials for the private source at all, ever, where the same check fails the exact same way every session and gets read as "confirmed current" indefinitely. Tell the two failure modes apart: a fast, clean failure (bad or missing credentials, a permission error) prints a "could not verify" line, distinct from silence.

## Detail
"Could not verify" is not "confirmed fresh" -- if the environment offers any way to reach the source directly, use it, instead of trusting silence. If no such mechanism exists either, say so plainly instead of reporting the sync as current.

## Why
An environment with a standing credential gap fails the same way, every single session, indefinitely -- without this distinction, real drift stays masked for as long as that environment exists.

## Story
Migrated here from RepoPersonalPreferences by the phase-3 private-set
migration; the Story is backfilled from that pack's own text, and it records
a specific failure found directly rather than reasoned about.

The freshness check against a private source was built deliberately silent
on failure -- offline, a timeout, a transient blip -- treating it as
"nothing has moved", because a notice that turned out to mean only "the
network hiccuped" would be worse than no notice at all. That assumption
holds for a blip and breaks completely for a standing gap.

On 2026-08-29, in a dependent repo, a session's check against the private
source returned `fatal: could not read Username for 'https://github.com':
terminal prompts disabled` -- an environment with no credentials for that
repo at all, ever. It was a fast, clean failure rather than a hang, and it
would fail identically every session, so the silent design would have read
it as "confirmed current" indefinitely and masked real drift for as long as
that environment existed.

Hence the split the rule turns on: a genuinely unreachable remote stays
quiet, unchanged, while a fast non-zero error prints a line saying the check
did not run. The judgment half matters as much as the mechanism -- "could
not verify" is not "confirmed fresh", so a session seeing that line reaches
the source another way if the environment offers one, and says plainly that
it could not verify if none exists. That is exactly how the gap was closed
the one time it was hit.

## Install
No mechanical check: the freshness-check mechanism this rule refines doesn't exist as code in this repo (it runs in a consuming repo, against a private source), and the actual distinction it requires -- printing "could not verify" instead of staying silent on a standing credential gap -- is behavior of that mechanism's own error handling, not a property this repo's tree can be scanned for.

