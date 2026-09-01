# AI 리스크 관리 4기능 색인 — NIST AI RMF 골격으로 나머지 크리스탈 재배열

> 🌐 **[Read in English](../en/17-ai-risk-management-index.md)**

**버전**: 1.1.0
**콘텐츠 해시**: sha256:5556dcd96d16 (본문 기준, 이 두 줄 제외)

이 크리스탈은 새 내용을 추가하지 않는다 — 대신 다른 크리스탈들이
**국제적으로 통용되는 리스크 관리 골격 안에서 각각 어디에 해당하는지**
재배열한 색인이다. 개별 문서를 각자 참고하는 대신, "지금 우리 프로젝트가
이 4가지 기능 중 어디가 비어있는가"를 한눈에 보기 위한 것이다.

**이 색인의 범위**: 아래 4기능에 실제로 배치된 크리스탈만 이 색인의
대상이다 — 전체 크리스탈 목록(README.md)의 부분집합이지 전수가 아니다.
NIST AI RMF는 리스크 관리에 초점을 둔 골격이라, 구조·재사용·문서화
축([08-module-format.md](08-module-format.md), [09-project-structure-
template.md](09-project-structure-template.md), [16-context-engineering-
principles.md](16-context-engineering-principles.md), [28-writing-craft-
guardrails.md](28-writing-craft-guardrails.md), [30-shared-context-
lifecycle-management.md](30-shared-context-lifecycle-management.md),
[33-sandboxed-harness-duplication-sync.md](33-sandboxed-harness-duplication-sync.md))처럼
리스크 관리 기능으로 억지로 분류하면 오히려 왜곡되는 크리스탈은 의도적으로
색인 밖에 둔다. [01-definition-of-done.md](01-definition-of-done.md)도
같은 이유로 밖에 둔다 — 아래 "이 4기능 색인을 쓰는 법"이 이미 그 이유를
설명한다("완성됐는가" 대 "안전하게 완성됐는가"는 다른 축). [24-application-
deadline-rule.md](24-application-deadline-rule.md)도 조사·적용 습관에
관한 것이라 리스크 관리 기능이 아니므로 밖에 둔다. **이 범위 밖 목록
자체도 크리스탈이 늘어나면 다시 확인해야 한다** — 아래 "이 크리스탈
자체의 한계"에 그 재확인 규칙을 명시한다.

## 근거 (1차 자료 확인 — 정직하게 밝힘)

🟢 **검증된 것**: NIST(미국 국립표준기술연구소)의 AI Risk Management
Framework(AI RMF 1.0)가 4개 핵심 기능 — **Govern(거버넌스), Map(맵핑),
Measure(측정), Manage(관리)** — 로 구성된다는 것은 nist.gov 공식 페이지
원문에서 직접 확인했다.

⚪ **검증 못한 것**: 각 기능의 NIST 공식 상세 정의는 이 문서 작성 시점의 도구
접근 범위 안에서 원문을 열람하지 못했다(문서 페이지 이동/404). 아래
"이 문서의 해석"은 **NIST의 공식 문구가 아니라, 4개 기능 이름과 통상적으로
알려진 AI 리스크 관리 실무 관행을 참고해 이 문서가 재구성한 것**이다 —
NIST를 인용하는 것처럼 보이지 않게, 아래 절 제목에 "이 문서의 해석"이라고
명시한다.

## 이 문서의 해석 — 4기능에 대응하는 실무 질문과 관련 크리스탈

### Govern — "이 결정을 누가, 어떤 권한으로 내리는가"
실무 질문: 자율 실행의 범위는 누가 정하는가? 비가역적 행동은 누가 승인
하는가? 조직 차원의 정책이 있는가?

관련 크리스탈: [05-autonomous-agent-operating-principles.md](05-autonomous-agent-operating-principles.md)
(0번째 원칙, unknown-unknowns 게이팅), [RISK-ANALYSIS.md](RISK-ANALYSIS.md)
(이 프레임워크 자체를 공개할지 결정하는 과정도 거버넌스의 실전 사례),
[10-human-ai-interaction-guidelines.md](10-human-ai-interaction-guidelines.md)
G17(전역 제어 제공), [02-directive-registry.md](02-directive-registry.md)
(결정·지시 자체를 우선순위·재적용 트리거와 함께 색인), [20-decision-rights-
raci.md](20-decision-rights-raci.md)(여러 사람이 같은 에이전트를 공유할 때
누가 승인·검토·실행 권한을 갖는지), [25-directive-editing-delegation-
levels.md](25-directive-editing-delegation-levels.md)(AI가 지시 문서 자체를
얼마나 고쳐도 되는지의 위임 수준), [36-execution-mode-escalation-
ladder.md](36-execution-mode-escalation-ladder.md)(실행 병렬화 수준을
올릴 권한을 신호 기반으로 정하는 것도 자율 범위 거버넌스의 한 형태).

### Map — "이 시스템이 어떤 상황에서 어떤 방식으로 실패할 수 있는가"
실무 질문: 이 기능이 다루는 위협 표면은 무엇인가? 어떤 입력이 시스템을
오작동시킬 수 있는가? 의도된 사용과 의도되지 않은 사용의 경계는 어디인가?

관련 크리스탈: [14-ai-red-team-checklist.md](14-ai-red-team-checklist.md)
(OWASP LLM Top 10 기반 위협 모델링), [15-model-card-template.md](15-model-card-template.md)
(Intended Use — 의도되지 않은 사용을 명시), [03-epistemic-immunity-catalog.md](03-epistemic-immunity-catalog.md)
(AI가 실패하는 12가지 패턴 지도), [19-chaos-engineering-for-agents.md](19-chaos-engineering-for-agents.md)
(실제 사고 전에 일부러 고장내며 실패 표면을 능동적으로 찾음), [27-premortem-
planning.md](27-premortem-planning.md)(실행 전에 낙관 없이 실패를 미리
가정), [32-quasi-identifier-aggregation-risk.md](32-quasi-identifier-aggregation-risk.md)
(개별로는 안전한 정보가 조합되면 재식별 위협 표면이 되는 패턴).

### Measure — "실제로 얼마나 잘 작동하는지 어떻게 아는가"
실무 질문: 통과 기준은 무엇인가? 실제로 측정했는가, 아니면 그럴듯하다고
가정만 했는가? 측정이 하위집단별로도 유효한가?

관련 크리스탈: [04-eval-engineering-methodology.md](04-eval-engineering-methodology.md)
(9단계 검증 파이프라인), [11-observability-and-agent-tracing.md](11-observability-and-agent-tracing.md)
(주장이 아니라 로그로), [15-model-card-template.md](15-model-card-template.md)
(Metrics/Quantitative Analyses), [18-determinism-and-reproducibility.md](18-determinism-and-reproducibility.md)
(같은 입력이 다른 답을 낼 때 그 측정 자체를 얼마나 믿을 수 있는지),
[21-spec-first-implementation.md](21-spec-first-implementation.md)(명세를
먼저 쓰는 관행의 효과를 정량으로 측정), [22-llm-benchmark-literacy.md](22-llm-benchmark-literacy.md)
(벤치마크 수치의 신뢰도·오염·절대vs상대를 읽는 법), [26-grounding-validity-
audit.md](26-grounding-validity-audit.md)(이미 써놓은 근거가 지금도
맞는지 주기적으로 재대조), [34-self-experiment-reporting-standard.md](34-self-experiment-reporting-standard.md)
(정해진 케이스가 없는 자가 실험 결과를 정직하게 측정·보고).

### Manage — "발견된 리스크를 실제로 어떻게 줄이는가"
실무 질문: 발견된 취약점·부채를 어떤 순서로 처리하는가? 재발을 어떻게
막는가? 사고가 나면 어떻게 학습으로 전환하는가?

관련 크리스탈: [13-debt-and-quality-bar.md](13-debt-and-quality-bar.md)
(부채 상환 우선순위), [12-blameless-postmortem-template.md](12-blameless-postmortem-template.md)
(사고를 재발방지 조치로 전환), [06-self-improving-heuristics-loop.md](06-self-improving-heuristics-loop.md)
(학습된 교훈을 다음 실행에 반영), [07-prompt-guardrails/](07-prompt-guardrails/)
(정보 유출 리스크를 실행 가능한 코드로 실제로 낮춤), [23-confidential-
project-protection.md](23-confidential-project-protection.md)(패턴으로
못 잡는 프로젝트 단위 기밀을 git push 강제로 관리), [29-agent-cost-and-
budget-management.md](29-agent-cost-and-budget-management.md)(토큰/비용
폭주라는 리스크를 한도 신호 구분·캐싱으로 관리), [31-synthetic-data-
memory-isolation.md](31-synthetic-data-memory-isolation.md)(평가용 합성
데이터가 영구 기억에 오염되는 특정 리스크에 대한 예방 절차), [35-personal-
oss-employer-confidentiality-separation.md](35-personal-oss-employer-confidentiality-separation.md)
(공개 의도 콘텐츠에 소속 조직 기밀이 섞이는 리스크를 스크럽·검토·고지문
절차로 관리 — Govern에 인용된 RISK-ANALYSIS.md의 공개-결정 자체가 아니라,
그 결정을 실행하는 구체적 완화 절차).

## 이 4기능 색인을 쓰는 법

새 AI 에이전트 기능을 만들 때, 완성 여부를 4기능 각각에 한 줄로
자문한다:
- [ ] **Govern**: 이 기능의 자율 실행 범위를 누가 정했고, 어디에 기록됐는가?
- [ ] **Map**: 이 기능이 실패할 수 있는 방식을 미리 생각해봤는가(레드팀
      체크리스트로)?
- [ ] **Measure**: 실제로 검증 케이스를 돌려봤는가, 아니면 "잘 될 것
      같다"는 추정에 그쳤는가?
- [ ] **Manage**: 실패가 발견되면 어디에 기록하고 어떻게 재발을 막을
      계획인가?

4개 중 하나라도 완전히 빈칸이면, 그 기능은 아직 "리스크 관리가 안 된"
상태다 — [01-definition-of-done.md](01-definition-of-done.md)의 구조
완성도 기준과는 다른 축(그건 "완성됐는가", 이건 "안전하게 완성됐는가")
이지만 서로 보완한다.

## 이 크리스탈 자체의 한계 (정직하게)

이 문서는 **NIST AI RMF의 공식 해설서가 아니다** — 4개 기능 이름만
NIST에서 가져오고, 그 안에 무엇을 채울지는 이 프레임워크 자신의 다른
크리스탈들로 채운 것이다. NIST의 실제 상세 가이드(서브카테고리, 실제
평가 기준 등)를 원문으로 직접 확인하고 싶다면 nist.gov의 AI RMF 1.0
문서를 별도로 열람해야 한다 — 이 크리스탈은 그 대체물이 아니라, 이미
있는 크리스탈들을 다른 관점으로 재조직한 목차다.

**이 색인 자신의 낡음(staleness) 위험 — 정직하게 밝힘**: 이 크리스탈은
"새 내용을 추가하지 않고 기존 크리스탈을 재배열만 한다"는 성격 때문에,
새 크리스탈이 추가될 때마다 이 문서도 같이 갱신돼야 한다는 사실을
잊기 쉽다 — 실제로 이 문서가 한동안 4기능 재배열 대상을 새로 추가된
크리스탈의 절반 이상 누락한 채로 방치된 적이 있다(이 프레임워크가
스스로 경계하는 바로 그 드리프트를 자기 자신에게는 놓친 사례). 새
크리스탈이 추가되고 그것이 거버넌스/위협 표면/측정/완화 넷 중 하나에
명백히 해당하면, 이 문서의 해당 절에도 한 줄 추가하는 걸 그 크리스탈의
"통합(integration)" 단계 체크리스트에 포함한다(BLUEPRINT.md 3절).
