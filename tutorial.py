"""Tutorial: Versioning This Tutorial with sv.

This module uses a simple VERSION file as the source of truth for its version.
The script reads the version, bumps it, and writes the updated value back to
that file.

Example usage:
    python sv/tutorial.py
"""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

_HERE = Path(__file__).resolve()
_ROOT_PARENT = _HERE.parent.parent
if str(_ROOT_PARENT) not in sys.path:
    sys.path.insert(0, str(_ROOT_PARENT))

from sv import get_semver_logic


_VERSION_PATH = Path(__file__).resolve().with_name("VERSION")


def bump_tutorial_version(
    bump_type: str = "dev",
    is_dev: bool = True,
    version_path: Path | None = None,
) -> str:
    """Bump the VERSION file and return the new version."""
    target_path = version_path or _VERSION_PATH
    version = target_path.read_text(encoding="utf-8").strip()
    if not version:
        raise ValueError("VERSION file is empty.")

    result = get_semver_logic().bump_with_dev(version, bump_type, is_dev=is_dev)
    new_version = result.new_version
    target_path.write_text(f"{new_version}\n", encoding="utf-8")
    return new_version


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Bump the tutorial VERSION file.")
    parser.add_argument(
        "--set",
        dest="set_version",
        help="Set VERSION to an explicit value (no bump).",
    )
    parser.add_argument(
        "--version-file",
        type=Path,
        default=_VERSION_PATH,
        help="Path to the VERSION file to update.",
    )
    parser.add_argument(
        "--bump",
        choices=["major", "minor", "patch", "dev", "none"],
        default="dev",
        help="Base version bump to apply before optional dev suffix.",
    )
    parser.add_argument(
        "--release",
        action="store_true",
        help="Write a release version (no dev suffix).",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = _parse_args()
    if args.set_version:
        get_semver_logic().parse(args.set_version)
        args.version_file.write_text(f"{args.set_version}\n", encoding="utf-8")
        print(f"Set tutorial version to {args.set_version}")
    else:
        bumped = bump_tutorial_version(
            bump_type=args.bump,
            is_dev=not args.release,
            version_path=args.version_file,
        )
        print(f"Updated tutorial to {bumped}")
