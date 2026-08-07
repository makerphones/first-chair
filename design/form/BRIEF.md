# First Chair — design brief

**Design me a headphone.** Not a variation on one I've already drawn — I have that, and it is
the problem. I want to see what you'd do with the constraints, not watch you execute my answer.

Previous passes failed because I over-specified: I handed over a parts list, a mechanism, exact
dimensions and a naming contract, and then was disappointed to get back a rearrangement of the
product I already had. This brief gives you the constraints that are genuinely fixed, the goals
that matter, and then gets out of the way.

---

## 1. What it is, and who it's for

An **open-back supra-aural (on-ear) headphone**, 3D printed, open source, built at home by
someone who owns a printer and has never built a headphone before.

It is the **first rung of a learning path**. Not the cheapest, not the simplest — the *first*.
Someone builds this, it works, it sounds good enough to keep wearing, and they believe they can
build the next one. That is the whole job.

The character we're accepting honestly: a supra-aural leaks by design, so it will be **bass-
light**. Grado is the reference point and Grados are famously bass-light *and* famously
unfussy about placement — those are the same fact. We lean into it rather than chasing
extension the hardware can't produce.

## 2. What is genuinely fixed — and why

Everything here is set from **outside** the design. None of it is my taste.

**A 40 mm dynamic driver.** Ø39.5 measured frame, ~32 Ω. Bought. 40 mm is the standard size and
we're not designing around a specialty part.

**A commodity Grado-pattern earpad. We design and ship no pad.** This is the single most
constraining thing in the brief and it works inward:

> The foam stretches over a rim of about **Ø54**, then grips a body of about **Ø48** behind a
> step of about **3 mm**. Retention is *axial* — the lip stops it climbing forward. Radially
> it's light: the pad rotates freely on the cup but doesn't slide off.

Those numbers have real tolerance — the same pads fit cups across Ø54–56.7 — so treat the
**relationship** as fixed and the exact figures as approximate. It must mount a pad someone can
buy for ten dollars, in a dozen variants, forever.

**Printed on an FDM machine.** 0.4 mm nozzle, 0.2 mm layers, PETG. Nothing thinner than 2 mm.
**Support-free is a constraint, not a preference** — if a part needs supports it's the wrong
part. Layer lines run *along* the load on anything structural; layer adhesion is the weak axis
and that's what snaps.

**No printed springs.** FDM plastics creep under sustained strain. A printed band works on day
one and is loose by month three — the most likely way this build disappoints someone.

**Fasteners: M3 only.** M3 heat-set inserts, M3 screws, M3 washers. One thread, one insert
size, all metric. Not fewer fasteners at the cost of variety — *one kind*.

**Real heads.** Ear-to-ear is roughly 147 mm at the 50th percentile, ~140–155 across adults.
Clamp force in the HD 600 / DT 770 class — but note that force on a supra-aural concentrates on
the ear rather than spreading onto the skull, so the *pressure* is much higher. Comfort is a
first-order problem here, not a finishing touch.

## 3. What is yours to decide — explicitly

I have previously prescribed every one of these. **I am not prescribing them now.**

- **The part breakdown.** How many parts, what they are, where they split. There does not have
  to be a "cup" and a "baffle" and a "clamp ring" — that's just what I did last time.
- **How the driver is held**, and whether the thing holding it is the same thing the pad mounts to.
- **How deep it is, how thick the walls are, how much volume is behind the driver.**
- **The rear treatment.** It must be acoustically open — you can see through to the driver — but
  what that looks like is open.
- **How it attaches to the head.** A sprung steel band is what I have; anything that clamps
  without a printed spring is fair game.
- **Whether height adjustment exists at all**, and how. My last mechanism was a post and a
  thumbscrew. It's gone. Discrete positions, a compliant layer, or nothing are all on the table.
- **How many rotation axes, and how they're achieved.** A joint is one answer. A printed
  variant is another. So is doing without.
- **Cable entry**, and how the driver gets wired.

## 4. What it has to actually do

Functions, not parts. Solve these however you like:

1. Hold a 40 mm driver at a controlled distance and angle from the ear
2. Present a rim a commodity Grado-pattern pad mounts to
3. Let the back radiate freely
4. Carry the whole thing on a head at a comfortable, consistent clamp force
5. Fit adult heads across the range
6. Get a cable to the driver
7. **Come apart and go back together, repeatedly.** The person building this will take it apart
   more than once. When serviceability and manufacturability conflict, serviceability wins.

## 5. The character

From the design letter I wrote to the industrial designer on my last headphone:

> *"Something that lasts a lifetime and gets passed down. It should exude quality craftsmanship,
> **almost looking handmade but with extreme precision**. Parts should be easily replaceable and
> durable. Reduce weight wherever possible."*

**And the house language is the print process itself.** Not applied to the object — generated by
it. With one filament, material can't separate parts, so *form* has to: profile, section change,
how an edge breaks, how one part meets the next. A printed part that owns its layer direction is
on-brief. One pretending to be injection-moulded is not. Fasteners are visible and that's fine —
deliberate, neither hidden nor fetishised.

Five rules, from the corrections I gave that designer:

1. **If a mechanism isn't needed, delete it.** I killed a fold hinge with *"an extra weakness we
   do not need."* Not "unnecessary" — a **weakness**.
2. **No ornament.** *"I am assuming this is for aesthetic reasons? I do not have to have this."*
3. **Simplify until it's simple, then stop before it's ugly.** Austere is not resolved.
4. **Material follows load.** Beefy where it works, gone where it doesn't.
5. **The prototype settles arguments, not the drawing.**

**The sentence the design has to survive:** *"The only parts not 3D printed are ___."* If that
can't be finished in a short breath, it isn't a 3D printed headphone — it's a buy-a-lot-of-parts-
and-print-a-few headphone. Target answer: screws, drivers, earpads, cable, and whatever provides
the spring.

## 6. Don't drift

- **It must not read as a shrunken over-ear.** A supra-aural sits *on* the ear; it's a different
  object, not a small version of another one. This is the failure mode I keep hitting.
- **Don't design for a factory.** No bezel-and-inlay, no polished collars, no four-material
  palette. Those are machining languages and we have one filament.
- **Don't make it precious.** Someone is printing this at home in PETG.

## 7. What I need back, and why

You can't produce a printable part — no booleans, no fillets, no tolerances — so I re-author the
chosen direction by hand in parametric CAD. **These five make that handoff clean, and none of
them constrain what you design:**

1. **1 unit = 1 mm.** glTF defaults to metres; unspecified, a model imports at 1/1000 into a
   slicer and nothing errors.
2. **Every number in one constants block** at the top.
3. **Build shapes from explicit profile arrays or curves**, not hardcoded primitives — a lathe
   profile as a list of `[radius, depth]` points is *directly* re-authorable by me. This is the
   single most useful thing you can do.
4. **One named node per part.** Your names, `_R`/`_L` for sides. Tell me what you chose.
5. **State the parts list and the rules in words.** I re-derive from rules; the geometry is the
   sanity check.

**GLB only, never OBJ** — OBJ has no scene graph and loses the hierarchy.

## 8. The deliverable

**Three directions**, each a genuinely different answer to §4 — not three finishes on one idea.
State each one's rule in words *before* you model it.

One page, one live 3D stage, nav switching between them. One line per direction on **what
doesn't close** — a stated conflict is worth more to me than a resolved-looking render, and it's
been the most valuable thing you've produced.

**No written study. If it isn't in the stage, it doesn't exist.**

---

*Context if you want it — my own prior headphone work is in `design/form/reference/` with
captions, and `docs/prior-art.md` records what we've studied and what's off-limits. Read them
as background, not as a template. `params.py` describes the design I'm replacing; don't take
numbers from it.*
