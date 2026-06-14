# RUNBOOK — follow-along

> README explains *what* ProjectGenome is; `docs/TECHNICAL-SPECIFICATION.md` is the *canonical* spec.
> This is the *do-this-then-that* guide for a first successful run.
>
> Remember: there is **no binary**. An AI runtime reads `skills/recreate/SKILL.md` and performs the
> pipeline. The steps below are what you tell the runtime + the deterministic checks you run yourself.

A worked output of these steps over the bundled `corpus/example/` lives in
[`examples/example-run/`](examples/example-run/) — read that alongside this guide to see what
"success" looks like.

---

## 0. Setup

```bash
mkdir -p .recreate
cp schemas/registry.empty.json .recreate/registry.json   # empty registry (version 0)
# corpus: either use the bundled examples, or add your own project folders to corpus/
#   corpus/MyProjectA/README.md, corpus/MyProjectB/README.md, ...
```

You also need the `pg` and `pgf` skills available to your runtime (bundled under `skills/`).

## 1. Run `map` (Phase 0–1) — corpus → 3-axis inventory

Tell the runtime:
> "Read `skills/recreate/SKILL.md`. Run **map** mode over `corpus/`: extract a ProjectGene for each
> project and build the inventory."

Expected outputs (under `.recreate/runs/{NNN}-pending/`):
- `genes.json` — one `ProjectGene` per corpus project (archetype/primitive/layer + verdict/vocab).
- `inventory.md` — ArchetypeShelf / LayerShelf / PrimitiveShelf / LensPalette / VocabRegistry.

Check it yourself:
```bash
python scripts/validate_projectgenome.py .recreate/runs/<run_id>
```

## 2. Run `generate` (Phase 2–5) — candidates → winner

> "Run **generate**: 3 paths × 8 divergence tools → K candidates, then avoidance, differentiation,
> select-or-integrate, and prove."

Expected: `candidates.md` (each candidate's parts, path/tool, differentiation verdict, 6-axis score)
and `avoidance_report.md` (every decision with reason + score). The winner is the top of the 6-axis
selection that passes the prove checks (≥2 parts, no overused vocab, explicit differentiation,
stdlib+cli_triplet fit, deterministic-engine answerable).

Gate intuitions:
- **avoidance** rejects name/source-fingerprint/corpus-name collisions (hard) and penalizes
  over-consumed sources (soft). On a fresh registry nothing is rejected.
- **integrate** only beats parents on a *structurally-ordered* axis (lifecycle/causal/pipeline) with a
  unique value — otherwise it's rejected (see `differentiation.md §3.2a`).

## 3. Review candidates

Read `candidates.md`. A good winner: ≥2 reused parts, a one-sentence `single_question`, a clear
`boundary` ("this is NOT ..."), a 3-way verdict, and a stdlib-only shape. If you disagree, ask the
runtime to pivot a `needs_pivot` candidate or re-run `generate`.

## 4. Emit the DesignSeed (Phase 6)

> "Emit the DesignSeed for the winner."

Expected: `DESIGN-SEED-{Name}.md` and the run renamed `{NNN}-{winner-slug}`; registry + `latest.json`
updated (Phase 7). Validate:
```bash
python scripts/validate_projectgenome.py .recreate/runs/<run_id>
```

## 5. Hand off to pgf (build it)

> "/pgf full-cycle {Name} --with-review"  (or, on a runtime without slash commands:
> "Run pgf full-cycle on this DesignSeed: design → review → plan → execute → verify.")

This produces a real stdlib-only CLI MVP (`sample`/`run`/`report`, deterministic verdict path,
optional hash-chained ledger) under `{Name}/`, plus `.pgf/*-{Name}.*` design/verify records.

## 6. (Optional) Multi-runtime consensus

Run `generate` on several runtimes, pool the candidates, and have each runtime score the finalists with
`schemas/crossmodel-scores.template.json`. Aggregate:
```bash
python scripts/aggregate_crossmodel.py <scores_dir>
```
Use consensus to confirm near-margin integrate decisions (±0.1). See `docs/TECHNICAL-SPECIFICATION.md §9`.

---

## Troubleshooting
- *"validate found problems"* — read the `!` lines; most are a missing DesignSeed section or a
  non-canonical fingerprint key (must be `"+".join(sorted(set(parts)))`).
- *"prove produced 0 candidates"* — by design that's a **failure**; broaden the corpus or relax nothing
  (the gate is intentional).
- *"integrate keeps getting rejected"* — expected unless the cluster sits on a naturally-ordered axis.
