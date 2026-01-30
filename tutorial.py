"""Tutorial: Versioning This Tutorial with sv.

This module uses a simple VERSION file as the source of truth for its version.
The script reads the version, bumps it, and writes the updated value back to
that file.

Example usage:
    python tutorial.py
"""

from __future__ import annotations

from pathlib import Path
import sys

_HERE = Path(__file__).resolve()
_ROOT_PARENT = _HERE.parent.parent
if str(_ROOT_PARENT) not in sys.path:
    sys.path.insert(0, str(_ROOT_PARENT))

from sv import get_semver_logic


_VERSION_PATH = Path(__file__).resolve().with_name("VERSION")


def bump_tutorial_version(is_dev: bool = True) -> str:

    result = get_semver_logic().bump_with_dev(_VERSION_PATH.read_text(encoding="utf-8").strip(), "dev", is_dev=is_dev)
    new_version = result.new_version
    _VERSION_PATH.write_text(f"{new_version}\n", encoding="utf-8")
    print(f"Bumped tutorial version to: {new_version}")
    return new_version


if __name__ == "__main__":
    bump_tutorial_version(is_dev=True)
