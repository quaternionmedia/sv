# Adoption Guide

This guide shows a lightweight, added-dependency-free way to adopt `sv` for consistent
versioning across a repo. It assumes a single `VERSION` file is the source of
truth and uses `tutorial.py` as the working reference.

## Quick start

1) Add a `VERSION` file at the repo root with an initial value like:
   `0.1.0.dev0`
2) Run the tutorial once to see the flow end-to-end:

```bash
python sv/tutorial.py
```

This reads `VERSION`, bumps the dev version, and writes it back. For a release
bump, run:

```bash
python sv/tutorial.py --bump minor --release
```

To set an explicit version:

```bash
python sv/tutorial.py --set 1.2.3
```

## Recommended structure

- Keep `VERSION` in the repo root.
- Use `tutorial.py` as the canonical example (copy its pattern into your own
  release scripts).
- Keep version changes committed so CI and packaging flows are reproducible.

## Typical adoption path

- **Local development:** Use dev bumps (`.devN`) for CI builds and snapshots.
- **Release prep:** Switch to a release bump (major/minor/patch) in your own
  script when you are ready to ship.
- **Distribution:** Use `npm_version` or `mod_version` depending on downstream
  tooling requirements.

## CI integration idea

In CI, run the bump script only on mainline branches and fail if `VERSION`
does not match the expected format. This keeps builds repeatable and avoids
surprising version jumps.

## Troubleshooting

- If you see `ModuleNotFoundError: No module named 'sv'`, run from the repo
  root (`python sv/tutorial.py`) or add the repo parent to your `PYTHONPATH`.
- If `VERSION` is missing or empty, create it with a valid semver like
  `0.1.0.dev0`.
