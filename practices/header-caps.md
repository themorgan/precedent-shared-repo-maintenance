---
slug:        header-caps
title:       "Header capitalization: pick one consistent schema, NY Times headline style by default"
tier:        on-demand
severity:    default
applies_to:  ["**/*.md"]
occasion:    "writing or reviewing a document's headers"
gates:       []
index_clause: "one capitalization schema per document; default to headline style"
checked_by:  null
defines:     []
status:      deduplicated
in_force_at: headline-capitalization
supersedes:  []
overrides:   null
added:       2026-08-31
approved_by: "Morgan F, migrated from RepoPersonalPreferences by the private-set migration session; retired by Morgan F"
---
## Rule
Headers and subheaders at the same rank in a document must all follow one capitalization style, never mixed; sibling headers at the same rank also share the same heading level. Absent a documented reason to pick something else, use NY Times headline-style capitalization -- capitalize principal words (nouns, verbs, adjectives, adverbs, pronouns), lowercase minor words (articles, short prepositions, coordinating conjunctions) except at the very start or end of the header -- consistently across every header and subheader in the document.

## Detail
A repo is free to choose a different scheme and document that choice inline, the same way it documents any other repo-wide convention. A document whose sections mix capitalization schemes, or mix heading levels, at the same rank is the failure this rule exists to catch.

## Why
Two different failures share one fix, which is why the rule states a consistency requirement before it states a default.

**Mixed capitalization at the same rank is the failure**, not any particular scheme. A document whose sections alternate between headline and sentence case reads as unmaintained regardless of which one a reader would have preferred, because the inconsistency itself is the signal.

The named default exists only so the question does not have to be re-decided per document — a repo is explicitly free to choose otherwise and document that choice inline, the same way it documents any other convention. What it is not free to do is leave the choice implicit, since an implicit choice is what drifts.

## Story
Retired on 2026-09-06 as a duplicate. BestPractice landed
[`headline-capitalization`](https://github.com/alex137/BestPractice/blob/precedent-beta-v01/practices/headline-capitalization.md)
at the universal level the same day, with the schema itself defined once in
[tools/title_case.py](https://github.com/alex137/BestPractice/blob/precedent-beta-v01/tools/title_case.py)
rather than restated in prose. A repo consuming both this team source and
the universal source would otherwise carry two practices asking for the same
NY Times headline capitalization, which is exactly what
[`no-duplication`](no-duplication.md) says to drop. Retired here rather than
moved, per
[spec/MOVING_PRACTICES.md](https://github.com/alex137/BestPractice/blob/precedent-beta-v01/spec/MOVING_PRACTICES.md)'s
step 2 -- the universal practice had already landed, so there was no gap.
`checked_by` is now null and `tools/checks/check_header_caps.py` and its
test are removed, since `code-cites-practice` (BestPractice universal)
forbids a `practice:` citation naming a retired practice.

Where this practice's two other clauses ended up (revised 2026-09-06,
after BestPractice moved twice the same day -- the first version of this
note is already wrong and is not preserved, since a Story records what
happened, not what a session believed at lunchtime):

- **Heading-level consistency** -- "sibling headers at the same rank also
  share the same heading level." Rebuilt at the universal level as
  [`heading-outline`](https://github.com/alex137/BestPractice/blob/precedent-beta-v01/practices/heading-outline.md),
  scoped to `**/*.md` and mechanically checked, but narrowed to the half
  that is decidable: no heading is more than one level deeper than the one
  before it. "Siblings share a rank" was dropped on purpose -- a section
  can legitimately nest deeper than the one before it, and no tool can tell
  that from a section demoted by accident. "The first heading is an H1" was
  measured against a real corpus and rejected. This set is already clean
  against it: 219 headings across 45 tracked files, zero skips.
- **Scope.** This practice applied to `**/*.md`. `headline-capitalization`
  shipped covering `documentation/` only and was rescoped the same day to
  `**/*.md` stated as an *exclusion* -- everything is outward-facing unless
  named internal in `title_case.py`'s `INTERNAL_DIRS`/`INTERNAL_FILES`. So
  the capitalization rule now reaches wider than this practice did for
  published content, and deliberately does not reach internal working files
  at all: practice files, specs, briefs, `AGENTS.md`, `TODO.md`. That is
  Morgan's ruling of 2026-09-06 -- how a heading is styled matters where
  strangers read it and nowhere else, and sentence case in a spec is
  correct and is never to be "fixed". This practice's own demand for one
  consistent schema *everywhere*, internal files included, is therefore not
  carried forward, and that is a decision rather than a gap.

Also dropped, deliberately: this practice's "a repo is free to choose a
different scheme and document that choice inline" escape hatch. The
universal practice mandates one schema applied by tool and offers no
per-repo alternative -- a tightening, not an omission.

## Install
Nothing to install: this practice is retired. Its rule is carried at the
universal level by
[`headline-capitalization`](https://github.com/alex137/BestPractice/blob/precedent-beta-v01/practices/headline-capitalization.md),
whose own Install section describes running
[tools/title_case.py](https://github.com/alex137/BestPractice/blob/precedent-beta-v01/tools/title_case.py).

While active, this practice was checked mechanically but only half of it, by
a `check_header_caps.py` (scope `tree`, over tracked markdown files) that
verified the rule's first, unambiguous sentence -- headers at the same rank
in one document never mix capitalization styles. It did this without a
minor-word dictionary: if the same word (excluding each header's own
first/last word) appeared capitalized one way in one same-rank header and
differently in another, that word was itself direct evidence of a mixed
scheme. What it never checked was that the default scheme, absent a
documented reason otherwise, is specifically NY Times headline style --
telling "principal word" from "minor word" has enough real edge cases (a
short verb doing the sentence's main work, a preposition used adjectivally)
that a fixed word list would misclassify often enough to not actually
enforce the rule. The universal practice solves that half differently, by
making one script the definition rather than the enforcement of a rule
written in prose.

The check and its two-direction test were removed with this retirement,
since `code-cites-practice` (BestPractice universal) forbids a `practice:`
citation in a tool naming a practice that is no longer active. Recovering
the same-rank check, if the gap this Story names is closed, means restoring
those two files from this commit's parent -- not rewriting them.
