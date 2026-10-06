#!/bin/bash
# Test for check_default_branch.py, against a local bare "remote" whose
# HEAD points at `trunk`, so nothing depends on a real host:
#   1. precedent.json declares `trunk: main`     -- require the check to fire;
#   2. precedent.json declares `trunk: trunk`    -- require it clean (the
#      trunk's name is the repo's own, 2026-10-05);
#   3. no `trunk`, `base_branch: main`           -- require COULD NOT VERIFY
#      (exit 2), never a violation;
#   4. the real repo's actual origin             -- require it clean.
set -euo pipefail
cd "$(dirname "$0")/../../.."
ROOT="$(pwd)"
SCRATCH="$(mktemp -d)"
trap 'rm -rf "$SCRATCH"' EXIT

BARE="$SCRATCH/bare-remote.git"
git init -q --bare -b trunk "$BARE"
WORK="$SCRATCH/work"
git clone -q "$BARE" "$WORK"
(
  cd "$WORK"
  git -c user.name="Test" -c user.email="test@example.com" commit -q --allow-empty -m "init"
  git push -q origin trunk
)

CHECKOUT="$SCRATCH/checkout"
git clone -q "$ROOT" "$CHECKOUT"
cp "$ROOT/tools/checks/check_default_branch.py" "$CHECKOUT/tools/checks/"
cd "$CHECKOUT"
git remote set-url origin "$BARE"

declare_json() {
  python3 - "$1" "$2" <<'PY'
import json, sys
p = "precedent.json"
d = json.load(open(p, encoding="utf-8"))
d.pop("trunk", None)
d.pop("base_branch", None)
if sys.argv[1]:
    d["trunk"] = sys.argv[1]
if sys.argv[2]:
    d["base_branch"] = sys.argv[2]
json.dump(d, open(p, "w", encoding="utf-8"), indent=2)
PY
}

declare_json main main
status=0; python3 tools/checks/check_default_branch.py > /dev/null || status=$?
if [ "$status" -ne 1 ]; then
  echo "FAIL: did not fire when the declared trunk is 'main' and the host's default is 'trunk' (exit $status)" >&2
  exit 1
fi
echo "ok: fires on planted violation"

declare_json trunk main
if ! python3 tools/checks/check_default_branch.py > /dev/null; then
  echo "FAIL: fired although the declared trunk 'trunk' is the host's default" >&2
  exit 1
fi
echo "ok: clean when the trunk is not called main"

declare_json "" main
status=0; python3 tools/checks/check_default_branch.py > /dev/null || status=$?
if [ "$status" -ne 2 ]; then
  echo "FAIL: an undeclared trunk with base_branch != host default should be COULD NOT VERIFY (exit 2), got $status" >&2
  exit 1
fi
echo "ok: undeclared trunk asks rather than fails"

cd "$ROOT"
status=0
python3 tools/checks/check_default_branch.py > /dev/null || status=$?
if [ "$status" -eq 2 ]; then
  echo "SKIPPED: could not reach the real origin from this environment -- not a check failure"
elif [ "$status" -ne 0 ]; then
  echo "FAIL: check_default_branch.py is not clean on the real repo's actual origin" >&2
  exit 1
else
  echo "ok: clean on real content"
fi
