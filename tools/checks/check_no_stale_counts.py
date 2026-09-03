#!/usr/bin/env python3
"""check_no_stale_counts.py -- the mechanical check for
practices/no-stale-counts.md.

# practice: no-stale-counts

Scope: tree. The practice's own Install text is right that the general
case -- telling a count "genuinely maintained alongside the thing it
counts" apart from one that "will drift" -- needs the writer's intent,
which no scan can read. But one specific, common shape of that violation
IS objectively checkable with no intent required: a sentence in this
repo's own tracked markdown stating "<N> practices" is a claim about
THIS repo's own practices/ directory, and that claim is either currently
true or it isn't -- independent of anyone's intent in writing it.

This only catches a count that has ALREADY gone stale (the concrete harm
the practice names: "goes stale... with nothing to flag it"). It says
nothing about whether stating the count at all was the right call, or
whether some other document's exact-count sentence should be rewritten to
the qualitative form the Rule prefers -- that's still a judgment call, per
the practice's own Install text, and stays one.

Exit 0 and print nothing when clean. Exit 1 and print the practice's own
Rule text (never a paraphrase) plus the specific finding(s) on a violation.
"""
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
PRACTICE_FILE = ROOT / "practices" / "no-stale-counts.md"
PRACTICES_DIR = ROOT / "practices"

# Deliberately narrow: "<N> practices" naming THIS repo's own count. Does not
# match "N rules", "N practices" describing some OTHER repo's set (context a
# script can't resolve from text alone), or a count inside a code span.
COUNT_RE = re.compile(r"(?<![`\w])(\d+)\s+practices\b")


def rule_text() -> str:
    text = PRACTICE_FILE.read_text(encoding="utf-8")
    m = re.search(r"## Rule\n(.*?)\n## ", text, re.S)
    return m.group(1).strip() if m else "(no Rule found)"


def tracked_markdown() -> list[str]:
    result = subprocess.run(
        ["git", "-C", str(ROOT), "ls-files", "*.md"],
        capture_output=True, text=True, check=True,
    )
    return [line for line in result.stdout.splitlines() if line.strip()]


def find_violations() -> list[str]:
    actual = len(list(PRACTICES_DIR.glob("*.md")))
    findings = []
    for rel in tracked_markdown():
        path = ROOT / rel
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for lineno, line in enumerate(text.splitlines(), 1):
            for m in COUNT_RE.finditer(line):
                # Skip a match sitting inside an inline code span -- a value,
                # not prose making a claim about this repo.
                before = line[:m.start()]
                if before.count("`") % 2 == 1:
                    continue
                stated = int(m.group(1))
                if stated != actual:
                    findings.append(
                        f"{rel}:{lineno}: states {stated!r} practices, but "
                        f"{PRACTICES_DIR.relative_to(ROOT)} currently holds "
                        f"{actual}: {line.strip()!r}")
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
