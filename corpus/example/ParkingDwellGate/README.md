# ParkingDwellGate

ParkingDwellGate is a stdlib-only CLI that answers one question:

> For this parked vehicle, is the dwell still authorized given permit, zone rules, and time window?

It checks one parking event against independent rules (permit validity, zone restriction, max-dwell
window, payment state) and emits the most severe verdict.

## Verdicts
- `allow` — all rules satisfied
- `review` — a soft rule is borderline (e.g. window nearly exceeded)
- `block` — a hard rule violated (no permit, restricted zone, payment missing)

## Input shape
```json
{ "vehicle_id": "...", "as_of_utc": "2026-01-01T00:00:00Z",
  "permit": {"valid": true, "expires_utc": "..."},
  "zone": {"restricted": false, "code": "A2"},
  "dwell": {"started_utc": "...", "max_minutes": 120},
  "payment": {"settled": true} }
```

## Boundary
This is not a parking-payment processor and not an enforcement/ticketing system — it only verifies
whether a dwell is authorized at evaluation time.

## Notes
Deterministic verdict path (no clock — caller supplies `as_of_utc`); stdlib-only; sample/run/report CLI.
Archetype: **Gate**. Layer: **Control**.
