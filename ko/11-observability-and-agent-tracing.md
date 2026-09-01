# 관측가능성(Observability) — 에이전트 실행을 로그가 아니라 주장으로 남기지 않는 법

> 🌐 **[Read in English](../en/11-observability-and-agent-tracing.md)**

**버전**: 1.1.0
**콘텐츠 해시**: sha256:95c42f5ffd75 (본문 기준, 이 두 줄 제외)

**검증 강도**: 🟢 (2026-09-01 재검증) 자체 원칙(의도-관찰 분리, 구조화
로그)은 ReAct 패턴 기반으로 확정했고, 외부 표준(OpenTelemetry GenAI
시맨틱 컨벤션, github.com/open-telemetry/semantic-conventions-genai)도
이번 재검증에서 실제 속성명(`gen_ai.operation.name`,
`gen_ai.usage.input_tokens` 등)을 원문으로 직접 확인했다 — 이전 판은
해당 저장소가 이전 중이라 접근 실패했었다.

AI 에이전트가 "완료했다"고 말하는 것과 실제로 그 도구 호출이 있었는지는
분리될 수 있다([03-epistemic-immunity-catalog.md](03-epistemic-immunity-catalog.md)
8번 항목). 이 크리스탈은 그 문제를 구조적으로 막는 **관측가능성 설계
원칙**을 정리한다.

## 핵심 원칙 — 세 가지 축

### 1. 의도(intent)를 행동 전에, 관찰(observation)을 행동 후에 기록한다

ReAct 패턴(Thought→Action→Observation)의 핵심은 "왜 이 행동을 하는지"를
행동 **전에** 명시적으로 남기고, "실제로 무엇이 일어났는지"를 행동 **후에**
별도로 기록하는 것이다. 이렇게 분리하면:
- 사후에 "왜 그때 그렇게 판단했는지"를 재구성 가능하다(사후 합리화와
  구분됨 — [03](03-epistemic-immunity-catalog.md) 7번).
- 행동이 실패했을 때, "의도는 맞았는데 실행이 실패했다"와 "애초에 잘못된
  의도였다"를 구분할 수 있다.

### 2. "완료했다"는 문장 옆에 항상 실제 로그를 인용한다

주장(claim)과 증거(evidence)를 같은 자리에 놓는다 — "테스트를 통과했다"라고
쓰는 대신 실제 테스트 실행 출력(통과 개수, 실패 개수)을 그 옆에 붙인다.
이건 사람이 읽는 보고서뿐 아니라, **다른 AI 에이전트가 이 결과를 나중에
참고할 때도 같은 기준을 적용**해야 한다 — 요약된 주장만 재사용하면 원본
검증이 유실된다.

### 3. 구조화된 로그는 자유서술 로그보다 나중에 훨씬 유용하다

실행 로그를 산문으로만 남기면("잘 됐다", "문제없었다") 나중에 집계·검색·
회귀 비교가 불가능하다. 최소한 다음 필드를 구조화해서 남긴다:

| 필드 | 예시 | 왜 필요한가 |
|---|---|---|
| 어떤 작업/단계였는가 | 작업 식별자 | 나중에 같은 단계끼리 비교(회귀 감지)하려면 필요 |
| 무엇을 의도했는가 | "케이스 3건 검증" | 사후 합리화 방지([03](03-epistemic-immunity-catalog.md) 7번) |
| 실제로 무엇을 했는가(도구 호출) | 도구명+입력 요약 | "주장이 아니라 로그로" 원칙의 핵심 |
| 결과가 무엇이었는가 | 성공/실패 + 구체 수치 | 사람이 육안으로 다시 확인 안 해도 되게 |
| 언제 | 타임스탬프 | 시간축 은폐 방지([03](03-epistemic-immunity-catalog.md) 10번) |
| 비용(선택) | 토큰/시간/API 호출 수 | FinOps 관측 — [13-debt-and-quality-bar.md](13-debt-and-quality-bar.md)와 연결 |

## 참고할 만한 신흥 표준 — OpenTelemetry GenAI 시맨틱 컨벤션

OpenTelemetry가 생성형 AI(GenAI)/에이전트 실행을 위한 시맨틱 컨벤션
(표준화된 로그 스키마)을 별도 저장소
(github.com/open-telemetry/semantic-conventions-genai)로 개발하고
있다 — 🟢 2026-09-01 재검증으로 실제 스팬·속성 원문을 확인했다:

| 이 크리스탈의 필드 | OpenTelemetry 실제 속성명 |
|---|---|
| 어떤 작업/단계였는가 | `gen_ai.operation.name` (스팬 이름도 `"{operation.name} {request.model}"` 형식) |
| 실제로 무엇을 했는가 | `gen_ai.request.model`, `gen_ai.provider.name` |
| 결과가 무엇이었는가 | `gen_ai.response.finish_reasons`, `error.type` |
| 비용(선택) | `gen_ai.usage.input_tokens`, `gen_ai.usage.output_tokens` |

**정직한 한계**: 위 매핑은 이 크리스탈이 자체 도출한 필드를 사후적으로
대응시킨 것이지, 이 크리스탈이 애초에 OpenTelemetry 표준을 따라
설계됐다는 뜻은 아니다 — "무엇을 의도했는가"·"언제" 두 필드는
OpenTelemetry의 표준 속성명과 정확히 대응하는 걸 이번 재검증에서 찾지
못했다(더 깊은 문서 탐색이 필요할 수 있다). 표준화된 스키마가 실제로
필요하면, 위 세 가지 원칙을 먼저 자체 구현한 뒤 이 저장소의 최신 문서를
직접 열어 필드명을 맞추는 걸 권한다 — 이 크리스탈이 표준 문서 전체를
대체하지는 않는다.

## 회귀 감지에 연결하기

구조화된 로그가 쌓이면, 새 실행 결과를 과거 로그와 자동 비교해 "이번이
지난번보다 나빠졌는가"를 판정할 수 있다 —
[04-eval-engineering-methodology.md](04-eval-engineering-methodology.md)
8단계(regression)가 이 원칙을 구체적 파이프라인 단계로 구현한 예시다.
관측가능성 설계 자체는 eval 파이프라인이 없어도 가치가 있다 — 사람이
"지난주 대비 뭐가 바뀌었지"를 물을 때 로그 검색만으로 답할 수 있게
해준다.

## 비용과의 트레이드오프 (정직하게)

모든 걸 구조화해서 기록하면 로그 자체가 비대해진다. 실전에서 통하는
절충: (1) 매 실행 후 한 줄 요약만 상시 로그에 남기고, (2) 실패하거나
애매한(boundary) 경우에만 상세 로그(전체 입출력)를 별도로 보존한다 —
[04](04-eval-engineering-methodology.md)의 "boundary 케이스에만 추가
비용을 쓴다"는 절충과 같은 정신이다. 로그 파일 자체가 계속 자라는 문제는
[06-self-improving-heuristics-loop.md](06-self-improving-heuristics-loop.md)의
"메모리 상한 + 아카이브" 패턴을 그대로 적용할 수 있다.
