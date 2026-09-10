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

# MIRROR SCOPE (added 2026-09-10). A derived file inside a tree this repo
# mirrors from elsewhere is the source repo's to fix -- the copy here is
# overwritten by the next sync, so a finding against it is unactionable by
# construction. Until this date the check walked every tracked file with no
# exclusion at all; it had simply never fired inside a mirror because
# nothing in the vendored catalogue happened to open with a "DERIVED from"
# line, which is luck rather than scope.
#
# Both directions are planted from ONE byte-identical file, so the only
# variable is where it sits. The engine is stubbed for the same reason
# test_light_check.sh stubs it: what is under test is that this check asks
# precedent_resolve.mirrored_prefixes() and honours the answer, not whether
# that function is itself correct.
SCRATCH3="$(mktemp -d)"
(
  set -e
  git clone -q "$ROOT" "$SCRATCH3"
  cd "$SCRATCH3"
  python3 - <<'PYEOF'
import json, pathlib
pathlib.Path("precedent.json").write_text(json.dumps({
    "format_version": 1,
    "sources": [{"name": "universal", "level": "universal",
                 "path": "precedent/universal"}],
}) + "\n")
pathlib.Path("tools/precedent_resolve.py").write_text(
    "def mirrored_prefixes(repo):\n"
    "    return (\"precedent/universal/\",)\n"
)
header = ("<!-- DERIVED from upstream/spec.yaml @ abc1234\n"
          "     Regenerate with: make regen -->\n"
          "# Planted\n")
d = pathlib.Path("precedent/universal/practices")
d.mkdir(parents=True, exist_ok=True)
(d / "planted-derived.md").write_text(header)
PYEOF
  git add -A
  git -c user.name="Test" -c user.email="test@example.com" commit -q -m "incomplete DERIVED header, inside the mirror"
  if ! python3 tools/checks/check_derived_file_marker.py > /dev/null; then
    echo "FAIL: reported an incomplete DERIVED header inside a mirrored tree -- not this repo's to fix" >&2
    exit 1
  fi
  echo "ok: silent on an incomplete DERIVED header inside a mirror"

  # The SAME file outside the mirror must still fire, or the case above is
  # passing because the check stopped looking at anything.
  cp precedent/universal/practices/planted-derived.md own-derived.md
  git add own-derived.md
  git -c user.name="Test" -c user.email="test@example.com" commit -q -m "the identical file, outside the mirror"
  out="$(python3 tools/checks/check_derived_file_marker.py 2>&1)" && {
    echo "FAIL: the identical file outside the mirror did not fire" >&2
    exit 1
  }
  if ! printf '%s' "$out" | grep -qF 'own-derived.md: claims DERIVED from but is missing `Recipe: <path>` line'; then
    echo "FAIL: fired, but not with the expected finding for own-derived.md" >&2
    printf '%s\n' "$out" >&2
    exit 1
  fi
  if printf '%s' "$out" | grep -qF "precedent/universal/"; then
    echo "FAIL: the mirrored copy was reported too -- the exclusion is not holding" >&2
    printf '%s\n' "$out" >&2
    exit 1
  fi
  echo "ok: the identical file OUTSIDE the mirror still fires, and only it"
)
status=$?
rm -rf "$SCRATCH3"
if [ "$status" -ne 0 ]; then
  exit "$status"
fi

cd "$ROOT"
if ! python3 tools/checks/check_derived_file_marker.py > /dev/null; then
  echo "FAIL: check_derived_file_marker.py is not clean on the real, current repo" >&2
  exit 1
fi
echo "ok: clean on real content"
