#!/usr/bin/env python3
"""check_deep_check.py -- the mechanical check for practices/deep-check.md.

# practice: deep-check

Scope: tree. The practice's own Install text names what its mechanical half
actually is: "every audit script the repo maintains, run together -- already
exactly what tools/checks/tests/run_all.sh does." That claim has a real,
objective, always-checkable failure mode that was going unchecked: a check
script added without a matching test never gets picked up by run_all.sh's
`test_*.sh` glob, so it silently never runs; a test script left behind after
its check script is deleted references a file that no longer exists. Either
way "every audit script, run together" would be false with nothing to catch
it -- exactly the class of gap this practice set's own catalogue was built
to close (spec/PRIVATE_ENFORCEMENT_BRIEF.md).

This does not (and cannot) check deep-check's review half -- reading the
repo's own rules against each other for contradiction or drift -- which the
practice's own Rule text names as a judgment call by design, not a mechanical
property.

Exit 0 and print nothing when clean. Exit 1 and print the practice's own
Rule text (never a paraphrase) plus the specific finding(s) on a violation.
Since 2026-09-06 it also holds one structural property of the check family
itself: every check separates SOURCE_ROOT (the set its own rule text ships
in) from ROOT (the repository it audits), and honors PRECEDENT_CHECK_ROOT.
One name used to serve both, which is how fourteen checks across two sets
came to raise FileNotFoundError from inside their own violation printers the
first time they ran anywhere but in place. These scripts are written by
copying the last one, so a property nothing checks propagates by copy --
which is exactly how one bad line reached fourteen files.

In a consuming repo this reaches every source's checks at once, since
precedent_materialize.py lands them all in one tools/checks/.

"""
import os
import pathlib
import re
import sys

# TWO different questions, which used to share one name -- and that is exactly
# how a practice file went missing. SOURCE_ROOT is the practice set this script
# ships in; ROOT is the repository it AUDITS.
#
# They are the same directory in both normal cases: run in place inside its own
# set, and materialized into a consuming repo (where precedent_materialize.py
# has written practices/ and tools/checks/ side by side). They differ in the
# third case -- a repo that DECLARES this source but never materializes it, and
# runs the script in place against itself. Precedent's own repo is exactly
# that: its practices/ is the universal catalogue, so `parents[2]/practices/`
# resolved to a directory this practice was never in, and rule_text() raised
# FileNotFoundError from inside the violation printer (2026-09-06). The rule
# text always ships beside the script, so it is looked up against SOURCE_ROOT
# and can no longer be absent; only what to audit is overridable.
SOURCE_ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
ROOT = pathlib.Path(os.environ.get("PRECEDENT_CHECK_ROOT") or SOURCE_ROOT)
PRACTICE_FILE = SOURCE_ROOT / "practices" / "deep-check.md"
CHECKS_DIR = ROOT / "tools" / "checks"
TESTS_DIR = CHECKS_DIR / "tests"
RUN_ALL = TESTS_DIR / "run_all.sh"


def rule_text() -> str:
    # A materialized check runs in whatever repo its source was resolved
    # into, and the practice file it quotes is not guaranteed to be there:
    # a repo that declares the source but never materializes it, or a
    # practice retired out of the tree, both leave PRACTICE_FILE absent.
    # Unguarded, this raised FileNotFoundError from inside the violation
    # PRINTER -- so the finding was correctly detected, correctly printed,
    # and then buried under a traceback. Found 2026-09-06 running every
    # source-supplied check against BestPractice; 14 of the 16 shared this
    # exact body. The Rule text being unavailable is not the check failing.
    if not PRACTICE_FILE.is_file():
        return "(practice file not found at %s)" % PRACTICE_FILE
    text = PRACTICE_FILE.read_text(encoding="utf-8")
    m = re.search(r"## Rule\n(.*?)\n## ", text, re.S)
    return m.group(1).strip() if m else "(no Rule found)"


def find_violations() -> list[str]:
    findings = []

    if not RUN_ALL.is_file():
        return [f"{RUN_ALL.relative_to(ROOT)} is missing -- there is no "
                f"'every audit script, run together' entry point at all"]
    run_all_text = RUN_ALL.read_text(encoding="utf-8")
    if "test_*.sh" not in run_all_text:
        findings.append(
            f"{RUN_ALL.relative_to(ROOT)} no longer globs test_*.sh -- it "
            f"may have stopped running every audit script together")

    check_scripts = sorted(p.stem for p in CHECKS_DIR.glob("check_*.py"))
    test_scripts = sorted(
        p.stem[len('test_'):] for p in TESTS_DIR.glob("test_*.sh"))

    for slug in check_scripts:
        name = slug[len('check_'):]
        test_path = TESTS_DIR / f"test_{name}.sh"
        if not test_path.is_file():
            findings.append(
                f"tools/checks/{slug}.py has no tests/test_{name}.sh -- "
                f"run_all.sh's test_*.sh glob will never exercise it, so "
                f"'every audit script, run together' silently skips it")
            continue
        test_text = test_path.read_text(encoding="utf-8")
        if f"{slug}.py" not in test_text:
            findings.append(
                f"tests/test_{name}.sh exists but never invokes "
                f"{slug}.py by name -- it isn't actually testing the "
                f"check it's named for")

    for name in test_scripts:
        check_path = CHECKS_DIR / f"check_{name}.py"
        if not check_path.is_file():
            findings.append(
                f"tests/test_{name}.sh references a check script "
                f"(check_{name}.py) that no longer exists -- a stale test "
                f"left behind after its check was removed")

    # Every check in this family separates WHAT IT AUDITS from WHERE ITS OWN
    # RULE LIVES. One name used to serve both, and that is precisely how the
    # rule text went missing: run against a repo that DECLARES this source but
    # never materializes it, `parents[2]/practices/` is that repo's own
    # catalogue, not this set's -- so rule_text() raised FileNotFoundError from
    # inside the violation printer, burying a correct finding under a traceback
    # (2026-09-06, fourteen checks across two sets, all sharing one copied
    # body). The rule text always ships beside the script, so PRACTICE_FILE
    # must resolve against SOURCE_ROOT; only ROOT -- what to audit -- may be
    # overridden, via PRECEDENT_CHECK_ROOT.
    #
    # Checked here rather than left to review because these scripts are written
    # by copying the last one: whatever the previous check did, the next one
    # will do, correct or not. That is how one bad line reached fourteen files.
    # Matched as real assignments at column 0, never as substrings anywhere in
    # the file -- the first draft of this block searched the whole text and
    # reported ITSELF, because the pattern it looks for is spelled out inside
    # its own condition. Same trap check_draft_marker.py already documents for
    # a marker that appears in prose describing the marker.
    ASSIGNS_PRACTICE_TO_ROOT = re.compile(r"^PRACTICE_FILE\s*=\s*ROOT\b", re.M)
    DEFINES_SOURCE_ROOT = re.compile(r"^SOURCE_ROOT\s*=", re.M)
    READS_CHECK_ROOT = re.compile(r"PRECEDENT_CHECK_ROOT[\"']")

    for slug in check_scripts:
        text = (CHECKS_DIR / f"{slug}.py").read_text(encoding="utf-8")
        if not DEFINES_SOURCE_ROOT.search(text):
            findings.append(
                f"tools/checks/{slug}.py does not define SOURCE_ROOT -- it "
                f"cannot tell the repo it audits apart from the set its own "
                f"rule text lives in, so its rule text goes missing the "
                f"moment it runs anywhere but in place")
            continue
        if ASSIGNS_PRACTICE_TO_ROOT.search(text):
            findings.append(
                f"tools/checks/{slug}.py resolves PRACTICE_FILE against ROOT, "
                f"not SOURCE_ROOT -- ROOT is the repo being audited, which "
                f"need not carry this set's practices at all; use SOURCE_ROOT")
        if not READS_CHECK_ROOT.search(text):
            findings.append(
                f"tools/checks/{slug}.py ignores PRECEDENT_CHECK_ROOT -- a "
                f"repo that declares this source without materializing it "
                f"has no way to point the check at itself")

    return findings


if __name__ == "__main__":
    findings = find_violations()
    if findings:
        print(f"VIOLATION: {PRACTICE_FILE.stem}")
        for f in findings:
            print(f"  {f}")
        print("\nthe rule:")
        print("  " + rule_text().replace("\n", "\n  "))
        sys.exit(1)
    sys.exit(0)
