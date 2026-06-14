# DESIGN-SEED-DwellProvenanceGate

> Example ProjectGenome output (run over `corpus/example/`). Input for `pgf full-cycle DwellProvenanceGate --with-review`.
> Illustrative — shows the shape of a real DesignSeed.

## 한 질문
> For this access event, is the dwell authorized, and is the decision committed to a tamper-evident ledger?

## 분류
- archetype: Gate+Ledger
- layers_used: Control, Evidence
- domain: access / parking operations with auditable decisions
- lens_stack: L6_Gap(inferred), L7_Tension(inferred)

## 재사용 계획 (reuse_plan)
| 부품 | source project | kind | reuse_cost |
|---|---|---|---|
| authorization rules + severity aggregate | ParkingDwellGate | engine | parametrize |
| append-only hash-chained decision ledger | HarvestLedger | ledger | copy |

source_fingerprint: `HarvestLedger+ParkingDwellGate`

## 판정 (verdict_scheme)
allow / review / block — and **every** verdict (not just blocks) is committed as a ledger entry, so the
decision trail is tamper-evident.

## 인터페이스 (skeleton)
- cli_triplet: sample / run / report
- output: JSON (machine) + Markdown (human)
- stdlib-only, deterministic verdict path (caller supplies `as_of_utc`; no clock/network/AI)
- append-only hash-chained ledger (genesis 64-zero; `verify_ledger` detects tampering)

## acceptance_criteria 씨앗
- sample emits allow / review / block example events
- run returns a deterministic verdict + reasons AND appends one ledger entry per decision
- same input → same verdict + same canonical entry (deterministic)
- report renders verdict, rule reasons, and the committed entry's hash
- verify_ledger re-validates the decision chain

## 경계 (boundary)
> 이것은 결제 처리기도, 단속/발권 시스템도, 범용 감사 플랫폼도 아니다 — 한 access 이벤트의 dwell 인가를
> 판정하고 그 한 결정을 tamper-evident ledger에 커밋한다.

## 차별점
ParkingDwellGate는 게이트만 하고 감사 체인을 남기지 않는다. HarvestLedger는 증거를 체인하지만 인가
결정을 하지 않는다. 이 통합(Control+Evidence LayerFusion)은 두 부모 어느 쪽도 갖지 못한 **인가 결정의
감사 가능한 체인**을 더한다. 코퍼스(3개)에 동일 조합·동일 질문 없음.

## pgf handoff
```text
/pgf full-cycle DwellProvenanceGate --with-review
```
