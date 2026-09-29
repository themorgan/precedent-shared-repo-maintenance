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

# 1b-1e (2026-09-29): what a push carries, and the two exemptions.
# 1b. The same trailer-less commit, once origin has it, is no longer judged
#     by default -- it was judged at the push that carried it -- and is still
#     found by --all-history.
PLANTED="$(git rev-parse HEAD)"
git push -q origin "HEAD:refs/heads/trailer-test-landed" 2>/dev/null
git fetch -q origin "refs/heads/trailer-test-landed:refs/remotes/origin/trailer-test-landed"
git -C "$ROOT" branch -D -q trailer-test-landed
if ! python3 tools/checks/check_session_trailer.py > /dev/null; then
  echo "FAIL: judged a commit origin already has -- only what a push carries is judged" >&2
  exit 1
fi
if python3 tools/checks/check_session_trailer.py --all-history > /dev/null; then
  echo "FAIL: --all-history did not find the trailer-less commit" >&2
  exit 1
fi
if python3 tools/checks/check_session_trailer.py --range "$PLANTED~1..$PLANTED" > /dev/null; then
  echo "FAIL: an explicit --range naming the commit did not judge it" >&2
  exit 1
fi
echo "ok: judges what a push carries; --all-history and --range still reach landed commits"

# 1c. A commit GitHub made with its own buttons (committer noreply@github.com).
touch web-flow.txt
git add web-flow.txt
GIT_COMMITTER_NAME=GitHub GIT_COMMITTER_EMAIL=noreply@github.com \
  git -c user.name="Test" -c user.email="test@example.com" commit -q -m "Update web-flow.txt"
if ! python3 tools/checks/check_session_trailer.py > /dev/null; then
  echo "FAIL: flagged a commit made with GitHub's own buttons" >&2
  exit 1
fi
echo "ok: a commit GitHub's buttons made is exempt"

# 1d. A revert with no trailer fires where revert-needs-no-trailer is not in
#     force (this scratch clone resolves no working-style set) ...
git -c user.name="Test" -c user.email="test@example.com" revert --no-edit HEAD >/dev/null
if python3 tools/checks/check_session_trailer.py > /dev/null; then
  echo "FAIL: a trailer-less revert passed where the revert exemption is not in force" >&2
  exit 1
fi
# 1e. ... and passes where it is.
if ! python3 - <<'PY'
import sys
sys.path.insert(0, "tools/checks")
import check_session_trailer as c
c.revert_exemption_in_force = lambda: True
findings, _ = c.find_violations([])
sys.exit(1 if findings else 0)
PY
then
  echo "FAIL: a trailer-less revert was flagged although the revert exemption is in force" >&2
  exit 1
fi
git reset -q --hard "$PLANTED"
echo "ok: a revert is exempt only where revert-needs-no-trailer is in force"

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
  out="$(cd "$ROOT" && PRECEDENT_CHECK_ROOT="$SHALLOW" python3 tools/checks/check_session_trailer.py --all-history 2>&1)" && {
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
  if ! (cd "$ROOT" && PRECEDENT_CHECK_ROOT="$FULL" python3 tools/checks/check_session_trailer.py --all-history > /dev/null); then
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
  out="$(cd "$ROOT" && PRECEDENT_CHECK_ROOT="$SHALLOW" python3 tools/checks/check_session_trailer.py --all-history 2>&1)" && {
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
