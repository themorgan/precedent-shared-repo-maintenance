---
slug:        practice-set-engine-refresh
title:       A practice-set repo of mine refreshes its own vendored engine
tier:        on-demand
severity:    default
applies_to:  [".github/workflows/**", "tools/ENGINE_MANIFEST.json"]
occasion:    "creating a practice-set repo of mine, or finding its vendored engine stale"
gates:       []
index_clause: "my own practice-set repos carry a weekly engine-refresh workflow"
checked_by:  null
defines:     []
status:      active
supersedes:  []
overrides:   null
added:       2026-09-06
approved_by: "Morgan F, 2026-09-06"
---
## Rule
A practice-set repo I maintain carries `.github/workflows/engine-refresh.yml`: a weekly, also-on-demand job that clones Precedent's `precedent-beta-v01`, refreshes the vendored engine under `tools/`, regenerates the views that engine produces, and -- only if that produced a diff -- opens a pull request for me to land. It never merges. This is my preference for my own repositories, not a default I ask anyone else to adopt: Precedent's own source templates deliberately ship no scheduled workflow, and a set that is not mine gets this only if its owner wants it.

## Detail
Four properties, each one earned rather than decorative:

1. **Refresh and regenerate land in one commit.** A refreshed generator whose views have not been re-run leaves the repo's committed `AGENTS.md` describing the *old* engine's output, which the repo's own `build_views.py --check` then fails on. Bumping the engine without re-running it produces a red repo, not a current one.

2. **The diff is the signal.** `git status --porcelain` empty means the engine was already current. Never parse a notice string for this -- a message can change wording upstream and silently stop matching.

3. **The notification never depends on a GitHub setting.** Opening a pull request from Actions needs *Allow GitHub Actions to create and approve pull requests*, which is off by default and which an organization or enterprise can withhold outright. So the job tries the pull request, and on **that specific permission failure** opens an issue instead -- `issues: write` is in the default token and nothing gates it. The issue carries a `compare/<base>...<branch>?expand=1` link, so I open the pull request myself in one click; the work is already pushed. The setting only ever bought *who presses the button*.

4. **One issue, and it closes itself.** The fallback reuses a single issue tagged `precedent-engine-stale` rather than opening one a week, and a later run that finds the engine current closes it. An open issue therefore means *stale right now*, not *was stale once*. Without this the channel becomes litter inside a month and gets muted, which is the same outcome as never reporting at all.

The fallback fires **only** on the permission signature. Any other failure -- branch protection, a moved base branch, a network blip -- still fails the job loudly. A fallback that swallowed every error would go on reporting the wrong problem forever.

## Why
A source set vendors Precedent's engine as tracked files, and refreshing it needs a clone of BestPractice, which an ordinary session in that set has no reason to have. Every other channel that reports staleness is incidental -- it fires when someone happens to be bootstrapping a set, or happens to be working in Precedent's own repo with the set attached. Incidental is not good enough for a repo I may not open for a month. A scheduled job is the only channel that fires whether or not anyone is looking, and I would rather spend a few Actions minutes a week than find out again by accident.

## Story
On 2026-09-06 this set, and `precedent-team-tms`, were both two hundred commits behind upstream. Both were generating a loader block carrying a defect that had been fixed upstream days earlier -- a standing instruction telling every session to run four gate commands, all four of which failed there. Nothing was broken; there was simply no channel through which "your copy is behind" could reach anyone. It surfaced only because a session happened to have a BestPractice clone attached and happened to run a freshness check by hand.

The first fix put this workflow in Precedent's own source templates, so every adopter would inherit it. That came out again the same day, on my own call: a cron job phoning a remote weekly, spending someone's Actions minutes and opening pull requests in their repository on a schedule they never chose, is an imposition, and a universal template is the wrong place to make that decision for people. The mechanism was right; its level was wrong. It belongs to whoever wants it, which is me.

**Moved to `precedent-team-maintainers` on 2026-09-09**, from `precedent-individual`, in the subject split recorded at Precedent's `TODO.md#split-team-sets-by-subject`. It was written as one person's own default, but the thing that breaks when it is wrong is a repository the whole team works in -- a stale checkout, a practice file whose links die on materialization, a vendored engine nobody refreshes. That is the maintaining team's business, not one person's preference. The copy left behind in the individual set is `status: deduplicated` and points here.

## Install
Copy `.github/workflows/engine-refresh.yml` from this repo into the new set. Precedent's [`spec/BOOTSTRAP_NEW_SOURCES.md`](https://github.com/alex137/BestPractice/blob/precedent-beta-v01/spec/BOOTSTRAP_NEW_SOURCES.md) records the same shape in prose, under "The scheduled channel, and why it is not shipped here", for anyone rebuilding it from scratch.

Turning on *Allow GitHub Actions to create and approve pull requests* (Settings → Actions → General → Workflow permissions) is optional and gets the nicer path. Leaving it off costs one extra click per refresh, which is the whole point of the fallback.

No mechanical check. What this practice asserts is that a *scheduled job in GitHub's infrastructure* runs and behaves correctly -- a claim about a remote system on a weekly clock, not about any state of this repo's tree. A check could confirm the file is present and mention the strings I care about, and that is exactly the check worth not writing: it would pass on a workflow that was disabled in the repo's settings, that GitHub auto-disabled for inactivity, or that failed every run for a month. Passing while the channel is dead is worse than no check, because it is the channel's own failure mode wearing a green tick. The real check is the one the workflow performs on itself: an open `precedent-engine-stale` issue, or a pull request sitting there.
