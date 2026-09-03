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
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
PRACTICE_FILE = ROOT / "practices" / "derived-file-marker.md"

DERIVED_FROM_RE = re.compile(r"DERIVED from\s+(.+?)\s+@\s+(\S+)")
RECIPE_RE = re.compile(r"Recipe:\s*(\S+)")
REGENERATE_RE = re.compile(r"Regenerate with:\s*(.+)")
ROUTING_SNIPPET = "regeneration replaces this file"
HEADER_WINDOW = 8  # how many leading lines to look across for the four fields


def rule_text() -> str:
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
        if ROUTING_SNIPPET not in header:
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
