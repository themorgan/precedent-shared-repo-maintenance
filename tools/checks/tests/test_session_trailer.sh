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
#
# Beside the repository, not in /tmp (2026-09-29). The check asks the
# resolver whether revert-needs-no-trailer is in force for the clone it
# judges, and a consumer's sources are relative paths (../precedent-shared-*)
# that only resolve from where the repository really lives. From /tmp none
# resolved, the exemption read as not in force, and case 4 flagged a
# consuming repo's real trailer-less revert -- a failure of the fixture's
# placement, not of the history. Case 1d's scratch clone stays in /tmp on
# purpose: it needs a clone that resolves no working-style set.
#
# Beside the MAIN checkout, not beside ROOT: the merge check runs this test
# from a worktree it makes under /tmp, where "beside ROOT" is /tmp again
# (found the same day, in a consuming repo's merge check). Git records the
# main checkout of a linked worktree; in an ordinary checkout it is ROOT.
COMMON="$(cd "$ROOT" && cd "$(git rev-parse --git-common-dir)" && pwd)"
if [ "$(basename "$COMMON")" = ".git" ]; then MAIN="$(dirname "$COMMON")"; else MAIN="$ROOT"; fi
PARENT="$(dirname "$MAIN")"
SHALLOW="$PARENT/.trailer-test-$$-shallow"
FULL="$PARENT/.trailer-test-$$-full"
SRC="$PARENT/.trailer-test-$$-src"
trap 'rm -rf "$SCRATCH" "$SHALLOW" "$FULL" "$SRC"' EXIT
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

  # 4b. ...and the clone resolves every source the real checkout resolves,
  #     so an exemption in force there is in force here. This is the
  #     property case 4 silently lost from /tmp.
  missing () {
    python3 - "$1" "$ROOT/tools" <<'PY'
import contextlib, io, json, sys
sys.path.insert(0, sys.argv[2])
with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
    import precedent_resolve as pr
    try:
        res = pr.resolve(pr.load_config(sys.argv[1]))
        out = sorted(m["name"] for m in res.get("missing") or [])
    except (Exception, SystemExit):
        out = ["<could not resolve>"]
print(json.dumps(out))
PY
  }
  if [ -f "$ROOT/tools/precedent_resolve.py" ] && [ "$(missing "$FULL")" != "$(missing "$MAIN")" ]; then
    echo "FAIL: the full clone resolves fewer sources than the real checkout ($(missing "$FULL") vs $(missing "$MAIN")) -- case 4 is judging a different set of practices" >&2
    exit 1
  fi
  echo "ok: the full clone resolves the same sources as the real checkout"

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

  # 6. a trailer-less revert, judged through the real resolver: flagged in
  #    the full clone as it stands, and passed once that clone declares a
  #    source where revert-needs-no-trailer is active. Case 1e stubs the
  #    answer; this asks the resolver the way a consuming repo does.
  (
    cd "$FULL"
    touch reverted-here.txt
    git add reverted-here.txt
    git -c user.name="Test" -c user.email="test@example.com" commit -q \
      -m "a change that will be reverted" -m "Session: https://example.invalid/session"
    git -c user.name="Test" -c user.email="test@example.com" revert --no-edit HEAD >/dev/null
  )
  mkdir -p "$SRC/practices"
  printf '%s\n' '---' 'slug:        revert-needs-no-trailer' 'status:      active' \
    '---' '## Rule' 'A revert commit may leave out the Session: trailer.' \
    > "$SRC/practices/revert-needs-no-trailer.md"
  printf '{"name": "zzz-trailer-test", "level": "shared"}\n' > "$SRC/precedent-source.json"
  in_force () {
    (cd "$ROOT" && PRECEDENT_CHECK_ROOT="$FULL" python3 -c '
import sys; sys.path.insert(0, "tools/checks")
import check_session_trailer as c
sys.exit(0 if c.revert_exemption_in_force() else 1)')
  }
  if ! in_force; then
    # The control: not in force, the same revert is flagged.
    if (cd "$ROOT" && PRECEDENT_CHECK_ROOT="$FULL" python3 tools/checks/check_session_trailer.py > /dev/null 2>&1); then
      echo "FAIL: a trailer-less revert passed while revert-needs-no-trailer was not in force" >&2
      exit 1
    fi
    python3 - "$FULL/precedent.json" "$(basename "$SRC")" <<'PY'
import json, pathlib, sys
p = pathlib.Path(sys.argv[1])
d = json.loads(p.read_text(encoding="utf-8")) if p.exists() else {"format_version": 1}
d.setdefault("sources", []).append(
    {"level": "shared", "name": "zzz-trailer-test", "path": "../" + sys.argv[2]})
p.write_text(json.dumps(d, indent=2) + "\n", encoding="utf-8")
PY
  fi
  if ! in_force; then
    echo "FAIL: case 6 could not put revert-needs-no-trailer in force through the resolver -- it would prove nothing" >&2
    exit 1
  fi
  if ! (cd "$ROOT" && PRECEDENT_CHECK_ROOT="$FULL" python3 tools/checks/check_session_trailer.py > /dev/null); then
    echo "FAIL: a trailer-less revert was flagged although revert-needs-no-trailer is in force through the resolver" >&2
    exit 1
  fi
  echo "ok: a trailer-less revert passes where the resolver puts revert-needs-no-trailer in force"
)

cd "$ROOT"
if ! python3 tools/checks/check_session_trailer.py > /dev/null; then
  echo "FAIL: check_session_trailer.py is not clean on the real, current history" >&2
  exit 1
fi
echo "ok: clean on real content"

# 7. The whole test again, from a worktree under /tmp -- the shape the merge
#    check runs it in. Once, never recursively.
if [ -z "${TRAILER_TEST_IN_WORKTREE:-}" ]; then
  WT_PARENT="$(mktemp -d)"
  WT="$WT_PARENT/tree"
  git -C "$ROOT" worktree add -q --detach "$WT" HEAD
  cleanup_wt () { git -C "$ROOT" worktree remove --force "$WT" >/dev/null 2>&1; git -C "$ROOT" worktree prune; rm -rf "$WT_PARENT"; }
  # The worktree holds HEAD; carry the files under test over, so an
  # uncommitted edit is what runs (as the rest of this test does).
  cp "$ROOT/tools/checks/check_session_trailer.py" "$WT/tools/checks/"
  cp "$ROOT/tools/checks/tests/test_session_trailer.sh" "$WT/tools/checks/tests/"
  if ! (cd "$WT" && TRAILER_TEST_IN_WORKTREE=1 bash tools/checks/tests/test_session_trailer.sh > "$WT_PARENT/out" 2>&1); then
    sed 's/^/    /' "$WT_PARENT/out" >&2
    cleanup_wt
    echo "FAIL: the test does not pass from a worktree under /tmp, as the merge check runs it" >&2
    exit 1
  fi
  cleanup_wt
  echo "ok: the whole test passes from a worktree under /tmp, as the merge check runs it"
fi
