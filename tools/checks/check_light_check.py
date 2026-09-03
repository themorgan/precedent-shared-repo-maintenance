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


def check_md_links(rel: str, text: str, findings: list[str]) -> None:
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
