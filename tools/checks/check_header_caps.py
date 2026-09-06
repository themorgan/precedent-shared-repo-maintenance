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
import json
import pathlib
import re
import subprocess
import sys
from collections import defaultdict

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
PRACTICE_FILE = ROOT / "practices" / "header-caps.md"

ATX_RE = re.compile(r"^(#{1,6})\s+(.*\S)\s*$")
WORD_RE = re.compile(r"[A-Za-z][A-Za-z'-]*")



# --- Findings this repo cannot act on where they are reported -------------
#
# A consuming repo mirrors trees it must NOT hand-edit: the vendored
# universal catalogue (byte-identical to upstream, re-mirrored wholesale)
# and any generated or re-synced copy of another repo's files. A finding
# inside one of those is real, but it is not actionable HERE -- the fix
# belongs in the repo that owns the text, and editing the mirror is
# forbidden and would be overwritten by the next sync anyway. Reporting
# them buries the findings that ARE actionable: one consuming repo's run
# showed dozens of violations, every single one inside its vendored copy
# of upstream's own prose (2026-09-06).
#
# Nothing is hardcoded. All three signals already exist and are already
# authoritative in any repo that has them:
#   1. process/manifest.json's upstream.vendored_at -- the mirror's own
#      declared path.
#   2. A "GENERATED FILE" / "do not hand-edit" / "DERIVED" marker in the
#      file's opening lines (practice: derived-file-marker).
#   3. MANIFEST.json's per-practice `level` -- practices/ is materialized
#      output, so a practice from any source but repo-local is owned
#      elsewhere. Attributing by the COMMITTED manifest rather than by
#      live source resolution is deliberate: a bare CI checkout cannot
#      reach a team sibling clone or a private user-level config, and
#      "did not resolve here" is not "owned here".
# A repo with none of these files loses nothing -- every part fails open.
_GENERATED_RE = re.compile(
    r"generated file|do not hand[- ]edit|DERIVED from", re.I)


def _mirrored_prefixes() -> tuple:
    manifest = ROOT / "process" / "manifest.json"
    if not manifest.is_file():
        return ()
    try:
        upstream = json.loads(manifest.read_text(encoding="utf-8")).get("upstream", {})
    except (ValueError, OSError):
        return ()
    at = str(upstream.get("vendored_at") or "").strip("/")
    return (at + "/",) if at else ()


def _is_generated(rel: str) -> bool:
    try:
        with (ROOT / rel).open(encoding="utf-8") as fh:
            head = "".join([next(fh, "") for _ in range(3)])
    except (OSError, UnicodeDecodeError):
        return False
    return bool(_GENERATED_RE.search(head))


def _foreign_practice(rel: str) -> bool:
    if not (rel.startswith("practices/") and rel.endswith(".md")):
        return False
    manifest = ROOT / "MANIFEST.json"
    if not manifest.is_file():
        return False
    try:
        entries = json.loads(manifest.read_text(encoding="utf-8")).get("practices", [])
    except (ValueError, OSError):
        return False
    slug = pathlib.PurePath(rel).stem
    for entry in entries:
        if entry.get("slug") == slug:
            return entry.get("level") != "repo-local"
    return False


def not_actionable_here(rel: str) -> bool:
    prefixes = _mirrored_prefixes()
    return (bool(prefixes) and rel.startswith(prefixes)) \
        or _foreign_practice(rel) or _is_generated(rel)

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
    return [line for line in result.stdout.splitlines()
            if line.strip() and not not_actionable_here(line.strip())]


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
