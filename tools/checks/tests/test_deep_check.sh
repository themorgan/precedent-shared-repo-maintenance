#!/bin/bash
# Two-direction test for check_deep_check.py:
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

if python3 tools/checks/check_deep_check.py > /dev/null; then
  echo "FAIL: check_deep_check.py did not fire on a check script with no matching test" >&2
  exit 1
fi
echo "ok: fires on planted violation"

cd "$ROOT"
if ! python3 tools/checks/check_deep_check.py > /dev/null; then
  echo "FAIL: check_deep_check.py is not clean on the real, current repo" >&2
  exit 1
fi
echo "ok: clean on real content"
