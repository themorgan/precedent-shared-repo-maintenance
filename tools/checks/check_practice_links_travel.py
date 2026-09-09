#!/usr/bin/env python3
"""A practice's relative links must survive materialization.

practice-links-travel. A practice file in THIS source is copied verbatim
into every consuming repo's own practices/ directory. Only two kinds of
relative link still resolve after that trip: a sibling practice
(`other-slug.md`), and this source's own check scripts
(`../tools/checks/...`), which materialize copies alongside. Everything
else -- `../bootstrap/x`, `../.claude/settings.json`, `../spec/y` -- names
a path that exists only in the publisher, and lands in the consumer as a
dead link.

WHY THIS CANNOT BE FIXED DOWNSTREAM, which is the whole reason it needs a
check up here. precedent_materialize.py's `_rewrite_links` repoints links
it can place, and for a PUBLIC source it turns an unplaceable one into an
absolute URL. It deliberately refuses to do that for an individual source:
minting `https://github.com/<owner>/<private repo>/blob/...` into a
consuming repo's tracked tree discloses a private repo's existence and
location, and a consuming repo can be public. Its own docstring: "a
relative link that does not resolve is a smaller failure than a disclosure
that cannot be taken back." That trade is right, and it means the dead link
is load-bearing -- nothing downstream will or should repair it.

So the repair has to happen here, by not writing the link: keep the
backticked path, drop the link markup. The prose already says which repo it
means.

THE INCIDENT (cite-the-incident). 2026-09-06, three times in one day.
First: fresh-before-write landed with three `../bootstrap/` links; a
consuming repo's Markdown lint went red on the first push that vendored it,
three BROKEN RELATIVE LINKS. The fix made them absolute -- and that tripped
the consuming repo's private-repo-scrub, because it was exactly the
disclosure the rewriter refuses to make. Corrected to bare backticked
paths. Then, hours later, buenos-aires-dates and commit-author landed with
seven more of the same. And a sweep found two in claude-web-bootstrap that
had been dead for weeks and were never reported, because doc_lint scopes to
CHANGED files and nobody had touched that file. Nine in total.

Three separate sessions made the same mistake against the same directory
inside a single day. Prose in a gotchas log had already recorded it and did
not stop the second or third. Hence a check.
"""
import json
import os
import pathlib
import re
import sys

# SOURCE_ROOT is the practice set this script ships in; ROOT is the
# repository it AUDITS. Same directory in both normal cases; they differ
# in a repo that declares this source without materializing it, where the
# rule text was looked up in a directory the practice was never in.
SOURCE_ROOT = pathlib.Path(__file__).resolve().parents[2]
ROOT = pathlib.Path(os.environ.get("PRECEDENT_CHECK_ROOT") or SOURCE_ROOT)

LINK = re.compile(r'\[(?:`[^`]*`|[^\]]*)\]\(([^)\s]+)\)')

# What still resolves after materialization writes practices/<slug>.md and
# tools/checks/** into a consuming repo, and nothing else from this source.
def _travels(target):
    bare = target.split('#', 1)[0]
    if not bare:
        return True                       # a pure #anchor
    if bare.startswith(('http://', 'https://', 'mailto:')):
        return True
    if bare.endswith('.md') and '/' not in bare:
        return True                       # a sibling practice
    if bare.startswith('../tools/checks/'):
        return True                       # copied alongside
    return False


def _foreign_slugs():
    """Slugs a consuming repo's MANIFEST.json attributes to another source.

    In a consumer, practices/ is materialized output holding every source's
    practices. A practice this source does not own is not this repo's text
    and cannot be fixed here, so it is skipped -- the same attribution rule
    check_private_repo_scrub.py uses, and for the same reason. Attribution
    comes from the COMMITTED manifest, never from live resolution: a bare
    CI checkout cannot reach a team source's sibling clone or an individual
    source's user-level config, and "did not resolve here" is not evidence
    of anything.
    """
    m = ROOT / 'MANIFEST.json'
    if not m.exists():
        return set()                      # a source repo: everything is ours
    try:
        entries = json.loads(m.read_text(encoding='utf-8')).get('practices', [])
    except Exception:
        return set()
    return {e.get('slug') for e in entries
            if e.get('source') != 'precedent-individual'}


def main():
    practices = ROOT / 'practices'
    if not practices.is_dir():
        print('SKIPPED: no practices/ directory here')
        return 0
    foreign = _foreign_slugs()
    findings = []
    for p in sorted(practices.glob('*.md')):
        if p.stem in foreign:
            continue
        for i, line in enumerate(p.read_text(encoding='utf-8').splitlines(), 1):
            for m in LINK.finditer(line):
                target = m.group(1)
                if _travels(target):
                    continue
                findings.append(
                    f"  practices/{p.name}:{i}: relative link to {target!r} "
                    f"names a path that exists only in the publishing repo, "
                    f"so it lands dead in every consuming repo -- and "
                    f"materialize will not repair it, because turning it "
                    f"into a URL would disclose a private repo. Keep the "
                    f"backticked path, drop the link markup.")
    if findings:
        print('VIOLATION: practice-links-travel')
        for f in findings:
            print(f)
        return 1
    print(f'OK: {len(list(practices.glob("*.md")))} practice file(s); '
          f'every relative link survives materialization')
    return 0


if __name__ == '__main__':
    sys.exit(main())
