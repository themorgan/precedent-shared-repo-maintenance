#!/usr/bin/env python3
"""check_header_caps.py -- the mechanical check for practices/header-caps.md.

# practice: header-caps

Scope: tree, over every tracked `*.md` file (applies_to). This covers one
half of the rule, the half that's unambiguous regardless of which scheme a
document picked: "headers and subheaders at the same rank in a document
must all follow one capitalization style, never mixed."

It does NOT check the other half -- that the default scheme, absent a
documented reason otherwise, is specifically NY Times headline style.
Classifying a word as "principal" vs. "minor" for headline-style has
enough genuine edge cases (a preposition used adjectivally, a short verb
that's actually the sentence's main verb) that a check built on a fixed
word list would misfire regularly rather than actually enforce the rule --
see the practice file's own Install section for where this is documented.

What IS checkable without a word list: the same word, appearing in more
than one header at the same rank in the same document, capitalized one
way in one header and a different way in another (excluding each header's
own first and last word, which the rule already exempts from the
minor-word rule) is exactly a scheme mix caught in the act -- direct
evidence of the violation the rule's first sentence names, with no
heuristic about what "principal" means required.

Exit 0 and print nothing when clean. Exit 1 and print the practice's own
Rule text (never a paraphrase) plus the specific finding(s) on a violation.
"""
import pathlib
import re
import subprocess
import sys
from collections import defaultdict

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
PRACTICE_FILE = ROOT / "practices" / "header-caps.md"

ATX_RE = re.compile(r"^(#{1,6})\s+(.*\S)\s*$")
WORD_RE = re.compile(r"[A-Za-z][A-Za-z'-]*")


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


def headers_by_rank(text: str) -> dict[int, list[str]]:
    by_rank: dict[int, list[str]] = defaultdict(list)
    in_fence = False
    for line in text.splitlines():
        if line.strip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        m = ATX_RE.match(line)
        if m:
            by_rank[len(m.group(1))].append(m.group(2))
    return by_rank


def find_violations() -> list[str]:
    findings = []
    for rel in tracked_md_files():
        path = ROOT / rel
        text = path.read_text(encoding="utf-8")
        for rank, headers in headers_by_rank(text).items():
            if len(headers) < 2:
                continue
            # word (lowercased) -> set of capitalization states seen, excluding
            # each header's own first/last word (the rule's own exemption)
            seen: dict[str, set[bool]] = defaultdict(set)
            examples: dict[str, list[str]] = defaultdict(list)
            for header in headers:
                words = WORD_RE.findall(header)
                if len(words) < 3:
                    continue  # nothing but boundary words to compare
                for w in words[1:-1]:
                    key = w.lower()
                    seen[key].add(w[0].isupper())
                    examples[key].append(f"{w!r} in {header!r}")
            for word, states in seen.items():
                if len(states) > 1:
                    findings.append(
                        f"{rel} (h{rank}): {word!r} capitalized inconsistently across "
                        f"same-rank headers -- {'; '.join(examples[word])}"
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
