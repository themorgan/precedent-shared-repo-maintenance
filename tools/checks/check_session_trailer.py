#!/usr/bin/env python3
"""check_session_trailer.py -- the mechanical check for
practices/session-trailer.md.

Scope: tree. Every commit reachable from HEAD in this repo must carry a
`Session:` trailer line -- either `Session: <url>` or the explicit
`Session: none available (<tool>)` opt-out. A commit with neither is the
"forgotten" case the practice's own Why section exists to make
distinguishable from "considered and skipped."

Exit 0 and print nothing when clean. Exit 1 and print the practice's own
Rule text (never a paraphrase) plus the specific finding(s) on a violation.
"""
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
PRACTICE_FILE = ROOT / "practices" / "session-trailer.md"

TRAILER_RE = re.compile(r"^Session:\s+(\S.*)$", re.MULTILINE)


def rule_text() -> str:
    text = PRACTICE_FILE.read_text(encoding="utf-8")
    m = re.search(r"## Rule\n(.*?)\n## ", text, re.S)
    return m.group(1).strip() if m else "(no Rule found)"


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
