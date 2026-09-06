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
printf '\nSee themorgan/precedent-individual for a worked example.\n' >> practices/install.md
git add practices/install.md
git -c user.name="Test" -c user.email="test@example.com" commit -q -m "planted violation: names a private repo in vendored content"

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
This text names precedent-team-maintainers, which is a private repo.
MD
cat > MANIFEST.json <<'JSON'
{"practices": [{"slug": "planted-foreign", "level": "team", "source": "precedent-team-maintainers"}]}
JSON
git add practices/planted-foreign.md MANIFEST.json
git -c user.name="Test" -c user.email="test@example.com" commit -q -m "planted foreign materialized practice"

if ! python3 tools/checks/check_private_repo_scrub.py > /dev/null; then
  echo "FAIL: check_private_repo_scrub.py fired on a practice the manifest attributes to another source" >&2
  exit 1
fi
echo "ok: silent on a materialized practice owned by another source"
