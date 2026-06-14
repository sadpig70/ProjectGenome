# GridCurtailIndex

GridCurtailIndex is a stdlib-only CLI that scores how close a local feeder is to a curtailment event.

> For this feeder, how severe is the curtailment risk given load, headroom, and threshold signals?

It turns observations (load, available headroom, weather/threshold flags) into a score and a tier —
a sensing/index posture, not a control action.

## Verdicts
- `low` — ample headroom
- `watch` — within margin of a curtailment threshold
- `critical` — threshold breached or imminent

## Input shape
```json
{ "feeder_id": "...", "load_kw": 0, "headroom_kw": 0,
  "thresholds": {"watch_kw": 0, "critical_kw": 0} }
```

## Boundary
This is not a grid controller and not a billing system — it only scores and flags curtailment posture.

## Notes
Deterministic scoring; stdlib-only; sample/run/report CLI.
Archetype: **Index**. Layer: **Sensing**.
