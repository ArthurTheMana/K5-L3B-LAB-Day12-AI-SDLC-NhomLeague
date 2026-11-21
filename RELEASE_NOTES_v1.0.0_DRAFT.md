# Release notes draft — v1.0.0

**Status: DRAFT — not a published GitHub Release.**

## Features
- Gather: movement, oxygen/HP, fish, crocodile and freshness tracking.
- Quan: ingredient stock, cooking and customer flow; Shop and day loop.
- Browser-based interface with warning cues and high-contrast mode.
- Contract v1.3, benchmark (`chonoi.bench`) and soak (`chonoi.soak`) entry points.

## Run
See README.md for the three-command clone workflow and controls.

## Verification
- Benchmark RGB software raster 1280×720, 3 s warmup, 30 s measured: see `docs/proof/phase-4/bench.json`. This is **not** browser Canvas/GPU FPS.
- Soak 10 days: see `docs/proof/phase-4/soak.json`.
- Full regression from release commit still requires verification.

## Known limitations / release gates
- Browser rendering performance and warnings need a manual UI test.
- TEAM.md and members' reports require verified real GitHub identities.
- Asset rights need verification; choose a source-code license only with group approval.
- Create the GitHub tag `phase-4` and release `v1.0.0` at the same main commit after integration.
