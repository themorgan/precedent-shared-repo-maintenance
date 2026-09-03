#!/usr/bin/env python3
"""check_default_branch.py -- the mechanical check for
practices/default-branch.md.

# practice: default-branch

Scope: tree, via one cheap remote query -- exactly what the practice's own
Install section endorses ("via a host API where the session's tools reach
that far"). `git ls-remote --symref <url> HEAD` asks the remote which
branch HEAD points at without cloning anything; that's this repo's actual
default branch, and the rule requires it to be `main`.

Exit codes: 0 clean, 1 violation, 2 the check could not run at all (no
network reachability to the remote) -- reported as SKIPPED, never treated
as a silent pass, per the NotApplicable convention: a check that can't
observe the property it's meant to verify must say so rather than stay
quiet.

Exit 0 and print nothing when clean. Exit 1 and print the practice's own
Rule text (never a paraphrase) plus the specific finding(s) on a violation.
"""
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
PRACTICE_FILE = ROOT / "practices" / "default-branch.md"

EXPECTED_BRANCH = "main"


class NotApplicable(Exception):
    pass


def rule_text() -> str:
    text = PRACTICE_FILE.read_text(encoding="utf-8")
    m = re.search(r"## Rule\n(.*?)\n## ", text, re.S)
    return m.group(1).strip() if m else "(no Rule found)"


def remote_url() -> str:
    result = subprocess.run(
        ["git", "-C", str(ROOT), "remote", "get-url", "origin"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0 or not result.stdout.strip():
        raise NotApplicable("no 'origin' remote configured")
    return result.stdout.strip()


def actual_default_branch() -> str:
    url = remote_url()
    result = subprocess.run(
        ["git", "ls-remote", "--symref", url, "HEAD"],
        capture_output=True,
        text=True,
        timeout=30,
    )
    if result.returncode != 0:
        raise NotApplicable(f"could not reach '{url}': {result.stderr.strip()}")
    m = re.search(r"^ref:\s+refs/heads/(\S+)\s+HEAD$", result.stdout, re.MULTILINE)
    if not m:
        raise NotApplicable(f"unexpected ls-remote output for '{url}'")
    return m.group(1)


def find_violations() -> list[str]:
    branch = actual_default_branch()
    if branch != EXPECTED_BRANCH:
        return [f"remote HEAD points at '{branch}', expected '{EXPECTED_BRANCH}'"]
    return []


if __name__ == "__main__":
    try:
        findings = find_violations()
    except NotApplicable as e:
        print(f"SKIPPED: {PRACTICE_FILE.stem}: {e}")
        sys.exit(2)

    if findings:
        print(f"VIOLATION: {PRACTICE_FILE.stem}")
        for f in findings:
            print(f"  {f}")
        print("\nthe rule:")
        print("  " + rule_text().replace("\n", "\n  "))
        sys.exit(1)
    sys.exit(0)
