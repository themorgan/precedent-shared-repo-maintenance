# Team Repo Visibility and Naming — Analysis, Not Yet Decided

**This file is a recommendation, not a decision.** Morgan asked for thoughts
on two changes to the three team sets — making them public, and renaming
`precedent-team-*` to `precedent-shared-*` — and asked for them written up.
Nothing below has been acted on; both are still his call.

**Date:** 2026-09-19.
**Scope:** `precedent-team-writing`, `precedent-team-repo-maintenance` (this
repo), `precedent-team-working-style` — all three currently single-owner
private repos under `themorgan`, no GitHub Team object involved.

## Question 1: Making the three repos public

**Current state.** All three are private on GitHub, and each one's own
`precedent-source.json` declares `"visibility": "private"`. Each README's
bootstrap-template language says outright: *"this is [repo]'s own private
space... Everyone on the team can read it; nobody else can."* Each carries
its own `leak-blocklist.txt` — the private-term list Precedent's leak gate
checks a **public** tree against.

That machinery exists because the layered design (public universal set,
private team/individual sets) depends on the private layer being a place
where specifics can be named before they're generalized upward — a staging
ground, not a mirror of the public one.

**Concrete finding.** This repo's own `candidates/` directory currently
holds a real draft file
(`candidates/resolved-issue-note-updates-2026-09-02.md`). A `candidates/`
directory is exactly the shape `tools/leak_gate.py` (upstream, BestPractice)
refuses to find in a **public** tree, because it "may carry private
context" — unreviewed drafts. That's not a hypothetical risk from making
this repo public; it's sitting there right now.

**Recommendation: don't flip visibility yet.** If the decision is to go
public, do it in this order:

1. Sweep every one of the three repos' `candidates/` directories, any
   findings-style or TODO-shaped documents, and the blocklist terms
   themselves, for content that was written on the assumption of privacy.
2. Only then set `"visibility": "public"` in each repo's own
   `precedent-source.json` — that field is what tells the leak gate to stop
   requiring scrubbing for that source.
3. Separately decide whether GitHub's own repo visibility should also
   change. The manifest field and GitHub's actual private/public setting
   are two different switches: flipping only the manifest leaves the repo
   exposed while the gate still believes it's covered; flipping only GitHub
   leaves the gate fighting content that's already world-readable. Both
   need to move together, in that order (manifest reflects an audited
   state; GitHub visibility follows it).

**Worth asking directly, independent of the mechanics:** is the goal "the
world can read this" or "a couple more specific people can read this"? The
second is adding collaborators to a repo that stays private, which is a
different and lower-cost move than publishing it.

## Question 2: Renaming precedent-team-\* to precedent-shared-\*

**This one is now mechanically safe**, and it wasn't always. Until
2026-09-18, four separate mechanisms parsed the `precedent-team-` prefix
out of a repo's name: level inference, the clone URL, the leak gate's
recognition of a vendored private set, and the attribution key. That
coupling is exactly what the `source-naming` practice retired that day
(Morgan approved it, relayed by Alex): level, name, and visibility are now
all read from each repo's own `precedent-source.json`, never parsed from
the repository name. **All three repos already carry `"level": "shared"`
internally** — the level itself was renamed from `team` to `shared` on
2026-09-18. Only the GitHub repository names still say "team."

Per `source-naming`'s own text: *"Nothing in the engine keys on a
repository's name... The repository may be called anything."*

**There's already a working precedent for the mechanics of a rename**:
`precedent-team-maintainers` → `precedent-team-repo-maintenance`
(2026-09-11, this repo's own history). GitHub's redirect kept old links
resolving, and the lineage was recorded once, in the README, rather than
scattered across every document that mentioned the old name.

**Two loose ends found while checking this, independent of what gets
decided:**

- `tools/precedent_source_credentials.py:421` (BestPractice,
  `precedent-beta-v01`) still checks `if src.get('level') != 'team':`
  literally. BestPractice's own `precedent.json` already declares all three
  sources as `"level": "shared"`, so this specific function currently skips
  all three and silently stops flagging a missing or broken shared source's
  `practices/` directory. This is a leftover gap from the 2026-09-18
  migration being incomplete in that one file, and needs fixing regardless
  of whether any repo gets renamed.
- `tools/checks/check_private_repo_scrub.py`'s `PRIVATE_TERMS` list (in
  this repo) hardcodes `themorgan/precedent-team-repo-maintenance` by exact
  owner-qualified name. The script's own header already says to update that
  list on a rename, so this is a known, bounded step rather than a surprise
  — but it has to happen in the same change as the rename, not after.

**Recommendation:** rename is low-risk and mechanically supported now — the
only real cost is doing the reference rewrite in one pass, the same way the
2026-09-11 rename did, so nothing is left pointing at a stale name outside
of GitHub's own redirect.

## Bottom line

- **Rename:** safe to do whenever Morgan wants it; the engine no longer
  depends on the old shape, and the process is already precedented.
- **Public:** hold off until the `candidates/` directories (and anything
  like them) across all three repos have been swept, and until it's clear
  whether "public" means GitHub-public or "more collaborators, still
  private."
