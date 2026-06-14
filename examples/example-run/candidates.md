# Example Candidates (Phase 2–5)

> Illustrative single-runtime run over `corpus/example/` (3 projects). Small corpus → few candidates.

## Phase 2b Avoidance
Fresh registry (version 0, 0 generated projects) → no hard-rejects, no penalties. All candidates `allow`.
(See `avoidance_report.md` in a real run; omitted here as everything passes trivially.)

## Phase 2 — Generated candidates

| # | candidate | path / tool | parts | verdict | overlap | tag_clash | aggregate |
|---|---|---|---|---|---|---:|---:|
| 1 | **DwellProvenanceGate** | RECOMBINE / LayerFusion | ParkingDwellGate, HarvestLedger | distinct | 0.28 | 0 | 4.55 |
| 2 | CurtailEvidenceWatch | RECOMBINE / LayerFusion | GridCurtailIndex, HarvestLedger | distinct | 0.33 | 0 | 4.30 |
| 3 | DwellCurtailReflex | RECOMBINE / DistantHybridization | ParkingDwellGate, GridCurtailIndex | needs_pivot → distinct | 0.41 → 0.36 | 1 | 4.10 |

> `parts ≥ 2` enforced; no overused vocab in names; each maps to a single deterministic question.

## Phase 4 — Select-or-Integrate

- Complementarity checked: the three pairs are distinct but **not** a same-problem cluster on a
  naturally-ordered axis → no integration attempted (would only widen the contract; see
  `differentiation.md §3.2a`). Original distinct candidates retained.
- 6-axis selection (novelty-weighted):

| candidate | reuse | novelty | demand | build | boundary | system | aggregate |
|---|---:|---:|---:|---:|---:|---:|---:|
| **DwellProvenanceGate** | 0.82 | 0.70 | 0.70 | 0.85 | 0.80 | 0.68 | **4.55** |
| CurtailEvidenceWatch | 0.78 | 0.68 | 0.68 | 0.82 | 0.78 | 0.56 | 4.30 |
| DwellCurtailReflex | 0.72 | 0.66 | 0.62 | 0.80 | 0.74 | 0.52 | 4.10 |

→ winner: **DwellProvenanceGate**.

## Phase 5 — Proven brief (winner)

### DwellProvenanceGate
- gen_path / tool: RECOMBINE / LayerFusion (Control + Evidence)
- parts: ParkingDwellGate (authorization engine, reuse_cost=parametrize); HarvestLedger (hash-chained ledger, reuse_cost=copy)
- single_question: "For this access event, is the dwell authorized, and is the decision committed to a tamper-evident ledger?"
- verdict_scheme: allow / review / block (with a committed ledger entry on every decision)
- differentiation: ParkingDwellGate gates but keeps no audit chain; HarvestLedger chains evidence but makes no authorization decision. The fusion adds an **auditable decision trail** neither parent has.
- boundary: "not a payment processor, not an enforcement system, and not a general audit platform — it gates one access event and commits that one decision."
- prove_checks: source≥2=true(2), no_overused_vocab=true, differentiated=true, cli_triplet_stdlib_fit=true, deterministic_engine=true

## Result
- proven_candidates: 3
- failure_condition_zero_candidates: false
- winner_for_seed: **DwellProvenanceGate**
