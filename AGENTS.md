# Repository notes for agents

This repo IS `precedent-team-repo-maintenance` — the **team** source for
[Precedent](https://github.com/alex137/BestPractice/tree/precedent-beta-v01)'s
maintaining team (Morgan and Alex). See [README.md](README.md) for what's
here and how the practices in [practices/](practices/) got here.

<!-- BEGIN GENERATED: precedent-loader -->

<!-- Regenerate with: python3 tools/build_views.py -- do not hand-edit this block; `python3 tools/build_views.py --check` exits non-zero on drift. -->

## Occasion index

```
When a README or other key file just gained an operational instruction:
  mirror-into-agents — an agent-relevant instruction lands in both AGENTS.md and its human home
When a new rule is proposed and its scope isn't obvious:
  rule-scope-ask — unclear if a new rule is repo-wide or one document? ask once
When a session starts in a repo that vendors a universal or team set:
  drift-notice — check source freshness at session start; raise it right away, not later
When a session-start freshness check against a private source can't be reached:
  fresh-check-escalation — tell "could not verify" apart from "confirmed fresh"; verify directly
When about to commit:
  light-check — a cheap mechanical audit runs before every commit, not just merges
When about to push after a thread of work:
  todo-gate — add missed ideas, check off finished ones, before every push
When adding a new rule to a maintained rules document:
  new-rule-placement — place a new rule by subject, slug it, renumber, mirror, re-check
When adding or reviewing a team-set rule:
  no-duplication — a rule that only restates universal gets dropped
When an unattended scheduled job hits something blocking its normal work:
  automation-issues — a blocked scheduled job opens or updates an issue, not just a log line
When asked for a "deep check" by name, or after drift-inviting work:
  deep-check — every mechanical audit, plus a full read of the repo against itself
When bringing a vendored practice layer into a new or existing repo:
  install — vendor the tree, weave conventions into AGENTS.md, wire checks and manifest
When committing anything:
  session-trailer — a Session: <url> trailer on every commit
When creating a file a later regeneration will overwrite:
  derived-file-marker — a regenerated file's header names its source, recipe, and command
When installing a vendored practice layer that could check in upstream:
  blank-blocklist — leave a check-in blocklist blank at install; don't ask, don't remind
When landing practices in bulk -- a migration, an import, or a move from another set:
  catalogue-carries-stories — no active practice in this set sits with an empty ## Story
When setting up a new repo, or installing into an existing one:
  default-branch — check or set the default branch to main, once, at install
When writing content that will vendor or ship into another repo:
  private-repo-scrub — name a private repo only in general terms in anything that ships elsewhere
```

## Standing instruction

Before starting work of a kind named in the occasion index above, run `python3 tools/precedent_show.py SLUG` for each listed slug to load its Rule. When editing a file, `python3 tools/precedent_paths.py FILE` prints any on-demand practice whose `applies_to` matches it, without needing the index at all. At a named moment — merging a branch, before pushing — run `python3 tools/precedent_gate.py merge|push`: some practices fire at a moment rather than in a file, and no path glob reaches those.

<!-- END GENERATED -->

## Working in this repo

- **Practices are in [practices/](practices/)**, one file per practice, in
  the format [`spec/PRACTICE_FORMAT.md`](https://github.com/alex137/BestPractice/blob/precedent-beta-v01/spec/PRACTICE_FORMAT.md)
  documents.
- **The loader block above is generated** — regenerate with
  `python3 tools/build_views.py`; hand-editing it is pointless, the next
  regeneration overwrites it. Run it bare, not `--agents-only`: since
  2026-09-06 this set renders [`MAP.md`](MAP.md) and
  [`GLOSSARY.md`](GLOSSARY.md) too, and `--agents-only` would leave both
  stale after a practice changes.
- **Changes to this set need an approver's yes** — see
  [`approvers.json`](approvers.json) and the README's "Approvers" section.
