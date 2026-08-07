This is a second pass on the **makerphones family form study** (the four-product one: First Chair, Daily Driver, Session, Encore). Keep everything that's there. This pass is about **one part: the yoke.**

## What's working — don't touch it

The ratio system is right. `RULES` R1–R6, and especially the decision that the only absolute numbers are the ones physics fixes — driver Ø, `EAR_CLEAR = 64`, `BOW_R = 108`. **The head doesn't scale**, and building the family around that is exactly correct. The relative scale across the four reads properly. The earcups are a good first pass.

Leave the earcups alone this round. I don't want to refine detail until the family's design language is settled.

## What's wrong: the yoke

Three things, and the third is the one I care about.

**1. It's too thick.** It reads as a slab, not a considered part.

**2. It's identical across all four products, and that's wrong.** The loads aren't identical — a Ø54 on-ear cup is a fraction of the mass of a Ø96 Encore cup, on a shorter arm. Every other dimension in the study derives from something; the yoke doesn't derive from anything, it's just repeated. That's the weak kind of family — a repeated detail rather than a rule. **Give the yoke a rule**, like everything else has: its section should follow the load it actually carries.

**3. It isn't elegant, and it should be the part that is.** The yoke is the only part with visible structure doing visible work. Right now it's the ugliest thing in the study.

## The constraint that's also the opportunity

The yoke **must print flat in its own plane, with the layer lines running along the arm.** That's not a preference — it carries bending load, layer adhesion is the weak axis, and this is the difference between a yoke that lasts and one that snaps.

So it's effectively a 2.5D part, and that tells you where elegance can come from:

- **Thickness is expensive to vary** — it's the print's Z and it's what the strength depends on.
- **The profile in the print plane is completely free.** Waisting, tapering, a swept outline, a cut-out, a section that changes along the arm's length, a shaped transition into the eye — all of it costs nothing to print and nothing in strength if the material follows the bending moment.

**That's the lever: shape the silhouette, don't thin the slab.** A part that's widest where the moment is highest and narrowest where it isn't looks designed, is stronger for its mass, and is the honest expression of a printed structural part. Thinning it uniformly just makes it weaker and still slabby.

## What I want back

**State the rule in words before you model anything.** Then:

1. **A yoke rule for the family** — how section, profile and arm length derive from the cup they carry, so First Chair's yoke and Encore's are visibly siblings but not the same part. Show me the numbers it produces at all four sizes.

2. **Three alternative yoke forms** built on that rule, so I can pick a language rather than approve a part. For each, say what it does at Ø54 and at Ø96, because the small one is where an elegant profile is hardest to keep.

3. **How the yoke meets the cup and the slider** in each — those two joints are most of what the eye reads, and right now they're abrupt.

## Two corrections to fold in

**Use my locked First Chair numbers exactly.** Your `derive()` currently gives Ø48.21 body and 27.4 depth; the locked values are **Ø48.0 body** and **27.6 depth**. The difference is trivial physically but these are round numbers on purpose. Bend the formula to hit them — `bodyD = d / 1.125` gives exactly 48.0 at Ø54, and `depth = 22.2 + 0.10·Ø` gives exactly 27.6 at Ø54 and 31.3 at Ø91. Keep your correction that depth is driver-and-ear driven rather than a fraction of Ø — that was right, and it's why the 0.51·Ø rule from the other study fails at Ø91.

**Flag it, don't hide it:** your rule gives Daily Driver a Ø81.3 body behind a Ø91 baffle. Daily Driver is already a shipped design and has no lip-and-body split — its outer diameter *is* its body. So this rule would change an existing product. I may well want that for family coherence, but tell me plainly what changes rather than quietly restyling it.

## Conventions — unchanged

Authored **1 unit = 1 mm**. **GLB, never OBJ.** Mesh names to the same contract you're already using — `cup_R`/`_L`, `yoke_R`/`_L`, `yoke_rod_R`/`_L`, with the side mirror. And if a number doesn't close, say so rather than fudging it — the stated conflicts in your last pass were the most useful part of it.
