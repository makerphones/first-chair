This is the design language for the whole makerphones family, and it supersedes the adjectives I gave you at the start. It sits alongside the yoke and upper-assembly prompts — those say what the mechanism does, this says what the whole thing should look and feel like.

I have designed and prototyped headphones before, professionally. Rather than describe the house style, I'm giving you the source material and the rules I actually applied.

## Attach these

*(from the archive — file paths for me, images for you)*

```
Deep Blue Design - Old Faithful/Old Faithful -A1.jpg  … -B1, -C1, -D1, -E1, -F1, -G1, -H1
Deep Blue Design - Old Faithful/Deep Blue Design Rev 4/headroom headphone-black.jpg
HeadRoom Old Faithful/Martin Ortiz Round 2/Cam 1.jpg … Cam 9
Design Idea Collection/Headphone Design/GradoGimbal.jpg
3D Print Files/Earcup - 07Rev B.STL
```

Plus the photographs of the built prototypes, the laser-cut spring-steel headband blanks, and the printed earcup series.

## The intent, in the words I used at the time

Writing to the industrial designer on the previous product:

> "The code name Old Faithful is chosen to represent something that lasts a lifetime and will be passed down for generations. It should exude quality craftsmanship, **almost looking handmade but with extreme precision**. Parts should be easily replaceable and durable. Reduce weight where ever possible."

That still holds, and "almost handmade but with extreme precision" is the single most useful sentence here. It tells you what to do with a tolerance, a parting line, a visible fastener: don't hide them, don't fetishise them, make them look *deliberate*. A printed part that owns its layer direction is on-brief. A printed part pretending to be injection-moulded is not.

## Five rules, taken from the corrections I gave that designer

These are what I actually pushed back on, not what I claim to value:

1. **If a mechanism isn't needed, delete it.** I killed a fold hinge with: *"an extra weakness we do not need."* Not "unnecessary" — a *weakness*. Every mechanism is a liability until it earns its place.
2. **No ornament.** They added a decorative step where the pad met the cup. I asked: *"I am assuming this is for aesthetic reasons? I do not have to have this, we prefer the previous straight transition."* A feature that exists only to look designed comes out.
3. **Simplify the mechanism until it is simple, then stop before it is ugly.** My note was *"there seems to be too much going on with the headband mechanism right now, we'd like to simplify"* — and separately, *"we're looking to simplify without looking ugly. Hopefully we can find a nice middle ground."* Both halves matter. Stripped-bare is a failure too.
4. **Material follows load.** On the yoke: *"if we don't need the extra metal, we can save weight — but it does look nice and beefy."* Beefy where it works, gone where it doesn't. This is the same principle as the yoke prompt: shape the silhouette, don't thin the slab.
5. **The prototype settles arguments, not the drawing.** We moved hinge pins 8 mm because a built part said so.

Rule 3 is the one you tripped on. The slider you drew had a knurled thumbscrew, a clamp block and a slotted leg doing what one printed detent should do. That's "too much going on," and it's the same note, ten years apart.

## The shape rule — and it is not one shape

I built oval and teardrop cups on the previous products, because **the cup outline should follow the ear coverage the product needs**:

- **Circumaural** cups enclose the pinna. A pinna is a teardrop. A round over-ear either pinches the ear or wastes cup volume to avoid it. So the over-ears — Daily Driver, Session, Encore — should be **teardrop / oval**.
- **Supra-aural** sits *on* the ear rather than enclosing it, so it has no outline to follow. **First Chair stays round**, and that is now decided rather than assumed: its commodity Grado-pattern pad is round, and that interface is locked.

**Correct one thing I used to believe:** I picked round because I assumed it was easier to manufacture. That is true for turning and moulding. It is **not** true for FDM printing — the printer does not care whether a cross-section is a circle or an ellipse, and there is no rotational tooling anywhere in the process. So don't let "round is simpler" drive anything here; it's a constraint from a process we don't use.

**Do not force one silhouette across the family.** The family is held by the *rule* and by the detail language — how an edge breaks, how a fastener shows, how a part transitions into the next one — not by a repeated outline. A repeated outline across products with different jobs is the weak kind of family, same as a repeated yoke.

Cost, stated so it isn't a surprise: oval cups mean oval pads, and the over-ears lose the commodity pad aftermarket. First Chair keeps it. That is an acceptable trade and it is mine to make.

## What I want

Re-do the family study in this language. Same ratio system, same physics-fixed constants — that part is right. What changes:

- **First Chair round, the over-ears teardrop**, with the outline rule stated and the proportions that hold across both.
- The **detail language** that makes them siblings when the outlines differ: the edge break, the fastener treatment, how the cup meets the yoke, how the yoke meets the slider. That is where the family actually lives now.
- Everything measured against the five rules above. If you add something, tell me which rule it passes.

Same conventions: 1 unit = 1 mm, GLB never OBJ, the existing mesh naming. And keep stating what doesn't close — that has been the most useful thing you've done.
