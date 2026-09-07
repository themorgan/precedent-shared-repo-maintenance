#!/usr/bin/env python3
"""check_light_check.py -- the mechanical check for practices/light-check.md.

# practice: light-check

Scope: tree. The practice names its own minimum audit: conflict markers,
invalid JSON/YAML syntax, secret-shaped strings, and broken relative doc
links. This script IS that audit, run against this repo itself -- the
same script the practice says every repo that adopts it should run
before every commit and wire into CI.

The Detail section adds a second half for a repo that has this team's own
set (or any vendored practice set) *installed*: verifying a tracking
manifest is real. This repo is the source of that set, not an installer
of one -- there is no manifest here to check -- so that half doesn't
apply to this repo's own tree and isn't implemented here; a repo that
vendors this set would extend the check with that piece itself.

The broken-relative-link check skips process/upstream/ unconditionally
(always a vendored mirror, wherever found) and nothing else. It used to
skip a materialized practices/ too, as a workaround for an upstream bug
that has since been fixed -- see _link_check_exempt for the full note and
what a finding there means now.

Exit 0 and print nothing when clean. Exit 1 and print the practice's own
Rule text (never a paraphrase) plus the specific finding(s) on a violation.
"""
import json
import os
import pathlib
import re
import subprocess
import sys

import yaml

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
PRACTICE_FILE = SOURCE_ROOT / "practices" / "light-check.md"

CONFLICT_MARKER_RE = re.compile(r"^(<{7}|={7}|>{7})(\s|$)")
SECRET_PATTERNS = [
    ("AWS-style access key ID", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("PEM private key header", re.compile(r"-----BEGIN (RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----")),
    ("GitHub personal access token", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{36}\b")),
    ("Slack token", re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}\b")),
]
FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n", re.S)
MD_LINK_RE = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")


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


def check_conflict_markers(rel: str, text: str, findings: list[str]) -> None:
    for lineno, line in enumerate(text.splitlines(), start=1):
        if CONFLICT_MARKER_RE.match(line):
            findings.append(f"{rel}:{lineno}: unresolved conflict marker: {line.strip()!r}")


def check_secrets(rel: str, text: str, findings: list[str]) -> None:
    for label, pattern in SECRET_PATTERNS:
        m = pattern.search(text)
        if m:
            findings.append(f"{rel}: looks like a {label} ({m.group(0)[:12]}...)")


def check_frontmatter_yaml(rel: str, text: str, findings: list[str]) -> None:
    m = FRONTMATTER_RE.match(text)
    if not m:
        return
    try:
        yaml.safe_load(m.group(1))
    except yaml.YAMLError as e:
        findings.append(f"{rel}: frontmatter is not valid YAML ({e})")


def check_json(rel: str, text: str, findings: list[str]) -> None:
    try:
        json.loads(text)
    except json.JSONDecodeError as e:
        findings.append(f"{rel}: not valid JSON ({e})")


def check_yaml_file(rel: str, text: str, findings: list[str]) -> None:
    try:
        yaml.safe_load(text)
    except yaml.YAMLError as e:
        findings.append(f"{rel}: not valid YAML ({e})")


# process/upstream/ is ALWAYS a vendored mirror of another repo -- its tree
# is never hand-edited here (generated-artifact-provenance, and the merge
# runbook's own "never hand-merge" rule for it), so a link written relative
# to that repo's own root is correct THERE, not resolvable once copied flat
# into this tree, and would be restored identically by the next sync.
# Reporting it every run is a permanent, unactionable backlog.
#
# MATERIALIZED practices/ USED TO BE EXEMPT HERE TOO, and is not any more
# (2026-09-06). The exemption was a workaround for a real upstream bug: a
# practice's relative links were copied verbatim into a consuming repo,
# where `../tools/very_deep_check.py` and `../spec/ATTENTION_CEILING.md`
# point at nothing -- so every consuming repo shipped ~60 practice files
# with dead internal links, and this check had to look away to stay green.
# Precedent's precedent_materialize.py now repoints those links for where
# the file actually lands (a commit URL into the source repository, or a
# recomputed relative path when the target is in this repo), so a broken
# link in a materialized practice is once again a real finding: it means
# the sync is stale, or the rewrite genuinely failed. Both are worth
# knowing. If this starts firing across the whole tree, the fix is
# `python3 tools/precedent_sync_views.py`, not a new exemption.
def _link_check_exempt(rel: str) -> bool:
    return rel.startswith("process/upstream/")


def check_md_links(rel: str, text: str, findings: list[str]) -> None:
    if _link_check_exempt(rel):
        return
    base = (ROOT / rel).parent
    for lineno, line in enumerate(text.splitlines(), start=1):
        for target in MD_LINK_RE.findall(line):
            target = target.split(" ", 1)[0].strip()  # drop an optional "title"
            if not target or target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            path_part = target.split("#", 1)[0]
            if not path_part:
                continue
            resolved = (base / path_part).resolve()
            if not resolved.exists():
                findings.append(f"{rel}:{lineno}: broken relative link to {target!r}")


SHARED_BEGIN = "# --- shared:"
SHARED_END = "# --- end shared:"


def check_shared_blocks_agree(findings: list[str]) -> None:
    """A block marked `# --- shared:<id> ---` is byte-identical everywhere.

    Some helpers genuinely have to be COPIED rather than imported: a check
    script's own contract is that it runs standalone, with no arguments and
    no sibling imports, and precedent_materialize.py vendors `check_*.py`
    files only -- a shared module placed beside them would not travel. So
    the copies are deliberate, and the risk is that they drift.

    They already had. All four copies of the scope helper were written in
    one pass on 2026-09-06 and one of them had picked up a different
    comment within the day -- behaviour identical, but that is what drift
    looks like on day one, and nothing was watching. Marked blocks are
    compared here because a consuming repo is where every copy lands in
    one directory; in their own source repos they never meet.

    Compares the marked text only, so the code around it is free to differ
    -- these are different checks, and only the shared part is shared."""
    blocks: dict = {}
    for rel in tracked_files():
        if "/checks/" not in rel or not rel.endswith(".py"):
            continue
        try:
            lines = (ROOT / rel).read_text(encoding="utf-8").splitlines()
        except (UnicodeDecodeError, OSError):
            continue
        ident, buf = None, []
        for line in lines:
            if line.startswith(SHARED_END):
                if ident is not None:
                    blocks.setdefault(ident, {})["\n".join(buf)] = \
                        blocks.setdefault(ident, {}).get("\n".join(buf), []) + [rel]
                ident, buf = None, []
            elif line.startswith(SHARED_BEGIN):
                ident = line[len(SHARED_BEGIN):].split()[0].rstrip("-— ")
                buf = []
            elif ident is not None:
                buf.append(line)
        if ident is not None:
            findings.append(f"{rel}: a `{SHARED_BEGIN}{ident}` block is never closed "
                            f"with `{SHARED_END}{ident} ---`")

    for ident, variants in sorted(blocks.items()):
        if len(variants) > 1:
            where = "; ".join(
                f"{', '.join(sorted(files))}" for files in variants.values())
            findings.append(
                f"shared block {ident!r} has {len(variants)} different "
                f"versions across the files that carry it ({where}). These "
                f"are copies on purpose -- a check script runs standalone "
                f"and cannot import a sibling -- so they have to be kept "
                f"byte-identical by hand. Reconcile them.")


def find_violations() -> list[str]:
    findings: list[str] = []
    for rel in tracked_files():
        path = ROOT / rel
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue

        check_conflict_markers(rel, text, findings)
        check_secrets(rel, text, findings)

        if rel.endswith(".md"):
            check_frontmatter_yaml(rel, text, findings)
            check_md_links(rel, text, findings)
        elif rel.endswith(".json"):
            check_json(rel, text, findings)
        elif rel.endswith((".yml", ".yaml")):
            check_yaml_file(rel, text, findings)

    check_shared_blocks_agree(findings)
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
