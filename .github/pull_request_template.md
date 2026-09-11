<!-- practices/pr-template-honest-gates.md (BestPractice/Precedent, universal --
     https://github.com/alex137/BestPractice/blob/precedent-beta-v01/practices/pr-template-honest-gates.md):
     fill this in from the actual diff, every time. An unchecked gate, or a
     "not applicable" note, is a normal and expected outcome of a real PR --
     never check a box, or write N/A across every field, just to make the
     form look complete. A checklist filled in mechanically looks like
     verification and isn't; that defeats the entire point of having one.

     This is precedent-team-repo-maintenance' own template, adapted to this
     repo's actual gates -- approver sign-off and CODEOWNERS, not
     RepoPersonalPreferences' old process/ tree or BestPractice's own
     deep-check suite, neither of which this repo has. -->

## What changed

<!-- One or two sentences, plain language. What is different after this merge? -->

## Why

<!-- The intent/critique that prompted it. -->

## Files touched

<!-- One line each: which practices/*.md, tools/, or candidates/ files, and why. -->

## Gates

- [ ] Loader block regenerated and clean: `python3 tools/build_views.py --agents-only --check`
- [ ] Every touched practice's own mechanical check passes (`tools/checks/check_<slug>.py`), where one exists
- [ ] An approver's yes obtained for this change (see `approvers.json`) — required before merge, per this set's own rule (README.md, "Approvers")
- [ ] `CODEOWNERS` still matches `approvers.json` (rerun `tools/build_codeowners.py` if approvers changed)

## Open questions / follow-ups

<!-- Anything deferred. -->
