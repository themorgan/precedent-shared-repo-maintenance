# Private Repo Names in the Public Tree — Findings and Scrub Plan

**Output for a later BestPractice-rooted session**, like
[NOT_BINDING_FINDINGS.md](NOT_BINDING_FINDINGS.md) beside it. Nothing here
has been applied upstream: the session that produced it treated
`alex137/BestPractice` as read-only.

**Why the two names appear in full below.** `private-repo-scrub` permits the
real names in content that never leaves the authoring repo, and requires
general terms in anything that ships. This file is the first kind:
`precedent_materialize.py` copies only `practices/` and `tools/checks/` into
a consuming repo, so a root document like this one stays here. Do not copy
its contents into a practice file, a vendored template, or an upstream
commit message — describe the situation generally there, exactly as the
scrub itself does.

## What Was Found

The leak gate has two vocabulary halves. The public default half is
committed upstream and always runs. The private half — the one that catches
actual private words — is named by an environment variable pointing at a
list that **cannot live in the repo it protects**, and it had never been
switched on against a real tree. Pointing it at the individual set's own
blocklist and setting `precedent.requireVocabulary` ran it for the first
time.

**It fails, on two patterns only**, both names of Morgan's private
repositories, across two dozen files including the README, the agent
instructions, the install guide, the plan of record, and two practice files.
No other blocklist pattern hits anything.

The same two names have also been **vendored outward**. They sit in
`tools/precedent_show.py` and `tools/precedent_vendor_engine.py`, which are
byte-identical engine copies in all three private practice sets — so the
leak is not confined to one public repo, and no set may hand-edit its own
copy to fix it.

## The Honest Framing

**These names are already published and have been for some time.** Removing
them now does not unpublish them: the history keeps them, and the repo is
world-readable. So this is not an emergency, and it should not be handled as
one. What it decides is what the tree says going forward, and whether the
gate is allowed to be green.

There is a real precedent pointing the other way, and it belongs in the
record. The blocklist's own header documents two earlier rounds where
patterns were *removed* after switching the layer on found them colliding
with content the repo legitimately needed — Morgan's own name, email,
timezone and account handle, all of which appear by design in commit
identity, dated headers and repo links. Same evidence-driven shape as this.

**The difference is what kind of thing is named.** Those were Morgan's own
already-public identity. These are the names of repositories that are
private, whose existence and subject matter the names disclose. That is the
category `private-repo-scrub` was written for, and it is `severity:
blocking` — the one severity `not_binding` may never exempt.

**Recommendation: keep both patterns blocked and scrub the tree forward.**
Unblocking them to make the gate green decides a real question by
convenience, and the gate failing is the gate working.

## The Scrub, per File

Counts are occurrences, current as of the run that produced this file.
Every one is a mention in prose or a comment; none is a functional
identifier, so each can be replaced with a general description — "a
dependent repo", "an earlier project", "a dependent content repo" — with no
behaviour change.

| File | `HavrutaBrainstorm` | `WorkingWithAI` |
|---|---|---|
| [spec/MIGRATING_EXISTING_INSTALLS.md](https://github.com/alex137/BestPractice/blob/precedent-beta-v01/spec/MIGRATING_EXISTING_INSTALLS.md) | 4 | 10 |
| [spec/PRELAUNCH_AUDIT.md](https://github.com/alex137/BestPractice/blob/precedent-beta-v01/spec/PRELAUNCH_AUDIT.md) | 2 | 5 |
| [documentation/WHAT_IS_THIS_AND_BENEFITS.md](https://github.com/alex137/BestPractice/blob/precedent-beta-v01/documentation/WHAT_IS_THIS_AND_BENEFITS.md) | — | 4 |
| [tools/precedent_vendor_engine.py](https://github.com/alex137/BestPractice/blob/precedent-beta-v01/tools/precedent_vendor_engine.py) | 3 | — |
| [tools/precedent_check.py](https://github.com/alex137/BestPractice/blob/precedent-beta-v01/tools/precedent_check.py) | — | 3 |
| [TODO.md](https://github.com/alex137/BestPractice/blob/precedent-beta-v01/TODO.md) | 2 | — |
| [tools/verify_harness.py](https://github.com/alex137/BestPractice/blob/precedent-beta-v01/tools/verify_harness.py) | 1 | 2 |
| [README.md](https://github.com/alex137/BestPractice/blob/precedent-beta-v01/README.md) | — | 2 |
| [spec/PHASE6_BRIEF.md](https://github.com/alex137/BestPractice/blob/precedent-beta-v01/spec/PHASE6_BRIEF.md) | — | 2 |
| [practices/migration-scrubs-vocabulary.md](https://github.com/alex137/BestPractice/blob/precedent-beta-v01/practices/migration-scrubs-vocabulary.md) | 1 | 1 |
| [AGENTS.md](https://github.com/alex137/BestPractice/blob/precedent-beta-v01/AGENTS.md) | 1 | — |
| [INSTALL.md](https://github.com/alex137/BestPractice/blob/precedent-beta-v01/INSTALL.md) | 1 | — |
| [practices/session-bootstrap.md](https://github.com/alex137/BestPractice/blob/precedent-beta-v01/practices/session-bootstrap.md) | 1 | — |
| [spec/BOOTSTRAP_NEW_SOURCES.md](https://github.com/alex137/BestPractice/blob/precedent-beta-v01/spec/BOOTSTRAP_NEW_SOURCES.md) | 1 | — |
| [spec/SOURCE_NAMING.md](https://github.com/alex137/BestPractice/blob/precedent-beta-v01/spec/SOURCE_NAMING.md) | 1 | — |
| [tools/precedent_show.py](https://github.com/alex137/BestPractice/blob/precedent-beta-v01/tools/precedent_show.py) | 1 | — |
| [tools/leak_gate.py](https://github.com/alex137/BestPractice/blob/precedent-beta-v01/tools/leak_gate.py) | — | 1 |
| [tools/precedent_materialize.py](https://github.com/alex137/BestPractice/blob/precedent-beta-v01/tools/precedent_materialize.py) | — | 1 |
| [CHANGES_TO_TELL_ALEX.md](https://github.com/alex137/BestPractice/blob/precedent-beta-v01/CHANGES_TO_TELL_ALEX.md) | — | 1 |
| [PRACTICE_ENGINE_PLAN.md](https://github.com/alex137/BestPractice/blob/precedent-beta-v01/PRACTICE_ENGINE_PLAN.md) | — | 1 |

**Two cases need care rather than a find-and-replace.** The mentions inside
`leak_gate.py` and `migration-scrubs-vocabulary.md` may be illustrative — a
worked example of the very thing being scrubbed — in which case the fix is
to change the example, not to delete the sentence. And **do not rewrite
published history**: fix forward, per `no-rewrite-for-warnings`.

The vendored engine files are fixed once upstream and reach the three
private sets on their next `precedent_vendor_engine.py refresh`. No set
should patch its own copy.

## The Proposed Practice, and One Correction to It

Morgan's proposal: a universal practice saying that **any private repo
named anywhere gets its name added to the scrub list the system already
has**, so the gate catches it from then on. The instinct is right, and it
converts a rule people must remember into one a mechanism enforces.

**It needs one correction, and it is the whole ballgame.** There are two
blocklists, not one. `tools/leak-blocklist.default.txt` is committed in the
public repo; the private half lives outside it precisely because a list of
secret terms, committed to the repo it guards, publishes the secrets it
exists to protect. A practice worded as "add it to the scrub list" will be
read as the committed one about half the time — and following it would
publish the private repo name in a *new* place, as the fix. So the practice
must name the private half explicitly, and say why.

With that fixed, the shape worth proposing:

- **When any text that ships names a private repository, its name goes into
  the private blocklist half in the same commit** — never the committed
  default list, which is public.
- **Adding the name does not scrub the mentions**; it makes the gate fail
  until somebody does. That is the intended order, since the gate failing is
  what forces the scrub rather than deferring it.
- **The cheap mechanical half** is a check that any `github.com/<owner>/<repo>`
  reference in shipping text resolves to a public repository, which is one
  API call per distinct repo and needs no blocklist at all. That catches the
  URL form, which is the common one, and it degrades honestly when it has no
  credentials rather than passing silently.
- **The bare-name form stays a judgment call.** No mechanism can tell a
  private repo's name from an ordinary capitalized noun without being told,
  which is exactly why the blocklist exists and why this practice feeds it.

This session did not write the practice, because it belongs in the universal
catalogue and the session could not push there.
