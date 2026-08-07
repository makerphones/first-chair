# Claude Design form pass — how to run it, and the record

**The prompt itself is `PROMPT.md`. Paste that; don't paste this file.** This one is the
how-to-run notes and the reproducibility record.

## Why `PROMPT.md` is self-contained

**Claude Design cannot see this repo.** It has no filesystem access, so a prompt that says
"read `docs/industrial-design-brief.md`" silently gets a design session working from nothing
but its own priors — which is the failure this pass exists to fix.

`PROMPT.md` therefore repeats every constraint inline and references no local file. It is
duplication on purpose. When `industrial-design-brief.md` changes, `PROMPT.md` has to be
updated with it.

*(A project can also be seeded from the public GitHub repo, which would give it real access to
these files. Even then, keep the prompt self-contained: "go and read X" is a weaker instruction
than stating X, and it fails quietly when the seed doesn't take.)*

## Running it

1. Create a Claude Design project — consider binding the **Makerphones Design System** project
   so the family language is available.
2. **Select the 3D design skill.** This is part of the reproducible unit; record which one.
3. Paste `PROMPT.md`.
4. Insist on the family **rules in words** before any geometry. If it starts modelling first,
   stop it — a "family" made of a repeated detail is the weak version and it defaults to that.
5. Download the GLB. Run `makerphones/scripts/inspect_glb.py` on it — it warns on **both**
   scale-failure directions, which is the only cheap check for the two conventions that fail
   silently.
6. Save the GLB into `design/form/<date>/` with the record below beside it.

There is **no MCP verb for the 3D agent** — it is driven by chatting in Claude Design. The MCP
can create and seed a project, and nothing more.

## The record — fill this in per run

The reproducible unit is **(skill + seed + prompt)**, not the prompt. All three, or the result
can't be reproduced later:

```
date          
skill         which 3D skill was selected
seed          design system bound / files uploaded / GitHub repo — be specific
prompt        PROMPT.md @ <git sha>, plus any follow-ups in the session, verbatim
output        the GLB filenames, and what inspect_glb.py said
picked        which direction, and why the others lost
```

A GLB sitting here without that block is an orphan nobody can regenerate.

---

## Run log

### 2026-08-06 — lineup form study v2

```
project    makerphones — lineup form study v2
           https://claude.ai/design/p/aac8535d-f9c9-4cbd-a518-687dcfcbf011
skill      (record which 3D skill was selected)
seed       github.com/makerphones/first-chair @ af72791 — connect as project source in the
           Claude Design UI. There is no MCP verb for this; create_project takes a design
           system id and nothing else. BRIEF.md was written into the project over MCP, and
           it carries public raw.githubusercontent URLs as the fallback path to the images.
prompt     BRIEF.md in the project == design/form/BRIEF-lineup-v2.md in this repo
output     (GLB filenames + what inspect_glb.py said)
picked     (which direction, and why the others lost)
```

**Supersedes** `PROMPT.md` (pass 01), `PROMPT-02-family-yoke.md`, `PROMPT-03-upper-assembly.md`.
Those stay as the record of what was actually sent, and of three corrections that should have
been one brief: pass 01 gave a parts list with no mechanism, the design language was adjectives
rather than the archive, and the cup-outline rule went round → teardrop → pad-decides before it
settled.
