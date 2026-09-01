#!/bin/bash
# Two-direction test for check_derived_file_marker.py:
#   1. plant a file that claims DERIVED from but is missing a required
#      field -- require the check to fire;
#   2. the real, current, unplanted repo -- require the check to stay clean.
set -euo pipefail
cd "$(dirname "$0")/../../.."
ROOT="$(pwd)"
SCRATCH="$(mktemp -d)"
trap 'rm -rf "$SCRATCH"' EXIT

git clone -q "$ROOT" "$SCRATCH"
cd "$SCRATCH"
cat > planted-derived.txt <<'EOF'
DERIVED from source/spec.yaml @ abc1234
Regenerate with: make regen
edits here are safe to make but not durable
EOF
git add planted-derived.txt
git -c user.name="Test" -c user.email="test@example.com" commit -q -m "planted violation: missing Recipe: line"

if python3 tools/checks/check_derived_file_marker.py > /dev/null; then
  echo "FAIL: check_derived_file_marker.py did not fire on a planted incomplete header" >&2
  exit 1
fi
echo "ok: fires on planted violation"

cd "$ROOT"
if ! python3 tools/checks/check_derived_file_marker.py > /dev/null; then
  echo "FAIL: check_derived_file_marker.py is not clean on the real, current repo" >&2
  exit 1
fi
echo "ok: clean on real content"
