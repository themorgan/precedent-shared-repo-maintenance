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
  rule-scope-ask — unclear which layer a new rule belongs to -- one document, the repo, or which SET? ask once
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
When an unattended job hits something blocking its normal work, or something optional it cannot reach:
  automation-issues — a blocked job opens or updates an issue; an optional input it cannot reach is skipped and reported, never either silently
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
- **Never try to attach a repo owned by somebody else — spawn a session
  rooted there instead.** `add_repo` refuses a cross-owner attachment
  outright: *"cross-tier adds are not supported in v1: requested
  `<other>/<repo>` but session already has repos from owner(s) [`<this>`]"*.
  So before reaching for `add_repo`, compare the owner you want against the
  owners this session already holds. Same owner, attach it. Different owner,
  the only route is a new session with that repo as its **initial** source,
  and a session rooted at one owner can never gain push access to another's
  — which also means it can never merge there, so plan who merges before
  starting the work, not after. This is a platform limit and no amount of
  retrying changes it; the refusal is recorded from both directions, ours on
  2026-09-12 and upstream's own on 2026-09-08 in
  [BestPractice's TODO](https://github.com/alex137/BestPractice/blob/precedent-beta-v01/TODO.md).
  Morgan, 2026-09-12: this has now been rediscovered many times and is not to
  be rediscovered again.

## Working with other sessions

Morgan's instructions, 2026-09-12, after a day that spent roughly $40 across a
fleet of sessions and produced one pull request that had to be closed as a
duplicate. Spawning sessions is **encouraged** — it is the only route to
another owner's repo, and far better than pasting work for a person to carry
between windows. What follows is about making a fleet cheap and legible, not
about having fewer of them.

- **Wake a live session before spawning a fresh one.** A trigger into an
  existing session reuses its context and costs almost nothing; a new session
  re-reads its repo from scratch, which is most of what a session costs
  (measured 2026-09-12: three separate sessions in one upstream repo, $3–9
  each, doing work one session could have done in sequence). Check
  `list_sessions` for a live session already rooted where the work belongs.
- **Pick the model for the job.** `create_session` takes `model`. Reading,
  diffing, inventory and "check whether X is true" do not need the largest
  model; judgment and writing do.
- **Before starting, check whether it is already done.** `git fetch` and read
  the default branch's recent commits, then check again immediately before
  opening a pull request. On 2026-09-12 a session here wrote a change another
  session had merged twenty minutes earlier, and it had to be closed unmerged.
  The repository is the authoritative record of what other sessions did; their
  own status summaries lag and describe intent rather than outcome.
- **A spawned session reports; it does not shop for more work.** Its final
  message says what it did and what is blocked, and stops. It never ends by
  offering a person adjacent work: an offer read as new work becomes a
  duplicate thread against something another session already owns, which is
  how the closed pull request above happened. Anything it noticed goes back to
  whoever spawned it, as an observation.
- **Never re-ask what was already authorized.** Where the next step is obvious
  and reversible, take it and report it; keep questions for the irreversible
  or genuinely ambiguous. A session that sat on a green pull request asking a
  second time for permission it had already been given cost two full context
  loads on 2026-09-12.
- **Make the tree visible in the one place a person looks.** A session that
  spawns another names it — session id and subject — in its own report, and
  titles it so the parent's subject is recognisable in a plain session list.
  Tags can be set but **cannot be filtered on**: `list_sessions` with `tags`
  returns *"tags filter is not currently available"* from inside a session
  (checked 2026-09-12), so the title is what carries lineage, not the tag.
- **Recommend compacting at task boundaries, not at a size.** When a
  deliverable has landed and the next thing is independent, a compact costs
  nothing because the summary carries the conclusion. Mid-investigation it
  costs a re-read. Length is not what is expensive; re-deriving is.
