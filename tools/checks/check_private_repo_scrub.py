#!/usr/bin/env python3
"""check_private_repo_scrub.py -- the mechanical check for
practices/private-repo-scrub.md.

# practice: private-repo-scrub

Scope: tree, over practices/*.md specifically -- that directory is
exactly the content this repo ships: per practices/install.md's own Rule,
a consuming repo vendors the whole practices/ tree verbatim. The rule
draws a hard line between content that ships (must stay general) and
content that stays local (the repo's own commit messages, README, and any
future decision record, which can and should keep naming things
precisely) -- so only practices/*.md is in scope here, not the whole
tree.

The private repos this rule exists to protect are named explicitly, not
inferred, because "detect anything that looks like a private repo name"
has no reliable general signature -- this check knows what it's guarding
because it's told, the same way a real blocklist is a list of specific
terms, not a heuristic.

Exit 0 and print nothing when clean. Exit 1 and print the practice's own
Rule text (never a paraphrase) plus the specific finding(s) on a violation.
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
PRACTICE_FILE = ROOT / "practices" / "private-repo-scrub.md"
PRACTICES_DIR = ROOT / "practices"

# The private repos this rule protects. Update this list if either is
# renamed, or if a new private set is added under the same account.
PRIVATE_TERMS = [
    "precedent-individual",
    "precedent-team-maintainers",
    "themorgan/precedent-individual",
    "themorgan/precedent-team-maintainers",
    "github.com/themorgan/precedent-individual",
    "github.com/themorgan/precedent-team-maintainers",
]


def rule_text() -> str:
    text = PRACTICE_FILE.read_text(encoding="utf-8")
    m = re.search(r"## Rule\n(.*?)\n## ", text, re.S)
    return m.group(1).strip() if m else "(no Rule found)"


def find_violations() -> list[str]:
    findings = []
    for path in sorted(PRACTICES_DIR.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        for lineno, line in enumerate(text.splitlines(), start=1):
            for term in PRIVATE_TERMS:
                if term in line:
                    findings.append(
                        f"{path.relative_to(ROOT)}:{lineno}: names a private repo "
                        f"({term!r}) in vendored content: {line.strip()!r}"
                    )
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
