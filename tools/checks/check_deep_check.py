#!/usr/bin/env python3
"""check_deep_check.py -- the mechanical half of the very deep check's
pass 2, for this set's own tools/checks/ suite.

# practice: very-deep-check

Repointed 2026-09-06. This script was written for this set's own
`deep-check` practice, which was retired on 2026-09-05 in favour of
BestPractice's universal `very-deep-check` -- so the citation above named a
retired practice, which `code-cites-practice` forbids. The work the script
does did not change and is not obsolete: `very-deep-check`'s pass 2 ("Every
mechanical check, gate, and tool, one at a time") is exactly the question
this answers mechanically, for the one part of it that IS mechanical.

Scope: tree. A check script added without a matching test never gets picked
up by tools/checks/tests/run_all.sh's `test_*.sh` glob, so it silently
never runs; a test script left behind after its check script is deleted
references a file that no longer exists. Either way "every audit script,
run together" is false with nothing to catch it -- exactly the class of gap
this practice set's own catalogue was built to close
(spec/PRIVATE_ENFORCEMENT_BRIEF.md), and the class pass 2 exists to hunt.

It does not (and cannot) check the judgment half of any check level --
reading the repo's own rules against each other for contradiction or drift
-- which `very-deep-check`'s own Rule names as the session's work by
design, not a mechanical property.

Exit 0 and print nothing when clean. Exit 1 and print the specific
finding(s) on a violation, plus a pointer to the practice. Unlike this
set's other checks it cannot print the practice's own Rule text: the
practice it now cites is universal, so its file is not in this repository
-- and the local deep-check.md that IS here is retired, which makes its
Rule the wrong thing to quote as authority.
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
PRACTICE_SLUG = "very-deep-check"
PRACTICE_URL = ("https://github.com/alex137/BestPractice/blob/"
                "precedent-beta-v01/practices/very-deep-check.md")
CHECKS_DIR = ROOT / "tools" / "checks"
TESTS_DIR = CHECKS_DIR / "tests"
RUN_ALL = TESTS_DIR / "run_all.sh"


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

    return findings


if __name__ == "__main__":
    findings = find_violations()
    if findings:
        print(f"VIOLATION: {PRACTICE_SLUG}")
        for f in findings:
            print(f"  {f}")
        print(f"\nthe practice: {PRACTICE_SLUG} (universal) -- {PRACTICE_URL}")
        print("  pass 2: every mechanical check, gate and tool, one at a time.")
        sys.exit(1)
    sys.exit(0)
