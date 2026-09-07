#!/usr/bin/env python3
"""check_derived_file_marker.py -- the mechanical check for
practices/derived-file-marker.md.

# practice: derived-file-marker

Scope: tree. Any tracked file that opens with a "DERIVED from" line (in
whatever comment syntax that file uses) is claiming to be a regenerated
file per this practice, and must carry all four fixed fields, in order,
near the top of the file:

    DERIVED from <source or glob> @ <sha>
    Recipe: <path>
    Regenerate with: <command or instruction>
    <the routing sentence, verbatim in substance>

There is deliberately no filename convention to key off (the practice's
own Detail section: "a git grep -l ... is the index that cannot be
wrong") -- a file only comes under this check by making the claim itself,
via that opening line.

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
PRACTICE_FILE = SOURCE_ROOT / "practices" / "derived-file-marker.md"

DERIVED_FROM_RE = re.compile(r"DERIVED from\s+(.+?)\s+@\s+(\S+)")
RECIPE_RE = re.compile(r"Recipe:\s*(\S+)")
REGENERATE_RE = re.compile(r"Regenerate with:\s*(.+)")
ROUTING_SNIPPET = "regeneration replaces this file"
HEADER_WINDOW = 8  # how many leading lines to look across for the four fields


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


def tracked_files() -> list[str]:
    result = subprocess.run(
        ["git", "-C", str(ROOT), "ls-files"],
        capture_output=True,
        text=True,
        check=True,
    )
    return [line for line in result.stdout.splitlines() if line.strip()]


def find_violations() -> list[str]:
    findings = []
    for rel in tracked_files():
        path = ROOT / rel
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        lines = text.splitlines()[:HEADER_WINDOW]
        header = "\n".join(lines)

        m = DERIVED_FROM_RE.search(header)
        if not m:
            continue  # doesn't claim to be derived -- not this check's business

        missing = []
        if not RECIPE_RE.search(header):
            missing.append("`Recipe: <path>` line")
        if not REGENERATE_RE.search(header):
            missing.append("`Regenerate with: <command>` line")
        # Compare with whitespace collapsed. A header comment wraps, and the
        # routing sentence is long enough that it usually does -- two real
        # derived files carried it correctly and were reported as missing it
        # because the wrap fell between "replaces" and "this file"
        # (2026-09-06). A check that demands prose sit on one physical line
        # is checking the line width, not the sentence.
        if ROUTING_SNIPPET not in " ".join(header.split()):
            missing.append("the routing sentence (\"...regeneration replaces this file...\")")

        if missing:
            findings.append(f"{rel}: claims DERIVED from but is missing " + ", ".join(missing))

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
