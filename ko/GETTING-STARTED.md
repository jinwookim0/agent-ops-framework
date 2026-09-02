# 시작하기 — 내 프로젝트에 이 프레임워크를 실제로 도입하는 단계별 절차

> 🌐 **[Read in English](../en/GETTING-STARTED.md)**

[USAGE-GUIDE.md](USAGE-GUIDE.md)가 "기획·설계·구현·개선·참조"라는 다섯
관점으로 이 프레임워크를 관점별로 정리한 문서라면, 이 문서는 그것과
다른 축이다 — **처음 이 폴더를 자기 프로젝트에 들여오는 사람이 0단계부터
순서대로 실행하는 절차**를 다룬다. 관점별 설명이 필요하면 USAGE-GUIDE.md를,
"지금 이 상황엔 뭘 봐야 하지"가 필요하면 USAGE-GUIDE.md의 참조 표를
계속 쓰면 된다 — 이 문서는 그 둘을 대체하지 않고, 처음 진입할 때만 쓰는
1회성 체크리스트다.

**전제 조건**: 이 프레임워크는 "AI를 쓰는 프로젝트" 전반이 아니라
[README.md](README.md)가 정의하는 좁은 범위 — **AI 에이전트가 여러
작업을 자율적으로, 반복적으로 처리하는 프로젝트**를 대상으로 한다. 1회성
질문-답변 기능 하나에는 이 폴더 전체가 과하다. 그게 아니라면 아래로.

**한눈에 보기**: 0단계(가져오기) → 1단계(상태 파일 초기화) → 2단계
(가드레일 설치·검증) → 3단계(나머지는 필요할 때만 순서대로) → 4단계
(내 프로젝트 사례로 키우기) → 5단계(검증 없이 완료라 부르지 않기). 아래로
갈수록 상세하다 — 지금 뭘 해야 할지만 빠르게 확인하고 싶으면 이 한 줄로
충분하다.

## 0단계 — 폴더를 가져온다: 복사할지, 클론해서 참조만 할지 먼저 정한다

**방식 A — 복사(권장, 기본 경로)**: 이 저장소를 통째로 복사하거나
서브모듈로 붙인다. 대상 프로젝트 루트에 `agent-ops-framework/`(또는
원하는 이름) 디렉터리로 둔다 — 크리스탈 문서 안의 상대경로 링크
(`02-directive-registry.md` 등)와 스캐너 스크립트의 경로 상수가 이
디렉터리 구조를 그대로 전제하므로, 폴더 자체를 쪼개지 않는 게 가장
간단하다. 아래 1단계부터는 이 방식을 전제로 쓴다.

**방식 B — 클론해서 경로만 참조**: 이 저장소를 별도 위치에 클론해두고
AI 에이전트의 프롬프트/`CLAUDE.md`에 "판단할 때 이 경로를 참고하라"고만
지시해도 된다 — 벤더링 없이, `git pull` 한 번으로 최신 크리스탈을 계속
참조할 수 있다. 다만 두 경우엔 안 통한다: **①
[07-prompt-guardrails/](07-prompt-guardrails/)는 실행 코드**라, Claude
Code 훅(`settings.json`의 `command` 경로)과 git `pre-push` 훅이 프로젝트
로컬의 실제 파일을 호출해야만 작동한다 — 클론 경로를 "참고"만 해서는
절대 실행되지 않으니 이건 반드시 2단계대로 로컬에 복사한다. **②
[02-directive-registry.md](02-directive-registry.md)·
[01-definition-of-done.md](01-definition-of-done.md)처럼 내 프로젝트의
실제 지시·사례로 채워나가야 하는 문서**는 클론 레퍼런스로 남겨두면
영영 남의 저장소로만 남는다 — 4단계에 해당하면 결국 복사해서 내
프로젝트 것으로 만든다. 두 방식을 섞어도 된다: 07은 항상 복사, 나머지는
클론 참조로 시작했다가 실제로 편집·확장이 필요해지는 시점에 복사로
전환한다.

## 1단계 — 운영용 상태 파일 3종을 초기화한다 (건너뛰면 안 됨)

크리스탈 파일(`NN-*.md`)은 전부 도메인 무관이라 그대로 복사해도 안전하다.
하지만 아래 파일들은 **원본 프로젝트의 실행 이력**을 담고 있어 그대로
들고 오면 새 프로젝트가 첫날부터 남의 이력을 섞어 쓰게 된다
([BLUEPRINT.md](BLUEPRINT.md) 7절에 전체 근거가 있다):

| 파일 | 할 일 |
|---|---|
| `REFLECTION-CANDIDATES.md` | 헤더(스캐너 설명)만 남기고 표는 비운다 |
| `.reflection-checkpoint` | 삭제하거나 0으로 초기화한다 |
| 스캐너 스크립트의 `ORIGIN_MAP` (`agent-ops-framework-sync-check.py`) | 원본 프로젝트의 파일 경로가 들어있다 — 내 프로젝트 자신의 문서 경로로 다시 채운다 |
| `DISCLAIMER.md` | (예외) 그대로 복사해도 안전 — 빈칸(소속 조직명)만 채운다 |
| `RISK-ANALYSIS.md` | 재사용하지 않는다 — **틀(4개 질문 + 결정 트리)만** 참고해 내 프로젝트 자신의 공개 안전성 판단을 새로 쓴다 |

## 2단계 — 07-prompt-guardrails부터 설치한다 (개인정보를 다루는 첫 작업 전에)

이건 원칙 문서가 아니라 **그대로 복사해서 실행하는 코드**다. 순서:

1. `07-prompt-guardrails/settings.json` → `.claude/settings.json`,
   `07-prompt-guardrails/hooks/guard-secrets.sh` →
   `.claude/hooks/guard-secrets.sh`, `07-prompt-guardrails/scripts/*` →
   `scripts/`로 복사한다.
2. `settings.json`의 `permissions.deny`에서 `shared/local/**`을 내
   프로젝트가 실제로 로컬 전용 민감 파일을 두는 디렉터리 이름으로 바꾼다.
3. `guard-secrets.sh`의 `Artifact` matcher를 내 프로젝트가 실제로 쓰는
   외부 발행/배포 도구 이름으로 바꾼다.
4. **라이브로 검증한다** — 민감 패턴이 든 더미 파일을 만들어 실제로
   발행/커밋을 시도하고, 차단 메시지가 실제로 뜨는지 확인한다. 설정
   파일이 문법적으로 맞다는 것과 실제로 작동한다는 것은 다른 문제다.
   확인 후 더미 파일은 지운다.
5. (선택) 4차 방어(네이티브 git pre-push 훅)까지 쓰려면
   `07-prompt-guardrails/hooks/pre-push-verify.sh`를 복사하고
   `.githooks/pre-push`가 그 파일을 가리키게 한 뒤
   `git config core.hooksPath .githooks`를 실행한다.

전체 설치 절차·4단 방어 구조·한계는
[07-prompt-guardrails/README.md](07-prompt-guardrails/README.md)에 있다.

## 3단계 — 나머지 크리스탈은 필요해질 때만, 이 순서로 들여온다

전부 한 번에 설치하지 않는다 — 그 자체가 "너무 이른 인프라"다. 아래
순서대로, 각 조건이 실제로 내 프로젝트에 해당될 때만 하나씩 추가한다:

1. **[01-definition-of-done.md](01-definition-of-done.md)** — 작업이
   3~5개를 넘어 "이 정도면 다 만든 것"이라는 기준이 사람마다 달라지기
   시작하면. 10개 기준을 그대로 체크리스트로 쓴다.
2. **[05-autonomous-agent-operating-principles.md](05-autonomous-agent-operating-principles.md)** —
   에이전트가 사람의 매 단계 확인 없이 반복 실행되기 시작하면.
3. **[02-directive-registry.md](02-directive-registry.md)** — 결정이
   쌓여 "이거 왜 이렇게 정했지?"라는 질문이 반복되면. 1번 행부터 내
   프로젝트 자신의 실제 지시로 채우기 시작한다.
4. **[09-project-structure-template.md](09-project-structure-template.md)** —
   프로젝트 구조 자체를 설계/재설계할 때. 이미 프로젝트가 있다면 기존
   폴더 구조를 5레이어에 강제로 맞추지 말고, "이 레이어에 해당하는 게
   지금 필요한가"부터 묻는다 — 4절의 13단계 순서가 "언제 뭐가
   필요해지는가"의 타임라인 역할을 한다.
5. **[03-epistemic-immunity-catalog.md](03-epistemic-immunity-catalog.md)**·
   **[04-eval-engineering-methodology.md](04-eval-engineering-methodology.md)** —
   산출물 품질을 눈대중이 아니라 처음으로 진지하게 측정해야 할 때.
6. **그 외 모든 크리스탈** — 각 문서 서두의 "왜 필요한가"가 실제로 내
   상황에 해당될 때만. "이 기능이 있으면 좋겠다"가 아니라 "이 부채/문제가
   실제로 발생했다"가 도입 트리거여야 한다.

## 4단계 — 복사만 하고 끝내지 않는다: 내 프로젝트 사례로 채운다

각 크리스탈은 정적 템플릿이 아니라 자라는 문서로 설계됐다. 이식 후 첫
실제 실패·발견이 생기면 바로 그 크리스탈에 추가한다:

- [03](03-epistemic-immunity-catalog.md)·[06](06-self-improving-heuristics-loop.md) —
  실제로 발견된 사례로 카탈로그를 키운다.
- [02-directive-registry.md](02-directive-registry.md) — 새 지시가 생길
  때마다 행을 추가한다(2단계에서 초기화한 그 표).
- [07-prompt-guardrails/](07-prompt-guardrails/)의 `PATTERNS`/`check(...)` —
  내 프로젝트에서 흔한 민감정보 패턴(사내 토큰 형식 등)을 발견하면
  즉시 정규식을 추가한다.

동시에 **비대화도 챙긴다** — [02](02-directive-registry.md)·
[06](06-self-improving-heuristics-loop.md)의 "비대화 방지"/"메모리 상한"
절을 따라, 자라기만 하고 정리되지 않는 문서가 되지 않게 한다.

## 5단계 — "도입했다"고 부르기 전에 검증한다

복사만 하고 한 번도 실제로 안 써봤다면 도입 완료가 아니다. 예:
2단계의 가드레일은 실제 발행/커밋 시도로 차단이 작동하는지 라이브
확인이 설치의 일부다(위 2단계 4번). 다른 크리스탈도 마찬가지로,
"문서를 복사했다"와 "이 프로젝트에서 실제로 한 번 이상 그 기준/절차를
적용해봤다"를 구분한다.

## 그다음부터는

이 문서는 여기서 끝난다 — 이후로는 상황이 생길 때마다
[USAGE-GUIDE.md](USAGE-GUIDE.md)의 참조(Reference) 표("지금 겪는 상황 →
참고할 크리스탈")를 색인으로 쓴다.

## 관련 문서

- [README.md](README.md) — 이 폴더 전체 개요와 37개 크리스탈 지도.
- [USAGE-GUIDE.md](USAGE-GUIDE.md) — 기획·설계·구현·개선·참조 다섯 관점,
  그리고 상황별 참조 표.
- [BLUEPRINT.md](BLUEPRINT.md) — 이 폴더 자신이 무엇이고, 새 크리스탈이
  통과해야 하는 게이트, 7절의 이식 시 초기화 절차(이 문서 1단계의 근거).
