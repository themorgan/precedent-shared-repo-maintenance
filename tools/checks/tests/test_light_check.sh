#!/bin/bash
# Two-direction test for check_light_check.py, one case per audit it runs:
#   A. an unresolved conflict marker;
#   B. invalid frontmatter YAML;
#   C. a secret-shaped string (AWS-style key ID);
#   D. a broken relative markdown link.
# Plus the derived-tree exemption, which is now ONE prefix, not two
# (real incident: this check had no exemption at all, and its own
# firing test failed against a real installing repo -- 124 planted-looking
# but unfixable findings under practices/ and process/upstream/, links
# written relative to another repo's own root):
#   E. process/upstream/ is exempt unconditionally -- always a vendored
#      mirror, never this repo's own content to fix;
#   F. a materialized practices/ is NOT exempt any more (2026-09-06).
#      That exemption was a workaround for an upstream bug -- practice
#      files were copied into a consuming repo with their links still
#      written relative to their own source repo. Precedent's
#      precedent_materialize.py repoints them now, so a broken link there
#      is a real finding again: a stale sync, or a rewrite that failed.
#      Case F plants exactly that and requires it to fire.
# Then: the real, current, unplanted repo must stay clean.
#
# NOTE, because it costs an hour every time: run_case does `git clone` of
# this repo, so it tests the COMMITTED check_light_check.py, not your
# working tree. An uncommitted change to the check appears to have no
# effect at all -- the planted case fails, and the reason is invisible.
# Commit, then run this.
set -euo pipefail
cd "$(dirname "$0")/../../.."
ROOT="$(pwd)"

run_case() {
  local label="$1"
  local mutate="$2"
  local scratch
  scratch="$(mktemp -d)"
  git clone -q "$ROOT" "$scratch"
  (
    cd "$scratch"
    eval "$mutate"
    if python3 tools/checks/check_light_check.py > /dev/null; then
      echo "FAIL: check_light_check.py did not fire on: $label" >&2
      exit 1
    fi
    echo "ok: fires on planted violation ($label)"
  )
  local status=$?
  rm -rf "$scratch"
  return $status
}

run_clean_case() {
  local label="$1"
  local mutate="$2"
  local scratch
  scratch="$(mktemp -d)"
  git clone -q "$ROOT" "$scratch"
  (
    cd "$scratch"
    eval "$mutate"
    if ! python3 tools/checks/check_light_check.py > /dev/null; then
      echo "FAIL: check_light_check.py fired on a non-violation: $label (false positive)" >&2
      exit 1
    fi
    echo "ok: stays clean on planted non-violation ($label)"
  )
  local status=$?
  rm -rf "$scratch"
  return $status
}

run_case "conflict marker" '
python3 -c "
open(\"planted-conflict.md\", \"w\").write(
    (\"<\" * 7) + \" HEAD\n\" + \"ours\n\" + (\"=\" * 7) + \"\n\" +
    \"theirs\n\" + (\">\" * 7) + \" branch\n\"
)
"
git add planted-conflict.md
'

run_case "invalid frontmatter YAML" '
cat > planted-bad-frontmatter.md <<EOF
---
slug: planted
title: This: breaks unquoted YAML
---
## Rule
Text.
EOF
git add planted-bad-frontmatter.md
'

run_case "secret-shaped string" '
python3 -c "open(\"planted-secret.txt\", \"w\").write(\"AKIA\" + \"ABCDEFGHIJKLMNOP\" + chr(10))"
git add planted-secret.txt
'

run_case "broken relative link" '
echo "[missing](./does/not/exist.md)" > planted-link.md
git add planted-link.md
'

run_clean_case "process/upstream/ broken link, exempt with no MANIFEST.json at all" '
mkdir -p process/upstream/practices
echo "[missing](tools/doc_lint.py)" > process/upstream/practices/planted.md
git add process/upstream/practices/planted.md
'

run_case "broken link in a MATERIALIZED practices/ -- no longer exempt" '
python3 -c "
import json, pathlib
pathlib.Path(\"MANIFEST.json\").write_text(json.dumps({
    \"generated_by\": \"tools/precedent_materialize.py\",
    \"note\": \"DERIVED ARTIFACT -- never hand-edit.\",
}) + \"\n\")
"
echo "[missing](../tools/does_not_exist.py)" > practices/planted-materialized.md
git add MANIFEST.json practices/planted-materialized.md
'

if ! python3 tools/checks/check_light_check.py > /dev/null; then
  echo "FAIL: check_light_check.py is not clean on the real, current repo" >&2
  exit 1
fi
echo "ok: clean on real content"
