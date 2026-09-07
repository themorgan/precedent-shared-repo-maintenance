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

# A complete marker whose routing sentence WRAPS is still complete. Two real
# derived files were reported as missing it because the line break fell
# between "replaces" and "this file" (2026-09-06).
SCRATCH2="$(mktemp -d)"
(
  set -e
  git clone -q "$ROOT" "$SCRATCH2"
  cd "$SCRATCH2"
  mkdir -p content
  cat > content/WRAPPED.md <<'DOC'
<!-- DERIVED from content/SOURCE.md @ abc1234
     Recipe: content/doc-recipes/WRAPPED.recipe.md
     Regenerate with: rewrite this page per the recipe.
     Edits here are safe to make but not durable — regeneration replaces
     this file. To make a change stick, edit the source or the recipe. -->

# Wrapped
DOC
  git add -A
  git -c user.name="Test" -c user.email="test@example.com" commit -q -m "derived file with a wrapped routing sentence"
  if ! python3 tools/checks/check_derived_file_marker.py > /dev/null; then
    echo "FAIL: reported a complete marker as incomplete because its routing sentence wrapped" >&2
    exit 1
  fi
  echo "ok: a wrapped routing sentence still counts"
)
status=$?
rm -rf "$SCRATCH2"
if [ "$status" -ne 0 ]; then
  exit "$status"
fi

cd "$ROOT"
if ! python3 tools/checks/check_derived_file_marker.py > /dev/null; then
  echo "FAIL: check_derived_file_marker.py is not clean on the real, current repo" >&2
  exit 1
fi
echo "ok: clean on real content"
