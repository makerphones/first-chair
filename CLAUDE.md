# CLAUDE.md — working notes for Claude Code

This repo is the parametric CAD for the **First Chair**, an open-source
40 mm open-back headphone. It's a project of MakerPhones / Warren Labs. The
designs are meant to be downloaded, forked, and modified, so the repo is the
source of truth — not chat.

## What this is

Code-based CAD in **CadQuery** (Python). The model emits both STL (print-ready)
and STEP (clean B-rep for editing elsewhere). Code-CAD was chosen on purpose:
text files diff and version-control naturally, and anyone can fork and modify.

## How it's laid out

- `params.py` — **single source of truth** for every dimension. Change values
  here, not inside part files. Derived values are `@property` helpers on
  `Params`.
- `parts/` — one file per part, each exposing a `make_<part>()` that returns a
  CadQuery `Workplane`. Each part builds **independently** (the spec wants every
  interface independently iterable).
  - `cup.py` — rebuilt at 54 mm (2026-08-06); see DESIGN-LOG
  - `baffle.py` — real geometry, but **still on Daily Driver's Ø91.44 numbers**
    (`baffle_outer_diameter` 77.0 against a LOCKED Ø54 plate). Next part to rebuild.
  - `yoke.py`, `slider.py` — real geometry, NOT stubs (a v0.4 lofted-arm fork and a
    v0.9 Beyerdynamic-style lozenge clamp respectively). The "stub" description was
    inherited from an outdated Daily Driver doc and would have had someone re-solving
    finished work.
  - `features.py` — **reusable mechanical primitives** (screw boss, post,
    fillet, thread, snap): established convention, **authored once and reused —
    never regenerated per part**, never re-derived by hand each time. Currently
    a stub. (cup.py's inline bosses migrate here later — see DESIGN-LOG.)
- `build.py` — renders parts to `output/`. `python build.py` for all, or
  `python build.py cup baffle` for specific ones. Failures are isolated per part.
- `design/` — the AI-assisted **form** pass. Runs in **Claude Design**, not in this
  repo: there is no MCP verb for its 3D agent, so the loop is prompt there →
  download the GLB → check it → ingest. It produces FORM and FIGURES; it has no
  boolean operations, so **nothing printable can originate there**. See
  `docs/design-pipeline.md`, and `warren-labs/docs/claude-design.md` for the
  verified capability map. (The old FAL image pipeline was deleted 2026-08-06.)
- `docs/design-spec.md` — the functional spec the CAD is built against.
- `docs/design-pipeline.md` — the AI design pipeline + the taste-vs-convention
  boundary (taste → `params.py` + parametric form in `parts/*.py`; convention →
  `parts/features.py`).
- `docs/DESIGN-LOG.md` — the running record. **For an open design the log is
  part of the product.** Add an entry for every real decision or iteration.
- `docs/filesystem-mcp-setup.md` — how to give a chat-side review session
  read-only access to this repo via the filesystem MCP (config + manual enable step).

## Setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python build.py
```

## Working rules (these matter)

1. **`params.py` is the only place dimensions live.** If you need a new
   dimension, add it there with a comment, don't hardcode it in a part.
2. **Don't silently resolve open questions.** The spec and DESIGN-LOG flag real
   unknowns (pad lip location, baffle screw direction, yoke-to-cup mount,
   headband radius, production driver, vent open area). If you make a call on
   one, it's because the human decided — record it in DESIGN-LOG with the
   reasoning. Never invent a driver, part, supplier, price, or spec to make
   geometry "work."
3. **Accuracy over plausibility.** If a dimension isn't known, say so and leave
   it parametric/flagged rather than guessing a number that looks right.
4. **Keep parts independently buildable.** Don't create cross-imports between
   part files; share only through `params.py`.
5. **Functional geometry in code; taste-driven form is a separate pass.** The
   outer profile, vent slot shape (the signature look), and yoke styling are
   refined deliberately, not auto-generated. Get fit and function right first.
6. **Log as you go.** New entry at the top of `DESIGN-LOG.md` each working
   session.

## Current state

Forked from Daily Driver 2026-08-06. All 17 parts build. The cup has been rebuilt
against the LOCKED 54/48/42 profile; the gate is at **1 HARD failure**, on the
inactive closed-back variant (see DESIGN-LOG for the three ways out).

**The standing hazard in this repo is inherited absolutes.** Daily Driver was a
Ø91.44 cup; only eight parameter values changed at the fork. Any hardcoded radius
you meet is suspect until it has been rebuilt at 54 — and note that a gate check
written at the old scale can read GREEN on geometry that is nowhere near the part.
`baffle.py` is the next part due this treatment.

## Distribution

`output/` is gitignored — STL/STEP ship to builders via tagged GitHub Releases,
not committed to the tree. License is still an open decision (see README).
