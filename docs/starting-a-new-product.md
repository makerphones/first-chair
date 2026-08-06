# Starting a new product (the template)

The "template" for product #2+ is **this repo** — fork it copy-on-write. There is no
separate skeleton to maintain (a parallel skeleton drifts from the live code; a fork
is always current). The value here is the **checklist of what to change**, so a new
product starts clean instead of half-edited.

> Hold until product #2 is actually greenlit. When it is, this is the cold-start.

## 1. Fork

```bash
cp -r builds/first-chair builds/<new-product>         # copy-on-write from the reference
cd builds/<new-product>
rm -rf .git && git init                               # its own standalone repo
rm -rf docs/DESIGN-LOG.md output/ docs/models/ docs/renders/   # start a fresh log + artifacts
```

Then run **`/headphone-intake`** → fill `BRIEF.md`. See `new-build-intake.md`
(pipeline), `decision-tree.md` (the order), `measurement-priorities.md` (what blocks
the first print).

## 1b. Run the form pass in Claude Design — BEFORE writing `params.py`

**This is the one point in the process where it has the most leverage and the least
risk**, and the ordering is the whole point: before `params.py` exists there is no
engineering to lose to a tool that cannot do booleans, and the output is a named part
list that reads straight into one. Afterwards it can only get in the way.

Seed the project with **this repo** and with `assembly.py`'s `SUBASSEMBLIES` naming
schema, then ask for the family rules **in words before it models anything** —
proportion and rule, not a repeated detail. Full process in `docs/design-pipeline.md`;
verified capability map in `warren-labs/docs/claude-design.md`.

Four conventions, and **two of them fail silently**:

- [ ] **Author at 1 unit = 1 mm.** glTF's spec convention is *metres*, so an
      unspecified model imports at **1/1000** into a slicer. Nothing errors — you just
      get a 0.054 mm cup.
- [ ] **GLB only, never OBJ.** OBJ has no scene graph, so it *structurally cannot*
      carry the `SUBASSEMBLIES` hierarchy that is the reason to use the tool at all.
- [ ] **Impose the mesh-naming schema** up front. It conforms exactly when asked;
      when it isn't asked, someone hand-maps every mesh.
- [ ] **Run `makerphones/scripts/inspect_glb.py`** on anything that arrives — it warns
      on **both** scale-failure directions, which is the only cheap way to catch the
      two silent ones above.
- [ ] **Record `(skill + seed + prompt)`, not the prompt.** A project can be seeded
      from a design system, uploaded files, or a GitHub repo. All three go in the
      record beside the GLB in `design/form/<date>/`, or the result cannot be
      reproduced later.

Then translate the resolved form into `params.py` (step 2).

## 2. Reset product-TASTE params, keep ARCHITECTURE params

`params.py` is ~60% reusable architecture, ~40% product taste. Reset the taste to
the new brief; leave the architecture unless the brief changes it.

| Keep (architecture / convention) | Reset to the new brief (taste / fit) |
|---|---|
| insert/screw dims, `m3_*`, `heatset_*` | `driver_od`, aperture/recess rules |
| structural floors (`wall_thickness*`) | `cup_interior_diameter`, `cup_outer_diameter` |
| pivot/insert mechanics, `pivot_boss_*` | `pad_*` (the earpad + lip) |
| gate thresholds (mostly) | `bow_*` (the chosen band) |
| the build→gate→log ritual | grille pattern, accents, `*_fillet`, signature |
| | `yoke_*`, `slider_*` if the mechanism changes |

Every dimension stays in `params.py` (single source of truth); parts stay
independently buildable.

## 3. The cross-cutting things that bite if you forget them

These live outside `params.py` and won't error — they just come out wrong:

- [ ] **`assembly.py` → `SUBASSEMBLIES`** — the node names (`cup_R`, `baffle_L`, …)
      are a public contract for the manual's parts viewer. Keep them or update the
      viewer's manifest to match.
- [ ] **`build.py` → `PRINTED` / `ACCESSORY` / `REFERENCE` sets** — re-classify any
      added/removed parts so the STL/STEP/render outputs are right.
- [ ] **`assembly.py` transforms** — if the cup/pad/mechanism orientation changes,
      the worn-pose transforms (`T_cup`, `T_yoke`, mirror) need re-deriving.
- [ ] **`bom.py`** — swap the driver / pad / bow rows + sources to the new brief.
- [ ] **GLB / Pages** — if the new product gets a web preview, enable GitHub Pages on
      the new repo from **main `/docs`** (`gh api -X POST repos/<org>/<repo>/pages
      -f 'source[branch]=main' -f 'source[path]=/docs'`). Pages serves
      `access-control-allow-origin: *`, which is what lets the manual's viewer fetch
      it cross-origin. Then add the build's pages to the website: a parts table in
      `src/data/build-parts.ts`, two `.mdx` pages under `src/content/docs/learn/`
      passing the new origin to `<PartsViewer>` / `<PartsGallery>`, and the handles
      into `astro.config.mjs` and `src/data/manual.ts`.
- [ ] **README + license** — restate scope; confirm the prior-art boundary (credit
      adopted ideas; never copy non-permissive files/geometry).

## 4. First build

`python build.py` (N/N) → `python gate.py` (0 HARD) → first DESIGN-LOG entry →
commit → **push**. Treat the first print as a measurement jig for the Tier-1
unknowns (`measurement-priorities.md`).

## When to extract a real code skeleton

After product #2 ships, you'll know what's *truly* reusable (vs Daily-Driver-
specific). That's the moment to lift the shared architecture into a `platform/`
base + a `parts/primitives/` library and turn this fork-guide into a thin skeleton.
Doing it now — from a sample size of one, mid-WIP — would just bake in guesses.
