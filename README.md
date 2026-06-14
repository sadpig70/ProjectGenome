<h1 align="center">ProjectGenome</h1>

<p align="center">
  <em>Decompose a corpus of existing projects into reusable parts (their "genome"),
  then recombine · mutate · transplant them into new, auditable project seeds.</em>
</p>

---

> **What this is.** ProjectGenome is a *meta-methodology and a runtime-neutral skill* that turns a
> corpus of existing projects (README-level descriptions) into a **generative device** for new
> projects. It does not guarantee that a generated candidate is correct, novel, or valuable — its
> design goal is to make mundane recombination *structurally hard*, and to keep every candidate
> **auditable** (reused parts · differentiation scores · evidence attached). The output `DesignSeed`
> is provisional until built and verified.

ProjectGenome 저장소(시스템) 안에서 실행 명령은 스킬 **`recreate`** 입니다 — 저장소(전체 시스템)와
스킬(실행 명령)은 포함 관계입니다.

## The governing principle: parts ≫ blank-slate

새 프로젝트는 **무에서** 나오지 않는다. 코퍼스가 검증한 엔진·어댑터·verdict·ledger를 재사용한다.
재사용 부품(`parts`)이 비면 후보를 기각해 **코퍼스 기반성**을 강제한다.

```
생성 단위                →  방법
  3축 부품 분해           →  형태(archetype) · 속성(primitive) · 기능(layer)
  3경로 생성              →  RECOMBINE · MUTATE · TRANSPLANT
  8 발산 도구             →  DistantHybrid · LayerFusion · ConflictCompiler …
  중복 회피               →  정량 차별화 게이트 + registry 기반 재실행 회피
  자기검증                →  실증 (후보 0개면 실패)
  여러 AI 합의            →  cross-model 6축 채점
```

## The pipeline

```
/recreate run
  Phase 0  Corpus        registry 로드 + run 격리 + 생성물 제외        → .recreate/runs/{id}/
  Phase 1  Inventory     형태/속성/기능 선반 + lens + vocab            → inventory.md
  Phase 2  Generate      3경로 × 8 발산도구 → K=12 후보                 → candidates.md
  Phase 2b Avoidance     registry 기반 재실행 회피 (hard + soft)        → avoidance_report.md
  Phase 3  Differentiate overlap + tag_clash + vocab 정량 게이트
  Phase 4  Select/Integrate  상보 통합(조건부) + 6축 평가 → top 5
  Phase 5  Prove         후보 brief 실증 (0개면 실패)
  Phase 6  SeedDesign    DesignSeed 출력                                → DESIGN-SEED-{Name}.md
  Phase 7  UpdateRegistry winner·소비 source 누적 + latest.json
```

산출 `DesignSeed`는 `pgf full-cycle {Name} --with-review`(설계→계획→실행→검증)의 DESIGN 입력으로
직결되어 stdlib-only CLI로 구현된다.

## Quick start

```bash
# 1) 당신의 코퍼스를 넣는다 (각 프로젝트의 README.md)
cp -r your-projects/*/README.md corpus/      # 또는 corpus/example/ 로 먼저 체험
cp schemas/registry.empty.json .recreate/registry.json   # 빈 registry로 시작

# 2) AI 런타임으로 recreate 스킬을 실행 (Claude Code: /recreate run, 그 외: 자연어 지시)
#    "Read skills/recreate/SKILL.md and run the full pipeline over corpus/"

# 3) 산출 DesignSeed를 pgf로 구현
#    /pgf full-cycle {Name} --with-review
```

> ProjectGenome은 별도 실행 엔진이 아니라 **AI 런타임이 스킬 문서(PG 표기)를 읽고 수행**하는
> parser-free 시스템이다. 결정론 부분(fingerprint·집계)만 `scripts/`로 스크립트화돼 있다.

## Repository layout

```
README.md                          이 문서
docs/TECHNICAL-SPECIFICATION.md    전체 기술서 (처음 보는 사람용 정본)
skills/recreate/                   실행 스킬 (SKILL.md + reference/ 5종)
skills/pg/  skills/pgf/            AI-native 표기 + full-cycle 의존 스킬
schemas/                           빈 데이터 계약 템플릿 (registry/gene/seed/scores)
scripts/aggregate_crossmodel.py    결정론 cross-model 집계
corpus/                            ← 당신의 README 코퍼스를 여기에 (+ corpus/example/)
examples/CASE-STUDY.md             익명 실증 (방법론이 실제로 작동함의 증거)
```

## Documentation

| 문서 | 내용 |
|---|---|
| [`docs/TECHNICAL-SPECIFICATION.md`](docs/TECHNICAL-SPECIFICATION.md) | **전체 정본** — 방법론·파이프라인·데이터 계약·구현 패턴·실증·용어집 |
| [`skills/recreate/SKILL.md`](skills/recreate/SKILL.md) | 스킬 진입점 (모드·파이프라인 Gantree) |
| `skills/recreate/reference/*` | gene-extraction · generation-paths · rerun-avoidance · differentiation · design-seed |
| [`examples/CASE-STUDY.md`](examples/CASE-STUDY.md) | 한 reference corpus 위 다중 런타임 실증 (익명) |

## License

Released under the [MIT License](LICENSE).
