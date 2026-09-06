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
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
PRACTICE_FILE = ROOT / "practices" / "deep-check.md"
CHECKS_DIR = ROOT / "tools" / "checks"
TESTS_DIR = CHECKS_DIR / "tests"
RUN_ALL = TESTS_DIR / "run_all.sh"


def rule_text() -> str:
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
