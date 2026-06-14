# Case Study — Multi-Runtime Validation (anonymized)

> ProjectGenome was validated on one **reference corpus** (≈48 README-level projects spanning bio,
> AI safety, payments, robotics, climate, energy, governance, space, …) by **five independent AI
> runtimes (labeled A–E)**. Project and runtime names are anonymized here; the numbers are the
> empirical evidence and identify no one. This documents *that the methodology works*; on your own
> corpus the winners and scores will differ — what stays the same is the pipeline, gates, and contracts.

## 1. Fleet — 6 generated projects across 7 runs

| run | generated project (mechanism) | gen_path | archetype | verdict scheme | author |
|---|---|---|---|---|---|
| 001 | a withheld-action witness (non-release justification) | MUTATE / NegativeSpaceInversion | Gate+Ledger | justified/thin/breach | A |
| 002 | a pre-dispatch delegation underwriter | INTEGRATE (within-run) | Gate+Appraisal | covered/conditional/uncovered | A |
| 003 | a policy-drift dossier | RECOMBINE | Gate+Index | aligned/drift/breach | B |
| 004 | a supply-shock tabletop rehearsal gate | MUTATE / Clearing | Clearing | passed/gaps/failed | C |
| 005 | an in-flight reflex-interrupt gate | RECOMBINE | Gate | cleared/intercepted/breached | D |
| 006 | a lifecycle governance fold (integration of 001+002+005) | INTEGRATE (cross-model) | Gate | governed/partial/ungoverned | A |
| 007 | (negative — no integrated candidate beat its parents) | INTEGRATE attempt | — | — | E |

All implemented projects were stdlib-only single-module CLIs (sample/run/report, deterministic verdict
path, hash-chained ledger) and published as independent repos.

## 2. Result — registry-based avoidance worked at fleet scale

Five runtimes, **without any coordination lock**, produced:
- **0 name collisions, 0 source-fingerprint collisions, 0 source overlap** — every consumed source had
  `use_count == 1` (perfect partition: ~17 of ~48 sources consumed, the rest left fresh).
- **0 hard-rejects** across the fleet — not because the gate is weak, but because each runtime read the
  registry's `consumed_sources` and steered to fresh parts *proactively*.

This partition held because registry updates were **sequential** (run 001 → … → 007). True concurrent
execution needs the optimistic-concurrency contract in `rerun-avoidance.md §10`.

## 3. Result — cross-model integration is conditional (the key finding)

The methodology's flagship move (integrate complementary candidates into a third) was tested twice and
cross-model verified both times.

| | single-evaluator margin | cross-model consensus margin | outcome |
|---|---:|---:|---|
| **run 006** (time-axis lifecycle integration) | +0.03 | **+0.150** | adopted, certified robust (5/5 runtimes) |
| **run 007** (non-time lens/layer integration) | −0.06 | **−0.195** | rejected, negative confirmed (4/4 runtimes) |

- **Positive (006)**: parents sat on one object's *timeline* (before/during/after). The integrated whole
  gained a **unique value** — cross-stage inconsistency detection no single parent can see — which offset
  the contract-widening cost. Consensus 5.10 > best parent 4.95.
- **Negative (007)**: lens/layer axes have weak natural ordering; integration only *parallel-folds*
  verdicts with no new unique value, so it widened the input contract and lost buildability/boundary
  clarity. Consensus 4.645 < best parent 4.840.

**Author self-bias check**: in run 006 the integration's author scored its own candidate the *lowest*
(self-bias −0.35) — the gate stood on *other* runtimes rating it higher, not on self-promotion. In run
007 the author rated its own candidate generously (+0.39) yet it still lost — the negative is structural.

## 4. Lessons baked back into the method

- **Integration applicability** (`differentiation.md §3.2a`): integrate beats parents only with strong
  `same_problem` + a **structurally-ordered** complementarity axis (lifecycle/causal/pipeline) + a
  unique value the parents lack. Lens-ensembles and arbitrary layer-stacks usually fail the gate.
- **Cross-model consensus amplifies single-evaluator margins in both directions** — so near-margin
  (±0.1) adoption/rejection decisions should be verified by consensus, not a single runtime.
- **Self-bias separation** (mark `self_authored`) is what lets a fleet trust its own scores.

## 5. Honesty

These results show the *machinery* works (avoidance, isolation, integration gate, cross-model consensus).
They do not claim the generated projects are valuable products — each `DesignSeed` is provisional until
built and verified, and domain demand was AI-judged without market validation.
