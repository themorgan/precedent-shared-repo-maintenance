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
(always a vendored mirror, wherever found) and practices/ only when THIS
repo's own MANIFEST.json shows practices/ is itself a materialized copy
(an installing repo, not this one) -- see _link_check_exempt. Confirmed
by running this script against precedent-team-maintainers' own tree
(zero exemption effect: no MANIFEST.json here, so practices/ stays fully
checked) versus against a repo that installed this set (where materialized
copies of OTHER sources' practice files carry links written relative to
THEIR OWN source repo's root, not resolvable here, and not this repo's to
fix).

Exit 0 and print nothing when clean. Exit 1 and print the practice's own
Rule text (never a paraphrase) plus the specific finding(s) on a violation.
"""
import json
import pathlib
import re
import subprocess
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
PRACTICE_FILE = ROOT / "practices" / "light-check.md"

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


def _practices_are_materialized() -> bool:
    """True when THIS repo's practices/ is a derived, tools/precedent_materialize.py
    -produced copy rather than hand-authored source content -- signalled by
    the MANIFEST.json that tool writes (generated-artifact-provenance).
    Only an installing/consuming repo has one; this repo's own tree never
    will, since it's a source, not an installer, of the set (see this
    file's own module docstring)."""
    manifest = ROOT / "MANIFEST.json"
    if not manifest.exists():
        return False
    try:
        data = json.loads(manifest.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return False
    return data.get("generated_by") == "tools/precedent_materialize.py"


# Path prefixes whose broken-link findings are never this repo's business
# to report, because the content isn't this repo's own to fix:
#  - process/upstream/ is ALWAYS a vendored mirror of another repo (its
#    own tree, wherever this convention is followed, is never hand-edited
#    here -- generated-artifact-provenance / the merge-runbook's own
#    "never hand-merge" rule for it).
#  - practices/ is a derived materialize() copy ONLY in an installing
#    repo (see _practices_are_materialized) -- in THIS repo, the source
#    of the set, practices/ is real, hand-authored content and stays
#    checked like anything else.
# Either way: a link written relative to another repo's own root is
# correct THERE and not always resolvable once copied flat into this
# tree, and re-running the vendoring sync would restore the identical
# "broken" link -- reporting it here every run is a permanent,
# unactionable backlog, not something this check's own gate should hold
# against a commit it can't fix.
def _link_check_exempt(rel: str) -> bool:
    if rel.startswith("process/upstream/"):
        return True
    if rel.startswith("practices/") and _practices_are_materialized():
        return True
    return False


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
