# Concurrency Policy — concurrent multi-runtime runs

> When several AI runtimes execute `recreate` over the **same shared registry at the same time**,
> they can read the same baseline and produce the same fingerprint/name. Without a lock/version/merge
> policy this corrupts the registry or loses updates. This document is the canonical design for that
> case. The sequential case (one run finishes before the next reads the registry) needs none of this.
> Normative summary lives in `skills/recreate/reference/rerun-avoidance.md §10`.

---

## 1. Hazards under true concurrency (H1–H7)

| # | hazard | result |
|---|---|---|
| H1 | **run_id collision** | two runs pick the same `008-pending` → directory overwrite |
| H2 | **source_fingerprint collision** | both read a baseline lacking fingerprint X, both emit a winner with X → both think it novel; avoidance premise broken |
| H3 | **generated_fingerprint collision** | same for integration parent sets |
| H4 | **name collision** | both pick the same winner name (each fresh vs the baseline `blocked_names`) |
| H5 | **source over-consumption** | avoidance penalizes consumed sources, but concurrent runs can't see each other's consumption → both over-use the same fresh part (soft erosion) |
| H6 | **registry write race** | two Phase-7 updates last-writer-wins → one update silently clobbered (lost update) |
| H7 | **latest.json ambiguity** | which run is "latest" is undefined |

H1–H4, H6 are **hard** (integrity broken); H5 is soft; H7 is cosmetic.

## 2. Design principles

1. **Determinism (PG)**: no wall-clock (`Date.now`). Collision tiebreak uses **claim order**, not time.
2. **Optimistic concurrency control (OCC)**: a run records the registry `version` it read at baseline.
   At commit it re-reads the registry; if version advanced, it **re-validates** its winner against the
   now-larger registry (replay the avoidance gate) before merging.
3. **Only two atomic boundaries**: Phase 0 (claim) and Phase 7 (commit) need mutual exclusion on the
   registry. Everything between (generate/differentiate/integrate) runs lock-free — minimal cost.
4. **Shared-registry assumption**: a single filesystem with a lockfile or atomic rename (or git-ref CAS)
   implements the compare-and-swap. Distributed runtimes without a shared FS need an external
   coordination service (out of scope — §6).

## 3. Registry schema additions (forward-compatible)

```jsonc
{
  "version": 12,                 // monotonic; claim and commit bump it
  "active_runs": [               // append-only claim log
    { "claim_seq": 12, "run_id": "008-<runtime>-pending", "runtime": "<runtime>",
      "baseline_version": 12, "status": "active" }   // active | committed | aborted
  ]
  // ... existing fields (generated_projects, source_fingerprints, ...)
}
```

Sequential runs increment `version` naturally; the fields are harmless when unused.

## 4. Phase 0 — claim (atomic)

```python
def claim_run(runtime: str) -> Run:
    with registry_lock():                        # OS file lock / atomic CAS
        reg = read_registry()
        nnn = next_run_number(reg)               # max existing run number + 1 (deterministic)
        claim_seq = reg["version"] + 1
        run_id = f"{nnn:03d}-{runtime}-pending"   # runtime suffix → eliminates H1 (dir collision)
        reg["version"] = claim_seq
        reg.setdefault("active_runs", []).append({
            "claim_seq": claim_seq, "run_id": run_id, "runtime": runtime,
            "baseline_version": claim_seq, "status": "active"})
        write_registry(reg)
    return Run(run_id=run_id, baseline_version=claim_seq, claim_seq=claim_seq)
```

The **runtime suffix** in `run_id` means two concurrent runs never write the same directory (H1 gone).
The winner-slug rename (`{NNN}-{winner-slug}`) happens after commit.

## 5. Phase 7 — commit (atomic OCC) — the core

```python
def commit_run(run, winner) -> Literal["committed","pivoted","discarded"]:
    with registry_lock():
        reg = read_registry()
        collision = avoidance_recheck(winner, reg)   # name / source_fp / generated_fp vs CURRENT reg
        if collision:
            mark_active_run(reg, run.run_id, "aborted"); reg["version"] += 1
            write_registry(reg)
    if collision:
        return pivot_against_merged_state(run, winner) or "discarded"   # outside lock
    with registry_lock():
        reg = read_registry()
        reg["generated_projects"][winner.name] = winner.record()
        reg["blocked_names"].append(winner.name)
        reg[fp_namespace(winner)][winner.fingerprint] = {"project": winner.name, "run_id": final_id}
        accumulate_sources(reg, winner)
        mark_active_run(reg, run.run_id, "committed"); reg["version"] += 1
        write_registry(reg); write_latest(run, winner)   # latest = max-version commit (H7 gone)
    rename_run_dir(run.run_id, f"{run_number(run)}-{slug(winner)}")
    return "committed"
```

**Collision resolution (deterministic outcome)**: commit is mutually exclusive, so the **first
committer keeps** the fingerprint/name; the second arrival sees the collision via OCC re-check and
**pivots** (regenerate against the merged state) or **discards**. Exactly one run holds each
fingerprint/name → H2/H3/H4/H6 resolved. Which run wins depends on lock-acquisition order
(scheduling), but the *integrity* of the result is deterministic. For reproducibility, replay commits
in ascending `claim_seq` to remove concurrency.

`latest.json` points to the max-`version` commit (H7 resolved).

## 6. Soft policy (optional — not needed for correctness)

For H5 (same fresh source over-consumed): at claim time, shard the fresh-source pool per runtime
(`hash(source) % active_count == my_index`) so concurrent runs prefer disjoint fresh parts. The
commit gate (§5) guarantees correctness regardless; sharding is only an optimization.

## 7. Audit / reproducibility

- Every claim/commit/abort is preserved in `active_runs` by status (append-only) → concurrent history
  is reconstructible.
- Log each collision resolution in `runs/{run_id}/avoidance_report.md`:
  `"OCC collision: lost to {winner_run}, pivoted to {new}"`.
- Full reproduction: serial-replay commits in ascending `claim_seq` → identical result.

## 8. Honest limits

- **Shared-FS assumption**: needs a working lockfile / atomic-rename on one registry. Distributed
  runtimes (no shared FS) need external coordination (git-ref CAS, distributed lock) — out of scope.
- **Pivot termination**: if a small corpus runs dry of fresh combinations under heavy concurrency, the
  second arrival's pivot may fail → discard. Concurrency ceiling: keep concurrent runs conservative
  relative to the fresh-source count.
- Until the first concurrent run, this policy is dormant by design; activate the §3 fields before it.
