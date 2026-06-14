# corpus/ — your input material

ProjectGenome works by decomposing **existing projects** into reusable parts. Put your corpus here.

## Format

One folder per project, each containing a `README.md` (code optional — README-level descriptions are
enough for gene extraction; a public source repo can be fetched as 2nd-tier material when a
mechanism / verdict scheme is ambiguous).

```
corpus/
    MyProjectA/README.md
    MyProjectB/README.md
    ...
    example/            # 3 fictional sample projects to try the pipeline immediately
```

## What a good corpus README contains (for clean gene extraction)

A README that maps cleanly to a `ProjectGene` (see `schemas/project-gene.schema.json`) states:

- **the single question** it answers ("for this X, is Y?"),
- **how it works** (mechanism — engine shape),
- **its verdict scheme** (e.g. cleared / thin / blocked),
- **input shape** (evidence model),
- **a boundary** ("this is NOT ..."),
- optionally provenance / lenses used.

The 7 archetypes (Gate/Mesh/Clearing/Index/Ledger/Stage/Appraisal) and 5 layers
(Sensing/Evidence/Control/Allocation/Release) are how each project is tagged — see
`docs/TECHNICAL-SPECIFICATION.md §4`.

## Minimum to run

- ≥ ~10 projects gives the generator enough parts; the method strengthens as the corpus grows
  (vocab_registry and lens palette auto-expand — co-evolution).
- Start with `corpus/example/` (3 fictional projects) to see the pipeline end-to-end, then replace
  with your own.

## Note

Generated project folders (produced by previous runs) must be **excluded** from the corpus scan —
the run's `input_manifest.json` records them in `excluded_generated_projects`.
