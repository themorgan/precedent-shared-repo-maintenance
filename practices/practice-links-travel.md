---
slug:        practice-links-travel
title:       A practice's relative links survive being materialized elsewhere
tier:        on-demand
severity:    default
applies_to:  ["practices/*.md"]
occasion:    "writing or editing a practice in one of my own private sets"
gates:       []
index_clause: "a practice links only what travels with it -- sibling practices and its own check scripts"
checked_by:  tools/checks/check_practice_links_travel.py
defines:     []
status:      active
supersedes:  []
overrides:   null
added:       2026-09-06
approved_by: "Morgan F, in the session that raised it"
---
## Rule
A practice file in one of my private sets uses a relative link only for
something that travels with it into a consuming repo: a **sibling practice**
(`other-slug.md`) or **one of this set's own check scripts**
(`../tools/checks/check_x.py`). Any other path -- `bootstrap/`, `.claude/`,
anything else that exists only in the publishing repo -- keeps its backticked
path and drops the link markup. The prose already says which repo it means.

## Detail
Materialization copies `practices/<slug>.md` and `tools/checks/**` into the
consuming repo and nothing else from the source. Those two shapes are
therefore the complete list of relative link targets that still resolve on
the other side.

`precedent_materialize.py`'s `_rewrite_links` repoints what it can, and for a
**public** source it turns an unplaceable relative link into an absolute
URL -- which is why the universal catalogue can link freely to its own
`spec/` and `templates/` and stay correct downstream. It deliberately refuses
to do that for an individual source, and the refusal is a privacy boundary,
not an oversight: minting
`https://github.com/<owner>/<private repo>/blob/...` into a consuming repo's
tracked tree discloses that repo's existence and location, and a consuming
repo can be public. Its own words: *"a relative link that does not resolve is
a smaller failure than a disclosure that cannot be taken back."*

That trade is right, and it is exactly what makes this a rule for the author
rather than a job for the tooling. Nothing downstream will repair the link,
and nothing downstream should.

Two failure shapes, and the second is worse. A link to `../bootstrap/x`
**404s** in the consumer, which at least a markdown lint can see. A link to
`../.claude/settings.json` **resolves** in the consumer -- to that
consumer's own settings file, rather than the one the sentence is about. No
lint anywhere reports that one; only reading the link as a claim about
*which repo* it assumes will catch it.

## Why
The obvious repair -- make the link absolute -- is the one thing that must
not happen here, and it is the first thing anyone tries. Writing the rule
down as "don't link publisher paths" without the reason invites exactly that
correction on the next pass.

## Story
2026-09-06, three times in one day, all against the same directory.

`fresh-before-write` landed with three `../bootstrap/` links. A consuming
repo's Markdown lint went red on the first push that vendored it: three
BROKEN RELATIVE LINKS, a hard failure. The fix made them absolute -- and
that tripped the consuming repo's `private-repo-scrub`, because it was
precisely the disclosure the rewriter refuses to make. Corrected to bare
backticked paths.

Hours later, `buenos-aires-dates` and `commit-author` landed with seven more
of the same, from a different session that had no way to know.

A sweep then found two more in `claude-web-bootstrap` that had been dead for
weeks and had never been reported once -- because `doc_lint` scopes to
CHANGED files, and nobody had touched that file since. Nine in total.

Three sessions, one day, one mistake, and a gotchas note written after the
first one did not prevent the second or the third. That is the case for a
check rather than more prose (`checkable-gets-checked`).

**Moved to `precedent-team-maintainers` on 2026-09-09**, from `precedent-individual`, in the subject split recorded at Precedent's `TODO.md#split-team-sets-by-subject`. It was written as one person's own default, but the thing that breaks when it is wrong is a repository the whole team works in -- a stale checkout, a practice file whose links die on materialization, a vendored engine nobody refreshes. That is the maintaining team's business, not one person's preference. The copy left behind in the individual set is `status: deduplicated` and points here.

## Install
Checked mechanically by `tools/checks/check_practice_links_travel.py`, which
scans this repo's own `practices/*.md`. In a consuming repo, where
`practices/` holds every source's output, it skips any practice the committed
`MANIFEST.json` attributes to another source -- that text is not this set's
and cannot be fixed here, the same attribution rule
`check_private_repo_scrub.py` uses, and read from the committed manifest
rather than live resolution so a bare CI checkout does not mistake an
unreachable source for an orphan.

Two-direction tested in `tools/checks/tests/test_practice_links_travel.sh`:
a publisher-only path fires, a consumer-shadowed `../.claude/` path fires, a
sibling practice and a check-script link both stay clean, and a practice the
manifest attributes elsewhere is skipped.
