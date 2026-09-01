#!/bin/bash
# Two-direction test for check_light_check.py, one case per audit it runs:
#   A. an unresolved conflict marker;
#   B. invalid frontmatter YAML;
#   C. a secret-shaped string (AWS-style key ID);
#   D. a broken relative markdown link.
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

if ! python3 tools/checks/check_light_check.py > /dev/null; then
  echo "FAIL: check_light_check.py is not clean on the real, current repo" >&2
  exit 1
fi
echo "ok: clean on real content"
