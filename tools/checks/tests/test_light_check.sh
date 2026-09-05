#!/bin/bash
# Two-direction test for check_light_check.py, one case per audit it runs:
#   A. an unresolved conflict marker;
#   B. invalid frontmatter YAML;
#   C. a secret-shaped string (AWS-style key ID);
#   D. a broken relative markdown link.
# Plus two planted NON-violations for the derived-tree link exemption
# (real incident: this check had no exemption at all, and its own
# firing test failed against a real installing repo -- 124 planted-looking
# but unfixable findings under practices/ and process/upstream/, links
# written relative to another repo's own root):
#   E. process/upstream/ is exempt unconditionally, even with no
#      MANIFEST.json -- it's always a vendored mirror, never this repo's
#      own content;
#   F. practices/ is exempt ONLY when this repo's own MANIFEST.json shows
#      it's a materialized copy (an installing repo) -- in this repo
#      itself (the source, no MANIFEST.json), practices/ stays checked,
#      confirmed by case D above still firing on a root-level broken link
#      and by the "clean on real content" run at the bottom finding this
#      repo's own practices/ genuinely clean, not silently exempted.
# Then: the real, current, unplanted repo must stay clean.
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

run_clean_case "practices/ broken link, exempt once MANIFEST.json shows a materialized install" '
python3 -c "
import json, pathlib
pathlib.Path(\"MANIFEST.json\").write_text(json.dumps({
    \"generated_by\": \"tools/precedent_materialize.py\",
    \"note\": \"DERIVED ARTIFACT -- never hand-edit.\",
}) + \"\n\")
"
echo "[missing](templates/AGENTS.md.template)" > practices/planted-materialized.md
git add MANIFEST.json practices/planted-materialized.md
'

if ! python3 tools/checks/check_light_check.py > /dev/null; then
  echo "FAIL: check_light_check.py is not clean on the real, current repo" >&2
  exit 1
fi
echo "ok: clean on real content"
