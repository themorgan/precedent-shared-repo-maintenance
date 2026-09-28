#!/bin/bash
# Two-direction test for check_deep_check.py (the first also asserts what
# its findings tell the author to write):
#   1. plant a check script with no matching test -- require the check to
#      fire (run_all.sh's test_*.sh glob would silently never exercise it);
#   2. the real, current, unplanted repo -- require the check to stay clean.
set -euo pipefail
cd "$(dirname "$0")/../../.."
ROOT="$(pwd)"
SCRATCH="$(mktemp -d)"
trap 'rm -rf "$SCRATCH"' EXIT

git clone -q "$ROOT" "$SCRATCH"
cd "$SCRATCH"
cat > tools/checks/check_planted_orphan.py <<'EOF'
#!/usr/bin/env python3
import sys
sys.exit(0)
EOF
git add tools/checks/check_planted_orphan.py
git -c user.name="Test" -c user.email="test@example.com" commit -q -m "planted violation: orphaned check script with no test"

if out="$(python3 tools/checks/check_deep_check.py)"; then
  echo "FAIL: check_deep_check.py did not fire on a check script with no matching test" >&2
  exit 1
fi
echo "ok: fires on planted violation"

# The finding must say what to write, not only what is missing: a repo-local
# check landed without either in a consumer repo, and the author had to work
# out the test path and the SOURCE_ROOT lines from the check's source
# (2026-09-28).
if ! grep -qF 'Add tools/checks/tests/test_planted_orphan.sh' <<<"$out"; then
  echo "FAIL: the missing-test finding does not name the test path to add" >&2
  echo "$out" >&2
  exit 1
fi
if ! grep -qF 'SOURCE_ROOT = pathlib.Path(__file__).resolve().parent.parent.parent' <<<"$out"; then
  echo "FAIL: the SOURCE_ROOT finding does not give the line to write" >&2
  echo "$out" >&2
  exit 1
fi
echo "ok: the finding names the test path and the SOURCE_ROOT line"

# A missing run_all.sh in the engine's own origin -- a repo whose
# precedent.json declares the repo itself as a source (path ".") -- is
# SKIPPED, not a violation: its tests run through its own harness. Run
# against BestPractice, this check failed the very deep check every time
# (2026-09-28). The control is the same tree declaring only other sources,
# which is every consumer and every practice set: it must still fail.
# Both run against a planted fixture root, so this repo's own precedent.json
# is untouched and whatever it declares cannot decide the outcome.
plant_root_without_driver() {  # $1 = the source path to declare
  local fixture
  fixture="$(mktemp -d)"
  mkdir -p "$fixture/tools/checks"
  printf '{"format_version": 1, "sources": [{"name": "s", "level": "universal", "path": "%s"}]}\n' \
    "$1" > "$fixture/precedent.json"
  printf '%s' "$fixture"
}
FIXTURE="$(plant_root_without_driver .)"
code=0
out="$(PRECEDENT_CHECK_ROOT="$FIXTURE" python3 "$SCRATCH/tools/checks/check_deep_check.py")" || code=$?
rm -rf "$FIXTURE"
if [ "$code" -ne 2 ] || ! grep -q '^SKIPPED: .*run_all.sh is missing' <<<"$out"; then
  echo "FAIL: a missing run_all.sh in a repo that declares itself as a source (path \".\") was not SKIPPED (exit $code)" >&2
  echo "$out" >&2
  exit 1
fi
echo "ok: SKIPPED, not failed, in the engine's own origin"
FIXTURE="$(plant_root_without_driver ../a-sibling-source)"
code=0
out="$(PRECEDENT_CHECK_ROOT="$FIXTURE" python3 "$SCRATCH/tools/checks/check_deep_check.py")" || code=$?
rm -rf "$FIXTURE"
if [ "$code" -ne 1 ] || ! grep -q 'run_all.sh is missing' <<<"$out"; then
  echo "FAIL: a missing run_all.sh in a repo that does NOT declare itself was not reported (exit $code)" >&2
  echo "$out" >&2
  exit 1
fi
echo "ok: still fires on a missing run_all.sh anywhere else"

cd "$ROOT"
if ! python3 tools/checks/check_deep_check.py > /dev/null; then
  echo "FAIL: check_deep_check.py is not clean on the real, current repo" >&2
  exit 1
fi
echo "ok: clean on real content"
