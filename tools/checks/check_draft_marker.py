#!/usr/bin/env python3
"""check_draft_marker.py -- the mechanical check for practices/draft-marker.md.

# practice: draft-marker

Scope: tree, over markdown files (where a draft placeholder actually
lives). The practice's own Detail section names the actual mechanical
moment: "before showing or sharing any document, scan it for the marker
specifically." Nothing committed to the repo should still carry a live
`**➡️ ... ⬅️**` placeholder -- if it's there, it was either missed on
that scan or the placeholder never got resolved before commit.

A line that only *illustrates* the marker's own format inside backtick
code -- as this practice's own Rule text does, and as this check's source
necessarily would if it weren't excluded -- is not a live placeholder, so
inline code spans are stripped before matching; only a marker sitting in
real document prose counts.

Exit 0 and print nothing when clean. Exit 1 and print the practice's own
Rule text (never a paraphrase) plus the specific finding(s) on a violation.
"""
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
PRACTICE_FILE = ROOT / "practices" / "draft-marker.md"

CODE_SPAN_RE = re.compile(r"`[^`]*`")
MARKER_RE = re.compile(r"\*\*\s*➡️.*?⬅️\s*\*\*")


def rule_text() -> str:
    text = PRACTICE_FILE.read_text(encoding="utf-8")
    m = re.search(r"## Rule\n(.*?)\n## ", text, re.S)
    return m.group(1).strip() if m else "(no Rule found)"


def tracked_md_files() -> list[str]:
    result = subprocess.run(
        ["git", "-C", str(ROOT), "ls-files", "*.md"],
        capture_output=True,
        text=True,
        check=True,
    )
    return [line for line in result.stdout.splitlines() if line.strip()]


def find_violations() -> list[str]:
    findings = []
    in_fence = False
    for rel in tracked_md_files():
        path = ROOT / rel
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        in_fence = False
        for lineno, line in enumerate(text.splitlines(), start=1):
            if line.strip().startswith("```"):
                in_fence = not in_fence
                continue
            if in_fence:
                continue
            stripped = CODE_SPAN_RE.sub("", line)
            if MARKER_RE.search(stripped):
                findings.append(f"{rel}:{lineno}: leftover draft marker: {line.strip()!r}")
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
