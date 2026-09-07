# `not_binding` Findings for BestPractice — Measurement Output

**This file is output for a later BestPractice-rooted session**, not a
practice and not a decision. It closes the measurement half of BestPractice's
TODO item [`unreachable-practices`](https://github.com/alex137/BestPractice/blob/precedent-beta-v01/TODO.md#unreachable-practices),
which was blocked on a session that could actually read the private practice
text. This session could: rooted in this set, with `precedent-individual` and
`precedent-team-tms` alongside it and a public clone of BestPractice as a
sibling, `precedent_resolve.py` resolved all four sources for the first time —
116 practices, 39 team, 13 individual, 63 universal, 1 repo-local.

**Nothing here has been applied.** BestPractice was treated as read-only for
the session that produced this, so `precedent.json`'s `not_binding` list is
still empty upstream. A later session rooted there should re-judge rather than
paste: the reasons below are the argument, and the argument is the part worth
checking.

## How to Read This

`not_binding` says a practice is **in force at its source but does not bind
BestPractice** — a rule about a different *kind* of repository. It is not a
way to record disagreement with a rule, and it is not a way to defer work.
Three separate verdicts are kept apart below, because collapsing them is how
an exemption gets written for something that was really just unfinished.

Every reason below is written to be **publication-safe**: BestPractice is
world-readable and its `precedent.json` is a tracked file, so these reasons
describe the *kind* of repository each rule is about, and never quote or
paraphrase private practice text.

A `severity: blocking` practice cannot be exempted at all. Two of the
practices in force here are blocking — `private-repo-scrub` and
`sensitive-characterization-scrub` — and neither appears below in any
verdict other than "binds".

## Verdict 1 — Does Not Bind (Recommended for `not_binding`)

Each of these is a rule whose own text names a kind of repository BestPractice
is not. Slug, source level, and the reason to record:

| Slug | Level | Reason to record in `precedent.json` |
|---|---|---|
| `content-subdirs` | team | The rule scopes itself to a content-oriented repo, one whose deliverable is the writing itself rather than software that runs. This repo's deliverable is a practice engine and the catalogue it publishes. |
| `bestpractice-sync` | individual | The rule governs a project that vendors a universal practice set as tracked files and keeps that copy current. This repo *is* the universal set; it vendors no practice source. |
| `pack-sync` | team | Same shape, pointed at a team set: it governs a project repo that vendors this team's practices as tracked files. This repo resolves its team source as a sibling clone and vendors nothing. |
| `no-duplication` | team | The rule governs a team set's relationship to the universal catalogue — drop a rule that only restates what universal already says. This repo is that universal catalogue, so there is no layer above it to restate. |

## Verdict 2 — Ambiguous, Needs Morgan's Call

**Do not write an exemption for any of these without deciding first.** Each
could equally be a rule this repo simply is not following yet, and an
exemption would make an unfinished thing look settled — the specific failure
`not_binding`'s mandatory-reason field exists to prevent.

- **`file-header`** (individual). This repo already carries a *variant* of the
  header on several dozen markdown files: a calendar date and an author
  phrase, but no hour/minute/second, no per-file version counter, and an
  author that names the session rather than a person. So it is neither
  following the rule nor plainly outside it. The real question is whether a
  public repo with more than one author is the kind of repo a personal
  per-file authorship header belongs in.
- **`drift-notice`** (team). This repo vendors no practice source, so the
  recorded-commit comparison the rule describes has no subject here. But it
  does declare a team source, and it does ship a session-start reporter for a
  source's vendored engine going stale, which is the same concern one layer
  over. Either reading is defensible.
- **`blank-blocklist`** (team). The rule governs a repo running the vendored
  layer's install procedure. This repo publishes that procedure rather than
  running it — but it also keeps blocklists of its own, so "never asks, never
  reminds" is not obviously inert here.
- **`practice-links-travel`** (individual). The rule's own text names a
  private set's practice files. This repo's `practices/` is the public
  universal source — but its files *do* materialize into consuming repos by
  the same mechanism, which is the condition the rule actually cares about.
- **`content-directory`** and **`assorted-notes`** (individual, both
  `severity: advisory`). Both are conditional on a `content/` directory this
  repo does not have, and `content-directory` already yields to an
  established layout by its own text. They may be inert rather than exempt,
  and an exemption for an already-self-limiting rule is clutter.

## Verdict 3 — Binds, and Finds a Real Problem

Not an exemption. **This is work**, and it was confirmed by reproducing it in
this session rather than by reading the practice.

**`claude-web-bootstrap`** (individual) binds and is violated.
`.claude/hooks/precedent-individual-bootstrap.sh` exists in BestPractice's
tree and is correct, but **no entry in `.claude/settings.json` invokes it** —
the wired `SessionStart` hooks are `session-start.sh`, `freshness-guard.sh`
and `commit-identity.sh`, and nothing else. So the hook never runs.

The consequence is not theoretical; it is what this session walked into.
`~/.config/precedent/config.json` did not exist, so the individual source did
not resolve at all, so `commit-identity.sh` in the sibling sets fell back to
*guessing* a timezone from the container's offset instead of enforcing the one
`identity.json` declares. The fix is one entry in `.claude/settings.json`.

## What Was Deliberately Not Judged

`precedent-team-tms` is not declared in BestPractice's `precedent.json`, so
its practices are not in force there and none was judged. The two practices
this session converted to `status: deduplicated` in this set are likewise out
of scope: they are not in force anywhere, so they cannot be exempted from
anything.
