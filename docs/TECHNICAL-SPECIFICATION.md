# ProjectGenome — Technical Specification

> **이 문서의 목적**: ProjectGenome를 처음 보는 AI 에이전트나 엔지니어가 *전체 방법론과 시스템을
> 이해하고, 처음부터 직접 구현/실행*할 수 있도록 모든 구성요소를 한 곳에 상세히 기술한다.
> `README.md` + `skills/recreate/`(SKILL + reference 5종) + `schemas/`를 종합·자기완결화했다.
>
> 표기: 본문은 한국어, 기술 용어·코드·스키마·CLI는 영어. `{Name}` = CamelCase 프로젝트명.
> registry 계약 `schema_version 1.1`. 다중 런타임 실증은 `examples/CASE-STUDY.md` 참조.

---

## 0. 빠른 지도 (이 문서를 읽는 법)

| 알고 싶은 것 | 절 |
|---|---|
| recreate가 무엇이고 왜 만드는가 | §1, §2 |
| 입력 재료(코퍼스)는 무엇인가 | §3 |
| 핵심 개념(3축 유전자·공통 골격·렌즈) | §4 |
| 새 프로젝트를 만드는 전체 파이프라인 | §5 |
| 재실행/동시실행 안전(registry·회피·락) | §6 |
| 모든 파일의 데이터 스키마 | §7 |
| 산출물을 실제 코드로 구현하는 법(PG/PGF) | §8 |
| 여러 AI 런타임 합의 검증 | §9 |
| 지금까지의 실증 결과 | §10 |
| **직접 구현하려면(개발자 가이드)** | §11 |
| 디렉토리 전체 지도 | §12 |
| 정직한 경계·한계 | §13 |
| 용어집 | §14 |

---

## 1. 한 문장 요약

**ProjectGenome는 이미 만들어진 프로젝트 코퍼스(48개, README only)를 3축으로 분해해 부품으로 환원한 뒤,
3경로 × 8 발산도구로 재조합·변형·이식하고, 정량 차별화 게이트와 실증을 통과시켜 새 프로젝트 씨앗
(`DesignSeed`)을 생성하는 메타 방법론이자, 그것을 실행하는 런타임 중립 스킬(`recreate`)이다.**

핵심은 "새 아이디어 1개를 더 고르기"가 아니라, 코퍼스가 이미 들고 있는 **생성 문법을 추출해 재사용
가능한 생성 장치를 돌리는 것**이다. 출력 `DesignSeed`는 `pgf full-cycle`(설계→계획→실행→검증)의 DESIGN
입력으로 직결되어 실제 stdlib CLI로 구현된다.

---

## 2. 문제 정의와 지배 명제

### 2.1 관찰

기존 프로젝트를 병렬로 더 만든다고 다양한 시스템이 나오지 않는다. 코퍼스 48개를 보면 거의 동일한
**골격**으로 수렴한다:

```
single_question("이 X에 대해 Y인가?")
  → deterministic_engine   # 정밀 계산은 코드, 판단만 규칙
  → k_way_verdict          # 3/4분 판정 (cleared/thin/blocked 류)
  → dual_output            # 기계용 JSON + 사람용 Markdown
  → cli_triplet            # sample / run / report
  → boundary_clause        # "이것은 ~가 아니다"
  → provenance             # lens stack (L1~L25)
```

부가 규율: append-only hash-chained ledger(다수), stdlib-only/무의존.

### 2.2 지배 명제 — parts ≫ blank-slate

새 프로젝트는 **무에서** 나오지 않는다. 코퍼스가 검증한 엔진·어댑터·verdict·ledger를 재사용한다.
재사용 부품(`parts`)이 비면 후보를 **기각**해 "코퍼스 기반성"을 강제한다. 이 명제가 다른 모든 규칙을
재정렬한다 — 차별화는 부품이 충분히 재사용될 때만 의미가 있다.

> **정직성 노트**: recreate는 *생성 방법론과 실행 스킬*이지, 생성된 후보가 옳거나 새롭거나 가치 있음을
> 보장하지 않는다. 목표는 mundane 조합을 *구조적으로 만들기 어렵게* 하고, 모든 후보를 **감사 가능**
> (재사용 부품·차별화 점수·근거 첨부)하게 유지하는 것이다. `DesignSeed`는 구현·검증 전까지 잠정이다.

### 2.3 자기참조 (방법론의 정박)

recreate 자신이 이 방법으로 만들어졌다 — `method_claude`(구조 강)와 `chatgpf`(발산 강)를 *고른* 게
아니라 *통합*해 `method_integrated`가 되었고, 통합본이 양쪽을 능가했다. 이 사실이 Phase 4의
`select-or-integrate`(단순 선택이 아니라 상보 통합)의 근거다.

---

## 3. 코퍼스 (입력 재료)

### 3.1 2계층 재료

- **1차 재료**: 코퍼스 루트 각 폴더의 `README.md`(코드 없음, README only) + `corpus/`
  (48개 1줄 요약).
- **2차 정밀 재료**: 각 프로젝트 전체 소스는 `<your-git-host>/<your-org>/<repo>`에 공개(`{repo}`=폴더명,
  대소문자 혼재: `ADPR`, `afferentcore`, `MCO`, `pact`, `RRE` 등). README만으로 엔진 로직·
  `verdict_scheme`·`adapter_contract` 분해가 모호하면 해당 repo의 코드/`.pgf/DESIGN-*.md`를 fetch해 보강.

### 3.2 코퍼스 48개 (도메인 다양성)

bio/AI provenance, AI safety, payments/compliance, robotics, climate, quantum infra, supply chain,
energy, governance, space 등 광범위. 전체 목록·요약은 `corpus/`. 생성된 프로젝트
폴더(이전 run의 생성물)는 코퍼스 스캔에서 **제외**된다(§6).

---

## 4. 핵심 개념 — 3축 ProjectGene

코퍼스의 각 프로젝트를 **세 축으로 동시에** 태깅한다. 한 축만으로는 조합 어휘가 빈약하다.
정본: `skills/recreate/reference/gene-extraction.md`.

### 4.1 ProjectGene 스키마

```python
ProjectGene = dict = {
    "project": str, "repo": str, "domain": str,
    # 축1 형태: 어떤 엔진 골격을 재사용
    "archetype": Literal["Gate","Mesh","Clearing","Index","Ledger","Stage","Appraisal"],
    # 축2 속성: 부품의 인터페이스·어휘
    "mechanism": str,          # 도메인 명사를 제거한 추상 작동원리 (TRANSPLANT가 재사용)
    "evidence_model": str,     # 입력 데이터 구조
    "control_primitive": str,  # 시스템 개입 방식
    "artifact_type": str,      # 출력물 형태
    "grammar": str,            # product grammar (이름 어휘)
    # 축3 기능: stack의 어느 계층 슬롯
    "layer": Literal["Sensing","Evidence","Control","Allocation","Release"],
    # 변형/검증 메타
    "lens_stack": list[str],   # 코퍼스 Provenance 역추출 L1~L25 (미기재 시 (inferred))
    "verdict_scheme": list[str],
    "adapter_contract": Optional[str],  # 도메인 차이를 격리하는 단일 계약
    "has_ledger": bool, "boundary": str,
    "vocab": list[str],        # 이름 토큰 (중복 회피)
    "derivative_risk_tags": list[str],
}
```

### 4.2 축1 — 7 아키타입 (형태)

| Archetype | engine shape (골격) | 분류 휴리스틱 | 코퍼스 실례 |
|---|---|---|---|
| **Gate** | 입력 → 독립 규칙 N개 → 가장 심각한 verdict | "가장 심각한 규칙 채택" | SettleMesh, SlotGate, VetoEscrow, SpendMesh |
| **Mesh** | heterogeneous → normalize → assess → price → ledger | 이종 입력을 canonical record로 정규화 | AgentMesh, PqcMesh |
| **Clearing** | supply/demand → 우선순위 청산 → posture | supply·demand 두 책 매칭 | ColdMkh, ReserveFlow, BuyBloc |
| **Index** | observations → score → tier | 관측→점수→tier/band | ENLI, PnR, ClimateMesh, FlowMesh |
| **Ledger** | envelope → hash → attestation | 핵심 산출이 tamper-evident hash chain | ADPR, AgentPACT, RoboTrace |
| **Stage** | profile → 단계화 스케줄 → rollback trigger | 시간축 단계 스케줄 | LazarettoStage, ThermalPlumeStage |
| **Appraisal** | asset → simulate → bankability | 자산 시뮬레이션 → 수익성 판정 | WasteStack, SeasonBat, CoverGate |

> 경계 사례는 주축 1개 + 보조축 표기(예: `Gate+Ledger`, `Appraisal+Ledger`).

### 4.3 축3 — 5 기능 계층 (layer) — archetype과 **직교**

| Layer | 역할 | 후보 |
|---|---|---|
| **Sensing** | 위험/변화 감지 | ENLI, ContextCreep, ClimateMesh, DriftDossier |
| **Evidence** | 증거/출처 고정 | ADPR, Qvidence, RoboTrace, PnR, AgentPACT |
| **Control** | 개입/중단/우회 | AfferentCore, SlotGate, VetoEscrow, LoopKit |
| **Allocation** | 자원/권리 배분 | ReserveFlow, BuyBloc, PowerRoam, CoverGate |
| **Release** | 배포/방출/스테이징 | LazarettoStage, ThermalPlumeStage, ReleaseMesh, ForgeQuarantine |

예: ClimateMesh = 형태 Index × 기능 Sensing. 두 축은 독립이라 조합 공간이 7×5로 넓어진다.

### 4.4 Lens Palette (L1~L25) — 코퍼스에서 역추출

변형 연산자는 임의 생성하지 않고 코퍼스 Provenance가 명시한 것을 쓴다. 주요 렌즈:

| Lens | 의미 |
|---|---|
| `L1_DirectionReversal` | 누가 비용/증명/공급하는가 반전 |
| `L6_Gap` | 아무도 책임 안 지는 공백 메움 |
| `L7_Tension` / `L7_FailureAsFeature` | 긴장·실패를 자산화 |
| `L8_SideEffectMining` | 부산물을 제품으로 |
| `L9_Counterfactual` / `L9_ScaleShift` | "만약 X가 Y처럼 규제됐다면" / 단일→스웜 |
| `L10_Generative` | 추상 상품화 → 희소 기질로 이동 |
| `L11_DomainTransplant` | A 메커니즘을 B 도메인으로 이식 |
| `L13_FrequencyShift` | 연속 → 1회/계절 |
| `L17_ConstraintSubstitute` | 구속 제약을 다른 제약으로 |
| `L19_Aggregation` | 분산 → 단일 책/거래소 |
| `L24_BoundaryRedraw` / `L25_StockToFlow` | 경계 재설정 / 재고→흐름권 |

> 새 코퍼스에서 미등록 lens는 팔레트에 추가하되 `(inferred)` 플래그. 코퍼스가 커질수록 팔레트·
> vocab_registry가 자동 확장(공진화).

---

## 5. 파이프라인 — Corpus → DesignSeed (Phase 0~7)

런타임 중립. Claude Code는 `/recreate run`, 슬래시 없는 타 런타임은 자연어 지시로 동일
수행. 모드: `run`(풀) / `map`(Phase0~1) / `generate`(Phase2~5) / `seed`(Phase6) / `status`.

```python
load_registry + create_run_scope + input_manifest   # 격리 + 생성물 제외
  → build_genes            # 코퍼스(생성물 제외) → 3축 ProjectGene
  → build_inventory        # [parallel] 형태/속성/기능 선반 + lens + vocab
  → generate_candidates    # [parallel] 3경로 × 8 발산도구 → K=12 후보
  → avoidance_gate (each)  # 과거 run/생성물 회피: hard-reject + AI penalty
  → differentiate (each)   # 코퍼스 대비 overlap + tag_clash + vocab_clash
  → select_or_integrate    # 상보 통합 → 원본+통합 풀에서 6축 top 5
  → prove                  # 실제 brief 산출 + 자기검증 (0개면 실패)
  → emit_design_seed       # runs/{run_id}/DESIGN-SEED-{Name}.md (run rename)
  → update_registry        # winner·소비 source 누적 + latest.json
  → /pgf full-cycle {Name} # 핸드오프
```

### 5.1 Phase 0 — Corpus + run 격리

1. `registry.json` 로드(없으면 빈 registry). `run_id = {NNN}-pending` 시퀀스(**timestamp 금지** — PG 결정론).
2. `.recreate/runs/{run_id}/` 생성. `input_manifest.json`에 코퍼스 included / **생성 프로젝트 excluded** 고정.
3. 코퍼스가 직전 run과 동일하면 `genes.json` 상속 가능(provenance 명기), 변경되면 재추출.

### 5.2 Phase 1 — Inventory (3축 선반)

`[parallel]`로 ArchetypeShelf / PrimitiveShelf / LayerShelf / LensPalette / VocabRegistry 구축 →
`inventory.md`. 기준: 코퍼스 전체 3축 비어있지 않음, lens 추론분 `(inferred)` 플래그.

### 5.3 Phase 2 — Generate (3경로 × 8 발산도구)

분류는 직교(3경로), 발상은 풍부(8도구). 각 후보 **`parts ≥ 2` source projects 강제**(코퍼스 기반성).
이름/mechanism에 **과밀 어휘 금지**: `OVERUSED = [mesh, clearing-market, generic ledger, simple gate, escrow, marketplace]`.

```text
RECOMBINE  (≥2 부품 합성)
    DistantHybridization   # 먼 domain + 중간 이상 evidence 유사도
    LayerFusion            # Sensing→Evidence→Control→Allocation→Release 각 1개 stack
    ConflictCompiler       # 충돌하는 두 프로젝트를 붙여 새 tension (L7을 생성도구로 역전)
MUTATE     (1 부품 × 렌즈로 축 교체)
    LensApply              # 코퍼스 lens 적용, axis 교체
    GrammarMutation        # 과밀 문법 → 신문법 치환 (mesh→atlas/compiler/protocol 등)
    NegativeSpaceInversion # "하지 않은 행위"를 제품화 (PnR 일반화)
TRANSPLANT (메커니즘을 새 도메인/OS로)
    DomainTransplant       # mechanism 추출 → 도메인 명사 제거 → 재명명
    SystemIntegration      # 다도메인 → 단일 OS 통합
```

산출: `candidates.md`. 목표 K=12 → 차별화·선정 후 top 5.

### 5.4 Phase 2b — Avoidance (재실행 회피) ★registry 있을 때

생성 프로젝트는 코퍼스 스캔에서 제외되므로 Phase 3가 못 본다 → 여기서 본다. **2게이트 분리**:

```python
# Hard reject (결정론)
if normalize_name(cand.name) in {normalize(n) for n in registry.blocked_names}: reject()
if source_fingerprint(cand.parts) in registry.source_fingerprints: reject()   # "+".join(sorted(set(parts)))
if normalize_name(cand.name) in corpus_source_names: reject()

# Soft (AI 우선, 공식은 가이드)
score = AI_assess_avoidance(cand, registry, guide=AVOIDANCE_GUIDE)
verdict = "reject" if score>=0.55 else "needs_pivot" if score>=0.30 else "allow"
# 모든 판정(reject/needs_pivot/allow)을 점수·근거와 함께 avoidance_report.md에 로깅 (감사)
```

소비 source를 완전 금지하지 않는다(코퍼스 48개뿐) — 같은 조합·같은 문제를 강회피하되 부품 재사용은
penalty로만 억제. `copy` 재사용은 더 높은 penalty, `redesign`은 약한 penalty.

### 5.5 Phase 3 — Differentiate (정량 차별화 게이트)

```python
overlap >= 0.7  or tag_clash >= 3                -> duplicate   (기각 or pivot)
overlap >= 0.4  or tag_clash >= 2 or vocab_clash -> needs_pivot (변형 후 재투입)
else                                              -> distinct    (통과)
```
`vocab_clash`면 distinct여도 **재명명 강제**(ContextCreep 교훈). `VocabRegistry`는 코퍼스가 커질수록
확장되어 차별화가 자동으로 강해진다.

### 5.6 Phase 4 — Select-or-Integrate (상보 통합 + 6축 선정)

`overlap`(결과물 중복도)과 `complementarity`(같은 문제·다른 강점축)는 **다른 신호**다.

```python
overlap 높음                         -> duplicate  (하나 버림 — Phase 3)
overlap 낮음 + complementarity 높음  -> integrate  (제3 후보로 통합 — Phase 4)
overlap 낮음 + complementarity 낮음  -> 독립 후보   (각자 select)
```

**통합 절차**: consensus 추출 → 상보 강점 매핑 → 골격(spine) 선택 → `AI_make_absorb`(흡수, 병합 아님)
→ 충돌 해소. **통합 게이트**: 통합 후보가 원본 최고 6축점을 **능가할 때만 채택**(아니면 폐기).

**6축 루브릭** (각 0~1, aggregate=합, 최대 6):

| 축 | 의미 | 임계 |
|---|---|---|
| `reuse_leverage` | 부품 재사용 효율(빠른 MVP) | ≥0.5 |
| `novelty` | 코퍼스 대비 차별성 (최우선 가중) | ≥0.6 |
| `domain_demand` | 도메인 수요/시급성 | ≥0.4 |
| `buildability` | stdlib·15분 노드·≤2일 MVP | ≥0.5 |
| `boundary_clarity` | "~가 아니다"를 명확히 | ≥0.5 |
| `system_potential` | 단발 MVP 너머 생성장치 가능성 | ≥0.3 |

**통합 적용 조건 (실증 — §10)**: 통합이 부모를 능가하려면 ① 강한 same_problem + ② **구조적으로 정렬된
상보축**(시간축 lifecycle/인과/파이프라인) + ③ 부모 단독으로 못 보는 **통합 고유가치**가 필요하다.
조건이 없으면 input contract만 넓어져 buildability·boundary_clarity를 잃고 게이트에서 기각된다.
렌즈 ensemble·임의 layer-stack은 회의적으로. margin이 ±0.1로 근소하면 cross-model 합의로 검증(§9).

### 5.7 Phase 5 — Prove (실증 자기검증) ★필수

top-K 후보를 brief로 풀어 5개 check 통과. **후보 0개 산출이면 방법론 실패로 본다.**
- source projects ≥ 2개
- 이름/mechanism에 과밀 어휘 없음
- 최근접 sibling 대비 명시적 차별점
- cli_triplet + stdlib-only skeleton 적합
- single_question이 결정론 엔진으로 답변 가능

### 5.8 Phase 6 — Seed (DesignSeed 출력)

선정 winner → `runs/{run_id}/DESIGN-SEED-{Name}.md`. run rename `{NNN}-pending → {NNN}-{winner-slug}`.
DesignSeed 스키마(§7.5)는 `pgf full-cycle`의 DESIGN 입력 계약이다.

### 5.9 Phase 7 — UpdateRegistry

`registry.json`에 winner를 `generated_projects`(구현된 것만)·`blocked_names`·`source_fingerprints`에
추가, 소비 source를 `source_projects`에 누적. `latest.json` 갱신.

---

## 6. 재실행 안전 (Rerun Safety)

정본: `skills/recreate/reference/rerun-avoidance.md`.

### 6.1 왜 필요한가 (4문제)

① 산출물 충돌(flat 파일 덮어쓰기) ② 추적 불명(어떤 seed가 어떤 구현으로) ③ 소비 이력 부재(같은 조합
재생성) ④ 코퍼스 오염(생성 프로젝트가 다음 run 스캔에 섞임). 코퍼스가 작아(48) ③④가 특히 실재.

### 6.2 run-scoped 디렉토리 계약

```
.recreate/
    latest.json              # 최신 run 포인터
    registry.json            # run을 넘어 누적되는 durable 기억
    runs/{run_id}/           # 불변 — 덮어쓰기 금지 (run_id = {NNN}-{winner-slug})
        input_manifest.json genes.json inventory.md candidates.md
        avoidance_report.md DESIGN-SEED-{Name}.md status.json
```

### 6.3 통합 예외 (§9 of rerun-avoidance) — cross-model integration

회피가 winner들을 disjoint source로 밀어내 통합을 구조적으로 막는 긴장을 푼다. 이미 *생성된 프로젝트들*을
부모로 한 통합은 원본 코퍼스 중복이 아니라 상위 합성이므로:
- `gen_path == "INTEGRATE"`, `parents` = registry의 `generated_projects`.
- **`generated_fingerprint`** = `"+".join(sorted(parents))` — 코퍼스 `source_fingerprints`와 별개 네임스페이스.
  같은 부모 조합 재통합은 hard-reject.
- 부모를 통해 transitive 재사용되는 코퍼스 source는 penalty **면제**(provenance가 부모 명시 필수).
- 통합 인플레이션 가드: 한 winner는 최대 2개 통합의 부모까지, 통합물을 다시 부모로 삼는 메타-통합은
  별도 정당화 + 후행 cross-model 합의 필수.

### 6.4 동시 실행 계약 (§10 of rerun-avoidance) — concurrent multi-runtime

순차 실행 전제를 넘어 진짜 동시 실행을 다룬다. 정본: `docs/CONCURRENCY-POLICY.md`.
- registry에 `version`(monotonic) + `active_runs`(append-only claim 로그).
- **OCC(낙관적 동시성 제어)**: 원자적 경계는 Phase 0 claim·Phase 7 commit 둘뿐, 그 사이는 병렬.
  - Phase 0: registry 락 → `run_id = {NNN}-{runtime}-pending`(runtime 접미사로 디렉토리 충돌 차단) + claim append + version++.
  - Phase 7: registry 락 → 현재 registry 대비 winner 재검증(OCC) → 충돌 없으면 commit+version++, 충돌이면 abort 후 pivot/discard.
- **충돌 해소(결정론 outcome)**: 먼저 커밋한 run이 fingerprint 보유, 두 번째 도달자는 pivot/discard.
  정확히 한 run만 각 fingerprint/이름 보유. wall-clock 미사용, 재현은 claim_seq 직렬 replay.
- 한계: 공유 FS 전제(분산은 외부 조정 필요), 코퍼스 48개라 동시성↑ 시 pivot 실패율↑ → 동시 run 상한 보수적.

---

## 7. 데이터 계약 (모든 파일 스키마)

### 7.1 `registry.json` (durable, run을 넘어 누적)

```jsonc
{
  "schema_version": "1.1", "updated_at": "<date>",
  "version": 7,                 // monotonic, claim/commit이 올림 (§6.4)
  "active_runs": [],            // append-only claim 로그
  "corpus_baseline": { "project_count": 48, "source": "corpus/" },
  "source_projects": {          // 코퍼스 원본 단위 사용 이력
    "<Source>": { "use_count": int, "used_by": [str], "roles": [str],
                  "last_used_run": str, "last_reuse_cost": "copy|parametrize|redesign" }
  },
  "generated_projects": {       // 실제 구현된 것만
    "<Name>": { "created_by_run": str, "seed_path": str, "implementation_path": str,
                "pgf_status_path": str, "status": "seeded|implemented", "public_repo": str?,
                "consumed_sources": [str], "source_fingerprint": str,
                "single_question": str, "archetype": str, "layers_used": [str],
                "verdict_scheme": [str],
                // 통합 winner 추가 필드:
                "gen_path": "INTEGRATE"?, "integrated_from": [str]?, "generated_fingerprint": str?,
                "transitive_consumed_sources": [str]?, "cross_model_certified": str? }
  },
  "blocked_names": [str],
  "source_fingerprints": { "<A+B+C>": {"project": str, "run_id": str} },   // 코퍼스 조합 중복키
  "generated_fingerprints": { "<P1+P2>": {"project": str, "run_id": str} } // 부모 조합 중복키
}
```

### 7.2 `latest.json`
```json
{ "latest_run_id": str, "latest_run_path": str, "winner": str, "seed_path": str }
```

### 7.3 `input_manifest.json` (run-scoped, run 시작 시 고정·불변)
```json
{ "run_id": str, "runtime": str, "corpus_root": str, "included_source_count": 48,
  "excluded_generated_projects": [str], "registry_snapshot": {...},
  "avoidance_policy": {...}, "genes_provenance": str }
```

### 7.4 `genes.json` — `[ProjectGene, ...]` (§4.1 스키마 배열, 48개)

### 7.5 `DESIGN-SEED-{Name}.md` (pgf DESIGN 입력 계약)

필드: `name · single_question · archetype · layers_used · reuse_plan(부품별 copy/parametrize/redesign)
· lens_stack · domain · verdict_scheme · cli_triplet · boundary · acceptance_seeds · differentiation_note`.
통합 winner는 `integrated_from · generated_fingerprint · transitive_consumed_sources` 추가.

### 7.6 run `status.json`
```jsonc
{ "mode": "run", "run_id": str, "runtime": str, "corpus_projects": 48,
  "winner": str|null, "consumed_sources": [str], "source_fingerprint": str|null,
  "selected_top": [str], "registry_updated": bool, "cross_model_certified": bool, "artifacts": [str] }
```

### 7.7 cross-model 채점 (`.recreate/crossmodel/scores/{runtime}.scores.json`)
```jsonc
{ "runtime": str, "independence_attestation": str,
  "scores": { "<Winner>": { "reuse_leverage": 0..1, "novelty": .., "domain_demand": ..,
              "buildability": .., "boundary_clarity": .., "system_potential": ..,
              "aggregate": float, "self_authored": bool, "rationale": str } },
  "integrate_gate_local": { "W6_aggregate": float, "best_parent": str,
              "best_parent_aggregate": float, "W6_exceeds_best_parent": bool } }
```

---

## 8. PG/PGF 의존성과 핸드오프

### 8.1 PG (PPR/Gantree Notation) — AI-native 명세 언어

recreate 문서는 PG 표기로 쓰인다. **Parser-Free**: 파서/컴파일러 불필요, AI가 *이해*해 실행.
- `AI_xxx(...)`: AI 인지 연산(판단/추론/인식/창조). 결정론 계산은 일반 코드로.
- `AI_make_xxx(...)`: 사역(대상을 ~하게 만든다).
- `a → b → c`: 파이프라인. `[parallel] ... [/parallel]`: 병렬 구간.
- 4칸 들여쓰기 = Gantree 계층(최대 5레벨, 6레벨 진입 시 `(decomposed)` 분리).
- 노드 status: `done|in-progress|designing|blocked|decomposed|needs-verify`. `@dep:`, `@v:`, `#tag`.
- `# acceptance_criteria:` 인라인 완료 조건.

타 런타임에 pg 스킬이 없어도 위 표기를 그대로 해석하면 된다(parser-free).

### 8.2 PGF (Framework) — full-cycle

`pgf full-cycle {Name} --with-review`가 DesignSeed를 DESIGN 입력으로 받아 자율 실행:
`DESIGN → (review 게이트) → PLAN(WORKPLAN+status.json) → EXECUTE → VERIFY(3관점)`. 산출:
`.pgf/{DESIGN,REVIEW,WORKPLAN,VERIFY,status}-{Name}.*`.

DesignSeed → pgf 매핑:
| seed 필드 | pgf 전개 |
|---|---|
| archetype | 아키타입별 표준 Gantree 골격으로 노드 분해 |
| reuse_plan | copy=이식 노드 / parametrize=인자화 / redesign=신규 PPR def |
| verdict_scheme | 판정 엔진 노드 + verdict 분기 PPR |
| acceptance_seeds | 각 노드 `# acceptance_criteria:` 인라인 |
| cli_triplet | sample/run/report 진입점 |
| boundary | DESIGN의 MVP Scope |

아키타입별 Gantree 골격 힌트:
```
Gate       → InputSpec → RuleEngine(N rules) → SeverityAggregate → Report
Index      → Observations → Score → Tier → Report
Ledger     → Envelope → Canonicalize → HashChain → Attest → Verify
Stage      → Profile → RiskBand → StagedSchedule(rollback) → Report
Appraisal  → Asset → Simulate → Settle → Bankability → Report
```

---

## 9. Multi-Runtime & Cross-Model 합의

recreate는 런타임 중립이라 여러 AI 런타임이 각자 run을 돌릴 수 있다.
정본: cross-model 채점 프로토콜은 `scripts/aggregate_crossmodel.py` + `schemas/crossmodel-scores.template.json`.

### 9.1 채점 프로토콜

- 마스터 TaskSpec(`TASKSPEC-crossmodel-scoring.md`): 채점 대상 winner들 + 6축 루브릭 앵커(0.0/0.5/1.0 고정)
  + 출력 계약 + 독립성 규율.
- 런타임별 복붙 지시(`INSTRUCTIONS-per-runtime.md`): 각 런타임이 `{runtime}.scores.json` 생성.
- 독립성: 채점 전 타 런타임 점수 미열람, 자기 winner는 `self_authored: true`(self-bias 분리).

### 9.2 집계·certification (`AGGREGATION.md`, `aggregate_crossmodel*.py`)

- consensus(X) = per-axis median 합. disagreement = per-axis stdev 합.
- integrate 게이트 재판정: consensus(통합) > max(consensus(부모))? + robustness(개별 지지 비율).
- self-bias = 저자 점수 − 타 런타임 median. 저자 과대평가가 게이트를 떠받치면 certification 강등.
- 판정: gate_holds ∧ robustness≥0.6 ∧ disagreement<0.9 → `true (robust)` / 게이트 안 서면 `false`.

---

## 10. 실증 결과 (reference case study)

이 방법론은 한 reference corpus 위에서 여러 AI 런타임으로 실제 검증됐다. 프로젝트명·런타임명을 익명화한
전체 실증은 **`examples/CASE-STUDY.md`** 에 있다. 핵심 결론만 요약하면:

- **multi-runtime 회피가 fleet 규모에서 작동**: 여러 런타임이 조율 락 없이 이름·fingerprint·source 충돌 0,
  소비 source 완전 분할(모든 use_count=1). 각 런타임이 registry consumed_sources를 읽고 사전에 신선 부품으로 방향 전환.
- **cross-model integrate 양성**: 시간축(lifecycle) 정렬 통합 후보가 부모를 cross-model 합의로 능가, certified robust.
  저자 self-bias가 음수(저자가 오히려 박하게) → 게이트가 self-promotion으로 서지 않음.
- **cross-model integrate 음성**: 비-시간축(렌즈/계층) 통합은 부모 미달, 전원 음성 지지.
- **통합 적용 조건 확정**: integrate는 강한 same_problem + 구조 정렬 상보축(특히 lifecycle)에서만 부모를 능가(§5.6).
- **합의가 단일 판정을 양방향 증폭**: 양성은 더 양성, 음성은 더 음성. cross-model 검증의 가치 입증.

> 이 결과들은 *방법론이 실제로 작동함*의 증거다. 당신의 코퍼스로 돌리면 winner·점수·통합 결과는 달라진다 —
> 동일한 것은 파이프라인·게이트·계약이다.

---

## 11. 직접 구현하려면 (개발자 가이드)

### 11.1 recreate 방법론을 실행하는 법

recreate는 별도 코드 실행 엔진이 아니라 **AI 런타임이 SKILL.md를 읽고 PG 표기를 해석해 수행**하는
parser-free 절차다. 따라서 "구현"은 두 층위다:

**(A) 방법론 실행** — AI 런타임으로:
1. `skills/recreate/SKILL.md`를 처음부터 끝까지 읽는다(+의존 `pg`/`pgf` 스킬, reference 5개).
2. `.recreate/registry.json` 로드 → run 격리(§5.1).
3. Phase 0~7을 순서대로 수행(§5). 각 Phase 산출을 `runs/{run_id}/`에 파일로 남긴다.
4. winner → DesignSeed → `pgf full-cycle`로 핸드오프.

결정론 부분(fingerprint, normalize, 집계 통계)은 `scripts/`로 스크립트화 가능(예:
`aggregate_crossmodel.py`). AI 판정 부분(archetype 분류, overlap, 6축 점수)은 런타임이 수행.

**(B) 생성된 프로젝트 구현** — 각 winner는 다음 패턴의 stdlib-only Python MVP:

### 11.2 생성 프로젝트의 표준 구현 패턴 (6개 모두 동일)

```
{Name}/
    {snake_name}.py        # 단일 모듈: 엔진 + CLI + ledger
    examples/              # sample 출력에서 생성 (covered/conditional/uncovered 등 3종)
    tests/                 # unittest (결정론·verdict·ledger 검증)
    README.md  LICENSE(MIT)  .gitignore
```

핵심 규율:
- **결정론 verdict path**: 네트워크·시계·AI 호출 **금지**. 시간이 필요하면 호출자가 `as_of_utc` 공급
  (시스템 시계 미사용). 같은 입력 → 같은 verdict.
- **CLI triplet**: `sample`(예제 JSON 방출) / `run <packet.json> [--ledger path]`(JSON verdict+reasons) /
  `report <packet.json>`(Markdown). `report`는 상태 불변, `run --ledger`만 기록.
- **k-way verdict**: 3분(또는 4분). 모든 verdict에 rule-level `reasons[]` 첨부(감사).
- **collect-all 규칙 평가**: 첫 실패에서 멈추지 말고 모든 위반 규칙을 reasons에 남긴다.
- **commitments**: `input_sha256` / `verdict_sha256` / `combined_sha256` (canonical JSON).
- **hash-chained ledger**(선택): JSONL, 각 entry가 직전 `entry_sha256`를 체인(genesis 64-zero),
  `verify_ledger()`가 변조 탐지. 모든 프로젝트가 동일 ledger shape를 써 fleet-wide verifier 호환.
- **boundary**: "이것은 ~가 아니다" 1문장을 코드 상수·README·report에 명시.

참조 구현 패턴: 단일 stdlib 모듈에 엔진+CLI+ledger를 담는다. reference case study의 실제 구현 사례는
`examples/CASE-STUDY.md`에서 익명으로 요약(예: underwriting gate, lifecycle-fold OS — 모두 단일 파일 stdlib).

### 11.3 canonical JSON / hash 헬퍼 (모든 프로젝트 공통)

```python
def canonical_json(obj):  # 정렬·무공백 → 결정론 직렬화
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
def sha256_hex(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()
```

### 11.4 GitHub 공개 절차 (참조)

독립 git repo init → commit(author = 프로젝트 소유자, Co-Authored-By 런타임) → `gh repo create
<your-org>/{Name} --public --source=. --push` → topics 부여 → registry에 `public_repo` 기록. (소유자/호스트는 당신 것으로.)
`.gitignore`로 `__pycache__` 등 제외. 루트 `D:\ProjectGenome`는 git 저장소가 아니며 하위 프로젝트만 독립 repo.

---

## 12. 디렉토리 전체 지도

```
ProjectGenome/
    README.md                  주 온보딩
    RUNBOOK.md                 단계별 실행 가이드
    LICENSE                    MIT
    .gitignore                 런타임 산출(.recreate/runs, .pgf, scores) 제외
    assets/                    projectgenome-hero.png
    docs/
        TECHNICAL-SPECIFICATION.md   ← 이 문서
        CONCURRENCY-POLICY.md        OCC 동시성 계약
    skills/
        recreate/SKILL.md + reference/{gene-extraction, generation-paths,
                            rerun-avoidance, differentiation, design-seed}.md
        pg/SKILL.md  pgf/SKILL.md   (의존 스킬)
    schemas/                   registry.empty.json · registry.schema.json ·
                               project-gene.schema.json · design-seed.template.md ·
                               crossmodel-scores.template.json
    scripts/                   fingerprint.py · validate_projectgenome.py ·
                               aggregate_crossmodel.py · concurrency.py   (결정론 도구, stdlib only)
    tests/                     결정론 헬퍼 unittest (stdlib only)
    .github/workflows/ci.yml   CI (py_compile + unittest + validate)
    corpus/                    ← 사용자의 README 코퍼스 (README.md + corpus/example/ 3종 동봉)
    examples/CASE-STUDY.md     익명 실증
    examples/example-run/      corpus/example로 돌린 축약 산출 (genes/inventory/candidates/DesignSeed)
    --- 런타임 실행 시 생성 (gitignored) ---
    .recreate/
        latest.json  registry.json   (schemas/registry.empty.json에서 시작)
        runs/{NNN}-{slug}/   (불변 run 산출)
        crossmodel/          TASKSPEC·scores/ (cross-model 채점 시)
    .pgf/
        {DESIGN,REVIEW,WORKPLAN,VERIFY,status}-{Name}.*   (각 winner의 full-cycle 산출)
    {generated project folders}/   (런타임이 생성) stdlib MVP + 독립 git repo (코퍼스 스캔 제외)
```

---

## 13. 정직한 경계와 한계

- lens 역추출은 Provenance 미기재 시 추론 — `(inferred)` 플래그로 구분.
- overlap/임계(0.4/0.7), tag_clash(2/3), avoidance penalty(0.30/0.55)는 코퍼스 초기값 — 성장 시 재보정.
- `domain_demand`·`system_potential`은 외부 신호 없이 AI 판단 — 시장 검증은 범위 밖.
- 6축 점수는 단일 평가자면 편향 가능 → 근소 margin은 cross-model 합의로 보정(§9).
- 통합은 무조건 좋은 장치가 아니라 조건부(§5.6, §10) — 자연 정렬축에서만 부모를 능가.
- 동시성 정책(§6.4)은 공유 FS 전제 — 분산 런타임은 외부 조정 서비스 필요(미설계).
- 코퍼스 48개라 동시 run이 많으면 신선 조합 고갈 — 동시성 상한 보수적.
- `DesignSeed`는 `pgf full-cycle` 구현·검증 전까지 잠정(provisional).

---

## 14. 용어집

| 용어 | 뜻 |
|---|---|
| **ProjectGene** | 한 코퍼스 프로젝트를 3축(형태/속성/기능)으로 환원한 부품 레코드 |
| **archetype** | 7 엔진 골격(Gate/Mesh/Clearing/Index/Ledger/Stage/Appraisal) |
| **layer** | 5 기능 계층(Sensing/Evidence/Control/Allocation/Release), archetype과 직교 |
| **lens** | 코퍼스에서 역추출한 변형 연산자 L1~L25 |
| **skeleton** | 코퍼스 공통 골격(single_question→engine→verdict→dual_output→cli_triplet→boundary→provenance) |
| **DesignSeed** | Phase 6 산출, pgf DESIGN 입력 계약(잠정) |
| **source_fingerprint** | `"+".join(sorted(코퍼스 source 조합))` — 조합 중복 검사 키 |
| **generated_fingerprint** | `"+".join(sorted(부모 생성프로젝트 조합))` — 통합 중복 검사 키(별도 네임스페이스) |
| **reuse_cost** | 부품 재사용 비용 copy(그대로)/parametrize(인자화)/redesign(개념만) |
| **integrate** | 상보 군집을 제3 후보로 통합(병합 아님, 골격+흡수). 부모 능가 시만 채택 |
| **cross_model_certified** | 통합 채택이 여러 런타임 6축 합의로 재현됨(robust/conditional/false) |
| **OCC** | 낙관적 동시성 제어 — baseline version 기록 후 commit 시 재검증 |
| **PG / PGF** | AI-native 명세 표기(parser-free) / 그 위의 full-cycle 실행 프레임워크 |

---

> **다음 단계 진입점**: 새 프로젝트를 만들려면 §5 파이프라인을 `/recreate run`(또는 자연어 등가)으로
> 실행하고, 산출 DesignSeed를 §8의 `pgf full-cycle {Name} --with-review`로 구현한다. 여러 런타임으로
> 다양성·합의를 얻으려면 §9. 동시 실행은 §6.4 계약을 먼저 활성화한다.
