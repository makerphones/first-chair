# Prior art — what we adopted, what we may not touch

`starting-a-new-product.md` requires confirming the prior-art boundary on every build:
**credit adopted ideas; never copy non-permissive files or geometry.** This file is where that
gets recorded, per source, before anything from it reaches a design decision.

This repo ships CAD publicly under **MIT**. That is the constraint every entry below is measured
against.

---

## Variable Openmod — Armored Soul (Variable Static Audio)

Three published designs, 2024–2025:

- Part 1 — <https://www.printables.com/model/818386>
- Part 2 — <https://www.printables.com/model/905734>
- Part 3 (headset) — <https://www.printables.com/model/1004464>
- Driver source list — <https://docs.google.com/spreadsheets/d/1I18ZVEiOJQHK4EqZPyXjhn9TTDELaiebMAgrZp_Bvf8>

### The licence, and why it is a hard boundary

**Creative Commons BY-NC-SA 4.0** — Attribution, NonCommercial, ShareAlike. Confirmed from the
Printables listing on all three parts. Two clauses are blockers rather than cautions:

- **ShareAlike is incompatible with MIT.** Any derivative of that work must itself be
  BY-NC-SA, and a BY-NC-SA derivative cannot be relicensed as MIT. Geometry from it entering
  this repo would take the repo's licensing with it.
- **NonCommercial forbids commercial use.** MakerPhones has a book with two assigned ISBNs and
  a plausible kit business. A derivative would be permanently barred from both.

Printables states as much on the page itself: **"✖ Meets Open Definition"** and **"✖ Free
Cultural Works."** Despite the title, BY-NC-SA does not meet the Open Source Definition. That
is the author's choice to make and it is a legitimate one — it is simply a different thing from
what this project is doing.

> **HARD BOUNDARY: none of their files, ever.** Not imported, not traced, not scaled, not
> measured-and-redrawn. The practical safeguard is the same one set for the Grado CAD — design
> ours from our own constraints, and do not have their files open while doing it.
>
> **The downloads must not enter this repo.** Not in `design/`, not in `reference/`, not
> gitignored inside it. An accidental `git add -A` would be expensive.

*(Not legal advice. The MIT-vs-ShareAlike conflict is not a grey area.)*

### What we adopted — ideas, methods and facts, which copyright does not cover

Credited here because it is right, and because the author was explicit that the series exists
as *"a base that people can build upon and improve."*

| Adopted | Why it matters to us |
|---|---|
| **Captured M4 hex nuts in printed pockets, instead of heat-set inserts** | Their whole fastener BOM is 10 × M4×20 pan-head + 10 × M4 DIN934 nuts. Ours was **22 heat-set inserts across three sizes, plus a soldering iron and the technique to use it**. First Chair exists because the Daily Driver's hardware was *"a wall for the person the manual is trying to reach"* — and we had removed the eight-supplier problem while keeping the technique problem. A captured nut costs pennies, ships anywhere, needs only a screwdriver. |
| **The rear shell as a separate, swappable part** | Their open/closed is a *part swap*; ours was a *parameter* — which is why deleting the closed-back variant deleted a whole capability. A part survives what a flag does not. They also ship `custom-open-shell` / `custom-closed-shell` as explicit hack points. |
| **Spacer-based pad adapters** | One mount plus a per-size spacer and ring reaches both Brainwavz HM5 and Sony MDR-XB1000. A direct answer to our "the pad decides the outline" rule: put an adapter layer in rather than redesigning the mount per pad. |
| **Ship a `-lower-tolerances` variant** | Rather than making the builder rescale for their printer. Cheap, and kind. |
| ~~Cross-generation part compatibility~~ **— CONSIDERED AND REJECTED 2026-08-07** | Their three products share a common parts kit, and I argued we should copy it. Wrong: part commonality is a manufacturing-economics answer to a **tooling** problem, and FDM has no tooling — a part costs the same printed once or four times. The payoff is zero and the cost is real, since a shared part must be sized for the worst case. Each of our products is a different size and shape, every part is printed individually, so each should be exactly what its product needs. We share the **bow** (a bought part, where tooling economics do apply) and **conventions**. Nothing else. |
| **Raw 1.75 mm TPU filament as a flexible component** | Part 3's BOM lists *"45 cm of unprinted 1.75 mm TPU filament"*. Using stock filament as a compliant element costs nothing and every builder already has it. |
| **BOM facts** — PJ392 socket, M4 DIN934, JST PH 2-pin, HM5 pads, MonsterBolts as a source | Part numbers and suppliers are facts, not expression. |
| **The driver source list** | A directory of parts and suppliers — factual data. Our brief calls choosing the driver *"the gate on everything else"*, so this is materially useful and entirely safe. |

### The architecture, read from their CAD (2026-08-07)

Measured from the published `.3mf` parts — bounding boxes only, to understand how it is put
together. No geometry taken.

```
EARCUP — three stacked plates, not a cup
  40mm-pad-mount.3mf     96 × 96 ×  5.0      driver-size specific, ±grille
  40mm-body.3mf         106 × 100 × 12.2     driver-size specific
  open/closed-shell     100 × 100 × 18.0     SHARED across every 40–60 mm driver
                                    ─────
                                     35.2 mm total depth, in three shallow plates

HEADBAND
  headband-arc          183 × 114.6 × 36     the band, 36 wide
  tpu-suspension-pad    200 ×  60  ×  1.5    a FLAT 1.5 mm sheet that flexes into shape
  yoke                  100 ×  71  × 10.0    a flat arc; mk2 11.1, 90°-variant 11.5
  headband-clip          36 ×  12  ×  9.2
  screw-holder           10 ×  10  × 12.2    the captured-nut part — IDENTICAL in Part 1 and 2
```

**The finding that matters more than any of the individual ideas: every part is a shallow,
flat-printing plate.** 5 mm, 12 mm, 18 mm, 10 mm, 1.5 mm. Nothing is a deep cup. Their 35 mm
of earcup depth is *three plates stacked*, which is how the listing can claim **"easy to print
out without any supports"** and mean it.

That is not a styling decision. **It is the print constraint doing the architecture** — and it
is the answer to a question this project has been circling for days. We went looking for a
house *language* and kept borrowing one from machined products. For a printed product the
language should fall out of what prints well: flat parts, no supports, layer lines along the
load. Their whole object is legible as that one rule applied consistently.

Ours, by contrast: one cup, 27.6 mm deep, printed grille-face-down with *"light supports
(pivot bosses)"*. Our brief demands support-free printing of the **yoke** and the **slider**
and says nothing at all about the cup. That is an inconsistency we imposed on ourselves.

Two more things the measurements give away:

- **Rotation is a file, not a joint.** `yoke.3mf`, `yoke-mk2.3mf`, `90-degree-rotation-yoke.3mf`
  share one 100 × 71 envelope. You do not build a swivel — you print the one you want. A whole
  degree of freedom's mechanism, deleted for the cost of an extra STL.
- **Height adjustment is clip position, not a slider.** There is no slider part anywhere in the
  bundle. Given ours is the hardest unsolved item in the build, that is worth a real look.

### The signal we should take most seriously

Part 3: *"you must have some experience with soldering before attempting this. It's a pain
trying to solder everything. **Which is why I made tools for it** to make it less of a pain."*

An experienced designer had to **build and publish separate tooling** to get past the soldering
step. That says the electrical assembly — not the mechanical — is the real barrier in a printed
headphone. Our brief has cable entry listed as an open question; it should be treated as a
first-class design problem, and the target should be *minimising or eliminating soldering*,
not documenting it better.

### What we deliberately did NOT adopt

**Their printed PETG headband.** Our position — no FDM plastic is a good spring, creep will
loosen it within months — is better evidenced, and it is backed by the maker's own experience
bending and tempering spring steel blanks. This is the one place our design is ahead.

### Context worth recording

The author states Part 3 is *"likely to be the last headphone I make and of course the last
open source headphone that is released,"* and the project website was **shut down for lack of
funds** in May 2025; the assembly instructions now survive only in the download bundle and the
Wayback Machine.

Noted without triumph — it is a real loss to the space, and the work was generous. But the
structural observation is worth keeping: **the NonCommercial clause foreclosed the funding path
that might have sustained it.** MakerPhones being MIT, with a commercial route, is a difference
in kind rather than a licensing preference.
