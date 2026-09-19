# Public Readiness Checklist — precedent-team-writing, precedent-team-repo-maintenance, precedent-team-working-style

**Morgan decided 2026-09-19 to make these three repos public**, excluding
`precedent-individual`. This is the audit that decision's own plan called
for before flipping anything — nothing below has been flipped yet.

## The one finding that matters most

**`precedent-team-repo-maintenance` currently holds two root documents that
name a large number of Morgan's other private GitHub repositories, in the
clear, by their real names and full URLs:**

- **`RPP_REFERENCE_SWEEP_FINDINGS.md`** — a table inventorying roughly 17 of
  Morgan's private repositories by name, several with subjects the names
  themselves disclose (voice/audio work, a book manuscript project, personal
  automation). Written as a sweep record for a 2026-09-14 migration; still
  useful as a record, not useful as a public document.
- **`LEAK_SCRUB_FINDINGS.md`** — names two of those same repositories
  explicitly, and says so on purpose: its own text states real names are
  fine here *because* "content that never leaves the authoring repo." That
  premise is exactly what going public breaks. It was written for
  BestPractice (already public, so the honest framing there is "the history
  already has it, fix forward") — that reasoning does not transfer to a
  repo about to go public **for the first time**.

**Neither file's content should be repeated here.** Both stay exactly where
they are until Morgan decides what happens to them — see "Decision needed"
below.

**No comparable finding in the other two repos.** `precedent-team-writing`
has two practice files (`practices/curly-quotes.md`,
`practices/create-word-doc.md`) whose `approved_by`/`Story` fields name one
private repo, `HavrutaBrainstorm`, as the practice's provenance — normal,
low-severity, and much narrower than the finding above (one name, plus what
its subject implies, not an inventory). `precedent-team-working-style` has
no private-repo mentions anywhere.

## Everything else checked, and clean

- **Blocklists.** All three `leak-blocklist.txt` files are still the
  unedited placeholder template — no real terms were ever entered, and
  `precedent.requireVocabulary` was never turned on for any of them. Not a
  blocker: there was nothing to scrub because the mechanism was never fed
  anything. Worth turning on properly once the visibility question is
  settled, so future commits get the same protection BestPractice gives
  itself.
- **`candidates/`.** Only `precedent-team-repo-maintenance` has one, holding
  a single file (`resolved-issue-note-updates-2026-09-02.md`) whose own
  frontmatter says `status: promoted` — already landed, generic content, no
  private detail. Harmless as content, but a `candidates/` directory is
  exactly the shape the leak gate distrusts on sight in a public tree, so
  it should go regardless of what it currently holds.
- **Secrets.** No hardcoded tokens, keys, or credentials found in any of the
  three repos (workflows, scripts, or docs).
- **Collaborators.** Morgan is the sole collaborator on all three repos —
  nothing to reconsider on access before or after the flip.
- **Everything else root-level** in `precedent-team-repo-maintenance`
  (`CHECK_WORKFLOW_TEMPLATE_FINDINGS.md`, `NOT_BINDING_FINDINGS.md`,
  `STORY_BACKFILL_ROLLOUT.md`) and all of `precedent-team-working-style`'s
  and `precedent-team-writing`'s own docs and `practices/*.md` read clean —
  generic engine/process content, no private specifics.

## The procedural point that matters as much as the content

**Fixing the two flagged files forward, in a new commit, is not enough by
itself.** These repos have never been public. Their full commit history —
every version of every file that was ever committed — becomes reachable
the moment GitHub's visibility flips, not just the current tree. A forward
commit that removes or redacts the two files leaves the sensitive versions
sitting in history, one click away in the commit log, for anyone who looks
after the flip.

That is a different situation from `LEAK_SCRUB_FINDINGS.md`'s own case
(BestPractice), where `no-rewrite-for-warnings` correctly says fix forward
— there, the repo is already public, other clones and links already depend
on its commit SHAs, and rewriting buys nothing back. Neither condition
holds here: nobody outside Morgan has ever had reason to clone or link a
commit SHA in these three repos, so a history rewrite costs nothing real
and closes the actual gap. **The right sequence is: scrub or remove the
files' history (not just their current content) before the repo ever goes
public, not after** — a targeted history rewrite (e.g. `git filter-repo`
on just the two paths) rather than an ordinary commit, since an ordinary
commit is the thing that would leave the real exposure in place while
looking finished.

## Decision needed (Morgan's call, not a mechanical one)

1. **What happens to `RPP_REFERENCE_SWEEP_FINDINGS.md` and
   `LEAK_SCRUB_FINDINGS.md`.** Options: delete outright (both record
   already-applied or informational-only findings that never landed
   upstream anyway, per their own text); move them to `precedent-individual`
   if the record is worth keeping somewhere that stays private; or rewrite
   them generically in place. Whichever is chosen, it needs the history
   rewrite above, not just a forward commit.
2. **Whether the two `HavrutaBrainstorm` mentions in
   `precedent-team-writing` are fine to leave.** Low severity, genuine
   provenance information, but it's a real private repo name and the call
   on comfort level is Morgan's, not mine.

## Once content and history are settled, the mechanical sequence

1. Delete the stale `candidates/` entry in `precedent-team-repo-maintenance`.
2. Set `"visibility": "public"` in each of the three repos' own
   `precedent-source.json`.
3. Flip each repo's actual GitHub visibility (Settings → Danger Zone) —
   the one step that is genuinely irreversible in effect (anyone can clone
   the instant it flips), so this is the step to do last, deliberately, and
   one repo at a time rather than all three at once.

Nothing above has been done except the analysis itself. No file has been
edited, no history rewritten, no visibility changed.
