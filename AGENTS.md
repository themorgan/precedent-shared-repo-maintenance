# Repository notes for agents

This repo IS `precedent-shared-repo-maintenance` — the **shared** source for
[Precedent](https://github.com/alex137/BestPractice/tree/staging)'s
maintaining team (Morgan and Alex). See [README.md](README.md) for what's
here and how the practices in [practices/](practices/) got here.

<!-- BEGIN GENERATED: precedent-loader -->

<!-- Regenerate with: python3 tools/build_views.py -- do not hand-edit this block; `python3 tools/build_views.py --check` exits non-zero on drift. Source: practices/ -- edit the practice file, never this block. -->

## Occasion index

```
When a key file gains an operational instruction:
  mirror-into-agents — it lands in both AGENTS.md and its human home
When a new rule's scope isn't obvious:
  rule-scope-ask — ask once which layer or set it belongs in
When about to commit:
  light-check — a cheap mechanical audit runs before every commit, not just merges
When adding or reviewing a shared-set rule:
  no-duplication — a rule that only restates universal gets dropped
When an unattended job is blocked, or can't reach an optional input:
  automation-issues — a blocked job files or updates an issue; skip an optional input, never silently
When asked for a "deep check":
  deep-check — every mechanical audit, plus a full read of the repo against itself
When asked for something another window may already be doing:
  dont-race-another-window — say so and decline; send me to the window already on it
When committing anything:
  session-trailer — a Session: <url> trailer on every commit
When creating a file regeneration will overwrite:
  derived-file-marker — a regenerated file's header names its source, recipe, and command
When installing Precedent or a shared set into a repo:
  install — precedent_install.py, declare the set, wire the individual set, main as default
When session start reports a source BEHIND or NOT VERIFIED:
  drift-notice — raise it at once and file it; not verified is not current -- verify directly
When setting up a project, or a session reporting its checkout is behind:
  fresh-before-write — verify and fast-forward the checkout before the first write
When writing a hook, script or rule another repo will vendor:
  vendor-neutral-by-default — default new code and rules to provider-neutral
When writing content that ships into another repo:
  private-repo-scrub — name a private repo only in general terms

(More on-demand practices are not listed here: one whose applies_to names real paths, or which declares a gate, is reached by those channels instead -- `precedent_paths.py FILE` and `precedent_gate.py MOMENT`. A trigger a PERSON SAYS cannot be reached that way and is always listed above. `precedent_show.py --index-omitted` names the omitted ones.)
```

## Standing instruction

Before starting work of a kind named in the occasion index above, run `python3 tools/precedent_show.py SLUG` for each listed slug to load its Rule. When editing a file, `python3 tools/precedent_paths.py FILE` prints any on-demand practice whose `applies_to` matches it, without needing the index at all. At a named moment — merging a branch, before pushing — run `python3 tools/precedent_gate.py merge|push`: some practices fire at a moment rather than in a file, and no path glob reaches those. If `.precedent/SESSION_PRACTICES.md` exists, read it too: it carries the practices in force from the other sources this repo declares, which are NOT in this block and bind work here exactly as these do. It is regenerated at session start and is deliberately untracked — never commit it or quote it into a pull request.

<!-- END GENERATED -->

## Working in this repo

- **Practices are in [practices/](practices/)**, one file per practice, in
  the format [`spec/PRACTICE_FORMAT.md`](https://github.com/alex137/BestPractice/blob/staging/spec/PRACTICE_FORMAT.md)
  documents.
- **The loader block above is generated** — regenerate with
  `python3 tools/build_views.py`; hand-editing it is pointless, the next
  regeneration overwrites it. Run it bare, not `--agents-only`: since
  2026-09-06 this set renders [`MAP.md`](MAP.md) and
  [`GLOSSARY.md`](GLOSSARY.md) too, and `--agents-only` would leave both
  stale after a practice changes.
- **Changes to this set need an approver's yes** — see
  [`approvers.json`](approvers.json) and the README's "Approvers" section.
- **Run `python3 tools/precedent_check.py --full-sweep` before pushing — it
  is the only check there is here now.** What matters is `0 violated`; the large
  skipped count is normal here and is not a failure — those checks belong
  to levels this set does not resolve. This repo carried a
  `precedent-check.yml` workflow from 2026-09-14 and a `leak-gate.yml` from
  2026-09-20; on 2026-09-21 the vendored engine deleted both on refresh,
  because a practice source installs no CI at all — universal's
  `source-sets-run-no-ci`, decided on a usage export in which four sets
  running two workflows each were 127 of 143 billed minutes in one day.
  Nothing runs after the push, on any branch: the check runs before it, or
  it does not run.
  **Run it with `--full-sweep`; the bare command is a trap.** Bare, it runs
  only the checks this diff routes to plus a one-in-ten rotation, and a
  check whose practice applies to `**` -- most of this set's -- is reached
  only by the rotation. That is how two links to a private repo, added
  2026-09-23, sat on `main` past a clean bare run until a sweep found them
  on 2026-09-24. The sweep takes about five seconds.
- **The hand-written half of this file describes the MECHANISM, never the
  INVENTORY.** A rule goes in a practice file, where the loader dedupes it,
  precedence ranks it and `supersedes` retires it. Written here as prose, it
  is invisible to all three, and stays in force after the rule it copied
  changes upstream. That is what happened: on 2026-09-12 this file restated
  a set of session-handling rules because this set resolved no universal
  practices then. From 2026-09-13 it did, through
  `.precedent/SESSION_PRACTICES.md`, and nobody removed the copies. One of
  them, "wake a live session before spawning a fresh one", went on
  instructing sessions after universal's `prompt-please` told them never
  to wake a live session to hand work over. They were removed on 2026-09-23. **Before adding a
  rule here, check whether a practice in any declared source already says
  it** -- `.precedent/SESSION_PRACTICES.md` is where to look.
