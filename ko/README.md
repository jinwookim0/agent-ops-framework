# agent-ops-framework — AI 에이전트 프로젝트 운영을 위한 크리스탈 모음

> 🌐 **[Read in English](../en/README.md)**

## 이것은 무엇인가

AI 에이전트가 여러 작업을 관리하는 프로젝트는 대개 **도메인 콘텐츠**(그
프로젝트가 실제로 다루는 대상 — 어떤 프로젝트든 자신만의 것이 있다)와,
그 콘텐츠를 만들어내는 **운영 방식**(거버넌스·품질기준·가드레일·자기개선
루프)이 뒤섞여 있다.

이 폴더는 후자만 뽑아낸 것이다 — 어느 도메인의 어느 프로젝트에 붙여도
그대로 동작하는 **구조적 패턴만** 담는다. "이 프로젝트가 무엇을 다뤘는가"는
안 들어있고, "**작업 완료를 어떻게 정의하는가**", "**지시를 어떻게
누적·색인하는가**", "**AI가 그럴듯하지만 틀린 말을 하는 패턴을 어떻게
검증하는가**", "**프롬프트에 비밀값이 새나가지 않게 어떻게 강제하는가**"
같은 **프로세스 그 자체**만 남겼다.

"AI 에이전트 프로젝트"가 정확히 가리키는 범위: AI를 한 번 호출하고 끝나는
기능이 아니라, **자율적으로, 반복적으로, 여러 작업을 스스로 처리하는**
프로젝트를 뜻한다 — "AI를 쓰는 프로젝트" 전반보다 좁다. 이 구분은 실제로
갈린다: [05-autonomous-agent-operating-principles.md](05-autonomous-agent-operating-principles.md)·
[06-self-improving-heuristics-loop.md](06-self-improving-heuristics-loop.md)·
[19-chaos-engineering-for-agents.md](19-chaos-engineering-for-agents.md)·
[20-decision-rights-raci.md](20-decision-rights-raci.md)·
[29-agent-cost-and-budget-management.md](29-agent-cost-and-budget-management.md)·
[36-execution-mode-escalation-ladder.md](36-execution-mode-escalation-ladder.md)은
이 자율성·반복성이 없으면 애초에 성립하지 않는 크리스탈이다. 범위를
"AI를 쓰는 프로젝트" 전반으로 넓히면 이런 크리스탈들이 왜 필요한지가
흐려진다.

## 왜 "결정체(crystal)"인가

이런 원칙들은 보통 실제 사고·정정·실전 경험을 근거로 자란다 — 그 서사
자체가 신뢰도의 근거이기도 하다("이건 지어낸 원칙이 아니라 실제 사고에서
나왔다"). 하지만 그 서사에는 날짜·특정 프로젝트의 고유 명사·특정 사건의
세부사항이 섞여 있어, 그대로 다른 프로젝트에 옮기면 안 맞는 참조가 남는다.
이 폴더의 각 문서는 **서사를 걷어내고 패턴만 남긴 "결정체" 버전**이다 —
왜 이 규칙이 필요한지의 일반적 근거는 남기되, "이 프로젝트에서 특정
사례를 이렇게 두 번 틀렸다" 같은 원본 프로젝트 전용 사례는 일반화된
예시로 축약하거나 뺐다.

**이 원칙은 이 README 자신에게도 적용된다** — 아래 목록에 날짜나 "어느
질문에 답하며 만들었는지" 같은 제작 서사를 남기지 않는다. 그런 서사(언제,
왜, 어떤 요청으로 이 문서가 생겼는지)는 원본 프로젝트의 지시 이력 문서
쪽이 있어야 할 자리이지, 다른 프로젝트로 옮겨질 이 폴더 쪽이 아니다.

## 번호는 추가 순서다, 중요도가 아니다 — 대신 우선순위는 여기서 본다

아래 각 크리스탈의 번호(`NN-`)는 **추가된 순서를 기록하는 영구 ID**이지
중요도 순위가 아니다 — 이건 실수가 아니라 의도적 설계다: 번호를 안정적
식별자로 고정해야 다른 크리스탈이 `[05-...](05-...)`처럼 서로를 참조하는
링크, 이 폴더를 가져다 쓰는 프로젝트의 참조, `directive-registry.md`류
문서가 크리스탈을 번호로 인용하는 기록이 전부 안 깨진다([BLUEPRINT.md](BLUEPRINT.md)
5절 — ADR·RFC·이 폴더 자신의 [02-directive-registry.md](02-directive-registry.md)가
쓰는 것과 같은 원칙: ID는 안정적이어야 하고 의미를 담으면 안 된다). 대신
"뭐부터 봐야 하는가"는 아래 우선순위 목록으로 따로 표시한다 — 번호를
바꾸지 않고도 정렬 정보를 준다.

**새 프로젝트에 처음 도입할 때 먼저 볼 것 (대략 이 순서)**:
1. [07-prompt-guardrails/](07-prompt-guardrails/) — 개인정보를 다루는 첫
   작업이 생기기 **전에** 반드시 먼저(사후 추가는 이미 노출된 걸 지우는
   훨씬 비싼 작업).
2. [01-definition-of-done.md](01-definition-of-done.md) — 작업이 3~5개를
   넘기 시작하면.
3. [05-autonomous-agent-operating-principles.md](05-autonomous-agent-operating-principles.md) —
   AI가 사람 확인 없이 반복 실행되기 시작하면.
4. [02-directive-registry.md](02-directive-registry.md) — 지시·판단이
   쌓여 "이거 왜 이렇게 정했더라"가 반복되면.
5. [09-project-structure-template.md](09-project-structure-template.md) —
   프로젝트 구조 자체를 설계/재설계할 때.
6. [03-epistemic-immunity-catalog.md](03-epistemic-immunity-catalog.md)·
   [04-eval-engineering-methodology.md](04-eval-engineering-methodology.md) —
   산출물 신뢰도·품질을 처음으로 체계적으로 재야 할 때.

나머지 크리스탈은 각 문서 서두의 "왜 필요한가"가 실제로 자기 프로젝트에
해당되는 시점에 본다 — 전부 한 번에 들여올 필요 없다([USAGE-GUIDE.md](USAGE-GUIDE.md)
"기획 관점"에 같은 순서가 더 자세히 설명돼 있다). 37개 전체를 하나의 총
순위로 매기지는 않는다 — 프로젝트마다 무엇이 먼저 필요한지가 실제로
다르고, 억지로 매긴 총순위는 그 차이를 숨겨 오히려 덜 유용하다.

## 구성 — 주제별

각 크리스탈은 그 자체로 독립적으로 읽고 쓸 수 있다 — 서로 참조하지만
순서대로 안 읽어도 된다. **검증 강도**는 그 문서가 인용하는 1차 자료를
얼마나 확인했는지를 뜻한다(🟢 원문 핵심 내용 직접 확인 / 🟡 골격·이름만
확인, 상세는 문서 자신의 재구성 — 과장하지 않기 위해 매 문서에 명시).
이 개별 검증 강도 표시는 의도적 설계 선택이다 — 같은 계열의 유명한
선례(예: The Twelve-Factor App)도 원칙 모음 전체에 "수백 개 사례에서
봤다"는 집단적 권위만 주장할 뿐 원칙 하나하나에 근거 강도를 개별 표시하지
않는다. 이 폴더는 그 관행보다 한 단계 더 정직하게, 문서 단위로 "어디까지
확인했는지"를 숨기지 않는다.

**이 등급이 정확히 무엇을 재는지, 무엇을 안 재는지(2026-09-01 레드팀
감사로 명확화)**: 🟢/🟡는 **인용의 충실도**(그 문서가 인용한 1차 자료를
실제로 열어 대조했는가)를 잰다 — **이 크리스탈을 실제로 따랐을 때
결과가 더 좋아지는지(효능)는 재지 않는다.** 이 둘은 다른 질문이고,
효능 검증(예: 이 크리스탈을 쓴 팀과 안 쓴 팀을 비교)은 이 프레임워크가
인용하는 외부 표준들(RACI, Amershi et al. 2019, NIST AI RMF 등) 자신도
제공하지 않는, 훨씬 비용이 큰 종류의 근거라 이 폴더가 요구하지 않는다.
또한 이 등급은 **크리스탈을 작성한 것과 같은 AI 세션이 스스로 재확인한
결과다** — 독립된 사람이나 다른 모델이 사후에 검증한 게 아니다("자기
채점"이라는 뜻). 이 폴더가 다른 크리스탈(예: [06-self-improving-
heuristics-loop.md](06-self-improving-heuristics-loop.md)의 Evaluator
게이트, [04-eval-engineering-methodology.md](04-eval-engineering-methodology.md)의
self-consistency 재채점)에서 이미 "자기 채점을 구조적으로 억제하는"
장치를 요구하면서, 크리스탈 편입 심사 자체(G1)에는 아직 같은 장치를
적용 못하고 있다는 것도 정직하게 남긴다 — 다음 확장 후보.

### 거버넌스·의사결정 — 누가, 언제, 무엇을 결정하는가

| 파일 | 다루는 것 | 검증 강도 |
|---|---|---|
| [02-directive-registry.md](02-directive-registry.md) | 지시·원칙을 우선순위·트리거와 함께 누적 색인하는 방법 | 🟢 |
| [05-autonomous-agent-operating-principles.md](05-autonomous-agent-operating-principles.md) | 자율 실행 AI 에이전트가 언제 멈추고 언제 계속할지 정하는 원칙 | 🟢 |
| [17-ai-risk-management-index.md](17-ai-risk-management-index.md) | 나머지 크리스탈을 NIST AI RMF 4기능(Govern/Map/Measure/Manage)으로 재배열한 색인 | 🟡 기능 이름만 원문 확인, 상세는 재구성 |
| [20-decision-rights-raci.md](20-decision-rights-raci.md) | 여러 사람이 같은 AI 에이전트를 함께 쓸 때의 책임 배분(RACI) | 🟢 |
| [24-application-deadline-rule.md](24-application-deadline-rule.md) | 연구·조사의 응용 아이디어에 마감을 걸어 "언젠가"로 무기한 방치되지 않게 하는 규칙 | 🟢 |
| [25-directive-editing-delegation-levels.md](25-directive-editing-delegation-levels.md) | AI가 지시 문서 자체를 고쳐도 되는지 3단계 위임 수준으로 판정 | 🟢 |

### 품질·검증 — 완성도·기준 판정 — 다 만든 건가, 얼마나 좋은가

크리스탈 7개 도달로 분할한 것(아래 "규모가 커질 때의 원칙" 참고) — 이
축은 "완성/품질의 기준 자체"에 집중한다.

| 파일 | 다루는 것 | 검증 강도 |
|---|---|---|
| [01-definition-of-done.md](01-definition-of-done.md) | "이 작업을 다 만들었다"를 판정하는 10개 기준 | 🟢 |
| [13-debt-and-quality-bar.md](13-debt-and-quality-bar.md) | 부채 분류 체계 + 최소 품질 기준선 5가지 | 🟢 |
| [21-spec-first-implementation.md](21-spec-first-implementation.md) | 명세를 먼저 쓰고 그대로 구현하는 것의 정량적 효과와 경계 | 🟢 두 논문 원문 확인(수치 포함) |

### 품질·검증 — 측정·근거 해석 — 그 판정을 어떻게 재고 믿을 것인가

이 축은 "측정 자체를 어떻게 설계하고, 그 결과를 어떻게 신뢰할지"에 집중한다.

| 파일 | 다루는 것 | 검증 강도 |
|---|---|---|
| [04-eval-engineering-methodology.md](04-eval-engineering-methodology.md) | 산출물 품질을 회귀 없이 검증하는 평가(eval) 설계 파이프라인 + 대상 위험도에 비례한 검증 강도 차등화(risk-tiered verification) | 🟢 |
| [18-determinism-and-reproducibility.md](18-determinism-and-reproducibility.md) | 같은 입력에 답이 달라지는 원인과 대응법 | 🟢 초록 확인(원문 전체는 아님, 문서에 명시) |
| [22-llm-benchmark-literacy.md](22-llm-benchmark-literacy.md) | LLM 벤치마크 수치를 인용받았을 때 신뢰도·오염·절대vs상대를 읽는 법 | 🟢 5개 벤치마크 논문 원문 확인 |
| [34-self-experiment-reporting-standard.md](34-self-experiment-reporting-standard.md) | 정해진 케이스가 없는 자가 실험(가설 검증)을 정성·정량·신뢰도 3요소로 정직하게 보고하는 법 | 🟡 표본크기 원칙은 원문 확인, 신뢰도 마커 체계는 자체 설계 |
| [37-target-metric-gaming-safeguards.md](37-target-metric-gaming-safeguards.md) | 대리 지표를 목표로 삼으면 진짜 목표와의 상관관계가 깨지는 문제(Goodhart's law)와 복수 지표·트립와이어 등 대응법 | 🟢 원문 확인(Amodei et al. 2016 완화 전략 전부, DeepMind 실사례) |

### 안전·보안 — 정보 유출 방어 — 무엇이 새나가는가

크리스탈 7개 도달로 분할한 것(아래 "규모가 커질 때의 원칙" 참고) — 이
축은 "정보가 어떤 경로로 새나가는가"에 집중한다.

| 파일 | 다루는 것 | 검증 강도 |
|---|---|---|
| [07-prompt-guardrails/](07-prompt-guardrails/) | 비밀값·개인정보가 프롬프트/외부로 새나가는 걸 3단으로 막는 실행 가능한 코드(그대로 복사해 쓸 수 있음) | 🟢 실제 라이브 차단 검증까지 완료 |
| [23-confidential-project-protection.md](23-confidential-project-protection.md) | 패턴으로 못 잡는 프로젝트 단위 기밀을 git push 강제로 보호 | 🟢 |
| [31-synthetic-data-memory-isolation.md](31-synthetic-data-memory-isolation.md) | 평가용 합성 입력이 영구 기억 파일에 실제 이력처럼 섞여 들어가는 사고를 막는 법 | 🟡 원본 프로젝트 실제 사고에서 일반화 |
| [32-quasi-identifier-aggregation-risk.md](32-quasi-identifier-aggregation-risk.md) | 개별로는 안전한 정보가 결합되면 재식별·표적 위험이 되는 준식별자 결합 위험과 대응 | 🟡 개념 정의는 원문 확인, Sweeney 원논문 자체는 미대조 |
| [35-personal-oss-employer-confidentiality-separation.md](35-personal-oss-employer-confidentiality-separation.md) | 공개할 의도로 만드는 콘텐츠에 소속 조직의 기밀이 섞이지 않게 스크럽·검토·고지문으로 분리하는 법 | 🟢 영업비밀 일반 정의는 Cornell LII 원문 확인, 실무 절차는 Google 공식 가이드라인 원문 확인 |

### 안전·보안 — 판단·추론 방어 — 무엇이 틀리는가

이 축은 "AI/사람의 판단이나 추론이 어떻게 그럴듯하지만 틀리는가"에 집중한다.

| 파일 | 다루는 것 | 검증 강도 |
|---|---|---|
| [03-epistemic-immunity-catalog.md](03-epistemic-immunity-catalog.md) | AI/사람이 만드는 "그럴듯하지만 가짜인" 추론 12유형과 검증법 | 🟢 |
| [14-ai-red-team-checklist.md](14-ai-red-team-checklist.md) | 적대적 위협(프롬프트 인젝션 등) 방어 체크리스트 | 🟢 |
| [26-grounding-validity-audit.md](26-grounding-validity-audit.md) | 이미 써놓은 가이드 문서의 인용을 주기적으로 원문과 재대조하는 감사 절차 | 🟢 |

### 사고 대응·복원력 — 실패를 어떻게 다루는가

| 파일 | 다루는 것 | 검증 강도 |
|---|---|---|
| [12-blameless-postmortem-template.md](12-blameless-postmortem-template.md) | 블레임리스 포스트모템 표준 템플릿 | 🟢 |
| [19-chaos-engineering-for-agents.md](19-chaos-engineering-for-agents.md) | 우발적 장애를 사고 전에 미리 실험하는 법(레드팀·포스트모템과 축이 다름) | 🟢 |
| [27-premortem-planning.md](27-premortem-planning.md) | 아직 실행 안 한 계획에 미리 실패를 가정해보는 기법(포스트모템의 거울상), 위험 비례 트리거 설계 | 🟢 핵심 메커니즘 원문 확인, 심리학적 계보(1989)는 골격만(🟡) |

### 관측·자가학습 — 실행 결과를 어떻게 남기고 배우는가

| 파일 | 다루는 것 | 검증 강도 |
|---|---|---|
| [06-self-improving-heuristics-loop.md](06-self-improving-heuristics-loop.md) | 에이전트가 "무엇이 통했는지"를 스스로 기록·정리·상한 관리하는 루프 | 🟢 |
| [11-observability-and-agent-tracing.md](11-observability-and-agent-tracing.md) | 에이전트 실행을 주장이 아니라 로그로 남기는 설계 | 🟡 자체 원칙은 확정, 외부 표준(OpenTelemetry) 세부는 미검증 명시 |
| [29-agent-cost-and-budget-management.md](29-agent-cost-and-budget-management.md) | 토큰/API 호출 비용·한도를 다루는 법(프롬프트 캐싱 경제성, 한도 신호 구분, 병렬 배치 낭비 방지) | 🟢 캐싱 메커니즘은 공식 API 문서 원문 확인, 나머지는 실전 운영 패턴 일반화 |
| [30-shared-context-lifecycle-management.md](30-shared-context-lifecycle-management.md) | 여러 세션에 걸쳐 자라는 공유 컨텍스트 파일을 압축·아카이빙·검색으로 관리하고 세션 재시작 시 동등한 수준으로 복구하는 법 | 🟢 핵심 메커니즘은 MemGPT·Anthropic 공식 문서 원문 확인 |

### 상호작용·문서화 — 사람에게 무엇을 어떻게 보여주는가

| 파일 | 다루는 것 | 검증 강도 |
|---|---|---|
| [10-human-ai-interaction-guidelines.md](10-human-ai-interaction-guidelines.md) | 사람-AI 상호작용 18개 원칙(Amershi et al. 2019) 체크리스트 | 🟢 |
| [15-model-card-template.md](15-model-card-template.md) | AI 기능 자체를 문서화하는 9섹션 템플릿(Mitchell et al. 2019) | 🟢 |
| [16-context-engineering-principles.md](16-context-engineering-principles.md) | 에이전트 컨텍스트 윈도우 설계 5원칙(Anthropic) | 🟢 |
| [28-writing-craft-guardrails.md](28-writing-craft-guardrails.md) | 산출물 텍스트의 "AI 티"를 제거하는 자가진단·체크리스트(Orwell/Graham/Strunk&White/Zinsser/Vonnegut/Kawasaki) | 🟢 |

### 구조·재사용 — 프로젝트/기능을 어떻게 조립하고 옮기는가

| 파일 | 다루는 것 | 검증 강도 |
|---|---|---|
| [08-module-format.md](08-module-format.md) | 개별 기능을 다른 프로젝트로 즉시 옮길 수 있는 패키징 규약 | 🟢 |
| [09-project-structure-template.md](09-project-structure-template.md) | AI-에이전트-관리형 프로젝트의 5레이어 구조 + 13단계 재구축 순서 | 🟢 |
| [33-sandboxed-harness-duplication-sync.md](33-sandboxed-harness-duplication-sync.md) | 로컬 import가 안 되는 실행 환경에서 검증된 로직을 정직하게 중복하고 기계적으로 대조하는 법 | 🟢 |
| [36-execution-mode-escalation-ladder.md](36-execution-mode-escalation-ladder.md) | 단일 세션→서브에이전트→파이프라인→분리 실행까지, 신호 기반으로 병렬화 수준을 올리는 4단계 사다리 | 🟡 원본 프로젝트 내 반복 검증(eval 통과 기록), 외부 대조는 없음 |

## 규모가 커질 때의 원칙

크리스탈 20개를 넘어서면서, [06-self-improving-heuristics-loop.md](06-self-improving-heuristics-loop.md)가
자가학습 규칙에 적용하는 "메모리 상한" 원칙을 이 폴더 자신에게도 적용해야
하는 시점이 온다 — 무한정 추가하는 것은
[16-context-engineering-principles.md](16-context-engineering-principles.md)의
"가능한 가장 작은 고신호 토큰 집합" 원칙과 충돌한다. **다음 확장 후보를
검토할 때는 매번**: (1) 기존 크리스탈과 실제로 겹치지 않는지, (2)
검증 가능한 1차 자료가 있는지, (3) 이 표의 카테고리 중 어디에도 안
맞으면 카테고리 자체를 새로 만들지 아니면 범위 밖인지부터 판단한다.
카테고리 하나에 크리스탈이 6~7개를 넘으면 그 카테고리를 다시 쪼개는
시점이다. **품질·검증과 안전·보안은 이미 두 축으로 나눠 표를 구성했다**
— 번호는 그대로 두고 표의 소속만 나눈 것이다([BLUEPRINT.md](BLUEPRINT.md)
5절의 분할 규칙). 품질·검증은 "완성도 판정"(01·13·21, 3개) 대 "측정·근거
해석"(04·18·22·34·37, 5개)으로, 안전·보안은 "정보 유출 방어"(07·23·31·32·35,
5개) 대 "판단·추론 방어"(03·14·26, 3개)로 나뉜다 — 둘 다 각 축이 아직
6~7개 미만이라 추가 분할은 필요 없다. **거버넌스·의사결정 카테고리는
아직 안 나뉜 채 6개(02·05·17·20·24·25)로 경계에 도달했다** — 다음에
이 카테고리에 추가할 후보가 생기면, 추가 전에 먼저 쪼갤지부터
판단한다(예: "지식/지시 자체의 거버넌스" 대 "실행 자율성의 거버넌스").

## 사용법 · 설계도 · 리스크 분석

- [BLUEPRINT.md](BLUEPRINT.md) — 이 폴더 자신은 무엇이고, 새 크리스탈이
  어떤 기준(편입 게이트)으로 들어오며, 그 편입 후보가 어떻게 자동으로
  발견되는지.
- [USAGE-GUIDE.md](USAGE-GUIDE.md) — 새 프로젝트에 이 프레임워크를 도입할 때
  기획·설계·구현·개선·참조 다섯 관점에서 무엇을 어떻게 쓰는지.
- [REFLECTION-CANDIDATES.md](REFLECTION-CANDIDATES.md) — 다른 프로젝트의
  고도화 중 이 폴더에 반영할 만한 패턴을 자동으로 찾아 누적한 후보 목록
  (`scripts/agent-ops-framework-reflection-check.py` 산출물).
- [RISK-ANALYSIS.md](RISK-ANALYSIS.md) — 이 폴더가 유래한 원본 프로젝트를
  기준으로, 오픈소스로 공개했을 때의 실제 리스크를 분석한 문서. **이 문서만
  예외적으로 원본 프로젝트에 특정된 서술을 담는다** — 다른 프로젝트로
  그대로 옮길 크리스탈이 아니라, "이 특정 사례에서 공개해도 되는지"를
  판단하는 부속 문서이기 때문이다.
- [DISCLAIMER.md](DISCLAIMER.md) — 실제 공개 시 그대로 붙여 쓰는 고지문
  템플릿. 번호 매긴 크리스탈에 안 넣은 이유: 이건 배우는 방법론이 아니라
  바로 게시할 산출물이라 따로 찾을 수 있어야 한다([35](35-personal-oss-employer-confidentiality-separation.md)가
  그 방법론).
- [LANGUAGE-POLICY.md](LANGUAGE-POLICY.md) — AI가 한국어(SSOT)/영문 번역
  중 무엇을 읽을지 정하는 실행 시점 설정(기본값·티어·예외).
- [GLOSSARY.md](GLOSSARY.md) — 이 폴더가 반복해서 쓰는 용어(크리스탈,
  서사, 도메인 지식/무관, SSOT, 게이트, STALE/DIVERGED 등)의 정의를
  한곳에 모은 색인.

## 이 폴더가 아닌 것

- 원본 프로젝트의 도메인 콘텐츠를 대체하지 않는다 — 그건 여전히 그
  프로젝트의 실제 활용 결과물이다.
- 완전히 새로 검증된 별도 프로젝트가 아니다 — 원본 문서가 원본 프로젝트
  안에서 거쳐온 실전 검증(실패 발견, 재발 방지 조치)의 **기록을 요약**한
  것이지, 이 폴더 자체를 독립적으로 다시 검증한 건 아니다
  ([08-module-format.md](08-module-format.md)의 "검증 표시는 정직하게"
  원칙과 동일하게 적용).
- `modules/`류(개별 기능 하나를 떼어내는 패키징)와는 스코프가 다르다 —
  이 폴더는 **기능 하나가 아니라 프로젝트 전체의 운영 방식**을 떼어낸다.
