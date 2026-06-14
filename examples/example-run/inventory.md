# Example Inventory (Phase 0–1)

> Corpus: `corpus/example/` (3 projects). Illustrative.

## Acceptance
- corpus_projects: 3
- genes: 3, all with non-empty archetype / mechanism / layer
- lens values flagged `(inferred)` where README provenance was implicit

## ArchetypeShelf
- **Gate** (1): ParkingDwellGate
- **Ledger** (1): HarvestLedger
- **Index** (1): GridCurtailIndex

## LayerShelf
- **Sensing** (1): GridCurtailIndex
- **Evidence** (1): HarvestLedger
- **Control** (1): ParkingDwellGate
- **Allocation** (0): —
- **Release** (0): —

## PrimitiveShelf
- **ParkingDwellGate**: Gate / Control / no-ledger — authorization check w/ severity aggregation | contract: DwellEvent
- **HarvestLedger**: Ledger / Evidence / ledger — append-only hash-chained provenance | contract: HarvestLot
- **GridCurtailIndex**: Index / Sensing / no-ledger — observation-to-tier risk scoring | contract: FeederObservation

## LensPalette
- L6_Gap(inferred): 1
- L7_Tension(inferred): 1
- L10_Generative(inferred): 1

## VocabRegistry
Seed overused tokens: `mesh, clearing, market, gate, escrow, veto, ledger, marketplace, option, clear`.
Corpus name tokens: parkingdwellgate:1, harvestledger:1, gridcurtailindex:1.

## Generation Notes
- Only 3 parts → small combination space. Cleanest pairings cross **layers**:
  Control(ParkingDwellGate) + Evidence(HarvestLedger), or Sensing(GridCurtailIndex) + either.
- A Control+Evidence fusion (gate that also commits an evidence ledger) is the most buildable, lowest-overlap recombination.
