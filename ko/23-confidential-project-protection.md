# 프로젝트 단위 대외비 보호 — 패턴 기반 비밀값 탐지로는 못 막는 것

> 🌐 **[Read in English](../en/23-confidential-project-protection.md)**

**버전**: 1.0.1
**콘텐츠 해시**: sha256:9a24b782c916 (본문 기준, 이 두 줄 제외)

🟢 검증 강도: 실제 `git push` 시도로 라이브 차단까지 확인된 원본 프로젝트의
운영 이력에서 추출.

## 왜 필요한가

[07-prompt-guardrails/](07-prompt-guardrails/)의 3단 가드레일은 이메일·API
키·비밀번호 같은 **패턴으로 식별 가능한** 민감정보를 막는다. 하지만 어떤
경우엔 개인정보 패턴이 하나도 없어도(가상 데이터만 써도) **사업 기획·구현
자체가 공개되면 안 되는** 경우가 있다 — 예: 아직 공개하지 않은 제품
컨셉, 경쟁사에 알려지면 안 되는 비즈니스 모델. 패턴 매칭으로는 이런 걸
못 잡는다 — "이 폴더 전체가 기밀"이라는 판단은 콘텐츠를 읽어야만 내릴 수
있는 사람의 결정이기 때문이다.

## 메커니즘

1. **지정**: 기밀로 분류할 경로를 한 줄에 하나씩 목록 파일에 적는다(예:
   `confidential-paths.txt`). 새 기밀 프로젝트가 생기면 이 목록에 줄만
   추가하면 된다 — 코드를 고칠 필요가 없다.
2. **강제 지점**: `git commit`은 막지 않는다(로컬 버전관리는 허용) —
   **`git push`에만** 강제한다. 커밋 이력에 그 경로를 건드린 미푸시
   커밋이 있으면 원격으로 올라가는 걸 차단한다.
3. **판정 방법**: 푸시하려는 범위(원격 브랜치가 있으면 `origin/<branch>..HEAD`,
   없으면 전체 이력)에서 목록의 각 경로를 건드린 파일이 있는지 확인한다.
   하나라도 있으면 차단.
4. **우회 방지**: 코드를 고쳐서 우회할 수 없게, 목록 파일에서 그 줄을
   사람이 직접 지워야만 통과되게 만든다 — 이건 실수로 새는 걸 막는
   의도적 마찰이지, 사람의 최종 결정을 대체하는 게 아니다. 정말 공개해도
   된다고 확인했으면 목록에서 줄을 지우고 다시 시도하면 된다.

## 07번(패턴 기반 가드레일)과의 차이 — 축이 다르다

| | 막는 대상 | 강제 시점 |
|---|---|---|
| [07-prompt-guardrails/](07-prompt-guardrails/) | 비밀값 **패턴**(API 키 형식, 이메일 형식 등) — 콘텐츠를 안 읽어도 정규식으로 판정 가능 | 프롬프트 전송, 커밋·푸시 |
| 이 크리스탈 | **프로젝트/경로 전체**의 기밀 여부 — 패턴이 아니라 사람의 판단으로만 정해짐 | `git push`만 |

두 메커니즘은 겹치지 않고 상호보완한다 — 07번은 "무엇이 비밀인지 형식으로
알 수 있는 것", 이 크리스탈은 "형식으로는 알 수 없고 사람이 지정해야만
아는 것"을 막는다.

## 부작용 — 정직하게 명시

로컬 저장소가 원격보다 여러 커밋 앞서 있고, 그 사이에 기밀 경로를 건드린
커밋이 하나라도 섞여 있으면 **그 이후의 모든 push가 통과 못 한다** — 기밀
경로를 안 건드린 최신 변경사항도 함께 막힌다(범위가 커밋 단위가 아니라
"이번에 올라갈 범위 전체"이기 때문). 필요하면 히스토리 정리나 별도 브랜치
전략을 사람과 상의해야 한다 — 이 메커니즘 자체가 그 판단을 대신하지
않는다.

## 최소 구현

```bash
# git push를 가로채는 훅(pre-push 또는 명령 실행 전 후크) 안에서:
if echo "$COMMAND" | grep -qE '\bgit\s+push\b' && [ -f confidential-paths.txt ]; then
  RANGE="HEAD"
  git rev-parse --verify origin/main >/dev/null 2>&1 && RANGE="origin/main..HEAD"
  while IFS= read -r CPATH; do
    [ -z "$CPATH" ] && continue
    if [ -n "$(git log --name-only --pretty=format: "$RANGE" -- "$CPATH")" ]; then
      echo "차단: 대외비 경로($CPATH)가 push 범위에 포함됨 — confidential-paths.txt에서 해당 줄을 지운 뒤 재시도" >&2
      exit 2
    fi
  done < confidential-paths.txt
fi
```

## 관련
- [07-prompt-guardrails/](07-prompt-guardrails/) — 패턴 기반 비밀값 차단(다른 축).
- [05-autonomous-agent-operating-principles.md](05-autonomous-agent-operating-principles.md) — 0번째 원칙(비가역 행동은 항상 확인) — 이 메커니즘의 "우회 방지" 설계가 같은 정신.
- [20-decision-rights-raci.md](20-decision-rights-raci.md) — 기밀 여부는 사람이 지정하고 AI가 강제만 한다는 구도가 "A는 항상 사람" 원칙과 같은 축.
