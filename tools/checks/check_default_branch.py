#!/usr/bin/env python3
"""check_default_branch.py -- the mechanical check for
practices/default-branch.md.

# practice: default-branch

Scope: tree, via one cheap remote query -- exactly what the practice's own
Install section endorses ("via a host API where the session's tools reach
that far"). `git ls-remote --symref <url> HEAD` asks the remote which
branch HEAD points at without cloning anything; that's this repo's actual
default branch, and the rule requires it to be the repo's TRUNK, whatever
it is called: the `trunk` precedent.json declares, else its `base_branch`.
Until 2026-10-06 this script demanded the name `main`, after universal's
copy of the rule had stopped doing so (2026-10-05); this copy now asks the
same question as the engine's `default-branch` check.

Where nothing declared settles which branch is the trunk (the host shows
one branch first, `base_branch` names another, no `trunk`), it exits 2
with COULD NOT VERIFY and the ask, never a violation.

Exit codes: 0 clean, 1 violation, 2 the check could not run at all (no
network reachability to the remote) -- reported as SKIPPED, never treated
as a silent pass, per the NotApplicable convention: a check that can't
observe the property it's meant to verify must say so rather than stay
quiet.

Exit 0 and print nothing when clean. Exit 1 and print the practice's own
Rule text (never a paraphrase) plus the specific finding(s) on a violation.
"""
import json
import os
import pathlib
import re
import subprocess
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
PRACTICE_FILE = SOURCE_ROOT / "practices" / "default-branch.md"


def _declared(key):
    """precedent.json's `key` as a non-empty string, or None."""
    try:
        v = json.loads((ROOT / "precedent.json").read_text(encoding="utf-8")).get(key)
        return v if isinstance(v, str) and v.strip() else None
    except (OSError, ValueError, AttributeError):
        return None


class NotApplicable(Exception):
    pass


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
    host = actual_default_branch()
    trunk = _declared("trunk")
    if trunk:
        if host != trunk:
            return [f"remote HEAD points at '{host}', and this repository's "
                    f"trunk is '{trunk}' (precedent.json `trunk`) -- set the "
                    f"host's default to '{trunk}' once, or, if '{host}' is the "
                    f"trunk, correct `trunk`"]
        return []
    base = _declared("base_branch")
    if base is None or host == base:
        # Nothing says otherwise: the branch the host shows first is the
        # trunk, whatever it is called.
        return []
    raise NotApplicable(
        f"COULD NOT VERIFY: the host shows '{host}' first and this "
        f"repository's work lands on '{base}' (`base_branch`), and nothing "
        f"declares which of them is the trunk. Ask the person once, then "
        f"record the answer as `trunk` in precedent.json")


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
