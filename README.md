<!-- Last updated: 2026-09-05 (Buenos Aires) by Morgan F, to version 4 -->

# precedent-team-maintainers

The team practice set for [Precedent](https://github.com/alex137/BestPractice/tree/precedent-beta-v01)
— one small group's working conventions, vendored into a project repo the
same way universal practices are, and (as of the 2026-09-03 precedence
reorder) the **strongest** of the four sources: team beats repo-local beats
individual beats universal by default
([PRACTICE_ENGINE_PLAN.md](https://github.com/alex137/BestPractice/blob/precedent-beta-v01/PRACTICE_ENGINE_PLAN.md),
"Precedence, and the One Case Precedence Alone Does Not Decide").

## What's here

**[AGENTS.md](AGENTS.md) is the working index** — its generated loader block
(resident practices in full, everything else grouped by occasion) is what a
session actually loads; regenerate it with
`python3 tools/build_views.py` after any practice change, which rebuilds
[`MAP.md`](MAP.md) and [`GLOSSARY.md`](GLOSSARY.md) alongside it. This
section gives the history and allocation reasoning `AGENTS.md`'s generated
block doesn't carry.

[`NOT_BINDING_FINDINGS.md`](NOT_BINDING_FINDINGS.md) — a one-off measurement
record, not a practice: which of the practices in force in BestPractice do and
do not bind that repository, produced here because this is where the private
practice text is actually readable. It is output for a later
BestPractice-rooted session to act on, and nothing in it has been applied
upstream.

[`LEAK_SCRUB_FINDINGS.md`](LEAK_SCRUB_FINDINGS.md) — what running the leak
gate's private vocabulary half against a real tree turned up, a per-file
scrub plan, and a proposed universal practice with the one correction it
needs. Also output for a later BestPractice-rooted session.

[`SOURCE_CHECK_AUDIT_FINDINGS.md`](SOURCE_CHECK_AUDIT_FINDINGS.md) — the
2026-09-10 audit of this set's own `tools/checks/` for install-model
assumptions: checks that read an INSTALL.md §1 path as if it were
universal, an absent optional file as a violation, an optional engine
module without a guard, or an empty `git log` as a clean tree. Three were
found and fixed, three open items are recorded with what each is blocked
on, and the two sibling team sets that supply no checks at all are
recorded as audited so nobody repeats the pass. Evidence for BestPractice's
TODO item 52, which this repo cannot close from here.

[`STORY_BACKFILL_ROLLOUT.md`](STORY_BACKFILL_ROLLOUT.md) — how to do the
`## Story` backfill in another repo that upgraded onto Precedent, including
how to tell whether it has the problem at all.

`practices/*.md` — one file per practice, in the format
[spec/PRACTICE_FORMAT.md](https://github.com/alex137/BestPractice/blob/precedent-beta-v01/spec/PRACTICE_FORMAT.md)
documents: practices migrated from RepoPersonalPreferences' 46 rules
(`PRIVATE_SETS_BRIEF.md`) — everything that wasn't the Morgan-specific
handful (now in
[`precedent-individual`](https://github.com/themorgan/precedent-individual),
private) or retired outright (`morgan-scope`, `bestpractice-wins` — both
existed only to declare something Precedent's own architecture now
expresses structurally, so there was nothing left for either to do).

**Default allocation, not a final judgment.** Several of these plainly read
as generic enough for universal — graceful failure, platform-neutral LLM
integrations, not stating counts that drift, linking what you cite — and
stayed team anyway: promoting to universal is a designed path with its own
approval step; demoting a universal practice means undoing something
already published to every Precedent user. Promote individually, as the
team decides each one is ready.

Two practices are marked `severity: blocking`
(`sensitive-characterization-scrub`, `private-repo-scrub`) — real
information-leak guards. This predates the precedence reorder above, from
when team ranked below individual and `blocking` was the only thing stopping
a personal override; team now already outranks individual by plain
precedence, so the marking is redundant rather than load-bearing for these
two specifically — left in place since it's harmless and still correct
(nothing above team can override a blocking team practice either way), not
re-litigated here.

`rule-links` and `go-merge` (the latter in `precedent-individual`) each
carry `overrides:` against a universal practice they specialize
(`doc-references-are-links`, `merge-authorization-keyword`).

`.claude/` holds two session hooks and their wiring, added 2026-09-06 from
BestPractice's Claude Code adapter. `freshness-guard.sh` stops a session
working on, or writing to, a stale checkout — it fetches and fast-forwards
where that is provably lossless, and refuses the session's first tool call
on a checkout it cannot vouch for, measuring staleness against the base
branch as well as against this branch's own remote.
`commit-identity.sh` makes a commit's author the person running the
session rather than the container's own bot account: it resolves whoever
that is at run time — an explicit override, then their individual source's
`identity.json`, then the session account, then the authenticated GitHub
account — so no person is named in any tracked file here, and installs a
`pre-commit` hook that refuses a bot-authored commit. Both are installed
into every newly bootstrapped source too, by
`precedent_bootstrap_source.py`.

`tools/` beyond `tools/checks/` is Precedent's vendored source-repo engine —
`build_views.py`, `precedent_gate.py`, `precedent_paths.py`,
`precedent_show.py`, `split_practices.py`, a trimmed `routing_scope.json`,
`precedent_vendor_engine.py` itself, and — since 2026-09-06 —
`build_codeowners.py`, which this repo wrote and owned privately until
BestPractice promoted it into the engine so that every team set it
bootstraps can turn a declared approver list into real enforcement. As of
2026-09-05 this is a real, tracked copy (`tools/ENGINE_MANIFEST.json`
records the BestPractice commit and a sha256 per file) instead of the
undocumented, un-refreshable hand-copy it was before — see
[`spec/BOOTSTRAP_NEW_SOURCES.md`](https://github.com/alex137/BestPractice/blob/precedent-beta-v01/spec/BOOTSTRAP_NEW_SOURCES.md#the-vendored-engine)'s
"The vendored engine". Never hand-edit these; refresh with
`python3 tools/precedent_vendor_engine.py refresh <bestpractice-clone>`.

## Approvers

[`approvers.json`](approvers.json) names who may say yes to a change in this
set (PRACTICE_ENGINE_PLAN.md, "Who the Approvers Are, and How They Get That
Job") — currently Morgan F ([`themorgan`](https://github.com/themorgan)) and
Alex ([`alex137`](https://github.com/alex137)), the set's only two members.
[`CODEOWNERS`](CODEOWNERS) is generated from it with
[`tools/build_codeowners.py`](tools/build_codeowners.py) — never hand-edited;
to add or remove an approver, edit `approvers.json` and rerun that script.
Per the plan, changing the approvers list is itself a change to the set, so
it needs the current approvers' own approval like any other change here.
