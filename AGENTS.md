# Repository notes for agents

This repo IS `precedent-team-repo-maintenance` — the **team** source for
[Precedent](https://github.com/alex137/BestPractice/tree/precedent-beta-v01)'s
maintaining team (Morgan and Alex). See [README.md](README.md) for what's
here and how the practices in [practices/](practices/) got here.

<!-- BEGIN GENERATED: precedent-loader -->

<!-- Regenerate with: python3 tools/build_views.py -- do not hand-edit this block; `python3 tools/build_views.py --check` exits non-zero on drift. Source: practices/ -- edit the practice file, never this block. -->

## Occasion index

```
When a new rule is proposed and its scope isn't obvious:
  rule-scope-ask — unclear which layer a new rule belongs to -- one document, the repo, or which SET? ask once
When a session starts in a repo that vendors a universal or team set:
  drift-notice — check source freshness at session start; raise it right away, not later
When a session-start freshness check against a private source can't be reached:
  fresh-check-escalation — tell "could not verify" apart from "confirmed fresh"; verify directly
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
When setting up a new repo, or installing into an existing one:
  default-branch — check or set the default branch to main, once, at install
When writing a hook, script, or practice-file rule in a repository this team maintains that vendors a layer out to other repos:
  vendor-neutral-by-default — a team-maintained vendor source ships out whole -- default to provider-neutral

(More on-demand practices are not listed here: one whose applies_to names real paths, or which declares a gate, is reached by those channels instead -- `precedent_paths.py FILE` and `precedent_gate.py MOMENT`. A trigger a PERSON SAYS cannot be reached that way and is always listed above. `precedent_show.py --index-omitted` names the omitted ones.)
```

## Standing instruction

Before starting work of a kind named in the occasion index above, run `python3 tools/precedent_show.py SLUG` for each listed slug to load its Rule. When editing a file, `python3 tools/precedent_paths.py FILE` prints any on-demand practice whose `applies_to` matches it, without needing the index at all. At a named moment — merging a branch, before pushing — run `python3 tools/precedent_gate.py merge|push`: some practices fire at a moment rather than in a file, and no path glob reaches those. If `.precedent/SESSION_PRACTICES.md` exists, read it too: it carries the practices in force from the other sources this repo declares, which are NOT in this block and bind work here exactly as these do. It is regenerated at session start and is deliberately untracked — never commit it or quote it into a pull request.

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
- **Run `python3 tools/precedent_check.py` before pushing.** What matters is
  `0 violated`; the large skipped count is normal here and is not a failure —
  those checks belong to levels this set does not resolve. Since 2026-09-14
  [`.github/workflows/precedent-check.yml`](.github/workflows/precedent-check.yml)
  runs the same suite on every push, on every branch (not just a pull
  request), so a violation is caught either way; running it yourself is how
  you find out before the push rather than
  after.
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
  be rediscovered again. **This bullet re-states universal, it does not author
  anything.** `spawn-session` at universal already requires naming the
  repositories work must read, write or push to and comparing them against the
  ones this session holds, before starting; and the refusal itself is recorded
  upstream in four places -- that repo's `AGENTS.md`, `INSTALL.md`, `TODO.md`,
  and a 2026-09-01 decision record. It is repeated here because this set
  declares no sources and materializes nothing into itself, so universal text
  never arrives and deleting the local copy would switch the guidance off
  rather than defer it. Not a `no-duplication` candidate for that reason.
  `catalogue-carries-stories` was the parallel case until 2026-09-13 and is
  deliberately no longer: `binds_publishers` lets a CHECK bind this set off
  universal's own text, so that local declaration was deduplicated. Nothing
  does the same for prose -- a check can be taught to bind a publisher, an
  occasion-index line cannot -- which is why this bullet stays where that
  one went.

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

### Where these rules actually live

Written here on 2026-09-12 as though this set owned them. It does not own most
of them, and a reader cannot tell which by looking -- so, in three groups:

- **Already universal, re-stated here only because nothing resolves into this
  set.** The repository check before starting work, and the cross-owner refusal
  above: both are `spawn-session` at universal, added 2026-09-11, gated on
  every reply. Read that practice for the authoritative wording; fix any
  disagreement *there*, not here.
- **Canonical in the working-style team set, not here.** "A spawned session
  reports rather than offering a person more work" is `report-up-the-chain`
  there, and "never re-ask what was already authorized" is a clause of
  `small-calls` there, both landed 2026-09-12. This set resolves that set no
  more than it resolves universal, which is the only reason a copy sits here.
- **Genuinely not upstream yet, and this is the export list.** Waking a live
  session rather than spawning a fresh one; choosing the model for the job; the
  cost of a cold start; naming a child session and carrying lineage in its
  title (with the checked negative about tag filtering); compacting at a task
  boundary; and checking the default branch before starting and again before
  opening a pull request. Verified absent from universal on 2026-09-12. These
  are the lines to carry upstream -- `mistakes-become-rules`' rung (c), the one
  the session that wrote them skipped.

**Why this section exists in this shape at all**, since it is the incident
worth remembering: the session that wrote these rules had a readable clone of
the universal set in its scratchpad the whole time and never searched its
`practices/` before writing. It verified every factual claim against upstream
that day and never verified a *rule* against upstream's catalogue, so it
re-authored a universal practice one level down. The level was chosen by which
repository it could merge in -- which `rule-scope-ask` now forbids in as many
words.
