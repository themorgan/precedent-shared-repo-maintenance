---
slug:        private-repo-scrub
title:       Private repo names and specifics get scrubbed before anything vendors or is shared
tier:        on-demand
severity:    blocking
applies_to:  ["**"]
occasion:    "writing content that will vendor or ship into another repo"
gates:       ["merge", "push"]
index_clause: "name a private repo only in general terms in anything that ships elsewhere"
checked_by:  tools/checks/check_private_repo_scrub.py
defines:     []
status:      active
supersedes:  []
overrides:   null
added:       2026-08-31
approved_by: "Morgan F, migrated from RepoPersonalPreferences by the private-set migration session"
---
## Rule
Anything that actually ships into another repo may describe the situation that prompted a rule only in general terms ("a dependent repo," "an earlier project," "a past install"), never by a private repo's real name, its URL, or specifics about its internal layout that would identify it. This doesn't reach content that never leaves the authoring repo -- its own decision records, its own conventions section, commit messages -- which can and should keep naming the real repo, since that is exactly where the full story belongs.

## Detail
**A convention name is not an identifying name.** Precedent's `source-naming` fixes a practice set's name by its level -- every person's individual set is called `precedent-individual`, every team set `precedent-team-<slug>` -- so those bare strings name a convention that every adopter uses, not anybody's repository. What identifies is the owner: `<owner>/precedent-individual` points at one specific person's private set; `precedent-individual` on its own points at nothing. Scrub the owner-qualified form; leave the bare convention name alone, since vendored content is often *required* to use it.

Keep the complete, specific account in the authoring repo's own decision record: the real repo name, what happened, why it mattered. Alongside it, write out the exact scrubbed sentence that actually appears in the vendored text, labeled "Vendor-safe version:" -- so a later session reuses an already-approved scrub instead of re-deriving one from scratch each time.

## Why
Marked blocking for the same reason as scrubbing sensitive characterizations: it guards against a real leak of private information into content that, once vendored, ships to every downstream repo -- not something a personal writing preference should be able to override.

## Story
Found the hard way when a team's own rule text, written to be vendored elsewhere, named one of its private repos directly and linked to it in text that shipped on every future install.

Writing this practice's own `checked_by` found the exact same thing again, in this repo: the install practice's own text named a sibling private set directly, as a worked example. Fixed in the same commit that added the check.

The list then went stale in the other direction, and a consuming repo is what surfaced it. `source-naming` landed upstream on 2026-09-06 and turned `precedent-individual` and `precedent-team-maintainers` from this account's private repo names into the fixed public names every adopter carries. The check still held the bare strings, so a consumer's own gate reported findings against a word the convention obliges it to use -- and, being materialized output, one it could not fix where it was reading it. A blocklist entry has a shelf life: the term it guards can become public without anyone editing the entry.

## Install
Checked mechanically by [`tools/checks/check_private_repo_scrub.py`](../tools/checks/check_private_repo_scrub.py), scope `tree`, over `practices/*.md` specifically -- per `practices/install.md`'s own Rule, that directory is exactly the content a consuming repo vendors verbatim, which is what this rule protects. It scans for a fixed list of this account's two known private sets in their owner-qualified forms only (`themorgan/...` and the full URLs), per the Detail above; it isn't a general "looks like it might be a private repo" heuristic, since nothing distinguishes that reliably, the same reason a real blocklist is specific terms rather than a pattern. It does not check README.md, commit messages, or any future decision record -- those stay local and are explicitly where the Detail section says the full, unscrubbed story belongs. Two-direction tested in [`tools/checks/tests/test_private_repo_scrub.sh`](../tools/checks/tests/test_private_repo_scrub.sh).

