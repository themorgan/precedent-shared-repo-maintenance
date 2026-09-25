# `precedent-check.yml` — Where the Sets' Copy Beats the Upstream Template

**This file is output for a later BestPractice-rooted session**, not a
practice and not a decision. It records four places where the copy of
`precedent-check.yml` now installed in this set is stronger than
[`templates/github-actions/precedent-check.yml.template`](https://github.com/alex137/BestPractice/blob/staging/templates/github-actions/precedent-check.yml.template)
upstream (added there by BestPractice PR #278), so the template can learn
them instead of overwriting them at the next bootstrap.

**Nothing here has been applied upstream.** BestPractice is a different
owner, and a session rooted in a practice set can never gain push access
there — so this is written to be read and re-judged, not pasted.

**Date:** 2026-09-13. **Template read at:** `alex137/BestPractice`
`precedent-beta-v01`, at the merge commit `21b14ca`.

## Why This File Exists At All

The template is the copy that gets installed into every future set, so
convergence normally runs set → template. It does not run that way here.
The sets' copy was written first, on 2026-09-13, against a real repository
and a real failing run; the template was genericized from a different
starting point the same day. Four of the differences are not style — each
one is a way the template can report success on a run that verified less
than it claims. They are listed worst-first.

All four sets carry the same copy, byte-identical
(sha256 `1df3d91f148a7728485a…`), so a template that learns these does not
have to reconcile four variants.

## 1. Refusal 2 Greps For a String Where It Should Inspect the Registry

**Template:**

```
if ! grep -q 'binds_publishers' tools/precedent_check.py; then
```

**Sets:** import the vendored module and ask the check registry itself —

```
flagged = sorted(s for s, c in pc.CHECKS.items() if c.get('binds_publishers'))
if not flagged:
    sys.exit('REFUSING: ...')
print(f'engine carries binds_publishers on {len(flagged)} check(s): ' + ', '.join(flagged))
```

A substring grep passes on any engine that merely *mentions* the string —
in a comment, a docstring, or, most likely of all, in the text of a future
refusal message about `binds_publishers` itself. It also passes on an
engine where the flag is defined but no check actually carries it, which is
precisely the state the refusal exists to catch.

The registry form cannot be fooled that way, and it makes the green case
say what it verified: measured in this set, it prints
`engine carries binds_publishers on 3 check(s): catalogue-carries-stories,
generated-artifact-provenance, practice-links-travel`. The grep form's
green case prints nothing at all.

Second-order gain: the registry form imports the engine, so an engine that
cannot be imported is refused *here*, with its own message naming the
exception, rather than surfacing as a confusing failure at the run step.

## 2. There Is No Refusal For a Missing `practices/`

The sets carry a fourth guard the template has no equivalent of:

```
if [ ! -d practices ]; then
  echo "No practices/ directory -- this repo publishes no practice files," \
       "so the publisher checks have nothing to bind. Remove this workflow." >&2
  exit 1
fi
```

The template's REFUSAL 3 (`0 passed`) does eventually catch this case, but
only after running the whole suite, and it reports it as "zero checks
passed" — a symptom three steps downstream of the cause. The guard above
names the cause before anything runs.

## 3. Refusal 3 Cannot See a Summary Line That Never Appeared

**Template:**

```
if printf '%s' "$out" | grep -qE 'precedent_check: 0 passed'; then
```

This asks only whether the summary line says zero. It is silent on the case
where **there is no summary line at all** — an engine that dies after
printing its per-check lines but still exits 0, a truncated pipe, or a
future change to the summary's wording. In every one of those the grep
finds no match, concludes nothing is wrong, and the workflow exits green
having checked nothing. That is the exact failure mode the whole file is
built to refuse, reachable through the refusal meant to be its backstop.

**Sets:** require the line to exist first, then read the count out of it —

```
summary="$(grep -E '^precedent_check: [0-9]+ passed' check-output.txt | tail -1)"
if [ -z "$summary" ]; then
  echo "No precedent_check summary line in the output. The run did not" \
       "finish the way this workflow expects; read the log above." >&2
  exit 1
fi
passed="$(printf '%s' "$summary" | sed -E 's/^precedent_check: ([0-9]+) passed.*/\1/')"
if [ "$passed" -eq 0 ]; then
```

"I could not find the line that tells me what happened" is treated as a
refusal rather than as an absence of bad news. Anchoring the pattern at
`^` also stops a per-check line or a quoted message elsewhere in the output
from being mistaken for the summary.

## 4. All Three Refusals Share One Step, So a Red X Names Nothing

The template folds refusals 1 and 2, the suite run, and refusal 3 into a
single `run:` block called *Run the Precedent checks*. The sets split them
into four named steps: *Refuse if this repo is not a source set carrying
the engine*, *Refuse if the vendored engine predates binds_publishers*,
*Run every check that binds this repo*, *Refuse a run that checked
nothing*.

The Actions UI shows step names on the summary page and log bodies only
when opened. Split, a failure is legible without opening anything, which
matters most for the refusals — they fire on people who have not read this
file and will not guess from a red check mark that their engine is stale.

The split is also what the `tee check-output.txt` in the sets' run step is
for: it hands the output to the next step. A template that adopts the split
needs that line; one that does not, does not.

## Deliberate Divergences — Do Not "Fix" These Back

- **The header.** The sets' copy cites this repository's own incident
  (two workflows each calling one check's function, and the moment deleting
  one of them silently dropped a gate); the template cites the generic
  shape. That is `cite-the-incident` working as intended in both places,
  and the two should stay different.
- **`--disable-pip-version-check`** on the pip install, in the sets only.
  Noise reduction, nothing more.
- **Job `name:`.** *Every Precedent check that binds this repo* here,
  *precedent_check.py (whole suite)* upstream.
- **Refusal 1's message** mentions `GITHUB_ACTIONS.md`'s Limits section
  upstream and does not here, because this repo has no such file. A set
  that vendors one should take the upstream wording.

## One Upstream Claim, Confirmed By Measurement

The template's PyYAML comment says the vendored *engine* needs no
third-party module, and that the dependency exists for a check script a
practice names in `checked_by:`. **True in this set as measured on
2026-09-13:** the only `import yaml` anywhere under `tools/` is
`tools/checks/check_light_check.py:39`, which is a `checked_by:` script.
The rationale is correct and worth keeping in the template as written.
