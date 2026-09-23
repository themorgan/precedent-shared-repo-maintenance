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
#   H. nothing wires the guard at all;
#   I. pre-write goes back to blocking a branch that has merely not been
#      pushed yet -- the original bug, where the first write of every new
#      branch was refused and `precedent.freshness.override` was offered as
#      the way out;
#   J. the naive fix for I -- never blocking on a failed fetch -- which
#      inverts D. I and J are planted separately on purpose: each is the
#      other's over-correction, and the guard can only pass both by telling
#      an unreachable remote apart from a merely absent branch.
#   K. PRECEDENT_FRESHNESS_ALSO stops being read, reopening the cross-repo
#      gap: a repo the session merely has ATTACHED goes unchecked, because a
#      hook only ever fires for the project dir;
#   L. the over-correction to K -- blocking on an entry that cannot be
#      resolved at all, so a typo in a config value wedges the session.
#      Planted in the pre-write loop, not in _also_resolve: that runs in a
#      command substitution, so an exit there cannot reach the caller.
#   M. a leading `~` in an also-entry stops being expanded, so the entry
#      names nothing, is skipped as "not a git repository", and the repo goes
#      unchecked while the variable reads as correctly configured;
#   N. an empty hook payload is reported as a missing jq and python3 --
#      fail-open either way, but the message sends whoever reads it after two
#      tools that are installed.
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
    # A plant that could not find its anchor has NOT produced evidence either
    # way: the check never saw a broken guard, so "it did not fire" says
    # nothing about the check. That is a skip, and it says why -- never a
    # pass, and never a FAIL blamed on the check (practice:
    # fixture-owns-its-state). The guard is canonical upstream and this
    # fixture does not own it, so its internals can move underneath us; what
    # this must never do is report the check broken when what moved was the
    # guard.
    if [ -f .plant-could-not-anchor ]; then
      echo "SKIPPED (not a pass): $label -- $(cat .plant-could-not-anchor)"
      exit 0
    fi
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
if not (old in t):
    pathlib.Path(".plant-could-not-anchor").write_text("the git exemption line moved -- update this plant")
    raise SystemExit(0)
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

run_case "pre-write blocks a branch that is merely unpushed" '
python3 - <<PY
import pathlib
# ANCHORED ON THE GUARD OWN MESSAGE, not on its shell structure. The guard is
# canonical upstream: its function names and control flow are not ours and
# have already moved once -- a _remote_branch_state / case-esac split this
# plant used to index into, replaced upstream by _branch_absent_from_origin
# and if/elif. Its user-facing wording is the part the check actually tests,
# so that is the stable thing to hold on to. The pre-write copy is the LAST
# of two: session-start carries the same sentence earlier in the file.
p = pathlib.Path("bootstrap/freshness-guard.sh")
lines = p.read_text().splitlines(True)
hits = [i for i, l in enumerate(lines) if "does not exist on origin yet" in l and l.strip().startswith("echo ")]
if not hits:
    pathlib.Path(".plant-could-not-anchor").write_text(
        "the guard no longer notes an unpushed branch in the words this plant anchors on "
        "(does not exist on origin yet), so the unpushed case could not be planted")
else:
    lines[hits[-1]] = "    _block " + chr(34) + "planted: blocks a merely unpushed branch" + chr(34) + "\n"
    p.write_text("".join(lines))
PY
'

run_case "pre-write stops blocking on a failed fetch" '
python3 - <<PY
import pathlib
# Same anchoring rule as the case above, on the other half of the same
# decision: the guard REFUSES when it could not fetch, and this plant removes
# that refusal so the check must notice. The _block line carries the wording
# the practice quotes -- a check that could not run is not a check that
# passed -- which is why it is the anchor rather than the surrounding shell.
p = pathlib.Path("bootstrap/freshness-guard.sh")
lines = p.read_text().splitlines(True)
hits = [i for i, l in enumerate(lines) if "could not fetch origin/" in l and "_block" in l]
if not hits:
    pathlib.Path(".plant-could-not-anchor").write_text(
        "the guard no longer refuses a failed fetch in the words this plant anchors on "
        "(_block ... could not fetch origin/), so the failed-fetch case could not be planted")
else:
    lines[hits[-1]] = "    true  # planted: no longer blocks on a failed fetch\n"
    p.write_text("".join(lines))
PY
'

run_case "PRECEDENT_FRESHNESS_ALSO is ignored" '
python3 - <<PY
import pathlib
D = chr(36); Q = chr(34)
p = pathlib.Path("bootstrap/freshness-guard.sh")
t = p.read_text()
old = "  local raw=" + Q + D + "{PRECEDENT_FRESHNESS_ALSO:-}" + Q
if not (old in t):
    pathlib.Path(".plant-could-not-anchor").write_text("the also-list parser moved -- update this plant")
    raise SystemExit(0)
p.write_text(t.replace(old, "  local raw=" + Q + Q))
PY
'

run_case "an unresolvable also-entry blocks instead of being skipped" '
python3 - <<PY
import pathlib
D = chr(36); Q = chr(34)
p = pathlib.Path("bootstrap/freshness-guard.sh")
t = p.read_text()
needle = "    resolved=" + Q + D + "(_also_resolve " + Q + D + "entry" + Q + ")" + Q + " || continue"
if not (t.count(needle) == 2):
    pathlib.Path(".plant-could-not-anchor").write_text("the resolve-or-skip line moved -- update this plant")
    raise SystemExit(0)
i = t.index(needle, t.index(needle) + 1)
blocker = needle.replace("|| continue", "|| _block " + Q + "unresolvable entry." + Q)
p.write_text(t[:i] + blocker + t[i + len(needle):])
PY
'

run_case "a tilde in an also-entry stops being expanded" '
python3 - <<PY
import pathlib
# ANCHORED ON THE TILDE CASE ARMS THEMSELVES, not on a count of lines that
# merely mention HOME. The old plant required exactly two such lines and the
# guard now has four -- it grew separate substitutions for ${HOME} and $HOME
# alongside the two tilde arms -- so a correct guard tripped the assertion.
# The arms are what this case is about, so they are what it edits; the
# $HOME substitutions are deliberately left alone, since the case name is
# about a tilde.
p = pathlib.Path("bootstrap/freshness-guard.sh")
Q = chr(39)
lines = p.read_text().splitlines(True)
arms = [i for i, l in enumerate(lines) if l.strip().startswith(Q + "~") and "path=" in l]
if not arms:
    pathlib.Path(".plant-could-not-anchor").write_text(
        "the guard no longer expands a leading tilde in a case arm this plant can find, "
        "so the tilde case could not be planted")
else:
    for i in arms:
        head = lines[i].split(")")[0]
        lines[i] = head + ") : ;;  # planted: tilde no longer expanded\n"
    p.write_text("".join(lines))
PY
'

run_case "an empty payload is blamed on jq and python3" '
python3 - <<PY
import pathlib
D = chr(36); Q = chr(34)
p = pathlib.Path("bootstrap/freshness-guard.sh")
t = p.read_text()
empty = "  if [ -z " + Q + D + "payload" + Q + " ]; then"
jq = "  if command -v jq >/dev/null 2>&1; then"
if not (empty in t and jq in t):
    pathlib.Path(".plant-could-not-anchor").write_text("the payload branch moved -- update this plant")
    raise SystemExit(0)
t = t[:t.index(empty)] + t[t.index(jq):]
t = t.replace(jq, "  if [ -n " + Q + D + "payload" + Q + " ] && " + jq.strip(), 1)
t = t.replace("  elif command -v python3 >/dev/null 2>&1; then",
              "  elif [ -n " + Q + D + "payload" + Q + " ] && command -v python3 >/dev/null 2>&1; then", 1)
t = t.replace("a hook payload arrived but neither jq nor python3 is on PATH to parse it",
              "could not read the hook payload (no jq, no python3)")
p.write_text(t)
PY
'

if ! python3 tools/checks/check_fresh_before_write.py > /dev/null; then
  echo "FAIL: check_fresh_before_write.py is not clean on the real, current repo" >&2
  exit 1
fi
echo "ok: clean on real content"
