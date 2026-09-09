---
slug:        fresh-before-write
title:       A session proves its checkout is current before it changes anything
tier:        on-demand
severity:    default
applies_to:  ["**"]
occasion:    "setting up a project I work in, or a session reporting that its checkout is behind"
gates:       []
index_clause: "verify and fast-forward the checkout before the session's first write, never after"
checked_by:  tools/checks/check_fresh_before_write.py
defines:     []
status:      active
supersedes:  []
overrides:   null
added:       2026-09-06
approved_by: "Morgan F, in the session that designed it"
---
## Rule
Every project I work in gets both halves of `bootstrap/freshness-guard.sh` wired into its own `.claude/settings.json`: a `SessionStart` hook that fetches and, where the update is provably lossless, fast-forwards the checkout before anything is read; and a `PreToolUse` hook that re-checks once, on the session's first tool call, and refuses that call when the checkout cannot be vouched for. "Stale" means two independent things and both are checked: behind `origin/<this branch>`, and — the one that actually catches it — missing commits from `origin/<the base branch>`, which a branch that is perfectly in sync with its own remote can still be.

The base branch is passed to the guard explicitly, as its second argument, in the settings file. Never detected from `origin/HEAD`, and never assumed to be `main`.

The automatic half is only ever `git merge --ff-only`, and only when the fetch succeeded, the working tree is clean, and the branch holds nothing `origin` doesn't. Anything else — a dirty tree, a diverged branch, a stale base — is reported and left to me or to a deliberate command, never resolved by the guard picking a side.

## Detail
The two hooks fail in opposite directions, deliberately. `session-start` always exits 0: a hook that can wedge a session over a freshness question is a worse failure than the staleness it guards against, and it is the same fail-gracefully contract [`claude-web-bootstrap`](claude-web-bootstrap.md) already holds its own bootstrap hook to. `pre-write` exits 2 — which is how a `PreToolUse` hook refuses a call and hands its stderr back as the reason — including when it simply could not fetch. A check that could not run is not a check that passed, and this is the one place where saying so out loud is cheap: the block is recoverable, one tool call later.

It is recoverable because a `git` command is never blocked. Every remedy the guard names, and the `git config precedent.freshness.override true` escape hatch, is a git invocation; gating those would leave a session unable to run the only commands that could clear the block. The single exception to failing closed is an unreadable hook payload — with no `jq` and no `python3` the guard cannot recognise a git command either, so blocking there would be that same deadlock, and it exits 0 with a note saying the check was skipped rather than passed.

The `PreToolUse` matcher includes `Bash`. An agent in a mode where file edits go through `cat`, `sed` or `python3` in Bash never touches `Edit` or `Write` at all, and a matcher naming only the edit tools is perfectly blind to every change it makes. This is not write-detection — trying to decide from a command string whether it writes is a losing game — it is a gate that fires once and then costs one file-existence test for the rest of the session.

Two mechanical traps the guard is written around, both learned the expensive way in BestPractice and recorded in its own gotchas log. `git rev-parse <missing-ref>` prints the ref *name* on stdout while exiting non-zero, so every possibly-absent ref goes through `--verify --quiet` instead. And `--depth` is passed only to a clone that is already shallow: handing it to a full clone does not limit a fetch, it truncates the repository into a shallow one — a guard meant to make history reliable, destroying the history every check it runs reads from.

## Why
The failure this exists for is not a branch that has fallen behind its own remote. It is a container that came up on a clone days old, where nothing looks behind because the branch and its remote counterpart are equally out of date, and the work then proceeds against code that has since moved — in the worst recorded case, a session concluding that files merged the week before "did not exist". A `SessionStart` warning was already there for that, and it was not enough twice: it prints before any of the work, sixty lines into startup output, and acting on it is left to whoever reads it. A gate on the first write is the same information at the moment it is impossible to skip.

The fast-forward is the smallest part on purpose. Under its four preconditions it cannot lose anything and cannot conflict, so it is free — but it fires only in the case where the warning was already easy to act on. The base-branch comparison is the one that closes the actual hole, and it stays a report rather than an action, because merging a base into a branch is a real merge and a guard should not be resolving those unasked.

## Story
Raised 2026-09-06, after asking whether BestPractice checked for a stale branch at session start and what it would take to have `precedent-individual` not just check but update itself before touching anything. It did check: [`.claude/hooks/session-start.sh`](https://github.com/alex137/BestPractice/blob/precedent-beta-v01/.claude/hooks/session-start.sh) fetches the current branch and warns, a guard added after a session there found its local branch sharing zero commits with origin, and hardened again after a container came up five days and 207 commits stale with the hook silent because its own fetch had failed. What that guard still could not see was a branch cut from a stale base: it compares `HEAD` against `origin/<the same branch name>` and nothing else, so on a feature branch — which is every working session there — it either compares against a ref that does not exist yet and silently checks nothing, or compares against one that is equally old and reports everything fine. This repo had no check of any kind: no `.claude/` directory at all, so a session working *in* `precedent-individual` ran with nothing watching, while the copy of it that other projects resolve had been quietly `git pull --ff-only`-ing itself at every session start for weeks.

**Moved to `precedent-team-maintainers` on 2026-09-09**, from `precedent-individual`, in the subject split recorded at Precedent's `TODO.md#split-team-sets-by-subject`. It was written as one person's own default, but the thing that breaks when it is wrong is a repository the whole team works in -- a stale checkout, a practice file whose links die on materialization, a vendored engine nobody refreshes. That is the maintaining team's business, not one person's preference. The copy left behind in the individual set is `status: deduplicated` and points here.

## Install
The canonical script and settings snippet live in this repo, at `bootstrap/freshness-guard.sh` and `bootstrap/freshness.snippet.json`. Installing into a project: copy the script into the project as `.claude/hooks/freshness-guard.sh` (executable), merge the snippet's `hooks.SessionStart` and `hooks.PreToolUse` entries into the project's own `.claude/settings.json` (appending to those arrays rather than replacing them), replace `main` in both commands with that project's real base branch, and commit both as tracked files — for the same reason [`claude-web-bootstrap`](claude-web-bootstrap.md)'s own hook is copied rather than referenced from `$HOME`: on a fresh container nothing under `$HOME` exists yet. This repo is the one exception to the copy step: `bootstrap/` is its own tracked directory, so `.claude/settings.json` here calls the canonical script in place rather than keeping a second copy to drift from it.

Validated end-to-end 2026-09-06 against throwaway repositories, one case per branch of the guard: a clean branch behind its remote is fast-forwarded and the commits it moved are printed; a branch in sync with its own remote but missing a commit from `origin/main` is reported by `session-start` and blocked by `pre-write`; a dirty tree and a diverged branch are each blocked rather than resolved; an unreachable remote blocks `pre-write` and still exits 0 from `session-start`; a `git` command passes while a `Write` is blocked in the same state; the fast-forward path blocks exactly once, writing its sentinel first, so the retry proceeds; and the override config passes with a note.

Checked mechanically by [`tools/checks/check_fresh_before_write.py`](../tools/checks/check_fresh_before_write.py), scope `tree`, and the check runs the guard rather than reading it: in a throwaway repository with an unreachable remote it asserts that `session-start` exits 0, that `pre-write` exits 2, and that `pre-write` lets a git command through in that same unverifiable state. It also holds the structural invariants — the script git-tracked executable, both hook entries wired with `Bash` in the `PreToolUse` matcher and the base branch passed as an argument, and no hard reset, rebase or bare `git pull` anywhere in the script's own code. Two-direction tested in [`tools/checks/tests/test_fresh_before_write.sh`](../tools/checks/tests/test_fresh_before_write.sh), one planted violation per invariant.
