#!/usr/bin/env python3
"""check_catalogue_stories.py -- the mechanical check for
practices/catalogue-carries-stories.md.

# practice: catalogue-carries-stories

Scope: tree. Every practice in this set with `status: active` must carry a
non-empty `## Story`.

Deliberately a whole-tree invariant rather than a changed-files gate. The
universal catalogue's own cite-the-incident check fires at authorship time
on the files a branch touches, which is right for writing one practice and
useless for two other cases this set actually hit: receiving a whole
catalogue in one migration, and a gap that is already sitting in the tree
from a commit nobody is going to touch again.

It tests that the incident was recorded, NOT that it was the right
incident -- the same limit cite-the-incident states about itself. A Story
that honestly says no originating incident was recorded passes, and should:
the rule refuses silence, not the absence of drama.

Exit 0 and print nothing when clean. Exit 1 and print the practice's own
Rule text (never a paraphrase) plus the specific finding(s) on a violation.
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
PRACTICE_FILE = ROOT / "practices" / "catalogue-carries-stories.md"
PRACTICES_DIR = ROOT / "practices"


def rule_text() -> str:
    text = PRACTICE_FILE.read_text(encoding="utf-8")
    m = re.search(r"## Rule\n(.*?)\n## ", text, re.S)
    return m.group(1).strip() if m else "(no Rule found)"


def _status(text: str) -> str:
    """Read `status:` out of the frontmatter only.

    Anchored to the frontmatter block rather than searched for anywhere in
    the file: a practice's own prose can easily contain the word `status:`
    (this set has several that discuss the status vocabulary directly), and
    a loose search would read one of those and mis-scope the check.
    """
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    if not m:
        return ""
    m2 = re.search(r"^status:\s*(\S+)", m.group(1), re.M)
    return m2.group(1).strip() if m2 else ""


def find_violations() -> list[str]:
    findings = []
    for path in sorted(PRACTICES_DIR.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        if _status(text) != "active":
            continue
        m = re.search(r"^## Story\n(.*?)(?=\n## |\Z)", text, re.S | re.M)
        if m is None:
            findings.append(
                f"practices/{path.name} has no ## Story section at all")
        elif not m.group(1).strip():
            findings.append(
                f"practices/{path.name} is status: active with an empty "
                f"## Story -- the reason this rule exists is recorded nowhere")
    return findings


def main() -> int:
    findings = find_violations()
    if not findings:
        return 0
    print("VIOLATION: catalogue-carries-stories")
    for f in findings:
        print(f"  {f}")
    print()
    print("the rule:")
    for line in rule_text().splitlines():
        print(f"  {line}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
