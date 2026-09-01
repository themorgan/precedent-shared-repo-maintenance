#!/bin/bash
# Two-direction test for check_header_caps.py:
#   1. plant two same-rank headers in one document that capitalize the
#      same shared word differently -- require the check to fire;
#   2. the real, current, unplanted repo -- require the check to stay clean.
set -euo pipefail
cd "$(dirname "$0")/../../.."
ROOT="$(pwd)"
SCRATCH="$(mktemp -d)"
trap 'rm -rf "$SCRATCH"' EXIT

git clone -q "$ROOT" "$SCRATCH"
cd "$SCRATCH"
cat > planted-headers.md <<'EOF'
# A Document

## The Quick Fix for Widgets

Some prose.

## Rolling out the quick Update

More prose.
EOF
git add planted-headers.md
git -c user.name="Test" -c user.email="test@example.com" commit -q -m "planted violation: mixed header capitalization at the same rank"

if python3 tools/checks/check_header_caps.py > /dev/null; then
  echo "FAIL: check_header_caps.py did not fire on inconsistently capitalized same-rank headers" >&2
  exit 1
fi
echo "ok: fires on planted violation"

cd "$ROOT"
if ! python3 tools/checks/check_header_caps.py > /dev/null; then
  echo "FAIL: check_header_caps.py is not clean on the real, current repo" >&2
  exit 1
fi
echo "ok: clean on real content"
