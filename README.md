# Semver Utilities

This package provides reusable version bumping logic for any project that
needs consistent semver handling. It is intended to be used as a drop in submodule or library and a lightweight wrapper for the semver library.

This module intentionally avoids third-party dependencies for lightweight portability.

## Tutorial

Start with the onboarding tutorial in `tutorial.py`. It walks through adopting
the library by using a repo-local `VERSION` file as the single source of truth,
then bumping that version with `sv` for repeatable releases.

To run it:

```bash
python sv/tutorial.py
```

This will read `VERSION`, increment the dev version, and write the new value
back to the file. You can also choose a release bump:

```bash
python sv/tutorial.py --bump minor --release
```

Or set an explicit version:

```bash
python sv/tutorial.py --set 1.2.3
```

The tutorial keeps the flow minimal so you can drop the same pattern into any
project that needs consistent versioning without adding dependencies or extra
tooling.

## Notes

- `npm_version` uses `-dev.N` format to stay compatible with npm.
- `mod_version` strips any dev suffix for cross-system compatibility.
- Supported input formats:
  - Core semver: `MAJOR.MINOR.PATCH`
  - Optional prerelease: `MAJOR.MINOR.PATCH-PRERELEASE`
  - Optional build metadata: `MAJOR.MINOR.PATCH+BUILD`
  - Optional combined prerelease/build: `MAJOR.MINOR.PATCH-PRERELEASE+BUILD`
  - Optional dev suffix: `.devN` or `-dev.N` (appended to the version)
- Prerelease values that start with `dev` must be exactly `dev.N` (e.g., `1.2.3-dev.4` is valid; `1.2.3-dev.x` is invalid).
- Bumps always operate on the core version and drop any prerelease/build/dev suffix.
