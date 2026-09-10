#!/bin/bash
# Two-direction test for check_session_trailer.py:
#   1. plant a commit with no Session: trailer -- require the check to fire;
#   2. the real, current, unplanted history -- require the check to stay clean.
# Plus the three TRUNCATED-HISTORY states (added 2026-09-10). This is a
# `Scope: tree` check that walks `git log`, and on a shallow clone the walk
# stops at the graft boundary, finds nothing beyond it, and used to exit 0 --
# "clean" and "could not look" produced the same green. Measured in this repo
# on the clone that session started from: 101 commits visible and the check
# said clean; after `git fetch --depth=1000 origin main`, 114. Thirteen
# commits had never been examined and nothing said so.
#   3. shallow, nothing visible to report -> exit 2 SKIPPED, naming the reason;
#   4. NOT shallow, clean -> exit 0, unchanged;
#   5. shallow, but a violation IS visible -> exit 1, still fires. A partial
#      view can only COST findings, never invent them, so what it did see is
#      trustworthy -- the only thing it must not do is report the repo clean.
set -euo pipefail
cd "$(dirname "$0")/../../.."
ROOT="$(pwd)"
SCRATCH="$(mktemp -d)"
trap 'rm -rf "$SCRATCH"' EXIT

git clone -q "$ROOT" "$SCRATCH"
cd "$SCRATCH"
touch planted-violation.txt
git add planted-violation.txt
git -c user.name="Test" -c user.email="test@example.com" commit -q -m "planted violation: no session trailer at all"

if python3 tools/checks/check_session_trailer.py > /dev/null; then
  echo "FAIL: check_session_trailer.py did not fire on a commit with no Session: trailer" >&2
  exit 1
fi
echo "ok: fires on planted violation"

# Cases 3-5. Cloned with file:// on purpose -- git ignores --depth for a
# plain local path clone and hardlinks the whole object store instead, so a
# path clone would silently not be shallow and case 3 would prove nothing.
SHALLOW="$(mktemp -d)"
FULL="$(mktemp -d)"
rmdir "$SHALLOW" "$FULL"
trap 'rm -rf "$SCRATCH" "$SHALLOW" "$FULL"' EXIT
(
  set -e
  git clone -q --depth 1 "file://$ROOT" "$SHALLOW" 2>/dev/null
  if [ "$(git -C "$SHALLOW" rev-parse --is-shallow-repository)" != "true" ]; then
    echo "FAIL: could not build a shallow clone -- cases 3 and 5 would be vacuous" >&2
    exit 1
  fi

  # 3. shallow, nothing to report -> must SKIP (2), not pass (0).
  out="$(cd "$ROOT" && PRECEDENT_CHECK_ROOT="$SHALLOW" python3 tools/checks/check_session_trailer.py 2>&1)" && {
    echo "FAIL: reported a shallow clone CLEAN -- it never walked most of the history" >&2
    exit 1
  }
  code=$?
  if [ "$code" -ne 2 ]; then
    echo "FAIL: shallow clone exited $code, expected 2 (the could-not-run convention)" >&2
    printf '%s\n' "$out" >&2
    exit 1
  fi
  if ! printf '%s' "$out" | grep -qF "SKIPPED: session-trailer: this is a shallow clone"; then
    echo "FAIL: exited 2 but did not say WHY it could not look" >&2
    printf '%s\n' "$out" >&2
    exit 1
  fi
  echo "ok: a shallow clone reports SKIPPED with a reason, not clean"

  # 4. a full clone of the same history -> exit 0, behaviour unchanged.
  git clone -q "file://$ROOT" "$FULL" 2>/dev/null
  if [ "$(git -C "$FULL" rev-parse --is-shallow-repository)" != "false" ]; then
    echo "FAIL: the control clone is shallow too -- case 4 would be vacuous" >&2
    exit 1
  fi
  if ! (cd "$ROOT" && PRECEDENT_CHECK_ROOT="$FULL" python3 tools/checks/check_session_trailer.py > /dev/null); then
    echo "FAIL: a FULL clone of a clean history did not come back clean" >&2
    exit 1
  fi
  echo "ok: a full clone of the same history is still clean"

  # 5. shallow, but the violation is inside the visible slice -> still fires.
  (
    cd "$SHALLOW"
    touch planted-in-shallow.txt
    git add planted-in-shallow.txt
    git -c user.name="Test" -c user.email="test@example.com" commit -q -m "planted violation: no session trailer at all"
  )
  out="$(cd "$ROOT" && PRECEDENT_CHECK_ROOT="$SHALLOW" python3 tools/checks/check_session_trailer.py 2>&1)" && {
    echo "FAIL: a violation visible inside the shallow slice was not reported" >&2
    exit 1
  }
  code=$?
  if [ "$code" -ne 1 ]; then
    echo "FAIL: expected exit 1 for a visible violation, got $code -- shallowness must not mask a real finding" >&2
    printf '%s\n' "$out" >&2
    exit 1
  fi
  if ! printf '%s' "$out" | grep -qF 'no `Session:` trailer in the commit message'; then
    echo "FAIL: exited 1 but not with the session-trailer finding" >&2
    printf '%s\n' "$out" >&2
    exit 1
  fi
  echo "ok: a violation visible in a shallow slice still fires (1), not skipped"
)

cd "$ROOT"
if ! python3 tools/checks/check_session_trailer.py > /dev/null; then
  echo "FAIL: check_session_trailer.py is not clean on the real, current history" >&2
  exit 1
fi
echo "ok: clean on real content"
