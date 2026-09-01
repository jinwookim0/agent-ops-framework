# 프리모템(Premortem) — 실행 전에 미리 실패를 가정해보는 기법

> 🌐 **[Read in English](../en/27-premortem-planning.md)**

**버전**: 1.0.2
**콘텐츠 해시**: sha256:5b7755973310 (본문 기준, 이 두 줄 제외)

[12-blameless-postmortem-template.md](12-blameless-postmortem-template.md)가
**이미 벌어진 일**에서 배우는 절차라면, 이 크리스탈은 그 거울상이다 —
**아직 실행 안 한 계획**에 적용해, 사고가 나기 전에 같은 학습 효과를 미리
당겨온다.

## 근거 (1차 자료 확인)

🟢 Gary Klein, ["Performing a Project Premortem,"](https://hbr.org/2007/09/performing-a-project-premortem)
*Harvard Business Review* (2007) 원문 확인. 핵심 메커니즘을 원문 그대로
인용한다:

> "Unlike a typical critiquing session, in which project team members are
> asked what might go wrong, the premortem operates on the assumption
> that the 'patient' has died, and so asks what did go wrong."

이 기법이 통하는 이유는 질문의 **시제**에 있다. "뭐가 잘못될 수 있을까요?"
(미래·가정형)는 아직 안 일어난 일을 걱정하는 것처럼 들려 사회적으로
조심스럽다. "뭐가 잘못됐**었**나요?"(과거·기정사실형)는 이미 죽었다고
전제하므로, 우려를 말하는 게 비관이 아니라 그냥 부검이 된다. Klein이
직접 짚은 동기도 원문에 있다:

> "Projects fail at a spectacular rate. One reason is that too many
> people are reluctant to speak up about their reservations during the
> all-important planning phase."

프리모템은 새 정보를 캐내는 도구가 아니라, **이미 알고 있던 우려를 말해도
되는 사회적 허가**를 만드는 장치에 가깝다.

🟡 Klein 자신이 밝힌 계보 — 더 오래된 심리학 개념인 "prospective
hindsight"(Mitchell, Russo & Pennington, 1989, *Journal of Behavioral
Decision Making*, "Back to the Future: Temporal Perspective in the
Explanation of Events")를 실무 절차로 정식화한 것. 2차 출처(백과사전류의
인용)로 그 존재와 논문 제목만 확인됐고, 원 논문의 구체적 효과 크기(정량
수치)는 확인되지 않았다 — 과장하지 않기 위해 정직하게 🟡로 남긴다.

## 언제 쓰는가 — 위험 비례, 전부 강제 안 함

프리모템의 정의 자체("아직 실행 안 한 계획")가 적용 범위를 좁혀준다. 어느
프로젝트든 "새 계획을 채택하는" 지점은 한정돼 있다 — 아키텍처/도구 결정
문서를 승인할 때, 새 작업/기능을 스캐폴딩할 때 정도다. 그마저도 **되돌리기
쉽고 위험 낮은 계획까지 매번 돌리면 체크박스 의례가 된다** — 이건
[04-eval-engineering-methodology.md](04-eval-engineering-methodology.md)의
"검증 강도를 위험도에 비례시킨다"는 원칙과 정확히 같은 로직이다.

**설계 규칙**: 새 임계값을 발명하지 않는다. 프로젝트에 이미 위험 등급
분류(예: 04번 크리스탈의 risk-tiered verification, 또는 사람 확인이
필요한 행동인지 판정하는 오버사이트 게이트)가 있다면, 그 신호를 그대로
재사용해 프리모템 트리거로 삼는다 — 고위험/비가역 등급으로 이미 분류된
계획에만 걸고, 저위험/가역 계획은 건너뛴다.

## 최소 기준

시나리오를 최소 **3개** 이상 구체적으로 뽑는다. 1개는 요행일 수 있고 2개는
우연일 수 있지만, 3개부터는 패턴이 보이기 시작한다. "예산이 부족할 수
있다"처럼 막연한 한 줄은 인정하지 않는다 — 구체적 메커니즘("어느 단계에서,
왜, 어떤 조건이 겹쳐야 실패하는가")까지 내려가야 한다.

## 표준 절차

```markdown
## Premortem

"[시점] 뒤 이 계획이 실패했다고 가정하면, 왜 실패했을까?"

1. [시나리오 1 — 구체적 메커니즘]
   완화책: [구조적 대응, "주의하겠다"류 정신론적 조치는 인정 안 함]
2. [시나리오 2]
   완화책: ...
3. [시나리오 3]
   완화책: ...
```

각 시나리오에는 반드시 완화책을 같이 쓴다 — 리스크만 나열하고 끝내면
불안만 만들고 아무것도 안 고친다([12번 크리스탈](12-blameless-postmortem-template.md)의
"액션 아이템 없는 포스트모템은 미완성"과 같은 원칙).

## AI 에이전트 프로젝트에 특히 중요한 이유

AI 에이전트는 낙관 편향을 사람보다 더 쉽게 만든다 — 계산이 끝나는 순간
(예: 여러 대안을 비교해 "최선"이 정해지는 순간)이 정확히 확신이 가장 강한
지점이고, 그 지점이 프리모템 없이 그대로 실행으로 넘어가면 반박 없이
굳어진다. **계산이 끝나는 지점에 프리모템을 자동으로 붙이는 것**(예: 여러
대안 중 1위가 정해지면 그 1위에 곧바로 프리모템을 요구)이 이 함정을
구조적으로 막는다.

## 이 원칙 자체에도 적용

이 크리스탈을 도입하는 결정 자체도 아직 실행 안 된 계획이라 프리모템
대상이다: (1) 매번 형식적으로 3줄만 채우고 넘어가는 의례화 위험 — 완화책은
프리모템의 "구체성"(막연한 시나리오 vs 실제 메커니즘을 짚은 시나리오)을
검증 단계에서 함께 채점하는 것. (2) 위험 분류 자체가 틀리면 트리거가
조용히 빠지는 위험 — 완화책은 위험 분류기 자신을 주기적으로 스팟체크하는
것(04번 크리스탈의 "검증 도구 자신의 스코프 관리" 참고). (3) 여러 절차
문서에 나눠 넣으면 기억에 의존해 빠뜨리는 위험 — 완화책은 기억이 아니라
절차 템플릿 자체에 체크리스트로 박아넣는 것.

## 관련
- [12-blameless-postmortem-template.md](12-blameless-postmortem-template.md) — 거울상(이미 실행한 것)
- [04-eval-engineering-methodology.md](04-eval-engineering-methodology.md) — 재사용하는 위험 비례 판단 로직
- [21-spec-first-implementation.md](21-spec-first-implementation.md) — 명세를 먼저 쓰는 것과 짝을 이룸: 명세는 "무엇을 만들지", 프리모템은 "그게 왜 실패할 수 있는지"
