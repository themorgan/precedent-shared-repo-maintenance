#!/bin/bash
# Two-direction test for check_private_repo_scrub.py:
#   1. plant a real private-repo name into a practices/*.md file -- require
#      the check to fire;
#   2. the real, current, unplanted repo -- require the check to stay clean.
set -euo pipefail
cd "$(dirname "$0")/../../.."
ROOT="$(pwd)"
SCRATCH="$(mktemp -d)"
trap 'rm -rf "$SCRATCH"' EXIT

git clone -q "$ROOT" "$SCRATCH"
cd "$SCRATCH"
# The planted string is OWNER-QUALIFIED on purpose. A bare
# "precedent-individual" is the public convention name every adopter's set
# carries (Precedent's own `source-naming`), so it identifies nobody and no
# longer fires -- planting one here would test the check into forbidding a
# word consuming repos are required to use.
#
# The plant goes into a NEW practice file rather than an existing one, and
# declares itself repo-local when a MANIFEST.json is present. Until
# 2026-09-06 it appended to practices/install.md, which works here and fails
# in a consuming repo for a reason that is not a bug: there practices/ is
# materialized output, install.md belongs to this source, and the check
# rightly skips practices the manifest attributes elsewhere -- so the check
# stayed silent and the test read that as "did not fire". Planting content
# the running repo actually OWNS keeps this direction meaningful in both
# places, instead of skipping it in one of them.
cat > practices/planted-private-name.md <<'MD'
## Rule
See themorgan/precedent-individual for a worked example.
MD
if [ -f MANIFEST.json ]; then
  python3 - <<'PY'
import json, pathlib
p = pathlib.Path('MANIFEST.json')
d = json.loads(p.read_text(encoding='utf-8'))
d.setdefault('practices', []).append(
    {'slug': 'planted-private-name', 'level': 'repo-local', 'source': 'local'})
p.write_text(json.dumps(d, indent=2, sort_keys=True) + '\n', encoding='utf-8')
PY
  git add MANIFEST.json
fi
git add practices/planted-private-name.md
git -c user.name="Test" -c user.email="test@example.com" commit -q -m "planted violation: names a private repo in content this repo owns"

if python3 tools/checks/check_private_repo_scrub.py > /dev/null; then
  echo "FAIL: check_private_repo_scrub.py did not fire on a planted private-repo name" >&2
  exit 1
fi
echo "ok: fires on planted violation"

cd "$ROOT"
if ! python3 tools/checks/check_private_repo_scrub.py > /dev/null; then
  echo "FAIL: check_private_repo_scrub.py is not clean on the real, current repo" >&2
  exit 1
fi
echo "ok: clean on real content"

# A materialized practice from another source must be SKIPPED: in a consuming
# repo practices/ is regenerated from every declared source, so a team- or
# individual-set practice naming its own private repo is that set's text, not
# the consuming repo's, and cannot be fixed there. Attribution is by the
# COMMITTED MANIFEST.json, never live resolution. Added 2026-09-06, after a
# consuming repo reported this check against practices/deep-check.md.
SCRATCH4="$(mktemp -d)"
trap 'rm -rf "$SCRATCH" "$SCRATCH4"' EXIT
git clone -q "$ROOT" "$SCRATCH4"
cd "$SCRATCH4"
mkdir -p practices
cat > practices/planted-foreign.md <<'MD'
## Rule
This text names precedent-team-repo-maintenance, which is a private repo.
MD
# APPEND to the manifest, never replace it. Overwriting it strips attribution
# from every OTHER practice in practices/, so any real materialized practice
# that happens to name a private repo is then read as this repo's own content
# and the check fires on it -- a failure in this case that has nothing to do
# with what this case is testing. 2026-09-06: that is exactly what happened in
# a consuming repo, where a newly vendored individual practice carrying an
# owner-qualified URL made this case go red while cases 1 and 2 both passed.
python3 - <<'PY'
import json, pathlib
p = pathlib.Path('MANIFEST.json')
d = json.loads(p.read_text(encoding='utf-8')) if p.exists() else {}
d.setdefault('practices', []).append(
    {'slug': 'planted-foreign', 'level': 'team', 'source': 'precedent-team-repo-maintenance'})
p.write_text(json.dumps(d, indent=2, sort_keys=True) + '\n', encoding='utf-8')
PY
git add practices/planted-foreign.md MANIFEST.json
git -c user.name="Test" -c user.email="test@example.com" commit -q -m "planted foreign materialized practice"

if ! python3 tools/checks/check_private_repo_scrub.py > /dev/null; then
  echo "FAIL: check_private_repo_scrub.py fired on a practice the manifest attributes to another source" >&2
  exit 1
fi
echo "ok: silent on a materialized practice owned by another source"
