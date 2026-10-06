---
slug:        light-check
title:       A light check runs on every commit path
tier:        on-demand
severity:    default
applies_to:  ["**"]
occasion:    "about to commit"
gates:       ["push"]
index_clause: "a cheap mechanical audit runs before every commit, not just merges"
index_required: true
checked_by:  tools/checks/check_light_check.py
defines:     []
status:      deduplicated
in_force_at: two-check-levels
supersedes:  []
overrides:   null
added:       2026-08-31
approved_by: "Morgan F, migrated from RepoPersonalPreferences by the private-set migration session; revised 2026-09-05, Morgan F, to document the materialized-check-has-a-source extension and its CI-resolution gotcha"
---
**Deduplicated 2026-10-06.** This rule lives in universal's
[two-check-levels](https://github.com/alex137/BestPractice/blob/staging/practices/two-check-levels.md),
which folded it in on 2026-09-28; this copy is history, kept so the set can
retire without losing a rule.

## Rule
A repo maintains one cheap, mechanical audit script that runs before every commit: conflict markers, invalid JSON/YAML syntax, secret-shaped strings (an Amazon Web Services (AWS)-style key ID, a Privacy-Enhanced Mail (PEM) private-key header, a token), and broken relative doc links, at minimum. Run it yourself before every commit, and wire it into the repo's commit or push gate (a local hook) so it binds even when a session forgets. Add a CI job only where changes arrive that no session checked, such as a consuming repo taking contributions from forks; a practice source runs none (universal [`source-sets-run-no-ci`](https://github.com/alex137/BestPractice/blob/staging/practices/source-sets-run-no-ci.md)).

## Detail
Where this shared set (or any vendored practice set) is installed into a project repo, extend the same check to verify the install is real, not a plain copy: the tracking manifest exists, parses, has at least one entry, and every entry's recorded path exists on disk. A style-oriented linter (accidental strikethrough, unlinked references, unglossed acronyms) is a separate, complementary tool -- this is the broader, cheaper net for "something obviously went wrong" that isn't a style question.

A second extension worth adding, if the install uses `precedent_materialize.py`: verify every materialized `tools/checks/check_*.py` actually traces back to one of its declared sources, catching a script hand-dropped straight into that directory (materialize's own rewrite-from-scratch output) instead of into its true source's own `tools/checks/` -- it would otherwise sit there looking fine until the next sync silently deletes it. Build this against the sync tool's own **committed** provenance record (`MANIFEST.json`'s `checks` list, for `precedent_materialize.py`), not by re-resolving live sources at check time: a private shared or individual source only resolves via a live sibling clone or a personal user-level config, neither of which exists in a bare CI checkout, so a version that treats "this source didn't resolve here" as "this file is orphaned" will flag every legitimately-sourced file the first time it ever runs in CI. Real incident, 2026-09-05, in a repo that installs this set: a first attempt at exactly this extension resolved sources live and failed 14 files -- every one legitimately sourced from a shared or individual set neither reachable from a GitHub Actions checkout -- on the very next push after the check was added. Fixed the same day by attributing through the committed manifest instead: a file with no manifest record at all is the real orphan (fails unconditionally); a recorded file whose source isn't reachable here is unverifiable, not orphaned (skipped, never failed); only a recorded file whose source *is* reachable gets its bytes actually checked.

## Why
A required CI check catches an install-time or commit-time mistake the moment it happens, rather than relying on every session remembering a runbook step.

## Story
Writing this practice's own checked_by turned it into the actual audit script it describes: run against this repo's own tree, it found three practice files (`deep-check`, `header-caps`, `push-back`) with a `title:` frontmatter value containing an unquoted colon -- invalid YAML that a strict parser rejects. Fixed in the same commit that added the check.

**Folded into the universal `two-check-levels` on 2026-09-28**, on Morgan's approval of a session's recommendation to merge the overlap (strength: assented): its Detail now carries this practice's minimum audit list, the CI wiring, the install-is-real extension, and the 2026-09-05 lesson about attributing materialized checks through the committed manifest rather than live resolution. **This copy stays active because it also carries this set's own implementation of the audit**, [`tools/checks/check_light_check.py`](../tools/checks/check_light_check.py), which did not move: universal already has its own fast level (BestPractice's [`tools/doc_lint.py`](https://github.com/alex137/BestPractice/blob/staging/tools/doc_lint.py)), and a deduplicated practice claims no check, so withdrawing this copy would stop the audit reaching consumers. Deduplicate it into `two-check-levels` once the check has a home or is retired.

## Install
[`tools/checks/check_light_check.py`](../tools/checks/check_light_check.py) IS the audit this practice describes, run against this repo, scope `tree`: conflict markers, invalid JSON/YAML (including every practice file's own frontmatter block), secret-shaped strings (an AWS-style key ID, a PEM private-key header, a GitHub or Slack token), and broken relative markdown links. The Detail section's second half -- verifying an *installed* copy's tracking manifest -- doesn't apply here, since this repo is the source of the set, not an installer of one; a repo that vendors this set would extend the check with that piece itself. Two-direction tested in [`tools/checks/tests/test_light_check.sh`](../tools/checks/tests/test_light_check.sh), one planted violation per audit.

