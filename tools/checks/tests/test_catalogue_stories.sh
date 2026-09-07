#!/bin/bash
# Two-direction test for check_catalogue_stories.py.
#
# Builds a SYNTHETIC practices/ tree rather than cloning this repo. The
# clone-the-repo pattern the other tests use cannot work here: this check is
# a whole-tree invariant over practices/, so its negative controls need a
# baseline with no other violations in it, and a clone's baseline is whatever
# the repo's committed catalogue happens to be. Cloning made the negative
# controls fail for a reason that had nothing to do with the case under test.
#
# Cases:
#   1. active practice, empty ## Story            -> must fire
#   2. non-active (deduplicated), empty ## Story  -> must stay clean
#   3. active practice, whitespace-only Story     -> must fire
#   4. active, real Story, but the word "status:" in its PROSE -> must stay
#      clean. A loose search for status: anywhere in the file would read the
#      prose and mis-scope the check; several real practices here discuss the
#      status vocabulary directly.
#   5. active practice with no ## Story section at all -> must fire
#   6. the real, current repo -> must stay clean
set -euo pipefail
cd "$(dirname "$0")/../../.."
ROOT="$(pwd)"
SCRATCH="$(mktemp -d)"
trap 'rm -rf "$SCRATCH"' EXIT

mkdir -p "$SCRATCH/tools/checks" "$SCRATCH/practices"
cp tools/checks/check_catalogue_stories.py "$SCRATCH/tools/checks/"
cp practices/catalogue-carries-stories.md "$SCRATCH/practices/"
# Assert rather than trust: if either file were missing, python3 would exit 1
# for "no such file" and every "must fire" case below would be a false pass.
# That is not hypothetical -- it is what this test did on its first run.
test -f "$SCRATCH/tools/checks/check_catalogue_stories.py" || { echo "FAIL: check script missing from fixture" >&2; exit 1; }
test -f "$SCRATCH/practices/catalogue-carries-stories.md" || { echo "FAIL: practice file missing from fixture" >&2; exit 1; }

CHECK="$SCRATCH/tools/checks/check_catalogue_stories.py"

plant() {  # $1 = filename, $2 = status, $3 = story body, $4 = extra Rule prose
  cat > "$SCRATCH/practices/$1" <<PLANTED
---
slug:        planted
title:       Planted fixture
tier:        on-demand
severity:    default
applies_to:  ["**"]
occasion:    "never"
gates:       []
index_clause: "planted"
checked_by:  null
defines:     []
status:      $2
supersedes:  []
overrides:   null
added:       2026-09-07
approved_by: "test"
---
## Rule
Planted. $4

## Why
Planted.

## Story
$3

## Install
Planted.
PLANTED
}

# Sanity: the fixture with only the real practice in it must be clean, or
# every negative control below proves nothing.
python3 "$CHECK" > /dev/null || { echo "FAIL: baseline fixture is not clean" >&2; exit 1; }
echo "ok: baseline fixture is clean"

plant "p.md" active "" ""
if python3 "$CHECK" > /dev/null; then
  echo "FAIL: did not fire on an active practice with an empty ## Story" >&2; exit 1
fi
echo "ok: fires on planted violation (active, empty Story)"

plant "p.md" deduplicated "" ""
if ! python3 "$CHECK" > /dev/null; then
  echo "FAIL: fired on a non-active practice, which is out of scope" >&2; exit 1
fi
echo "ok: stays clean on planted non-violation (deduplicated, empty Story)"

plant "p.md" active "   " ""
if python3 "$CHECK" > /dev/null; then
  echo "FAIL: did not fire on a whitespace-only ## Story" >&2; exit 1
fi
echo "ok: fires on planted violation (whitespace-only Story)"

plant "p.md" active "A real recorded incident." "It mentions status: retired in its own prose."
if ! python3 "$CHECK" > /dev/null; then
  echo "FAIL: fired on a practice whose PROSE contains 'status:' -- the check is reading prose, not frontmatter" >&2; exit 1
fi
echo "ok: stays clean on planted non-violation (status: in prose, not frontmatter)"

python3 - "$SCRATCH/practices/p.md" <<'PY'
import pathlib, re, sys
p = pathlib.Path(sys.argv[1])
p.write_text(re.sub(r"\n## Story\n.*?(?=\n## Install)", "", p.read_text(), flags=re.S))
PY
if python3 "$CHECK" > /dev/null; then
  echo "FAIL: did not fire on a practice with no ## Story section at all" >&2; exit 1
fi
echo "ok: fires on planted violation (no ## Story section at all)"

# 7. the consuming-repo case: an empty-Story practice that a committed
#    MANIFEST.json attributes to ANOTHER source -> must stay clean. Without
#    this, every repo consuming this set would go red on the universal
#    catalogue's own empty Stories -- real findings, unactionable where
#    reported. Reproduced here rather than reasoned about: the universal
#    catalogue really did have 30 of 65 empty when this was written.
rm -f "$SCRATCH/practices/p.md"   # case 5 left it Story-less on purpose
plant "foreign.md" active "" ""
cat > "$SCRATCH/MANIFEST.json" <<'JSON'
{"practices": [{"slug": "foreign", "level": "universal"}]}
JSON
if ! python3 "$CHECK" > /dev/null; then
  echo "FAIL: fired on a practice a committed MANIFEST.json attributes to another source -- unactionable where reported" >&2; exit 1
fi
echo "ok: stays clean on planted non-violation (empty Story owned by another source)"

# 8. same manifest, but the practice is attributed to THIS repo -> must fire.
#    Without this, case 7 would pass even if _foreign_practice always returned
#    true, which would disable the check entirely in every consuming repo.
cat > "$SCRATCH/MANIFEST.json" <<'JSON'
{"practices": [{"slug": "foreign", "level": "repo-local"}]}
JSON
if python3 "$CHECK" > /dev/null; then
  echo "FAIL: did not fire on an empty Story this repo owns, with a manifest present" >&2; exit 1
fi
echo "ok: fires on planted violation (empty Story owned here, manifest present)"
rm -f "$SCRATCH/MANIFEST.json" "$SCRATCH/practices/foreign.md"

cd "$ROOT"
if ! python3 tools/checks/check_catalogue_stories.py > /dev/null; then
  echo "FAIL: check_catalogue_stories.py is not clean on the real, current repo" >&2; exit 1
fi
echo "ok: clean on real content"
