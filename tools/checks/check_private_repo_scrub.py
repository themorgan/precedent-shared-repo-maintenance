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
import json
import os
import pathlib
import re
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
PRACTICE_FILE = SOURCE_ROOT / "practices" / "private-repo-scrub.md"
PRACTICES_DIR = ROOT / "practices"

# The private repos this rule protects, OWNER-QUALIFIED. Update this list
# if either is renamed, or if a new private set is added under the same
# account.
#
# WHY THE BARE NAMES CAME OFF (2026-09-06). This list used to carry
# "precedent-individual" and "precedent-team-maintainers" on their own,
# and that was right when it was written: they were this account's private
# repo names, and nothing else in the world used those strings. Precedent's
# `source-naming` practice then made them the FIXED, PUBLIC names every
# adopter's sets carry -- one `precedent-individual` per person, in that
# person's own account, by convention rather than by choice. They are now
# printed in the universal catalogue's own practice text, in the upstream
# install guide, and in the resolver's own error messages. A bare
# occurrence identifies nobody, and flagging one told a consumer repo to
# scrub a word it was required to use.
#
# What still identifies is the OWNER. `themorgan/precedent-individual`
# names a specific person's private set; `precedent-individual` names a
# convention. So the owner-qualified forms stay, and only those. If a
# future private set is named something genuinely its own -- not a
# convention name -- put the bare string back for that one.
PRIVATE_TERMS = [
    "themorgan/precedent-individual",
    "themorgan/precedent-team-maintainers",
    "github.com/themorgan/precedent-individual",
    "github.com/themorgan/precedent-team-maintainers",
]



# practices/ is MATERIALIZED output in a consuming repo: precedent_materialize.py
# rewrites it from every declared source on each sync. A practice that came from
# the team or individual set is that set's text, not the consuming repo's -- it
# cannot be fixed there, and the next sync would overwrite the edit anyway. In
# THIS repo (a source, with no MANIFEST.json) the lookup finds nothing and every
# practice is checked exactly as before, which is the intended asymmetry.
#
# Attribution comes from the COMMITTED MANIFEST.json, never from live source
# resolution: a bare CI checkout can reach neither a team sibling clone nor a
# private user-level config, so "did not resolve here" is not "owned here".
#
# 2026-09-06: a consuming repo reported this check against practices/deep-check.md
# -- a team-set practice that names the team repo in its own Install section,
# entirely correctly, since that text never leaves the private sets.
def _foreign_practice(path: pathlib.Path) -> bool:
    manifest = ROOT / "MANIFEST.json"
    if not manifest.is_file():
        return False
    try:
        entries = json.loads(manifest.read_text(encoding="utf-8")).get("practices", [])
    except (ValueError, OSError):
        return False
    for entry in entries:
        if entry.get("slug") == path.stem:
            return entry.get("level") != "repo-local"
    return False

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


def find_violations() -> list[str]:
    findings = []
    for path in sorted(PRACTICES_DIR.glob("*.md")):
        if _foreign_practice(path):
            continue
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
