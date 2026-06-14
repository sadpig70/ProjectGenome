# example-run — a worked pipeline output over `corpus/example/`

> This is an **abbreviated, illustrative** output of running ProjectGenome over the three bundled
> example projects (`corpus/example/`: ParkingDwellGate, HarvestLedger, GridCurtailIndex). It shows a
> first-time user *what success looks like* — the shape and content of each artifact — without having
> to run anything. A real run produces these under `.recreate/runs/{run_id}/`.

| file | phase | what it is |
|---|---|---|
| `input_manifest.json` | 0 | corpus included / generated excluded, registry snapshot (here: empty) |
| `genes.json` | 0–1 | one ProjectGene per example project (3) |
| `inventory.md` | 1 | archetype / layer / primitive shelves + vocab |
| `candidates.md` | 2–5 | generated candidates + differentiation + 6-axis selection + winner |
| `DESIGN-SEED-DwellProvenanceGate.md` | 6 | the winner's DesignSeed (pgf input) |

The winner here, **DwellProvenanceGate**, is a `LayerFusion` recombination of two example parts
(a Gate/Control authorization engine + a Ledger/Evidence hash chain): an access gate that *also*
commits every authorization decision to a tamper-evident ledger.

> Numbers (overlap, 6-axis) are illustrative single-runtime judgments. On a real corpus your winner and
> scores differ — the pipeline and contracts stay the same. Validate any run with
> `python scripts/validate_projectgenome.py .recreate/runs/<run_id>`.
