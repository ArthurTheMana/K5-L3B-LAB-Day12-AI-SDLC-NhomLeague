# Phase 4 QA run — Release candidate v1.0.0

## Benchmark (real 1280×720 RGB offscreen raster, not browser Canvas/GPU)

Command: `python -m chonoi.bench --seed 42 --duration 30 --out docs/proof/phase-4/bench.json`

- avg_fps: 178.75
- p1_low_fps: 106.21
- frames: 5363
- measured_s: 30.0027
- load_ms: 11.199

## Soak

Command: `python -m chonoi.soak --seed 7 --days 10 --out docs/proof/phase-4/soak.json`

- days_completed: 10 / 10
- crashes: 0
- results entries: 10

## Regression

- Combined discovery command: `python -m unittest discover -s tests` PASS 100% in a single invocation (29 files, 180 tests in ~33.5s).
- Full regression suite verified on final main commit.

## Release verification
- Verified three visual warnings and high contrast mode (H key) in `chonoi/web/index.html` and `tests/test_ui_alerts.py`.
- Verified member handles and roles in `TEAM.md`, `CREDITS.md` and `docs/ai-usage-log.md`.
- All assets, MIT license and package contents verified.
- Ready for GitHub tag `phase-4` and release `v1.0.0`.
