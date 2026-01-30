from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
import re
from typing import Literal


BumpType = Literal["major", "minor", "patch", "dev", "none"]
ReleaseBumpType = Literal["major", "minor", "patch"]


@dataclass(frozen=True)
class SemverBumpResult:
    current_version: str
    base_version: str
    new_version: str
    npm_version: str
    mod_version: str


class SemverLogic(ABC):
    @abstractmethod
    def parse(self, version: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def bump(self, version: str, bump_type: ReleaseBumpType) -> str:
        raise NotImplementedError

    @abstractmethod
    def bump_with_dev(self, current_version: str, bump_type: BumpType, is_dev: bool) -> SemverBumpResult:
        raise NotImplementedError


class DefaultSemverLogic(SemverLogic):
    def parse(self, version: str) -> None:
        base_version, _ = _split_dev_version(version)
        core_version = _strip_prerelease_build(base_version)
        _parse_base_version(core_version)

    def bump(self, version: str, bump_type: ReleaseBumpType) -> str:
        base_version, _ = _split_dev_version(version)
        core_version = _strip_prerelease_build(base_version)
        if bump_type == "major":
            return _bump_major(core_version)
        if bump_type == "minor":
            return _bump_minor(core_version)
        return _bump_patch(core_version)

    def bump_with_dev(self, current_version: str, bump_type: BumpType, is_dev: bool) -> SemverBumpResult:
        base_version, current_dev_num = _split_dev_version(current_version)
        base_core_version = _strip_prerelease_build(base_version)
        is_current_dev = current_dev_num is not None

        if bump_type == "major":
            new_version = _bump_major(base_core_version)
        elif bump_type == "minor":
            new_version = _bump_minor(base_core_version)
        elif bump_type == "patch":
            new_version = _bump_patch(base_core_version)
        else:
            new_version = base_core_version

        if is_dev:
            if is_current_dev and new_version == base_version:
                dev_num = current_dev_num + 1
            else:
                dev_num = 0
            new_version = f"{new_version}.dev{dev_num}"

        npm_version = _to_npm_version(new_version)
        mod_version = _strip_dev_suffix(new_version)

        return SemverBumpResult(
            current_version=current_version,
            base_version=base_core_version,
            new_version=new_version,
            npm_version=npm_version,
            mod_version=mod_version,
        )


_DEFAULT_SEMVER_LOGIC = DefaultSemverLogic()


def get_semver_logic() -> SemverLogic:
    return _DEFAULT_SEMVER_LOGIC


_DEV_SUFFIX_RE = re.compile(r"(?:\.dev|-dev\.)(\d+)$")
_DOT_DEV_RE = re.compile(r"\.dev(\d+)$")
_BASE_VERSION_RE = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")
_SEMVER_RE = re.compile(
    r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    r"(?:-([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?"
    r"(?:\+([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?$"
)


def _split_dev_version(version: str) -> tuple[str, int | None]:
    match = _DEV_SUFFIX_RE.search(version)
    base_version = _DEV_SUFFIX_RE.sub("", version)
    dev_num = int(match.group(1)) if match else None
    return base_version, dev_num


def _strip_prerelease_build(version: str) -> str:
    match = _SEMVER_RE.match(version)
    if not match:
        raise ValueError(f"Invalid semver version: {version}")
    return f"{match.group(1)}.{match.group(2)}.{match.group(3)}"


def _parse_base_version(version: str) -> tuple[int, int, int]:
    match = _BASE_VERSION_RE.match(version)
    if not match:
        raise ValueError(f"Invalid semver base version: {version}")
    return int(match.group(1)), int(match.group(2)), int(match.group(3))


def _format_base_version(major: int, minor: int, patch: int) -> str:
    return f"{major}.{minor}.{patch}"


def _bump_major(version: str) -> str:
    major, minor, patch = _parse_base_version(version)
    return _format_base_version(major + 1, 0, 0)


def _bump_minor(version: str) -> str:
    major, minor, patch = _parse_base_version(version)
    return _format_base_version(major, minor + 1, 0)


def _bump_patch(version: str) -> str:
    major, minor, patch = _parse_base_version(version)
    return _format_base_version(major, minor, patch + 1)


def _to_npm_version(version: str) -> str:
    return _DOT_DEV_RE.sub(r"-dev.\1", version)


def _strip_dev_suffix(version: str) -> str:
    return _DEV_SUFFIX_RE.sub("", version)
