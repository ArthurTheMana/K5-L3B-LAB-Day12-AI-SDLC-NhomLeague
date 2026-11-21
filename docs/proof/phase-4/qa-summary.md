# Phase 4 QA run — local ZIP working copy

**Not a tagged release or final `main` commit.**

## Benchmark (real 1280×720 RGB offscreen raster, not browser Canvas/GPU)

Command: `python -m chonoi.bench --seed 42 --duration 30 --out docs/proof/phase-4/bench.json`

- avg_fps: 178.75
- p1_low_fps: 106.21
- frames: 5363
- measured_s: 30.0027
- load_ms: 11.199

The browser UI has not been visually benchmarked.

## Soak

Command: `python -m chonoi.soak --seed 7 --days 10 --out docs/proof/phase-4/soak.json`

- days_completed: 10 / 10
- crashes: 0
- results entries: 10

## Regression

- Ran each `test_*.py` file separately: 29 files, 180 tests PASS.
- Combined discovery command timed out; not confirmed PASS in a single invocation.
- Rerun CI on final `main` commit before tagging.

## Pending release-owner checks

- Verify three warnings and high contrast in the live browser.
- Complete true member handles in `TEAM.md`, individual reports and retro.
- Confirm asset provenance, license decision and package contents.
- Tag `phase-4` and publish GitHub Release `v1.0.0` from **the same main commit**.
