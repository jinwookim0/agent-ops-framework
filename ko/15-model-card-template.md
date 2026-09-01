# 시스템/모델 카드 템플릿 — 프로젝트가 아니라 "이 AI가 뭘 하는지"를 문서화

> 🌐 **[Read in English](../en/15-model-card-template.md)**

**버전**: 1.0.2
**콘텐츠 해시**: sha256:9d1df1000ee3 (본문 기준, 이 두 줄 제외)

지금까지의 크리스탈(01~14)은 대부분 **프로젝트를 어떻게 운영하는가**를
다뤘다. 이 크리스탈은 다른 질문이다 — **이 AI 에이전트/기능 자체가
정확히 무엇을 하고, 어디까지 믿을 수 있고, 어디서 잘못될 수 있는지를
사용자에게 어떻게 알려주는가.**

## 근거 (1차 자료 확인)

🟢 Mitchell et al. 2019, *Model Cards for Model Reporting*(Google,
FAT* 2019) — [arXiv:1810.03993](https://arxiv.org/abs/1810.03993) 원문을 직접 확인. 핵심
동기를 원문 그대로 인용: "모델의 의도된 사용 사례를 명확히 하고, 적합하지
않은 맥락에서의 사용을 최소화하기 위해서"다.

## 원문이 제시하는 9개 섹션 (원문 그대로 확인된 목록)

1. **Model Details** — 모델의 기본 정보(개발 주체, 버전, 유형, 학습 방식,
   참고 문헌, 연락처).
2. **Intended Use** — 원래 의도된 사용처와 사용자, 그리고 **의도되지 않은
   사용**(out-of-scope use cases)을 명시.
3. **Factors** — 성능이 달라질 수 있는 요인(인구통계학적 그룹, 환경 조건,
   기술적 속성 등).
4. **Metrics** — 성능을 어떤 지표로 측정했는지, 왜 그 지표를 골랐는지.
5. **Evaluation Data** — 평가에 쓴 데이터셋과 그 출처·전처리 과정.
6. **Training Data** — 학습에 쓴 데이터(가능한 만큼 공개, 불가능하면
   최소한 그 특성이라도).
7. **Quantitative Analyses** — 그룹별로 나눈 정량 성능 비교(전체 평균만이
   아니라 하위집단별로 — [03-epistemic-immunity-catalog.md](03-epistemic-immunity-catalog.md)
   9번 "미시-거시 반전"과 같은 원칙).
8. **Ethical Considerations** — 사용 시 고려해야 할 윤리적 리스크.
9. **Caveats and Recommendations** — 추가 테스트가 필요한 부분, 알려진
   한계, 개선 권고.

## AI 에이전트 프로젝트에 적용하는 법 — "모델"에서 "기능/작업"으로 단위를 바꾼다

원문은 학습된 ML 모델 하나를 문서화하는 걸 전제로 한다. AI 에이전트
프로젝트에서는 보통 모델 자체를 학습시키지 않으므로, **문서화 단위를
"모델"에서 "이 프로젝트가 제공하는 개별 기능/작업"으로 옮겨** 적용한다:

| 원문 섹션 | AI 에이전트 기능 카드로 재해석 |
|---|---|
| Model Details | 이 기능이 어떤 도구/모델을 쓰는지, 언제 만들어졌는지, 누가 관리하는지 |
| Intended Use | 이 기능이 하는 일과, **명시적으로 하지 않는 일**(예: "투자 자문이 아니다", "법률 자문이 아니다") |
| Factors | 이 기능의 결과가 달라질 수 있는 조건(입력 언어, 도메인, 데이터 최신성) |
| Metrics | [04-eval-engineering-methodology.md](04-eval-engineering-methodology.md)의 통과 기준 |
| Evaluation Data | 어떤 평가 케이스로 검증했는지 |
| Training Data | (해당 시) 이 기능이 참고하는 공유 컨텍스트/이력 데이터의 성격 |
| Quantitative Analyses | 케이스 유형별 통과율(전체 평균만 보여주지 않는다) |
| Ethical Considerations | 이 기능이 다루는 민감한 판단(재정·건강·법률 등)과 그 한계 |
| Caveats and Recommendations | [알려진 한계 절 — 04·11 등 다른 크리스탈이 이미 쓰는 형식] |

## "의도되지 않은 사용"을 명시하는 게 핵심

원문에서 가장 자주 간과되는 섹션이 Intended Use의 "의도되지 않은 사용"
부분이다 — 많은 문서가 "이걸 할 수 있다"만 쓰고 "이걸 위해 쓰면 안 된다"는
안 쓴다. [01-definition-of-done.md](01-definition-of-done.md) 10번째
기준(콘텐츠 출처 동기 편향)과 [10-human-ai-interaction-guidelines.md](10-human-ai-interaction-guidelines.md)
G1(시스템이 할 수 있는 것을 명확히 한다)이 이미 이 방향을 다루지만, Model
Card는 그걸 **"하지 않는 것"까지 대칭적으로 명시하라**는 걸 구조적으로
강제한다는 점에서 보완적이다.

## 실용적 축소판 — 전체 9섹션이 부담스러울 때

작은 기능 하나하나에 9섹션 전체를 채우는 건 과할 수 있다. 최소 축소판:
**Intended Use(하는 일 + 안 하는 일) + Metrics(통과 기준) + Caveats(알려진
한계)** 세 개만이라도 채운다 — 나머지는 규모가 커지거나 민감도가 높은
기능에만 전체를 적용한다.

## 관련 크리스탈
- [01-definition-of-done.md](01-definition-of-done.md) — 이 크리스탈의
  "Metrics/Evaluation Data" 부분이 DoD 4번(평가 케이스) 기준과 겹친다 —
  중복 작성하지 않고 상호 참조한다.
- [14-ai-red-team-checklist.md](14-ai-red-team-checklist.md) — "Ethical
  Considerations"와 위협 모델링이 만나는 지점.
