# AI-Assisted Design Pipeline

**v0.3 · 2026-08-06 · Claude Design replaces the FAL image pipeline**

This describes how AI assists the design of a MakerPhones build and, just as importantly,
**where it stops**. The pipeline produces *form* and *figures*. It never produces engineered
CAD. The headphone you can actually build is authored by hand in CadQuery, from human
decisions.

This file is not First-Chair-specific. First Chair is the fork template for every build
after it (`starting-a-new-product.md`), so what is written here is the standing process.

**Capability map: `warren-labs/docs/claude-design.md`** (internal — deliberately not linked,
since this repo is public and that one is not). That file is the source of truth for what the
tool can and cannot do — verified by direct probe on 2026-08-06, not from marketing copy —
and it applies line-wide, beyond MakerPhones. It is not restated here; the one conclusion
that changes how you work is repeated below, and nothing else.

What follows is the MakerPhones-specific part: where it sits in *this* process, what we hand
it, what we demand back, and what we do with the result.

---

## The one thing to internalise

**It has no boolean operations.** No CSG means a hole in an arbitrary place on a curved wall
is impossible, which means **nothing printable can originate there** — and that settles the
handoff with no per-part judgement. Form and figures upstream, engineering in CadQuery. It
described its own output as *"industrial-design intent, not a print-ready CAD part"*, which
is the same boundary we draw from the other side. Both parties agreeing on that unprompted
is the reason it is safe to adopt.

The corollary is the useful part: **it is valuable at the two ENDS of a project and useless
in the middle.** Before CAD exists, nothing is lost to a tool that can't do booleans, because
there is no engineering yet. After CAD exists, it is the best documentation-figure tool we
have. While CAD exists, it can only get in the way.

---

## Workflow: Diverge → Resolve → Engineer

Three phases, each with its own surface and its own job. The discipline is not doing one
phase's work on another's surface.

```
DIVERGE                          RESOLVE                          ENGINEER
find the form + family           develop it into a buildable      author the geometry
Claude Design (3D)               design — chat + SVG sketches     Claude Code + CadQuery
named, scaled GLB                parts, fit, fasteners,           params.py + parts/*.py
       │                         acoustics, wall, weight          build · gate · log · commit
       │                                  │                                │
  GLB + part list ────────────> resolved design intent ──CC prompt──> verified parts
       └──────── inspect_glb.py, then read into chat ────┘

                                                    ┌─────────────────────────────┐
DOCUMENT (after Engineer)                           │ CadQuery/OCP renders ───────┼──> Claude Design
compose, annotate, typeset the figures              │ (our geometry, our fidelity)│    composes the plate
                                                    └─────────────────────────────┘
```

### 1 · DIVERGE — find the form, before any CAD exists

Run the family/form pass in Claude Design, seeded with the repo and the naming schema (see
Conventions). Ask for **the rules in words before it models anything** — proportion and rule,
not a repeated detail; something that still works at 54 mm and at 91 mm. Then let it model.

Output: **a named, hierarchical, correctly-scaled GLB** — not a picture. That is the whole
reason this replaced what came before. Run `makerphones/scripts/inspect_glb.py` on it (it is
in the parent repo, not this one), read the part list, and
carry the numbers into the discussion.

**Two things to push back on, every time.** It will try to make a "family" by repeating a
detail — that is the weak version. And it drifts toward glossy injection-moulded consumer
product, because that is what the training data is full of; anything printed, machined or
hand-built has to be asked for explicitly and defended on the second pass.

### 2 · RESOLVE — develop the chosen direction into a buildable design

With the direction picked, work the design conversationally in chat: the parts, how they fit
and fasten, then the engineering-taste calls — connector choice, acoustic treatment, wall
thickness, weight, and the design language carried across parts. Claude sketches schematic 2D
concepts (SVG) and reasons through structure, constraints, acoustics and printability.

**This is where the acoustic and mechanical decisions are made, not just the visual ones** —
chat is the only one of the three surfaces that can *reason*, so the judgment calls live here.
Output: a resolved design intent, ready to engineer.

### 3 · ENGINEER — author the geometry

In Claude Code: author the parametric CadQuery geometry (`params.py` + `parts/*.py`), then
build, gate, log, commit. The CC loop is for engineering and verification — **not** for
iterating taste one tweak at a time; that belongs in Resolve.

### 4 · DOCUMENT — the strongest mode, and the workflow it proposed itself

**Do not have it re-model geometry at lower fidelity to draw a picture of something we
already hold as real CAD.** Export views from CadQuery/OCP, hand it the renders, and let it
compose, annotate, sequence and typeset: exploded assemblies, print-orientation plates with
overhang callouts, numbered step figures, hardware tables. For schematic figures that need no
dimensional truth (exploded order, orientation, fastener callouts) it can build them directly.

For a documentation-led product this is plausibly worth more than anything it does for the
CAD, since the CAD is already solved and illustration is a cost you pay forever.

---

## Conventions — set these in every prompt

**Two of these fail silently. That is why they are a checklist and not advice.**

- **Author at 1 unit = 1 mm.** Matches CadQuery and every slicer. glTF's spec convention is
  **metres**, so a model that does not say otherwise imports at **1/1000 scale** into a
  slicer — a 54 mm cup arrives as a 0.054 mm speck, or a correctly-authored-in-metres file
  arrives 1000× too big. Nothing errors. `makerphones/scripts/inspect_glb.py` warns on **both** failure
  directions; run it on anything that arrives, without exception.
- **GLB only, never OBJ.** OBJ has no scene graph — it carries groups, not parent/child nodes
  — so it *structurally cannot* express the `SUBASSEMBLIES` hierarchy that makes the output
  worth having. An OBJ silently degrades the one property we are asking for.
- **Impose the mesh-naming schema.** Give it `assembly.py`'s `SUBASSEMBLIES` contract up
  front. It conforms exactly — verified against a test part whose names (`cup_R`,
  `cup_shell_R`, `boss_m3_1..4_R`) landed against the contract unchanged. When the names
  match, ingest is nearly free; when they don't, someone hand-maps 69 meshes.
- **Seed it, and record the seed.** A project can be seeded from a design system, uploaded
  files, or a GitHub repo. **The reproducible unit is (skill + seed + prompt), not the prompt
  alone** — record all three or the result cannot be reproduced later. A prompt kept without
  its skill and its seed is not a record of anything.
- **Write the prompt self-contained. It cannot see this repo.** Claude Design has no
  filesystem access, so "read `docs/industrial-design-brief.md`" silently yields a session
  working from its own priors — the exact failure the pass exists to fix. State every
  constraint inline and reference no local path. Seeding from the public GitHub repo does give
  it real access, but keep the prompt self-contained anyway: "go and read X" is a weaker
  instruction than stating X, and it fails quietly when the seed doesn't take.

The `claude-design` MCP has **no verb for the 3D agent** — that capability is driven by
chatting in Claude Design itself, so the loop is: prompt there, download the GLB, ingest here.
What the MCP usefully adds is **seeding**: writing our conventions and parameter table into a
project so the session starts inside our constraints instead of inventing its own.

---

## Taste vs. convention — the split that decides what AI touches

This boundary predates Claude Design and survives it unchanged. It is worth being explicit
about why: **Claude Design produces taste, never convention.** It is a form tool. It cannot
author a screw boss you would reuse, and it should never be asked to.

**TASTE is human and manual.** Cup depth, grille form, where the screws go, proportions,
stance, finish. These are judgment calls, decided from references **plus real measurements**
(that deciding is **Resolve**; **Engineer** only encodes the result). Taste is encoded two
ways, both authored by you, in code: some taste is a **number** (cup depth → a value in
`params.py`), and some is **form** (grille pattern, cup profile) authored as parametric
**geometry in `parts/*.py`** and driven by those params. AI may *inform* taste by showing
options; it never *sets* it, never writes a dimension, and never authors a part.

**ESTABLISHED MECHANICAL CONVENTIONS are not reinvented.** A screw boss, a fillet, a standard
thread, a snap fit — solved by decades of practice. They live as **reusable parametric
helpers**, authored once from convention in `parts/features.py`, and **reused** across parts.
Convention is a library, not a creative act.

| | Who/what | Where it lives |
|---|---|---|
| **Taste** | Human decision, informed by form refs + measurement | `params.py` (numbers) + `parts/*.py` (form) |
| **Convention** | Standard practice, authored once | `parts/features.py` (reusable helpers) |
| **Form + family** | Claude Design (3D) | `design/form/<date>/` — GLB + the prompt record |
| **Engineered parts** | Human + CadQuery | `parts/*.py` |
| **Documentation figures** | Claude Design, over **our** renders | `docs/figures/` |

There is a second reason the boundary holds, beyond "no CSG": **engineered features are
decisions, not pixels.** Where the screws go, how deep the cup is, how the baffle seats, the
vent open area — these have consequences for fit, acoustics and print success. They are
reasoned and measured, not inferred from a form study, and no form study knows your driver's
caliper measurements or your printer's tolerance.

---

## Layout

```
docs/industrial-design-brief.md   the form brief that seeds the Diverge pass
docs/design-pipeline.md           this file
design/
  form/<date>/                    Claude Design GLB + the (skill + seed + prompt) record
  figures/                        source renders handed out for documentation plates
scripts/inspect_glb.py            (in the makerphones repo) scale + naming + hierarchy check
parts/features.py                 reusable mechanical primitives (convention)
```

Curated keepers are committed; the exploration history is part of an open design's story.
Record the seed alongside the GLB — a GLB with no `(skill + seed + prompt)` note beside it is
an orphan nobody can regenerate.

---

## What this replaced, and why the old pipeline is gone

The **FAL image pipeline** — Stage 1 text→concept image, Stage 2 image→reference mesh — was
removed from this repo on 2026-08-06 along with `pipeline/` (`config.py`, `gen_concepts.py`,
`gen_reference_mesh.py`, `smoke_test.py`) and the FAL client dependency.

It was a two-stage lossy path whose output was images we did not want to build, and it was
abandoned rather than finished. Claude Design does both stages in one and returns **named,
hierarchical, correctly-scaled geometry instead of a picture**. That is not an incremental
improvement: an image has to be re-interpreted by a human before it can become parameters,
and a named part list reads straight into `params.py`.

**Deleted rather than kept as a documented fallback — that is a decision, recorded here so it
is not mistaken for neglect.** The argument for keeping it was that a fallback costs nothing
to leave in place. It doesn't cost nothing: an abandoned two-stage path sitting in `pipeline/`
with working code, a config file and a smoke test reads as *current* to the next person who
opens the repo, and the fork template propagates it into every future build. A trap that
regenerates itself with each fork is worse than a paragraph of history. The code is in git
history and in the Daily Driver repo if it is ever genuinely wanted.

*(Daily Driver still carries the FAL pipeline and its v0.2 version of this document. It is
paused, not deleted, and reconciling it is deliberately out of scope here.)*

---

*v0.3 · 2026-08-06 · Rewritten around Claude Design; FAL pipeline and `pipeline/` deleted;
conventions promoted to a checklist because two of them fail silently.
v0.2 · 2026-06-14 · Added the Diverge → Resolve → Engineer workflow (Resolve was the missing
layer). v0.1 · 2026-06-13 · Written as the form pass opened.*
