# 의사결정권 배분 — 여러 사람이 같은 AI 에이전트를 함께 쓸 때

> 🌐 **[Read in English](../en/20-decision-rights-raci.md)**

**버전**: 1.0.1
**콘텐츠 해시**: sha256:f8a8aaf76785 (본문 기준, 이 두 줄 제외)

지금까지의 크리스탈, 특히 [05-autonomous-agent-operating-principles.md](05-autonomous-agent-operating-principles.md)는
"**AI가 언제** 사람 확인 없이 행동해도 되는가"를 다뤘다. 이 크리스탈은
다른 축이다 — 그 결과물을 놓고 **여러 사람 중 누가 무슨 권한을 갖는가**.
1인 프로젝트에는 필요 없지만, 팀이 같은 AI 에이전트 도구를 함께 쓰기
시작하는 순간부터 필요해진다.

## 근거 (1차 자료 확인)

🟢 RACI 매트릭스(Responsibility Assignment Matrix) — 위키백과 및 PMBOK
Guide(5판, 2013) 원문 확인. 4개 역할:

- **R (Responsible, 실무 수행자)**: 실제로 작업을 완료하는 사람(여러 명
  가능).
- **A (Accountable, 최종 책임자)**: 산출물이 올바르게 완료됐는지 **최종
  답변할 책임이 있는 사람** — 작업을 승인하고 위임한다. **핵심 규칙**:
  "각 작업/산출물마다 Accountable은 정확히 한 명이어야 한다."
- **C (Consulted, 자문 대상)**: 의견을 구하는 대상(주로 전문가), 양방향
  소통.
- **I (Informed, 통보 대상)**: 진행 상황을 계속 안내받는 사람, 일방향
  소통(대개 완료 시점에만 통보).

프로젝트 관리 협회(PMI)가 인정하는 표준 기법이고, 부서 간 협업에서 역할과
책임을 정의하는 데 널리 쓰인다.

## AI 에이전트가 결과물을 만들 때 RACI를 적용하는 법

AI 에이전트가 R(실무 수행자) 역할을 대신하는 경우가 많아지면서, 나머지
세 역할(A/C/I)이 **사람들 사이에서** 어떻게 배분되는지가 오히려 더
중요해진다 — AI가 다 했다고 해서 "누가 책임지는가"라는 질문이 사라지지
않는다.

| 역할 | AI 에이전트 도입 후 누가 맡는가 |
|---|---|
| **R** | AI 에이전트(실제 산출물 생성) — 단, 사람이 R을 겸할 수도 있다(AI 산출물을 사람이 다시 다듬는 경우) |
| **A** | **반드시 사람 한 명** — AI는 Accountable이 될 수 없다. "AI가 그렇게 만들었다"는 최종 책임을 대신하지 않는다. 이 프레임워크의 [05](05-autonomous-agent-operating-principles.md) 0번째 원칙("비가역적 행동은 여전히 먼저 묻는다")이 사실상 "A는 항상 사람"이라는 이 규칙의 구체적 적용이다 |
| **C** | 도메인 전문가(법률·의료·재무 등 전문 조언이 필요한 산출물) — [01-definition-of-done.md](01-definition-of-done.md) 4번째 항목(전문 조언 면책)이 걸리는 영역은 실제 전문가를 C로 넣는 걸 고려한다 |
| **I** | 산출물의 영향을 받는 나머지 이해관계자 |

## 왜 "A는 항상 사람"이 협상 불가능한 규칙인가

RACI의 핵심 규칙("Accountable은 정확히 한 명")을 AI 에이전트에 적용할 때
생기는 가장 흔한 실패는 **"AI가 담당"이라고 암묵적으로 방치하는 것**이다
— 명시적으로 배정하지 않으면 사고가 났을 때 "누구도 최종 책임지지
않았다"는 상태가 된다.
[12-blameless-postmortem-template.md](12-blameless-postmortem-template.md)의
"AI가 실수했다로 끝내지 않는다"는 규칙이 바로 이 문제의 사후 대응
버전이다 — RACI는 그 문제를 **사전에** 구조로 막는다.

## 이 크리스탈과 05·10번의 차이 — 축이 다르다

| | 묻는 질문 | 적용 시점 |
|---|---|---|
| [05-autonomous-agent-operating-principles.md](05-autonomous-agent-operating-principles.md) | AI가 **언제** 사람 확인 없이 행동해도 되는가(시간/게이팅 축) | 실행 전 자동/수동 판단 |
| [10-human-ai-interaction-guidelines.md](10-human-ai-interaction-guidelines.md) G10 | 불확실할 때 AI가 서비스 **범위**를 어떻게 좁히는가(AI 자신의 행동 축) | AI가 응답을 생성하는 순간 |
| **이 크리스탈(20)** | 그 결과물을 놓고 **사람들 사이에서** 누가 책임·자문·통보 대상인가(조직 축) | 프로젝트/팀 구조 설계 시점 |

세 크리스탈이 "AI 산출물을 둘러싼 권한과 책임"이라는 같은 주제를 다루지만,
05·10은 **AI 대 사람** 경계를, 이 크리스탈은 **사람 대 사람** 경계를
다룬다는 점에서 겹치지 않는다.

## 1인 프로젝트에서 팀 프로젝트로 확장할 때

1인 프로젝트([09-project-structure-template.md](09-project-structure-template.md)가
전제하는 기본 구조)는 암묵적으로 그 한 사람이 모든 작업에서 R이자 A다 —
RACI를 명시할 필요가 낮다. 두 명 이상이 같은 에이전트 설정·거버넌스
문서·공유 컨텍스트를 함께 쓰기 시작하는 순간부터 이 크리스탈이 필요해진다
— 특히 [02-directive-registry.md](02-directive-registry.md)(누가 이
지시를 확정할 권한이 있는가)와 [07-prompt-guardrails/](07-prompt-guardrails/)
설정 변경(누가 가드레일 규칙을 완화할 권한이 있는가) 같은, 여러 사람이
동시에 건드릴 수 있는 공유 자원에 A를 명시적으로 배정하는 것부터
시작한다.

## 관련 크리스탈
- [05-autonomous-agent-operating-principles.md](05-autonomous-agent-operating-principles.md) —
  "A는 항상 사람"의 근거가 되는 0번째 원칙.
- [12-blameless-postmortem-template.md](12-blameless-postmortem-template.md) —
  A가 불분명했을 때 실제로 나는 사고의 사후 대응.
