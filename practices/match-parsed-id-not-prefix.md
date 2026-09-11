---
slug:        match-parsed-id-not-prefix
title:       Match the parsed identifier, not a filename-prefix glob
tier:        on-demand
severity:    default
applies_to:  ["**"]
occasion:    "counting or matching entries by name against other entries that may share a prefix"
gates:       []
index_clause: "When counting how many files or entries share a name (recurrence, a duplicat..."
checked_by:  null
defines:     []
status:      retired
in_force_at: none
supersedes:  []
overrides:   null
added:       2026-09-02
approved_by: "Morgan F, 2026-09-02"
source_practice_number: null
---
## Rule
When counting how many files or entries share a name (recurrence, a duplicate check, a registry lookup), match on each entry's own parsed identifier field, never a filename-prefix or substring glob. A longer, differently-named entry that merely shares the shorter one's prefix (`foo-bar` alongside `foo`) will silently match too, and the miscount is invisible until something adversarial or coincidental actually produces the collision.

## Why
Raised via Precedent's creation pipeline (Stage 1 signal: review-found-defect), promoted at individual level, approved by Morgan F on 2026-09-02.

## Story
**Retired 2026-09-11, by Morgan**, `strength: decided` -- his own words,
*"okay I think we can retire these"*, going further than the proposal on
the table, which was to move them into a subject set for engineering
craft. The same review as
`llm-neutral`, on the same ground: this is a rule about
writing code that matches identifiers, not a rule about maintaining a
repository, and it landed here in the subject split for want of anywhere
better. There is still nowhere better; Morgan retired it rather than open a
set for it.

**Two loose ends this leaves, neither of them invisible:**

The copy in `precedent-individual` is `status: deduplicated` with
`in_force_at:` naming this slug, which no longer resolves in force. That
pointer has to be re-pointed or the copy re-activated, from a session that
can reach that set -- this one could not.

`verify_harness.py` in BestPractice carries a `# practice:
match-parsed-id-not-prefix` comment over the fix this rule came from. The fix
stays; the citation now names a retired rule. The bug itself was real and
remains fixed, and retiring the rule does not un-fix it -- what goes is the
standing instruction not to write the same glob again.

Deep-checking Precedent's phase-5 creation pipeline before phase 6 (per spec/PHASE5_BRIEF.md's own request for adversarial pressure), found that tools/precedent_promote.py's check_recurrence_or_cost() counted same-slug candidate files with cand_dir.glob(f'{slug}-*.md'). That glob also matches a DIFFERENTLY-slugged candidate that merely shares a name prefix: raising a one-time candidate named 'foo' alongside an unrelated candidate named 'foo-bar' made 'foo' silently read as having recurred twice, letting it pass Stage 3's recurrence-or-cost criterion without a real second occurrence ever happening. Fixed by parsing each file's own frontmatter slug field and comparing that, never the filename.

**Moved to `precedent-team-repo-maintenance` on 2026-09-09**, from `precedent-individual`, in the subject split recorded at Precedent's `TODO.md#split-team-sets-by-subject`. It was written as one person's own default, but the thing that breaks when it is wrong is a repository the whole team works in -- a stale checkout, a practice file whose links die on materialization, a vendored engine nobody refreshes. That is the maintaining team's business, not one person's preference. The copy left behind in the individual set is `status: deduplicated` and points here.

## Install
No mechanical check yet -- reached via occasion only, per checkable-gets-checked's own standing rule, a real check should still be attempted before this stays null indefinitely.
