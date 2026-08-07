Stop. We've had the process backwards and I want to reverse it.

## The order was wrong

We've been building parts and then trying to make the assembly elegant. That's the engineering order, and it's why everything reads as primitives butted together — because that's what it is.

The right order is form first:

1. **This pass — one continuous form.** No parts.
2. **Next — split that form into parts.** Where the baffle separates, where the yoke attaches, where the pad rim sits. Serviceability and printability enter here.
3. **After — details.** Grille, mark, fasteners, the treatment at each joint.
4. Then I re-author it as engineered CAD by hand.

## This pass: one body per product, no parts at all

Each product is **one continuous form** — the ear unit and the arm that carries it, flowing into each other. No part lines. No joints. No bosses, no fasteners, no grille, no rim step, no clamp ring. Nothing that implies assembly.

I want to judge it as an **object** before it becomes an assembly.

**Build each as a profile, lofted or swept — not a stack of primitives.** If a section changes, it changes through the loft. If something is round, the roundness lives in the profile curve. Where the arm meets the cup, that's one surface changing section, not two shapes meeting.

This plays to what you're good at. With no boolean operations you can't cut features into a body anyway — so a single continuous lofted body is your strongest mode, and assembling primitives is your weakest. I've been asking for the wrong one and then complaining that it looks assembled.

It also sets up step 2 properly: **if the form is a profile, splitting it into parts is a split of the profile, not a boolean.** The whole path stays inside what you can actually do.

## Reference, in the repo

`design/form/reference/shape-sketches-overview.jpg` — six cup outlines, and note the **waisted stem flowing into each one**. No step, no boss, no joint. That is the level of resolution I want back from this pass, in 3D.

The headband blanks in the same folder are the same idea in metal: one continuous taper over the whole length, and where a cut ends it ends in a teardrop.

## What I want back

The **four products, each as one body**, at true relative scale — First Chair, Daily Driver, Session, Encore. Three directions to choose between. One live 3D stage, nav switches between them. Rule stated in words first, one line on what doesn't close.

Numbers from `params.py`. Nothing else.

Don't hand me a written study. If it isn't in the stage it doesn't exist.
