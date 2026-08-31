<!-- Last updated: 2026-08-31 20:00:00 (Buenos Aires) by Morgan F, to version 1 -->

# precedent-team-maintainers

The team practice set for [Precedent](https://github.com/alex137/BestPractice/tree/precedent-beta-v01)
— one small group's working conventions, vendored into a project repo the
same way universal practices are, and beating universal by precedence but
losing to a person's own individual set (unless marked `severity:
blocking`) ([PRACTICE_ENGINE_PLAN.md](https://github.com/alex137/BestPractice/blob/precedent-beta-v01/PRACTICE_ENGINE_PLAN.md),
"Precedence, and the One Case Where the Individual Does Not Win").

## What's here

`practices/*.md` — one file per practice, in the format
[spec/PRACTICE_FORMAT.md](https://github.com/alex137/BestPractice/blob/precedent-beta-v01/spec/PRACTICE_FORMAT.md)
documents: 40 practices, migrated from RepoPersonalPreferences' 46 rules
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
information-leak guards that no individual practice should be able to
override by precedence alone.

`rule-links` and `go-merge` (the latter in `precedent-individual`) each
carry `overrides:` against a universal practice they specialize
(`doc-references-are-links`, `merge-authorization-keyword`).
