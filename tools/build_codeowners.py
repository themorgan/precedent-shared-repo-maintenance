#!/usr/bin/env python3
"""build_codeowners.py -- generate CODEOWNERS from approvers.json.

PRACTICE_ENGINE_PLAN.md, "Who the Approvers Are, and How They Get That Job":
"Approvers are declared in the practice set's own config, not in a
host-specific file... GitHub's CODEOWNERS is then generated from that list,
the same way every other view in this system is generated, so there is one
source and the platform enforcement derives from it rather than competing
with it."

approvers.json is that config; CODEOWNERS is the generated GitHub-specific
view. Never hand-edit CODEOWNERS -- edit approvers.json and rerun this
script. CODEOWNERS carries this repo's own derived-file-marker header
(practices/derived-file-marker.md), since it is exactly the case that
practice describes: a file a later regeneration overwrites wholesale.

Run: python3 tools/build_codeowners.py
"""
import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
APPROVERS_FILE = ROOT / "approvers.json"
CODEOWNERS_FILE = ROOT / "CODEOWNERS"


def _source_sha() -> str:
    result = subprocess.run(
        ["git", "-C", str(ROOT), "rev-parse", "HEAD"],
        capture_output=True, text=True, check=True,
    )
    return result.stdout.strip()


def load_approvers() -> list[dict]:
    data = json.loads(APPROVERS_FILE.read_text(encoding="utf-8"))
    approvers = data.get("approvers", [])
    if not approvers:
        raise SystemExit(f"{APPROVERS_FILE}: no approvers declared -- a team "
                          f"set needs at least one (PRACTICE_ENGINE_PLAN.md: "
                          f"'at creation, whoever creates a team set is its "
                          f"first approver; no ceremony, and there is always "
                          f"at least one').")
    for entry in approvers:
        if not entry.get("github"):
            raise SystemExit(f"{APPROVERS_FILE}: approver {entry!r} has no "
                              f"'github' field -- CODEOWNERS needs a GitHub "
                              f"username to address, not just a name.")
    return approvers


def render(approvers: list[dict], sha: str) -> str:
    owners = " ".join(f"@{a['github']}" for a in approvers)
    lines = [
        f"# DERIVED from approvers.json @ {sha}",
        "# Recipe: tools/build_codeowners.py",
        "# Regenerate with: python3 tools/build_codeowners.py",
        "# edits here are safe to make but not durable -- regeneration replaces this file;",
        "# to make a change stick, edit the source or the recipe.",
        "#",
        "# Every approver reviews every change to this practice set -- there is",
        "# no per-path split; the whole repo is the thing being approved.",
        "",
        f"*  {owners}",
        "",
    ]
    return "\n".join(lines)


def main():
    approvers = load_approvers()
    sha = _source_sha()
    CODEOWNERS_FILE.write_text(render(approvers, sha), encoding="utf-8")
    print(f"wrote {CODEOWNERS_FILE.relative_to(ROOT)} from {len(approvers)} "
          f"approver(s): {', '.join('@' + a['github'] for a in approvers)}")


if __name__ == "__main__":
    sys.exit(main())
