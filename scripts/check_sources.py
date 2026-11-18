#!/usr/bin/env python3
"""scripts/check_sources.py: every plugin source in the catalogue must point at a Git ref that exists.

Reasoning:
- `claude plugin validate` checks the catalogue's shape, not whether the repositories and branches it points at
  still exist. A renamed default branch would leave an entry that validates and fails on install, so this asks
  each remote for the ref with `git ls-remote` (no clone, no credentials: every source is a public repository).
- Standard library only, so it runs on a bare CI runner.

Usage: python scripts/check_sources.py [path/to/marketplace.json]
"""

from __future__ import annotations

import json
import subprocess  # nosec B404 - fixed argument list, no shell
import sys
from pathlib import Path

CATALOGUE = Path(".claude-plugin/marketplace.json")


def remote_and_ref(source: object) -> tuple[str, str] | None:
    """The Git URL and ref of a plugin source, or None for a source this check does not cover."""
    if not isinstance(source, dict):
        return None
    kind = source.get("source")
    if kind == "github":
        return f"https://github.com/{source['repo']}.git", str(source.get("ref", "HEAD"))
    if kind in ("git-subdir", "url"):
        return str(source["url"]), str(source.get("ref", "HEAD"))
    return None


def main(argv: list[str]) -> int:
    path = Path(argv[1]) if len(argv) > 1 else CATALOGUE
    plugins = json.loads(path.read_text(encoding="utf-8"))["plugins"]
    failures = 0
    for plugin in plugins:
        target = remote_and_ref(plugin["source"])
        if target is None:
            print(f"skip   {plugin['name']}: source type not checked")
            continue
        url, ref = target
        result = subprocess.run(  # nosec B603 - fixed argument list
            ["git", "ls-remote", "--exit-code", url, ref],
            capture_output=True,
            text=True,
            timeout=60,
            check=False,
        )
        if result.returncode == 0:
            print(f"ok     {plugin['name']}: {url} {ref}")
        else:
            failures += 1
            print(f"FAILED {plugin['name']}: {url} {ref}: {result.stderr.strip()[:200]}")
    print(f"{len(plugins) - failures} of {len(plugins)} sources resolve")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
