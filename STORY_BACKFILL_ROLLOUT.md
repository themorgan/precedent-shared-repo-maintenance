# Rolling the Story Backfill Out to Other Upgraded Repos

**Who this is for:** a session in any repo that migrated onto Precedent from
an older practice system and may be carrying practices with an empty
`## Story`. Written after doing exactly this in the two private sets, so the
steps are the ones that actually mattered rather than the ones that sounded
right.

## Nothing About This Propagates on Its Own

**Say this first because the opposite is the natural assumption.** Neither a
vendored-engine refresh nor a source sync will fill in a Story anywhere.

- **An engine refresh carries tools, never practices.**
  `precedent_vendor_engine.py` mirrors a fixed list of engine scripts. No
  practice text travels with it, so it cannot fix or spread this.
- **A sync carries practices, but only into consuming repos, and only from
  their declared sources.** That keeps a consumer's materialized copy in step
  with a source that has already been fixed. It does nothing for a source
  that still has empty Stories.
- **The check travels; the fix does not.** A repo consuming this set picks up
  `catalogue-carries-stories` and its check on its next sync — and the check
  is deliberately silent there on practices owned by another source, because
  a Story missing upstream cannot be written downstream.
- **This document does not travel at all.** `precedent_materialize.py` copies
  only `practices/` and `tools/checks/`; a root document like this one stays
  in the repo it was written in.

So **every source repo has to be fixed in itself, by a session, once.** There
is no mechanism that will do it in the background, and treating the next sync
as though it might is how the backlog survives.

## First, Check Whether the Repo Even Has the Problem

Most repos will not. A **consuming** repo materializes its practices from
its sources, so its `practices/` directory is generated output — fixing a
Story there is fixing a copy, and the next sync overwrites it. **Only a
source repo authors practices**, so only a source repo can have this
problem or fix it.

```
python3 - <<'PY'
import pathlib, re
for f in sorted(pathlib.Path('practices').glob('*.md')):
    t = f.read_text()
    fm = re.match(r'---\n(.*?)\n---\n', t, re.S)
    status = re.search(r'^status:\s*(\S+)', fm.group(1), re.M) if fm else None
    if status and status.group(1) != 'active':
        continue
    m = re.search(r'^## Story\n(.*?)(?=\n## |\Z)', t, re.S|re.M)
    if not m or not m.group(1).strip():
        print('EMPTY:', f.name)
PY
```

If that prints nothing, stop — there is nothing to roll out. If the repo has
a `MANIFEST.json` under `practices/`, it is a consuming repo: fix the
source instead, then re-sync.

## Then Find the Original Text, and Do Not Start Without It

**The whole job is transcription, not authorship.** The incidents still
exist in whatever the repo migrated *from* — that is why nothing was
actually lost, only made unreachable. Get that source open before writing a
line. Working from the practice's own Rule and reasoning alone produces
plausible-sounding invented incidents, which is worse than the empty section
it replaces: an empty Story is a visible gap, and a fabricated one is a
false record that will be trusted.

Match old to new by slug. In the sets done so far the old system's rule
headings carried their slug in parentheses, which made the mapping
mechanical and exact.

## Writing Each One

**Where the source records a real incident, the Story is that incident** —
what somebody did, what broke, what it cost, what changed as a result.
Concrete beats general: a placeholder that read as body text and got shown
anyway; a check whose fixed filename list produced a false positive; a
document claiming a count that was already wrong when written.

**Where the source records only reasoning, say so plainly.** A Story reading
"no originating incident was recorded, and this Story does not invent one",
followed by the reasoning that actually justified the rule, is a complete
and honest Story. Roughly half the practices in the sets done so far are
this kind, and blurring the two to make every rule look battle-tested would
destroy the distinction the field exists for.

**Watch for practices that were never migrated at all.** At least one turned
out to have been written natively after the migration and simply never got a
Story — same blank section, different cause, and its Story should say which.
Check the file's `added:` date against the migration date, and its first
commit, before assuming.

**Scrub as you go.** The old system's text will name private repos, real
people, and internal specifics freely, because it lived somewhere that never
shipped. A practice file ships: it materializes into every consuming repo.
Replace a private repo's name with a general description ("a dependent
repo", "an earlier project") and keep the incident intact. Run the repo's
own blocklist over the result rather than trusting a read-through — this is
`private-repo-scrub`, which is `severity: blocking`.

## Close the Gap So It Cannot Reopen

Backfilling alone leaves the same hole open for the next migration. **In a
repo whose engine is current, nothing needs building** — the universal
`catalogue-carries-stories` check ships in `precedent_check.py` and runs
wherever that practice is in force, and (since `binds_publishers`) in any repo
that publishes a `practices/` tree whether the text is vendored there or not.

**A SOURCE set used to have to put the practice in force on itself, and no
longer does — do not copy that step.** The reasoning was real: a source repo
consumes no catalogue, so the universal copy never reaches it, and
`precedent_check.py` gated every check on its practice being in force *in that
repo*. A source set therefore kept its own
`practices/catalogue-carries-stories.md` at `status: active` with
`checked_by: null`, not as a duplicate of the universal rule but as the switch
that turned the universal check on.

**Superseded 2026-09-12 by `binds_publishers`** (BestPractice PR #261). A check
carrying that flag binds any repo that PUBLISHES a practices/ tree, whether or
not the practice text is vendored there, and `catalogue-carries-stories` is one
of the three that carry it. So the switch is in the engine now. **What a source
set has to do is refresh its vendored engine** —
`python3 tools/precedent_vendor_engine.py refresh <bestpractice-clone>` — and
nothing else; a set that re-declares the practice instead gets a second copy
that will drift from universal's, which is what happened here. This set's own
copy was deduplicated on 2026-09-13 once its engine carried the flag, and
`--only catalogue-carries-stories` still reports `1 passed`.

**Why a set-local check was needed, and why it is not any more.** The
universal `cite-the-incident` check does demand a Story, and would have
caught the landing commit — but it lived in `tools/precedent_check.py`,
which was in `CONSUMER_ENGINE_FILES` but **not** in `ENGINE_FILES`. So a
*consuming* repo had it all along and a *source set* never did, which is
exactly backwards from where migrated catalogues land. (Corrected
2026-09-07: an earlier draft said neither list. Wrong about consumers,
right about sources, and asserted from reading one list rather than both.)

**Fixed upstream on 2026-09-07** — it is in both lists now, with the four
optional dependencies a source set lacks guarded so their checks skip by
name instead of erroring. **That fix was necessary and not sufficient**, and
the sentence that stood here saying a refreshed set "does not need a local
copy" was wrong for five days: having the file is not the same as running the
check, and the practice-in-force gate went on skipping it in every source set
until `binds_publishers` landed on 2026-09-12. Both halves are needed, and
both are in an engine refreshed after that date.

Two design points worth knowing about the check — you no longer copy anything,
but they explain what it does and does not cover:

- **Whole-tree, not changed-files.** An authorship-time gate on changed
  files is right for writing one practice and blind to thirty already
  sitting in the tree.
- **Its test builds a synthetic `practices/` fixture rather than cloning the
  repo.** A whole-tree invariant's negative controls need a baseline with no
  other violations in it; a clone's baseline is whatever the committed
  catalogue happens to be, so cloning made the negative controls fail for
  reasons unrelated to the case under test. On the first run, a missing
  fixture file also made a "must fire" case pass because `python3` exited 1
  for *no such file* — assert the fixture exists before trusting any result.

## Order of Operations

Backfill first, then refresh the engine. Turning the check on in a repo that
still has empty Stories puts its gates red immediately, which pressures the next
session into writing filler to clear them — the precise outcome all of this
exists to prevent.
