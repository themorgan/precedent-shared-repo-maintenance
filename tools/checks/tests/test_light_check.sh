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
#   E. a mirrored tree is exempt -- always a vendored copy, never this
#      repo's own content to fix. Two cases now, because WHICH tree that
#      is stopped being a hardcoded path on 2026-09-10:
#        E1. process/upstream/ (INSTALL.md section 1's layout) with no
#            engine present -- the fallback path;
#        E2. a section 0 install, where the mirror is at whatever
#            precedent.json declares and there is NO process/manifest.json
#            and NO process/upstream/ at all. Before the fix the exclusion
#            covered nothing here and the check reported 174 unactionable
#            broken links inside the vendored catalogue;
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

# The clean cases assert on what they PLANTED, never on the exit code of
# the whole tree. This test ships into every repo that installs this set,
# and the scratch is a clone of THAT repo, so "exit 0" asks about content no
# fixture here created. E2 is where that bit (2026-09-25): its stubbed
# resolver names only its own mirror, so in a repo that also vendors
# process/upstream/ the stub stopped exempting that tree, the check reported
# the links inside it, and E2 failed with nothing wrong in the check. The
# host tree's own cleanliness is still asserted -- once, by the last line of
# this file, where it is the actual question.
#
# A non-zero exit is accepted only with the check's own VIOLATION header,
# so a crash can never pass as "the planted path was not reported".
run_clean_case() {
  local label="$1"
  local mutate="$2"
  local planted="$3"
  local scratch
  scratch="$(mktemp -d)"
  git clone -q "$ROOT" "$scratch"
  (
    cd "$scratch"
    eval "$mutate"
    local out
    if ! out="$(python3 tools/checks/check_light_check.py 2>&1)"; then
      if ! printf '%s\n' "$out" | head -n 1 | grep -q '^VIOLATION: '; then
        echo "FAIL: check_light_check.py did not run cleanly on: $label" >&2
        printf '%s\n' "$out" >&2
        exit 1
      fi
      if printf '%s' "$out" | grep -qF "$planted"; then
        echo "FAIL: check_light_check.py fired on a non-violation: $label (false positive)" >&2
        printf '%s\n' "$out" | grep -F "$planted" >&2
        exit 1
      fi
    fi
    echo "ok: stays clean on planted non-violation ($label)"
  )
  local status=$?
  rm -rf "$scratch"
  return $status
}

# Asserts the FINDING TEXT, not just a non-zero exit. A negative control
# that only proves "exited 1" proves nothing here: every one of these cases
# can exit 1 for an unrelated reason, and the mirror cases specifically are
# about WHICH path appears in the output.
run_case_expecting() {
  local label="$1"
  local mutate="$2"
  local expect="$3"
  local forbid="${4:-}"
  local scratch
  scratch="$(mktemp -d)"
  git clone -q "$ROOT" "$scratch"
  (
    cd "$scratch"
    eval "$mutate"
    local out
    if out="$(python3 tools/checks/check_light_check.py 2>&1)"; then
      echo "FAIL: check_light_check.py did not fire on: $label" >&2
      exit 1
    fi
    if ! printf '%s' "$out" | grep -qF "$expect"; then
      echo "FAIL: $label -- fired, but no finding matched: $expect" >&2
      printf '%s\n' "$out" >&2
      exit 1
    fi
    if [ -n "$forbid" ] && printf '%s' "$out" | grep -qF "$forbid"; then
      echo "FAIL: $label -- output contained what must be excluded: $forbid" >&2
      printf '%s\n' "$out" >&2
      exit 1
    fi
    echo "ok: fires with the expected finding ($label)"
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

run_clean_case "E1: process/upstream/ broken link, exempt with no MANIFEST.json at all" '
mkdir -p process/upstream/practices
echo "[missing](tools/doc_lint.py)" > process/upstream/practices/planted.md
git add process/upstream/practices/planted.md
' \
  "process/upstream/practices/planted.md"

# E2 -- THE SECTION 0 CASE, which is the whole reason the exemption stopped
# being a hardcoded "process/upstream/" on 2026-09-10. This scratch has no
# process/upstream/ and no process/manifest.json (INSTALL.md section 0 step 5
# says outright to skip the manifest); the mirror is at the path
# precedent.json declares. Under the old literal the exclusion matched
# nothing and the vendored tree was reported in full.
#
# The engine is STUBBED rather than vendored: what is under test here is
# that this check asks precedent_resolve.mirrored_prefixes() and honours the
# answer, not whether that function is itself correct -- upstream's
# verify_harness.py owns that, in
# check_mirrored_prefixes_answers_both_install_models(). A stub also keeps
# this suite self-contained, with no clone of BestPractice required to run it.
S0_SETUP='
python3 - <<PYEOF
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
d = pathlib.Path("precedent/universal/practices")
d.mkdir(parents=True, exist_ok=True)
(d / "planted.md").write_text("[missing](../tools/doc_lint.py)\n")
PYEOF
git add -A
'

run_clean_case "E2: section 0 mirror at a precedent.json-declared path, no manifest, no process/upstream/" \
  "$S0_SETUP" \
  "precedent/universal/practices/planted.md"

# ...and the same broken link OUTSIDE the mirror must still be reported, or
# E2 would be passing by having switched the link check off altogether.
run_case_expecting "E2 control: an identical broken link outside the mirror still fires" \
  "$S0_SETUP"'
echo "[missing](../tools/doc_lint.py)" > own-page.md
git add own-page.md
' \
  "own-page.md:1: broken relative link to '../tools/doc_lint.py'" \
  "precedent/universal/practices/planted.md"

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

run_clean_case "a link shown inside inline code is an example, not a link" '
echo "Write \`[the Glossary](GLOSSARY-missing.md)\`, not the filename." > planted-code-span.md
git add planted-code-span.md
' \
  "planted-code-span.md"

run_case_expecting "code-span control: the same link outside code still fires" \
  'echo "Write [the Glossary](GLOSSARY-missing.md) here." > planted-code-span.md
git add planted-code-span.md' \
  "planted-code-span.md:1: broken relative link to 'GLOSSARY-missing.md'"

if ! python3 tools/checks/check_light_check.py > /dev/null; then
  echo "FAIL: check_light_check.py is not clean on the real, current repo" >&2
  exit 1
fi
echo "ok: clean on real content"
