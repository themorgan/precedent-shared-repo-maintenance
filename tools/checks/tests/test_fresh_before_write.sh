#!/bin/bash
# Two-direction test for check_fresh_before_write.py, one case per
# invariant it holds:
#   A. the guard loses its tracked executable bit;
#   B. the guard's one allowed automatic operation is swapped for a
#      destructive one the practice rules out by name;
#   C. session-start gains a non-zero exit (it must never wedge a session);
#   D. pre-write stops blocking on a checkout it could not verify (the
#      "a skip reads as a pass" inversion this whole practice exists for);
#   E. pre-write starts blocking git commands (which would leave a session
#      unable to run the remedy the block itself names);
#   F. Bash is dropped from the PreToolUse matcher (an agent editing files
#      through cat/sed in Bash would never trigger the guard at all);
#   G. the base branch stops being passed explicitly;
#   H. nothing wires the guard at all.
# Then: the real, current, unplanted repo must stay clean.
set -euo pipefail
cd "$(dirname "$0")/../../.."
ROOT="$(pwd)"

run_case() {
  local label="$1"
  local mutate="$2"
  # A mutation that manipulates bootstrap/ is a claim about THIS repo's own
  # publishing path -- the canonical script and settings snippet that only the
  # publisher carries. A consuming repo materializes this test too (its test
  # driver started being generated on 2026-09-06), and there the mutation dies
  # on a missing file: "chmod: cannot access 'bootstrap/...': No such file or
  # directory", which reads like a broken test rather than an inapplicable one.
  # Skipped explicitly, and only for the cases that actually need that path --
  # every other direction, including the final clean-on-real-content check,
  # still runs everywhere.
  if [[ "$mutate" == *bootstrap/* || "$mutate" == *" bootstrap"* ]] && [ ! -d "$ROOT/bootstrap" ]; then
    echo "skip: $label -- needs this repo's own bootstrap/ publishing path, which a consuming repo does not have"
    return 0
  fi
  local scratch
  scratch="$(mktemp -d)"
  git clone -q "$ROOT" "$scratch"
  (
    cd "$scratch"
    eval "$mutate"
    if python3 tools/checks/check_fresh_before_write.py > /dev/null; then
      echo "FAIL: check_fresh_before_write.py did not fire on: $label" >&2
      exit 1
    fi
    echo "ok: fires on planted violation ($label)"
  )
  local status=$?
  rm -rf "$scratch"
  return $status
}

run_case "executable bit dropped" '
chmod -x bootstrap/freshness-guard.sh
git add bootstrap/freshness-guard.sh
'

run_case "fast-forward swapped for a hard reset" '
python3 - <<PY
import pathlib
p = pathlib.Path("bootstrap/freshness-guard.sh")
p.write_text(p.read_text().replace("merge --ff-only", "reset --hard"))
PY
'

run_case "session-start can exit non-zero" '
python3 - <<PY
import pathlib
p = pathlib.Path("bootstrap/freshness-guard.sh")
p.write_text(p.read_text().replace("mode_session_start() {", "mode_session_start() {\n  exit 7", 1))
PY
'

run_case "pre-write stops blocking what it cannot verify" '
python3 - <<PY
import pathlib
p = pathlib.Path("bootstrap/freshness-guard.sh")
p.write_text(p.read_text().replace("mode_pre_write() {", "mode_pre_write() {\n  exit 0", 1))
PY
'

run_case "pre-write starts blocking git commands" '
python3 - <<PY
import pathlib
p = pathlib.Path("bootstrap/freshness-guard.sh")
t = p.read_text()
old = "    git\\\\ *|git) exit 0 ;;"
assert old in t, "the git exemption line moved -- update this plant"
p.write_text(t.replace(old, "    git\\\\ *|git) : ;;"))
PY
'

run_case "Bash dropped from the PreToolUse matcher" '
python3 - <<PY
import json, pathlib
for name in ("bootstrap/freshness.snippet.json", ".claude/settings.json"):
    p = pathlib.Path(name)
    d = json.loads(p.read_text())
    for entry in d["hooks"]["PreToolUse"]:
        entry["matcher"] = "Edit|Write|NotebookEdit"
    p.write_text(json.dumps(d, indent=2))
PY
'

run_case "base branch no longer passed explicitly" '
python3 - <<PY
import json, pathlib
for name in ("bootstrap/freshness.snippet.json", ".claude/settings.json"):
    p = pathlib.Path(name)
    d = json.loads(p.read_text())
    for event in ("SessionStart", "PreToolUse"):
        for entry in d["hooks"][event]:
            for hook in entry["hooks"]:
                hook["command"] = " ".join(hook["command"].split()[:2])
    p.write_text(json.dumps(d, indent=2))
PY
'

run_case "nothing wires the guard at all" '
git rm -q bootstrap/freshness.snippet.json .claude/settings.json
'

if ! python3 tools/checks/check_fresh_before_write.py > /dev/null; then
  echo "FAIL: check_fresh_before_write.py is not clean on the real, current repo" >&2
  exit 1
fi
echo "ok: clean on real content"
