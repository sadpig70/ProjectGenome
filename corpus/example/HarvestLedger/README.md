# HarvestLedger

HarvestLedger is a stdlib-only CLI that turns crop-harvest events into a tamper-evident provenance
chain.

> For this harvest lot, can its origin and handling be attested without holding the produce itself?

It hashes canonical lot records (field, date, handler) into an append-only chain — commitments only,
no custody of the produce or proprietary data.

## Verdicts
- `verified` — lot record canonicalizes and chains cleanly
- `thin` — record present but missing optional provenance fields
- `invalid` — record breaks the hash chain or lacks required fields

## Input shape
```json
{ "lot_id": "...", "field": "...", "harvested_utc": "...",
  "handler": "...", "prev_entry_sha256": "..." }
```

## Boundary
This is not a food-safety certifier and not a marketplace — it only maintains hash commitments over
harvest provenance.

## Notes
Append-only JSONL hash chain (genesis 64-zero); stdlib-only; sample/run/report CLI.
Archetype: **Ledger**. Layer: **Evidence**.
