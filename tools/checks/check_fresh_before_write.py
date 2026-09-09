#!/usr/bin/env python3
"""check_fresh_before_write.py -- the mechanical check for
practices/fresh-before-write.md.

# practice: fresh-before-write

Scope: tree. Like check_claude_web_bootstrap.py, this repo plays two roles
and the check tells them apart: it is the PUBLISHER of the canonical guard
(`bootstrap/freshness-guard.sh` plus `bootstrap/freshness.snippet.json`),
and any other repo running this check is a CONSUMER that copied the guard
into `.claude/hooks/` per the practice's own Install section.

Most of what matters here is behavior, not text, so this check RUNS the
guard rather than reading it. In a throwaway repository whose remote does
not exist -- the state where a session genuinely cannot know whether its
checkout is current -- it asserts the three properties the practice's
Detail section says the two halves must have, and that a regression would
silently invert:

  1. `session-start` exits 0 even there. A freshness hook that can wedge a
     session is a worse failure than the staleness it guards against.
  2. `pre-write` exits 2 there. A check that could not run is not a check
     that passed, and this is the half whose whole job is to refuse.
  3. `pre-write` still lets a `git` command through in that same state.
     Every remedy it names is a git command; blocking those would leave a
     session unable to run the only thing that could clear the block.

Plus the structural invariants: the guard is git-tracked executable with a
bash shebang; some settings file wires BOTH hooks, with `Bash` in the
PreToolUse matcher (an agent editing files through `cat`/`sed` in Bash
never touches Edit or Write at all) and an explicit base-branch argument on
each command (detection gets it wrong in at least one real repo); and the
guard's own code contains `merge --ff-only` and none of the three verbs the
practice forbids it.

Exit 0 and print nothing when clean. Exit 1 and print the practice's own
Rule text (never a paraphrase) plus the specific finding(s) on a violation.
"""
import json
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

# A fixture commit is not a person's commit. The global commit backstop
# (commit-identity.sh, 2026-09-07) reaches every repository on the
# machine, including the throwaway ones this script builds, and refused
# them with an error naming only the git command. This is the override
# that backstop documents.
os.environ.setdefault('PRECEDENT_ALLOW_ANY_AUTHOR', '1')

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
PRACTICE_FILE = SOURCE_ROOT / "practices" / "fresh-before-write.md"
PUBLISHER_GUARD = ROOT / "bootstrap" / "freshness-guard.sh"
SNIPPET = ROOT / "bootstrap" / "freshness.snippet.json"
CONSUMER_HOOKS_DIR = ROOT / ".claude" / "hooks"
SETTINGS = ROOT / ".claude" / "settings.json"

# The practice's Rule names exactly one automatic operation, and three it
# rules out by name. A guard that grew any of the three would still pass
# every behavioral assertion below while being the wrong thing entirely.
FORBIDDEN = ["reset --hard", "git pull", "rebase"]
REQUIRED = "merge --ff-only"


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


def tracked_mode(path: pathlib.Path) -> str | None:
    rel = path.relative_to(ROOT)
    result = subprocess.run(
        ["git", "-C", str(ROOT), "ls-files", "-s", str(rel)],
        capture_output=True, text=True, check=True,
    )
    line = result.stdout.strip()
    return line.split()[0] if line else None


def find_guard() -> pathlib.Path | None:
    if PUBLISHER_GUARD.exists():
        return PUBLISHER_GUARD
    if CONSUMER_HOOKS_DIR.is_dir():
        for script in sorted(CONSUMER_HOOKS_DIR.glob("*.sh")):
            try:
                text = script.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):
                continue
            if "session-start" in text and "pre-write" in text and "freshness" in text:
                return script
    return None


def code_lines(text: str) -> str:
    """The script with whole-line comments dropped. The guard's own header
    discusses the forbidden verbs at length -- explaining why it does not
    use them is exactly what a good comment does, and must not read as a
    violation."""
    out = []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            continue
        out.append(line)
    return "\n".join(out)


def wiring_findings(guard: pathlib.Path) -> list[str]:
    """Both hook entries must be wired somewhere -- the publisher's snippet,
    or a consumer's own settings file. Only if no candidate file wires them
    correctly is that a violation."""
    candidates = [p for p in (SNIPPET, SETTINGS) if p.exists()]
    if not candidates:
        return [f"neither {SNIPPET.relative_to(ROOT)} nor {SETTINGS.relative_to(ROOT)} exists -- the guard is not wired into anything"]

    per_file = {}
    for path in candidates:
        rel = path.relative_to(ROOT)
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            per_file[rel] = [f"{rel}: not valid JSON ({e})"]
            continue

        findings = []
        hooks = data.get("hooks") or {}

        def commands(event):
            for entry in hooks.get(event) or []:
                for hook in entry.get("hooks", []):
                    yield entry, hook, hook.get("command", "")

        start = [(e, h, c) for e, h, c in commands("SessionStart") if guard.name in c]
        if not start:
            findings.append(f"{rel}: no SessionStart hook runs {guard.name}")
        for entry, hook, command in start:
            if hook.get("async") is True:
                findings.append(f"{rel}: the SessionStart entry sets \"async\": true -- it must finish before the session reads anything")
            if "session-start" not in command:
                findings.append(f"{rel}: the SessionStart command does not pass the session-start mode ({command!r})")
            if len(command.split()) < 3:
                findings.append(f"{rel}: the SessionStart command passes no base branch ({command!r}) -- it must be explicit, never detected")

        pre = [(e, h, c) for e, h, c in commands("PreToolUse") if guard.name in c]
        if not pre:
            findings.append(f"{rel}: no PreToolUse hook runs {guard.name}")
        for entry, hook, command in pre:
            matcher = entry.get("matcher", "")
            if "Bash" not in matcher:
                findings.append(f"{rel}: the PreToolUse matcher {matcher!r} does not include Bash -- an agent editing files through cat/sed in Bash would never trigger it")
            if "pre-write" not in command:
                findings.append(f"{rel}: the PreToolUse command does not pass the pre-write mode ({command!r})")
            if len(command.split()) < 3:
                findings.append(f"{rel}: the PreToolUse command passes no base branch ({command!r}) -- it must be explicit, never detected")

        per_file[rel] = findings

    if any(not f for f in per_file.values()):
        return []
    # Nothing wires it correctly -- report the closest attempt.
    best = min(per_file.items(), key=lambda kv: len(kv[1]))
    return best[1]


def behavior_findings(guard: pathlib.Path) -> list[str]:
    findings = []
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="fresh-before-write-check-"))
    try:
        repo = tmp / "repo"
        repo.mkdir()
        env_git = ["git", "-C", str(repo), "-c", "user.email=check@example.invalid",
                   "-c", "user.name=check"]
        subprocess.run(["git", "init", "-q", "-b", "work", str(repo)],
                       capture_output=True, check=True)
        (repo / "f.txt").write_text("x\n", encoding="utf-8")
        subprocess.run(env_git + ["add", "-A"], capture_output=True, check=True)
        subprocess.run(env_git + ["commit", "-qm", "one"], capture_output=True, check=True)
        # A remote that exists in config and cannot be reached: the exact
        # state where the guard must not pretend to know anything.
        subprocess.run(env_git + ["remote", "add", "origin", str(tmp / "nowhere.git")],
                       capture_output=True, check=True)

        sentinels = tmp / "sentinels"
        sentinels.mkdir()
        env = {"PATH": "/usr/bin:/bin:/usr/local/bin",
               "HOME": str(tmp),
               "TMPDIR": str(sentinels),
               "CLAUDE_PROJECT_DIR": str(repo)}

        def run(mode, payload=None):
            return subprocess.run(
                ["bash", str(guard), mode, "main"],
                input=(payload or ""), capture_output=True, text=True, env=env,
            ).returncode

        rc = run("session-start")
        if rc != 0:
            findings.append(f"{guard.relative_to(ROOT)}: session-start exited {rc} on an unreachable remote -- it must always exit 0 rather than wedge a session")

        write_payload = json.dumps({"session_id": "check-block", "tool_name": "Write",
                                    "tool_input": {"file_path": "f.txt"}})
        rc = run("pre-write", write_payload)
        if rc != 2:
            findings.append(f"{guard.relative_to(ROOT)}: pre-write exited {rc} on a checkout it could not verify -- it must exit 2 (block); a check that could not run is not a check that passed")

        git_payload = json.dumps({"session_id": "check-git", "tool_name": "Bash",
                                  "tool_input": {"command": "git fetch origin work"}})
        rc = run("pre-write", git_payload)
        if rc != 0:
            findings.append(f"{guard.relative_to(ROOT)}: pre-write exited {rc} on a git command -- git must never be blocked, or a session cannot run the remedy the block itself names")
    except subprocess.CalledProcessError as e:
        findings.append(f"could not build the throwaway repository for the behavioral check: {e}")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    return findings


def find_violations() -> list[str]:
    guard = find_guard()
    if guard is None:
        return [f"{PUBLISHER_GUARD.relative_to(ROOT)}: missing, and no copy of it in {CONSUMER_HOOKS_DIR.relative_to(ROOT)} either -- nothing is guarding this repo's freshness"]

    findings = []
    rel = guard.relative_to(ROOT)

    mode = tracked_mode(guard)
    if mode != "100755":
        findings.append(f"{rel}: git-tracked mode is {mode}, expected 100755 (executable)")

    text = guard.read_text(encoding="utf-8")
    if not text.startswith("#!/bin/bash") and not text.startswith("#!/usr/bin/env bash"):
        findings.append(f"{rel}: doesn't start with a bash shebang")

    code = code_lines(text)
    if REQUIRED not in code:
        findings.append(f"{rel}: no `{REQUIRED}` in the script's code -- the one automatic update this practice allows")
    for verb in FORBIDDEN:
        if verb in code:
            findings.append(f"{rel}: uses `{verb}`, which this practice rules out by name -- the automatic half is `{REQUIRED}` and nothing else")

    findings.extend(wiring_findings(guard))
    findings.extend(behavior_findings(guard))
    return findings


if __name__ == "__main__":
    found = find_violations()
    if found:
        print(f"VIOLATION: {PRACTICE_FILE.stem}")
        for f in found:
            print(f"  {f}")
        print("\nthe rule:")
        print("  " + rule_text().replace("\n", "\n  "))
        sys.exit(1)
    sys.exit(0)
