---
slug:        mirror-into-agents
title:       Agent-relevant instructions in a README or other key file also go in AGENTS.md
tier:        on-demand
severity:    default
applies_to:  ["**"]
occasion:    "a README or other key file just gained an operational instruction"
gates:       ["merge"]
index_clause: "an agent-relevant instruction lands in both AGENTS.md and its human home"
checked_by:  null
defines:     []
status:      active
supersedes:  []
overrides:   null
added:       2026-08-31
approved_by: "Morgan F, migrated from RepoPersonalPreferences by the private-set migration session"
---
## Rule
`AGENTS.md` is the file a session is told to read first. A README, `CONTRIBUTING.md`, a getting-started guide, or any other key file can still pick up its own operational instructions over time -- a setup step, a gotcha, a rule about how to work in the repo -- written where a human reader would look, not where an agent is told to look. When any such file gains an instruction useful for an agent to know (the operational kind: how to build it, a constraint on how to work, a step an agent would otherwise miss -- not general project description), fold the same instruction into `AGENTS.md` too, in its own words if that reads better there.

## Detail
This runs both directions: whether the instruction lands first in the README and needs pulling into `AGENTS.md`, or is written into `AGENTS.md` directly and never mirrored back to where a human would expect to read it. It does not run the other way for content that only belongs in one place -- a README's marketing framing has no business in `AGENTS.md`, and `AGENTS.md`'s own meta-structure has no business padding out a README.

## Why
A stray instruction left in only one file is exactly the kind of drift a capture gate exists to catch -- check for it at the same checkpoint any other captured decision gets folded in.

## Story


## Install
No mechanical check: deciding whether a given addition to a README or other key file is "the operational kind... not general project description" is the judgment the rule's own Rule text names explicitly. A check could flag any `AGENTS.md`/README divergence at all, but that would fire constantly on content that correctly belongs in only one place, which the rule's own Detail section says is normal.

