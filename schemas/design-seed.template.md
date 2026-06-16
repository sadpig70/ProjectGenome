# DESIGN-SEED-{Name}

> ProjectGenome Phase 6 output. Input contract for `pgf full-cycle {Name} --with-review`.
> Fill every field. See skills/recreate/reference/design-seed.md.

## 한 질문 (single_question)
> {이 X에 대해 Y인가? — one interrogative sentence answerable by a deterministic engine}

## 분류
- archetype: {Gate|Mesh|Clearing|Index|Ledger|Stage|Appraisal (+secondary)}
- layers_used: {Sensing/Evidence/Control/Allocation/Release subset}
- domain: {target domain}
- lens_stack: {L...}

## 재사용 계획 (reuse_plan)
| 부품 | source project | kind | reuse_cost |
|---|---|---|---|
| ... | ... | engine/contract/verdict/ledger | copy / parametrize / redesign |

(≥2 parts enforced. For an INTEGRATE seed, parents are generated projects; add
`integrated_from`, `generated_fingerprint`, `transitive_consumed_sources`.)

## 판정 (verdict_scheme)
{k-way: 예 cleared / thin / blocked}

## 인터페이스 (skeleton)
- cli_triplet: sample / run / report
- output: JSON (machine) + Markdown (human)
- stdlib-only, deterministic verdict path (no clock/network/AI; caller supplies time)
- optional: append-only hash-chained ledger

## acceptance_criteria 씨앗
- {seed 1}
- {seed 2}

## 경계 (boundary)
> 이것은 {~}가 아니다.

## 차별점 (differentiation_note)
{최근접 siblings 대비 왜 다른가}

## Idea Trace (idea-layer, 선택)
<!-- idea-layer가 켜진 run에서만 채운다. 없으면 위 필드만으로 유효. 정본: skills/recreate/reference/idea-layer.md -->
- kernel_id: {IK-NNN}
- problem_frame: {어떤 결핍/마찰/비대칭}
- method_archetype: {source_grounded_linking / program_search / ...}
- deterministic_engine_hint: {MVP 결정론 엔진이 답할 단일 질문 — EvaluatorGate 통과 근거}
- proof_surface: {CLI / report / test / fixture}
- strength_label: {verified | claimed}
- why_not_existing_projects: {anti_examples 대비 차별}
