# Repository notes for agents

This repo IS `precedent-team-maintainers` — the **team** source for
[Precedent](https://github.com/alex137/BestPractice/tree/precedent-beta-v01)'s
maintaining team (Morgan and Alex). See [README.md](README.md) for what's
here and how the practices in [practices/](practices/) got here.

<!-- BEGIN GENERATED: precedent-loader -->

<!-- Regenerate with: python3 tools/build_views.py -- do not hand-edit this block, tools/verify_harness.py's regeneration check fails on drift. -->

## Resident block (~248 of 2000 token budget, 3 of 39 practices)

**bold-key-phrases.** People don't read; they skim, and bolding makes skimming easy. Bold the key phrases in a document by default, without being asked, scaling with length -- a long paragraph or document is where a skimmer most needs a spine to follow, a short note usually needs little or none.

**nonblocking-questions.** Once a question is worth asking at all, asking is not itself a stopping point. A session holding a queue of work and an open question doesn't go idle waiting for the answer -- it keeps going on everything the answer doesn't touch.

**small-calls.** Default to continuing, not asking. When a judgment call is needed to keep the work moving -- filling in a default, picking between two reasonable implementations, resolving an ambiguity that doesn't change the shape of what gets delivered -- make the call and note it, rather than stopping to ask first. Reserve stopping and asking for calls that are genuinely big: hard or costly to undo, change what gets delivered or to whom, spend real money, touch credentials or production, or are the kind of toss-up where two reasonable people would clearly land in different places.

## Occasion index

```
When a README or other key file just gained an operational instruction:
  mirror-into-agents — an agent-relevant instruction lands in both AGENTS.md and its human home
When a commit fixes, closes, or resolves something a document names in prose as a known, open issue:
  resolved-issue-note-updates — When a commit fixes a bug, closes a gap, or resolves a limitation that some ...
When a new rule is proposed and its scope isn't obvious:
  rule-scope-ask — unclear if a new rule is repo-wide or one document? ask once
When a numbered list's entries are durable content likely to be cited by position:
  durable-list-anchors — anchor and slug each entry of a durable numbered list, not just its number
When a paragraph just got a substantial edit, or the piece is done:
  trim-prose — trim a paragraph right after editing it, and before calling it done
When a project repo vendors this team's own practice set, and it has moved:
  pack-sync — the team-set sync is the universal sync's sibling, against a private repo
When a session starts in a repo that vendors a universal or team set:
  drift-notice — check source freshness at session start; raise it right away, not later
When a session-start freshness check against a private source can't be reached:
  fresh-check-escalation — tell "could not verify" apart from "confirmed fresh"; verify directly
When a standing constraint on one file gets stated a second time:
  doc-recipe — present-tense rules for one file, in doc-recipes/<name>.recipe.md
When about to commit:
  light-check — a cheap mechanical audit runs before every commit, not just merges
When about to commit a document that characterizes a real, identifiable person:
  sensitive-characterization-scrub — soften or ask before committing a blunt description of a real person
When about to format connected prose as bullet points:
  list-restraint — don't reformat connected reasoning as bullet fragments
When about to push after a thread of work:
  todo-gate — add missed ideas, check off finished ones, before every push
When adding a new rule to a maintained rules document:
  new-rule-placement — place a new rule by subject, slug it, renumber, mirror, re-check
When adding or reviewing a team-set rule:
  no-duplication — a rule that only restates universal gets dropped
When an unattended scheduled job hits something blocking its normal work:
  automation-issues — a blocked scheduled job opens or updates an issue, not just a log line
When bringing a vendored practice layer into a new or existing repo:
  install — vendor the tree, weave conventions into AGENTS.md, wire checks and manifest
When building or setting up a system that talks to an LLM:
  llm-neutral — build LLM integrations provider-neutral; assume an OpenRouter token
When citing support for a claim in a formal document:
  brainstorm-citations — cite a formal document for support, never a raw brainstorm entry
When committing anything:
  session-trailer — a Session: <url> trailer on every commit
When creating a file a later regeneration will overwrite:
  derived-file-marker — a regenerated file's header names its source, recipe, and command
When drafting or reviewing prose meant to persuade or be judged:
  push-back — argue a real counter-case before building on a stated stance
When drafting or revising a list, or a document with list-like sections:
  list-item-parity — keep list items comparable in length; default to the shorter side
When installing a vendored practice layer that could check in upstream:
  blank-blocklist — leave a check-in blocklist blank at install; don't ask, don't remind
When leaving a placeholder or fill-in-later note mid-draft:
  draft-marker — wrap a draft placeholder in ➡️ TEXT ⬅️, bold and all caps
When mentioning a repo file in a chat reply, PR description, or commit message:
  file-mention-links — every file mention in chat or PR/commit text is a live GitHub link
When naming a git branch in a document, reply, or status update:
  branch-links — link every git branch mentioned to its tree view
When naming anything that has a destination, in a document or a reply:
  rule-links — link anything mentioned that has a destination, on first use
When reporting a check's outcome that includes a known pre-existing backlog:
  quiet-checks — "checks passed" is fine; don't re-explain the same old backlog
When reviewing a draft's balance before calling it done:
  proportional-emphasis — give a point space matching its importance, not its drafting mood
When root has accumulated three or more deliverable-content documents:
  content-subdirs — group deliverable content under a named subdirectory -- a recommendation
When setting up a new repo, or installing into an existing one:
  default-branch — check or set the default branch to main, once, at install
When writing a sentence that cites an exact, changeable count:
  no-stale-counts — drop a count that will go stale; say "several", not the number
When writing code that depends on something outside its own control:
  fail-gracefully — degrade on a missing config, file, network call, or credential
When writing content that will vendor or ship into another repo:
  private-repo-scrub — name a private repo only in general terms in anything that ships elsewhere
When writing or reviewing a document's headers:
  header-caps — one capitalization schema per document; default to headline style
```

## Standing instruction

Before starting work of a kind named in the occasion index above, run `python3 tools/precedent_show.py SLUG` for each listed slug to load its Rule. When editing a file, `python3 tools/precedent_paths.py FILE` prints any on-demand practice whose `applies_to` matches it, without needing the index at all. At a named moment — merging, reviewing, pushing, ending a turn — run `python3 tools/precedent_gate.py merge|review|push|reply`: some practices fire at a moment rather than in a file, and no path glob reaches those.

<!-- END GENERATED -->

## Working in this repo

- **Practices are in [practices/](practices/)**, one file per practice, in
  the format [`spec/PRACTICE_FORMAT.md`](https://github.com/alex137/BestPractice/blob/precedent-beta-v01/spec/PRACTICE_FORMAT.md)
  documents.
- **The loader block above is generated** — regenerate with
  `python3 tools/build_views.py --agents-only`; hand-editing it is pointless,
  the next regeneration overwrites it. `--agents-only` skips `MAP.md`/
  `GLOSSARY.md` rendering, which assumes BestPractice's own repo structure
  and isn't meaningful here.
- **Changes to this set need an approver's yes** — see
  [`approvers.json`](approvers.json) and the README's "Approvers" section.
