# Semver Utilities

This package provides reusable version bumping logic for any project that
needs consistent semver handling. It is intended to be used as a drop in submodule or library.

This module intentionally avoids third-party dependencies for lightweight portability.

## Usage

```python
from sv import get_semver_logic

semver_logic = get_semver_logic()
semver_logic.parse("1.2.3")
new_version = semver_logic.bump("1.2.3", "patch")
```

For dev builds:

```python
result = semver_logic.bump_with_dev("1.2.3.dev4", "dev", is_dev=True)
print(result.new_version)  # 1.2.3.dev5
```

For prerelease/build inputs (suffixes are accepted but dropped when bumping):

```python
semver_logic.parse("1.2.3-alpha.1+build.7")
new_version = semver_logic.bump("1.2.3-alpha.1", "minor")
print(new_version)  # 1.3.0
```

## Notes

- `npm_version` uses `-dev.N` format to stay compatible with npm.
- `mod_version` strips any dev suffix for cross-system compatibility.
- Supported input formats:
  - Core semver: `MAJOR.MINOR.PATCH`
  - Optional prerelease: `MAJOR.MINOR.PATCH-PRERELEASE`
  - Optional build metadata: `MAJOR.MINOR.PATCH+BUILD`
  - Optional combined prerelease/build: `MAJOR.MINOR.PATCH-PRERELEASE+BUILD`
  - Optional dev suffix: `.devN` or `-dev.N` (appended to the version)
- Bumps always operate on the core version and drop any prerelease/build/dev suffix.
