#!/usr/bin/env python3
"""Check that repository tracking docs move with meaningful changes."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


TRACKING_DOCS = {"Changelog.md", "Context.md", "Progress.md"}
IGNORED_NAMES = {".DS_Store"}
IGNORED_PREFIXES = {".git/"}


def git_lines(args: list[str]) -> set[str]:
    result = subprocess.run(["git", *args], capture_output=True, text=True, check=False)
    if result.returncode != 0:
        raise SystemExit(result.stderr.strip() or f"git {' '.join(args)} failed")
    return {line.strip() for line in result.stdout.splitlines() if line.strip()}


def changed_paths(base: str | None) -> set[str]:
    if base:
        return git_lines(["diff", "--name-only", base])
    return (
        git_lines(["diff", "--name-only"])
        | git_lines(["diff", "--cached", "--name-only"])
        | git_lines(["ls-files", "--others", "--exclude-standard"])
    )


def is_ignored(path: str) -> bool:
    name = Path(path).name
    return name in IGNORED_NAMES or any(path.startswith(prefix) for prefix in IGNORED_PREFIXES)


def missing_tracking_docs() -> list[str]:
    return sorted(path for path in TRACKING_DOCS if not Path(path).is_file())


def main() -> int:
    parser = argparse.ArgumentParser(description="Require tracking docs to change with meaningful repo changes.")
    parser.add_argument("--base", help="Git revision range to compare, for example origin/main...HEAD.")
    args = parser.parse_args()

    paths = {path for path in changed_paths(args.base) if not is_ignored(path)}
    missing_docs = missing_tracking_docs()
    if missing_docs:
        print("Documentation lockstep check failed.")
        print("Required tracking files are missing from the checkout:")
        for path in missing_docs:
            print(f"- {path}")
        return 1

    meaningful = {path for path in paths if path not in TRACKING_DOCS}
    if not meaningful:
        print("Documentation lockstep check skipped: no meaningful non-tracking changes.")
        return 0

    missing_updates = sorted(TRACKING_DOCS - paths)
    if missing_updates:
        print("Documentation lockstep check failed.")
        print("Meaningful changes were detected, so these tracking files must be updated together:")
        for path in missing_updates:
            print(f"- {path}")
        print("\nChanged non-tracking paths:")
        for path in sorted(meaningful):
            print(f"- {path}")
        return 1

    print("Documentation lockstep check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
