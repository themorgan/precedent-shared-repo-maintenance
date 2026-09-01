#!/bin/bash
# Two-direction test for check_private_repo_scrub.py:
#   1. plant a real private-repo name into a practices/*.md file -- require
#      the check to fire;
#   2. the real, current, unplanted repo -- require the check to stay clean.
set -euo pipefail
cd "$(dirname "$0")/../../.."
ROOT="$(pwd)"
SCRATCH="$(mktemp -d)"
trap 'rm -rf "$SCRATCH"' EXIT

git clone -q "$ROOT" "$SCRATCH"
cd "$SCRATCH"
printf '\nSee precedent-individual for a worked example.\n' >> practices/install.md
git add practices/install.md
git -c user.name="Test" -c user.email="test@example.com" commit -q -m "planted violation: names a private repo in vendored content"

if python3 tools/checks/check_private_repo_scrub.py > /dev/null; then
  echo "FAIL: check_private_repo_scrub.py did not fire on a planted private-repo name" >&2
  exit 1
fi
echo "ok: fires on planted violation"

cd "$ROOT"
if ! python3 tools/checks/check_private_repo_scrub.py > /dev/null; then
  echo "FAIL: check_private_repo_scrub.py is not clean on the real, current repo" >&2
  exit 1
fi
echo "ok: clean on real content"
