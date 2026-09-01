# 사용 가이드 — 기획·설계·구현·개선·참조 다섯 관점

> 🌐 **[Read in English](../en/USAGE-GUIDE.md)**

이 프레임워크(`agent-ops-framework/`)를 새 프로젝트에 도입할 때, 다섯 관점 각각
무엇을 어떻게 쓰는지 정리한다. 순서대로 읽을 필요는 없다 — 지금 어느
단계에 있는지에 따라 해당 절만 봐도 된다.

## 기획(Planning) 관점 — "이걸 왜, 언제 도입하나"

**언제 도입할 가치가 생기는가**: AI 에이전트(Claude Code 등)가 한 사람의
여러 작업을 여러 세션에 걸쳐 반복 관리하기 시작하는 순간부터다. 1회성
질문-답변에는 이 프레임워크 전체가 과하다 — [09-project-structure-template.md](09-project-structure-template.md)
4절의 "13단계 재구축 순서"가 정확히 "언제 뭐가 필요해지는가"의 타임라인
역할을 한다.

**최소 시작점**: 전부 한 번에 들여올 필요 없다. 우선순위:
1. [07-prompt-guardrails/](07-prompt-guardrails/) — 개인정보를 다루는
   작업이 하나라도 생기기 **전에** 반드시 먼저 설치한다(사후 추가는 이미
   노출된 걸 지우는 훨씬 비싼 작업이 된다).
2. [01-definition-of-done.md](01-definition-of-done.md) — 작업이 3~5개를
   넘어가는 시점.
3. [02-directive-registry.md](02-directive-registry.md) — 사용자 지시가
   반복적으로 재확인이 필요해지는 시점.
4. 나머지(04·05·06·08·09)는 각 문서 서두의 "왜 필요한가"가 실제로 자기
   프로젝트에 해당될 때.

**의사결정 근거**: "이 기능이 있으면 좋겠다"가 아니라 "이 부채/문제가
실제로 발생했다"가 도입 트리거여야 한다 — [05-autonomous-agent-operating-principles.md](05-autonomous-agent-operating-principles.md)의
"최종 수혜자는 사용자다" 원칙과 같은 정신: 거버넌스 인프라 자체가 목적이
되지 않게 한다.

## 설계(Design) 관점 — "이걸 내 프로젝트 구조에 어떻게 맞추나"

**스키마를 그대로 가져오고 값만 바꾼다**: [09-project-structure-template.md](09-project-structure-template.md)
3.1~3.4절의 메타데이터 필드(감독등급, 확신도등급, 도메인 등)는 이름과
값 집합을 그대로 써도 대부분 맞는다 — 새로 설계하지 말고 먼저 그대로
써보고, 실제로 안 맞는 부분만 조정한다("이미 있는 표준을 확인 안 하고
임의로 이름 붙이면 나중에 리네이밍 비용이 든다"는 교훈이 원본 프로젝트에도
있다).

**어느 것부터 5레이어에 매핑할지**: 이미 프로젝트가 있다면, 기존 폴더
구조를 5레이어([09](09-project-structure-template.md) 1절)에 강제로
맞추지 않는다 — 대신 "지금 이 프로젝트에 이 레이어에 해당하는 게 있는가?
없다면 그게 실제로 필요한가?"를 먼저 묻는다. 예: 제품 레이어(사용자에게
보여줄 완성된 산출물)가 아직 없어도 된다 — 작업 레이어와 거버넌스 레이어만
있어도 프로젝트는 정상 작동한다.

**가드레일은 설치 즉시 실사격 검증한다**: [07-prompt-guardrails/README.md](07-prompt-guardrails/README.md)의
"설치" 절 4단계(더미 민감 파일로 실제 차단 확인)를 생략하지 않는다 —
설정 파일이 문법적으로 맞다고 실제로 작동한다는 보장은 아니다.

## 구현(Implementation) 관점 — "실제로 뭘 복사·수정하나"

| 크리스탈 | 그대로 복사 가능? | 수정해야 할 것 |
|---|---|---|
| [07-prompt-guardrails/](07-prompt-guardrails/) | 거의 그대로(코드) | `settings.json`의 경로 예시, 훅의 matcher 이름 |
| [01](01-definition-of-done.md)·[02](02-directive-registry.md)·[03](03-epistemic-immunity-catalog.md)·[04](04-eval-engineering-methodology.md)·[05](05-autonomous-agent-operating-principles.md)·[06](06-self-improving-heuristics-loop.md) | 원칙/방법론(문서) | 그대로 채택 가능 — "왜"는 범용적이다. 실제 사례 절만 자기 프로젝트 사례로 채워나간다 |
| [08](08-module-format.md) | 규약(문서) | 대상 프로젝트의 실행 파일 형식에 맞춰 확장자·경로만 조정 |
| [09](09-project-structure-template.md) | 템플릿(문서+스키마) | 실제 폴더 이름을 이 프로젝트의 명명 규칙에 맞춘다 |

**구현 순서**: 기획 관점의 "최소 시작점" 순서를 그대로 따른다. 한 번에
9개 문서를 전부 설치하고 시작하지 않는다 — 그 자체가 "너무 이른 인프라"
([09](09-project-structure-template.md) 4절 13번 경고)가 된다.

**검증 없이 완료 처리하지 않는다**: 복사만 하고 실제로 그 프로젝트에서
한 번도 안 써봤다면 "도입했다"고 부르지 않는다 — 예를 들어
[07-prompt-guardrails/](07-prompt-guardrails/)는 실제 발행/커밋 시도로
차단이 작동하는지 라이브 확인이 설치의 일부다.

## 개선(Improvement) 관점 — "이걸 자기 프로젝트에 맞게 어떻게 키우나"

각 크리스탈은 **정적 템플릿이 아니라 자라는 문서**로 설계됐다:

- [03-epistemic-immunity-catalog.md](03-epistemic-immunity-catalog.md)와
  [06-self-improving-heuristics-loop.md](06-self-improving-heuristics-loop.md)는
  명시적으로 "실제 프로젝트에서 발견된 사례로 성장시켜라"는 지침을 담고
  있다 — 추상적 원리만 두지 말고, 이식 후 첫 실제 실패/발견이 생기면
  즉시 그 프로젝트만의 사례를 추가한다.
- [02-directive-registry.md](02-directive-registry.md)는 새 프로젝트에서
  1번 행부터 그 프로젝트의 실제 지시로 채우기 시작하면 된다.
- [07-prompt-guardrails/](07-prompt-guardrails/)의 `PATTERNS`/`check(...)`
  목록은 그 프로젝트에서 흔한 민감정보 패턴(사내 토큰 형식 등)이 발견되면
  즉시 추가한다.

**비대화 방지**를 함께 챙긴다 — [02](02-directive-registry.md)와
[06](06-self-improving-heuristics-loop.md)은 각각 "비대화 방지" 절과
"메모리 상한" 절을 갖고 있다. 문서가 자라기만 하고 정리되지 않으면, 원본
프로젝트가 실제로 겪은 것과 같은 인지부채 문제를 반복한다.

## 참조(Reference) 관점 — "빠르게 뭘 찾아봐야 하나"

| 지금 겪는 상황 | 참고할 크리스탈 |
|---|---|
| "이 작업, 다 만든 건가?" | [01-definition-of-done.md](01-definition-of-done.md) |
| "이거 이미 정한 원칙 아니었나?" | [02-directive-registry.md](02-directive-registry.md) |
| "이 주장, 너무 그럴듯한데 의심스럽다" | [03-epistemic-immunity-catalog.md](03-epistemic-immunity-catalog.md) |
| "이 산출물 품질을 어떻게 검증하지?" | [04-eval-engineering-methodology.md](04-eval-engineering-methodology.md) |
| "모든 대상에 같은 검증 비용을 쓰는 게 비효율 같다" | [04-eval-engineering-methodology.md](04-eval-engineering-methodology.md)의 "검증 강도를 대상 위험도에 비례시킨다" |
| "지금 이 자동 실행, 사람 확인 없이 진행해도 되나?" | [05-autonomous-agent-operating-principles.md](05-autonomous-agent-operating-principles.md) |
| "자동 루프가 자꾸 스스로 멈춘다 / 재예약 간격을 어떻게 정해야 하나" | [05-autonomous-agent-operating-principles.md](05-autonomous-agent-operating-principles.md)의 "자기재예약 백스톱"·"예약 간격 자동 조정" |
| "장시간 실행 중인 에이전트가 목표에서 벗어나거나 근거 없는 주장을 계속 쌓고 있는 것 같다, 실시간으로 멈추게 하고 싶다" | [05-autonomous-agent-operating-principles.md](05-autonomous-agent-operating-principles.md)의 "정지 트리거를 인식론적 신호로도 확장" |
| "이 실패, 다음에 또 반복 안 하려면?" | [06-self-improving-heuristics-loop.md](06-self-improving-heuristics-loop.md) |
| "비밀값/개인정보가 새나가는 걸 막고 싶다" | [07-prompt-guardrails/](07-prompt-guardrails/) |
| "이 기능을 다른 프로젝트로 옮기고 싶다" | [08-module-format.md](08-module-format.md) |
| "프로젝트 전체를 어떻게 구조화하지?" | [09-project-structure-template.md](09-project-structure-template.md) |
| "사용자 경험 관점에서 이 기능이 놓친 게 있나?" | [10-human-ai-interaction-guidelines.md](10-human-ai-interaction-guidelines.md) |
| "AI가 '완료했다'는 말을 믿을 수 있는 근거가 있나?" | [11-observability-and-agent-tracing.md](11-observability-and-agent-tracing.md) |
| "이 사고, 어떻게 기록해야 재발을 막나?" | [12-blameless-postmortem-template.md](12-blameless-postmortem-template.md) |
| "지금 부채가 얼마나 쌓였고, 서비스로 내놔도 되는 수준인가?" | [13-debt-and-quality-bar.md](13-debt-and-quality-bar.md) |
| "누가 일부러 이 시스템을 공격하려 하면 어디가 뚫리나?" | [14-ai-red-team-checklist.md](14-ai-red-team-checklist.md) |
| "이 AI 기능이 정확히 뭘 하고 뭘 안 하는지 문서로 남기고 싶다" | [15-model-card-template.md](15-model-card-template.md) |
| "에이전트 컨텍스트 윈도우에 뭘 넣을지 헷갈린다" | [16-context-engineering-principles.md](16-context-engineering-principles.md) |
| "공유 문서가 임계값을 넘었는데, 압축해도 되는 문서인지 먼저 판단하고 싶다" | [16-context-engineering-principles.md](16-context-engineering-principles.md)의 "압축 전에 먼저" |
| "지금 우리 프로젝트가 리스크 관리의 어느 기능이 비어있는지 한눈에 보고 싶다" | [17-ai-risk-management-index.md](17-ai-risk-management-index.md) |
| "방금 됐던 게 왜 지금은 안 되지?" | [18-determinism-and-reproducibility.md](18-determinism-and-reproducibility.md) |
| "실제 사고가 나기 전에 일부러 고장내보고 싶다" | [19-chaos-engineering-for-agents.md](19-chaos-engineering-for-agents.md) |
| "우리 팀이 같이 이 AI 에이전트를 쓰는데, 결과물 책임은 누가 지나?" | [20-decision-rights-raci.md](20-decision-rights-raci.md) |
| "AI에게 기획/설계부터 시키는 게 실제로 효과가 있나?" | [21-spec-first-implementation.md](21-spec-first-implementation.md) |
| "이 벤치마크 수치, 얼마나 믿어도 되나?" | [22-llm-benchmark-literacy.md](22-llm-benchmark-literacy.md) |
| "개인정보 패턴은 없는데 이 프로젝트/폴더 전체가 공개되면 안 된다" | [23-confidential-project-protection.md](23-confidential-project-protection.md) |
| "조사 아이디어가 계속 쌓이기만 하고 실제 적용은 안 된다" | [24-application-deadline-rule.md](24-application-deadline-rule.md) |
| "AI가 지시 문서 자체를 고쳐도 되나? 어디까지?" | [25-directive-editing-delegation-levels.md](25-directive-editing-delegation-levels.md) |
| "예전에 써둔 가이드 문서의 근거가 지금도 맞는지 확인하고 싶다" | [26-grounding-validity-audit.md](26-grounding-validity-audit.md) |
| "이 계획을 실행하기 전에, 낙관 없이 뭐가 잘못될 수 있는지 미리 짚고 싶다" | [27-premortem-planning.md](27-premortem-planning.md) |
| "이 산출물, 사실은 맞는데 읽는 맛이 없다 — AI 티가 난다" | [28-writing-craft-guardrails.md](28-writing-craft-guardrails.md) |
| "토큰/API 비용이 갑자기 치솟았다, 한도 에러를 어떻게 다뤄야 하나" | [29-agent-cost-and-budget-management.md](29-agent-cost-and-budget-management.md) |
| "공유 컨텍스트 파일이 계속 커지는데, 압축했다가 다음 세션이 못 따라잡을까 걱정된다" | [30-shared-context-lifecycle-management.md](30-shared-context-lifecycle-management.md) |
| "새 세션이 '이어서 진행해'로 시작했는데 이전 세션 수준으로 못 따라간다" | [30-shared-context-lifecycle-management.md](30-shared-context-lifecycle-management.md)의 "세션 시작 시 고정 순서 부트스트랩" |
| "평가(eval) 테스트가 실제 사용자 이력 파일에 가짜 기록을 남긴 것 같다" | [31-synthetic-data-memory-isolation.md](31-synthetic-data-memory-isolation.md) |
| "각 항목은 개인정보 스캐너에 안 걸리는데 문서 전체로 보면 특정 개인이 좁혀질 것 같다" | [32-quasi-identifier-aggregation-risk.md](32-quasi-identifier-aggregation-risk.md) |
| "이 실행 환경이 로컬 import를 막아서 같은 로직을 여러 파일에 복사해야 하는데, 드리프트가 걱정된다" | [33-sandboxed-harness-duplication-sync.md](33-sandboxed-harness-duplication-sync.md) |
| "개인 프로젝트를 오픈소스로 공개하려는데 소속 조직의 기밀이 섞여 있을까 걱정된다" | [35-personal-oss-employer-confidentiality-separation.md](35-personal-oss-employer-confidentiality-separation.md) |
| "정해진 케이스가 없는 즉흥 실험 결과를 어떻게 정직하게 보고해야 하나" | [34-self-experiment-reporting-standard.md](34-self-experiment-reporting-standard.md) |
| "지금 이 작업을 혼자 순차로 할지, 병렬화/분리 실행으로 올릴지 매번 감으로 정하고 있다" | [36-execution-mode-escalation-ladder.md](36-execution-mode-escalation-ladder.md) |
| "새 크리스탈을 추가하고 싶은데 기준을 모르겠다 / 다른 프로젝트 고도화를 어떻게 이 폴더에 반영하나?" | [BLUEPRINT.md](BLUEPRINT.md) |

## 관련 문서

- [README.md](README.md) — 이 폴더 전체 개요
- [RISK-ANALYSIS.md](RISK-ANALYSIS.md) — 오픈소스 공개 시 리스크 분석
