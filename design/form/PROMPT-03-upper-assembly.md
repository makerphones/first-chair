Follow-on to the yoke pass. **The whole upper assembly is wrong** — the bow, the slider, and how they join. That's my fault, not yours: I gave you a parts list and never gave you the mechanism, so you invented one. Here it is properly. Design the three together, because they only make sense together.

## 1. The bow — a bought part, measured, not a variable

It's a Beyerdynamic DT-family sprung steel head bow. We buy it. Every number here is measured off the real part:

```
relaxed arc radius        63.5      (a 5 inch circle)
flexed on a head          ~78       this is the radius that sets ear spacing
developed length         236.2      rolled flat
strap width               33.0
strap thickness            0.8
```

The central ~110 mm carries an X-brace cut-out pattern. Each end runs out into **two flat prongs about 7 mm wide** over roughly the last 28 mm, and **each prong has a Ø3.2 hole about 5 mm in from its tip. The two holes are 26.0 mm apart.**

Both your studies have this wrong, and they don't agree with each other:

- the four-directions study: `BOW = { R: 98, t: 1.1, w: 13 }`
- the family study: `BOW_R = 108`

**The width matters most.** 13 mm reads as a wire; the real part is a 33 mm strap, and it looks and behaves completely differently. The radius being 98 or 108 instead of ~78 worn puts the cups in the wrong place relative to the head. Since the bow is the one component genuinely identical across all four products, getting it right is what makes the family study trustworthy.

## 2. How the bow attaches — settled, and simpler than what you drew

**Two M3 screws straight through the bow's own end-tab holes**, into heat-set inserts in the slider. That's it.

No clamp sandwich, no cover plate, no recess the prongs drop into, no captured band. You drew a clamp block that grips the strap; delete it. The bow was manufactured with mounting holes and is designed to be screwed — we use the holes it already has, at their 26 mm pitch.

This is the one joint in the build where we deliberately spend fasteners, because it's the only one carrying sustained spring load. Everywhere else, a screw has to justify itself.

## 3. The slider — this is the part to actually design

**A printed cantilever leaf with a detent bump, riding a notch ladder.** Height adjustment clicks from notch to notch.

**It deletes the thumbscrew, the brass insert and the pressure shoe in one move — that deletion is the whole point.** You drew a knurled brass thumbscrew clamping a printed leg with a smooth travel slot. That's a friction lock, it's what our over-ear does, and replacing it is a deliberate decision, not an oversight. There is no thumbscrew on this product.

Four things that constrain it:

- **The leaf must bend in the print plane, with the layer lines running along the leaf.** Same rule as the yoke, same reason: printed flat, it bends exactly across the layer boundaries where adhesion is weakest and it snaps early.
- **It has to print support-free.** If a form needs supports, it's out.
- **It tunes by leaf thickness.** That's the adjustment knob, and we're settling the actual number by printing a physical coupon — one rail, five sleeves at graduated leaf thickness — and picking by feel. So don't agonise over the exact spring dimension; get the architecture right and leave thickness as the parameter.
- **The rail is rectangular, so the slider can't rotate in its sleeve.** This is why both rotational axes have to be real designed joints out at the yoke, and it's a large part of why the yoke is crowded. The two prompts connect here. If you think a round rail is better — returning swivel to the slider for free, at the cost of letting the cup twist under load — say so and make the argument.

This part has less prior art than anything else in the build. Printed detents that still hold after a few hundred adjustments are not a solved problem, and I'd rather see the difficulty than have it styled over.

## What I want back

**The rules in words first**, then the upper assembly as one designed thing across the family — bow, slider, attachment, and how the yoke hangs off it.

Show me at least two ways to arrange the detent ladder and leaf (where the ladder lives, which part carries the leaf, which way the leaf faces) with the trade-offs stated, rather than one resolved answer.

And keep doing the thing you did well last time: **if something doesn't close, say so.** The stated conflicts in your first pass were the most useful part of it. If the detent can't produce enough holding force at this scale against a real bow's spring load, that's exactly what I need to hear.

## Unchanged

1 unit = 1 mm. GLB, never OBJ. Same mesh naming — `slider_R`/`_L`, `yoke_R`/`_L`, `bow_ref`, and no `thumbscrew_*` or pressure-shoe nodes any more, because those parts stop existing.
