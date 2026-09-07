#!/usr/bin/env python3
"""check_session_trailer.py -- the mechanical check for
practices/session-trailer.md.

# practice: session-trailer

Scope: tree. Every non-merge commit reachable from HEAD in this repo must
carry a session trailer line -- `Session: <url>`, `Claude-Session: <url>`
(the trailer key Claude Code Remote's own harness actually emits as of
2026-09; functionally the same trailer the practice's Rule describes,
under a different key), or the explicit `Session: none available (<tool>)`
opt-out. A commit with none of these is the "forgotten" case the
practice's own Why section exists to make distinguishable from "considered
and skipped."

Merge commits are excluded: a merge doesn't represent new planned work of
its own (the substantive commits underneath it already carry their own
trailers), and GitHub's own merge-via-API/UI commits never carry a custom
trailer at all -- checking them would fail on every single PR merge,
forever, for a reason that has nothing to do with this practice's actual
intent ("committing anything" in the occasion sense means authoring a
change, not the structural act of merging one).

Exit 0 and print nothing when clean. Exit 1 and print the practice's own
Rule text (never a paraphrase) plus the specific finding(s) on a violation.
"""
import os
import pathlib
import re
import subprocess
import sys

# TWO different questions, which used to share one name -- and that is exactly
# how a practice file went missing. SOURCE_ROOT is the practice set this script
# ships in; ROOT is the repository it AUDITS.
#
# They are the same directory in both normal cases: run in place inside its own
# set, and materialized into a consuming repo (where precedent_materialize.py
# has written practices/ and tools/checks/ side by side). They differ in the
# third case -- a repo that DECLARES this source but never materializes it, and
# runs the script in place against itself. Precedent's own repo is exactly
# that: its practices/ is the universal catalogue, so `parents[2]/practices/`
# resolved to a directory this practice was never in, and rule_text() raised
# FileNotFoundError from inside the violation printer (2026-09-06). The rule
# text always ships beside the script, so it is looked up against SOURCE_ROOT
# and can no longer be absent; only what to audit is overridable.
SOURCE_ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
ROOT = pathlib.Path(os.environ.get("PRECEDENT_CHECK_ROOT") or SOURCE_ROOT)
PRACTICE_FILE = SOURCE_ROOT / "practices" / "session-trailer.md"

TRAILER_RE = re.compile(r"^(?:Session|Claude-Session):\s+(\S.*)$", re.MULTILINE)

# practice: no-rewrite-for-warnings -- this one commit predates the
# practice's own check, is not a merge, and isn't ours to rewrite (authored
# before this exemption mechanism existed). Rewriting already-published
# history to silence a check is exactly what that practice forbids; its
# own Install section calls for scoping the check instead, which is what
# this list does. Found and left as a noted, unfixed backlog item
# 2026-09-03. Every non-merge commit made after this list was added is
# still fully checked -- this exempts exactly this one SHA, nothing else.
GRANDFATHERED_SHAS = {
    "61f2ed8b24020eaaedc03336e262709bb7725176",  # 2026-09-02, pre-check
}


def rule_text() -> str:
    # A materialized check runs in whatever repo its source was resolved
    # into, and the practice file it quotes is not guaranteed to be there:
    # a repo that declares the source but never materializes it, or a
    # practice retired out of the tree, both leave PRACTICE_FILE absent.
    # Unguarded, this raised FileNotFoundError from inside the violation
    # PRINTER -- so the finding was correctly detected, correctly printed,
    # and then buried under a traceback. Found 2026-09-06 running every
    # source-supplied check against BestPractice; 14 of the 16 shared this
    # exact body. The Rule text being unavailable is not the check failing.
    if not PRACTICE_FILE.is_file():
        return "(practice file not found at %s)" % PRACTICE_FILE
    text = PRACTICE_FILE.read_text(encoding="utf-8")
    m = re.search(r"## Rule\n(.*?)\n## ", text, re.S)
    return m.group(1).strip() if m else "(no Rule found)"


def _is_merge(sha: str) -> bool:
    """Parent count, read from the raw commit object rather than
    `git log`/`show --format=%P`. On a shallow clone (this repo's own
    documented default -- see AGENTS.md's environment-gotchas), git's
    pretty-printers report a commit at the shallow boundary as parentless
    for TRAVERSAL purposes, even when its object header genuinely records
    two parents: `git log --format=%P` on this repo's own root-looking
    commit silently came back empty at depth 1, and only `git cat-file -p`
    -- which reads the object's own header, unaffected by shallow grafting
    -- showed the real `parent`/`parent` pair. Using `%P` here would have
    made this exact check wrongly re-flag a real merge commit as a bare,
    trailer-missing one on the next fresh shallow clone."""
    result = subprocess.run(
        ["git", "-C", str(ROOT), "cat-file", "-p", sha],
        capture_output=True,
        text=True,
        check=True,
    )
    return sum(1 for line in result.stdout.splitlines() if line.startswith("parent ")) >= 2


def find_violations() -> list[str]:
    result = subprocess.run(
        ["git", "-C", str(ROOT), "log", "--format=%H%x00%B%x01"],
        capture_output=True,
        text=True,
        check=True,
    )
    findings = []
    for entry in result.stdout.split("\x01"):
        entry = entry.strip("\n")
        if not entry.strip():
            continue
        sha, _, body = entry.partition("\x00")
        if sha in GRANDFATHERED_SHAS:
            continue
        if _is_merge(sha):
            continue  # see the module docstring
        if not TRAILER_RE.search(body):
            findings.append(f"commit {sha[:12]}: no `Session:` trailer in the commit message")
    return findings


if __name__ == "__main__":
    findings = find_violations()
    if findings:
        print(f"VIOLATION: {PRACTICE_FILE.stem}")
        for f in findings:
            print(f"  {f}")
        print("\nthe rule:")
        print("  " + rule_text().replace("\n", "\n  "))
        sys.exit(1)
    sys.exit(0)
