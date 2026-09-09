#!/bin/bash
# Two-direction test for check_practice_links_travel.py:
#   A. a practice links a publisher-only path (../bootstrap/x) -- must fire;
#   B. a practice links ../.claude/settings.json -- must fire. The nastier
#      shape: in a consuming repo it RESOLVES, just to the consumer's own
#      settings file rather than the one the sentence means, so no lint
#      anywhere reports it. Only this check can.
#   C. a sibling practice link and a ../tools/checks/ link -- must NOT fire;
#      those are exactly what materialize copies alongside.
#   D. a practice the manifest attributes to ANOTHER source -- must NOT
#      fire; not this source's text, and not fixable here.
# Then: the real, current, unplanted repo must stay clean.
#
# Cases are FUNCTIONS, not strings passed to eval. The first version used
# eval'd single-quoted strings containing unquoted heredocs; bash ran the
# backticked paths inside them as command substitution, so the planted file
# never contained the link under test. Every case still reported "ok" --
# case C's clean verdict was a pass on content that had had its links eaten.
# The giveaway was on stderr ("bootstrap/thing.sh: No such file or
# directory"), not in the result.
set -euo pipefail
cd "$(dirname "$0")/../../.."
ROOT="$(pwd)"

plant_publisher_path () {
  cat > practices/planted-link.md <<'MD'
## Rule
See [`bootstrap/thing.sh`](../bootstrap/thing.sh) for the canonical copy.
MD
}

plant_consumer_shadowed_path () {
  cat > practices/planted-link.md <<'MD'
## Rule
This repo is the exception: [`.claude/settings.json`](../.claude/settings.json)
here calls the canonical script in place.
MD
}

plant_travelling_links () {
  cat > practices/planted-link.md <<'MD'
## Rule
See [`commit-author`](commit-author.md) and
[`tools/checks/check_commit_author.py`](../tools/checks/check_commit_author.py).
MD
}

plant_foreign_practice () {
  cat > practices/planted-link.md <<'MD'
## Rule
See [`bootstrap/thing.sh`](../bootstrap/thing.sh).
MD
  # APPEND to the manifest, never replace it. Overwriting it strips
  # attribution from every OTHER practice in practices/, so in a consuming
  # repo -- where practices/ holds 120 of them from four sources -- they all
  # read as this source's own, and the check fires on somebody else's
  # non-travelling link. This case then fails for a reason that has nothing
  # to do with what it tests.
  #
  # 2026-09-06: this exact mistake was found and fixed in
  # precedent-team-maintainers' test_private_repo_scrub.sh earlier the same
  # day, and then made again here hours later, by the session that had just
  # fixed it. The shape is the lesson: a test that rebuilds shared state
  # from scratch instead of adding to it will eventually fail on something
  # it never meant to touch, and blame the code.
  python3 - <<'PY'
import json, pathlib
p = pathlib.Path('MANIFEST.json')
d = json.loads(p.read_text(encoding='utf-8')) if p.exists() else {}
d.setdefault('practices', []).append(
    {'slug': 'planted-link', 'level': 'team',
     'source': 'precedent-team-maintainers'})
p.write_text(json.dumps(d, indent=2, sort_keys=True) + '\n', encoding='utf-8')
PY
}

run () {
  local label="$1" expect="$2" fn="$3"
  local scratch; scratch="$(mktemp -d)"
  git clone -q "$ROOT" "$scratch"
  cp "$ROOT/tools/checks/tests/$(basename "$0")" "$scratch/tools/checks/tests/" 2>/dev/null || true
  (
    cd "$scratch"
    "$fn"
    # Prove the plant landed intact before trusting the verdict: a mangled
    # fixture that produces the expected result is the failure mode this
    # rewrite exists for.
    if ! grep -q '](\.\./\|](commit-author\.md)' practices/planted-link.md; then
      echo "FAIL: $label -- the planted file has no link in it; fixture is broken" >&2
      exit 1
    fi
    if python3 tools/checks/check_practice_links_travel.py > /dev/null 2>&1; then
      got=clean
    else
      got=fires
    fi
    if [ "$got" != "$expect" ]; then
      echo "FAIL: $label -- expected $expect, got $got" >&2
      exit 1
    fi
    echo "ok: $label ($got, as required)"
  )
  local status=$?
  rm -rf "$scratch"
  return $status
}

run "publisher-only path (../bootstrap/)"                      fires plant_publisher_path
run "resolves in a consumer, means the publisher's (../.claude/)" fires plant_consumer_shadowed_path
run "sibling practice and check script both travel"            clean plant_travelling_links
run "practice owned by another source is skipped"              clean plant_foreign_practice

if ! python3 tools/checks/check_practice_links_travel.py > /dev/null; then
  echo "FAIL: check_practice_links_travel.py is not clean on the real, current repo" >&2
  exit 1
fi
echo "ok: clean on real content"
