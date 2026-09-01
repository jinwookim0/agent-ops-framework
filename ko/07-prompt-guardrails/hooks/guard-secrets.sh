#!/usr/bin/env bash
# PreToolUse 훅 — Artifact/외부 발행 도구 호출 직전, git commit·push 직전에
# password·api key 등 민감 패턴을 실제로 차단한다.
#
# 왜 훅까지 필요한가: 경고만 하는 스캐너나 능동 마스킹 스크립트는 "사람(AI)이
# 기억해서 직접 실행"해야 작동한다는 한계가 있다. 훅으로 걸면 도구 호출
# 자체를 자동으로 가로채므로, 실행을 잊는 실패 모드가 구조적으로 사라진다.
#
# 이 훅이 막는 것: 발행 도구(Artifact 등) 직전 file_path 내용, git commit/
# push 직전 커밋 대상 전체(public-repo-check.sh 재사용). 둘 다 exit 2로
# 도구 호출 자체를 막는다 — stderr가 에이전트에게 보이는 차단 사유가 된다.
#
# 이 훅이 안 막는 것(정직하게 밝힘): 사람이 채팅에 직접 붙여넣은 텍스트,
# Bash 출력으로 화면에만 찍히고 파일/커밋/발행으로 안 나가는 내용 — 이건
# 도구 호출 경계가 아니라서 이 훅이 볼 수 없다. 완벽한 방어가 아니라
# "외부로 실제로 나가는 지점"에서의 마지막 관문이다.
#
# Bash 경로의 더 좁은 한계(2026-09-01 레드팀 발견, 위 문단과는 다른
# 종류의 한계라 별도로 명시함): Bash matcher 아래에서도 이 훅이 실제로
# 검사하는 건 명령어 문자열에 "git commit"/"git push"라는 리터럴
# 부분문자열이 있는지뿐이다(아래 grep -qE 참고). 즉:
#   - 과소탐지(bypass): git 별칭(alias)·래퍼 스크립트·함수로 커밋/푸시를
#     하거나, curl/scp/aws s3 cp/gh release upload/npm publish/docker
#     push처럼 git이 아닌 다른 방법으로 같은 Bash 도구 경계 안에서
#     내보내면 이 훅은 그 시도를 전혀 못 본다 — "도구 호출 경계 안이면
#     다 본다"는 뜻이 아니라 "git commit/push라는 특정 명령 형태만
#     본다"는 훨씬 좁은 보장이다.
#   - 과대탐지(false positive): 반대로, 실제로 git commit/push를
#     실행하지 않는 명령이라도 명령어 문자열 안에 그 부분문자열이 그냥
#     텍스트로 들어있으면(예: grep으로 "git commit"이라는 단어를 찾는
#     명령, 그 문구가 든 echo/주석) 이 훅이 오작동으로 걸어낸다 — 실제로
#     이 감사 작업 중 정확히 이 상황이 발생해 무관한 grep 호출이
#     confidential-paths 검사까지 통과하며 차단당했다(라이브로 재현
#     확인됨). 두 방향 다 "명령어를 실제로 파싱해 이해하는" 게 아니라
#     "리터럴 부분문자열을 찾는" 정규식 매칭의 근본적 한계다 — 완전히
#     없앨 수 없고, 이 훅을 "git commit/push라는 좁은 케이스를 위한
#     안전망"으로만 신뢰하고 일반적인 Bash 유출 경로 전체를 막는
#     걸로 과신하지 않는 게 맞는 대응이다.
#
# 이식할 때: matcher 이름("Artifact")을 이 프로젝트가 실제로 쓰는 발행/
# 배포 도구 이름으로 바꾼다. 여러 개면 settings.json의 matcher를 파이프로
# 나열하거나 훅을 여러 개 등록한다.

set -uo pipefail
cd "${CLAUDE_PROJECT_DIR:-.}"

INPUT=$(cat)

block() {
  echo "🚫 guard-secrets 훅: $1" >&2
  exit 2
}

# 2026-09-01 레드팀 발견 수정: JSON 파싱 자체가 실패하면(잘못된 입력 등)
# 예전엔 TOOL_NAME이 조용히 빈 문자열이 되고, 아래 case에 와일드카드가
# 없어서 도구 호출이 그냥 통과(fail-open)했다 — 보안 관문에서 파싱 실패는
# "이 도구가 Artifact/Bash가 아니다"(정상, 통과)와 구분 없이 취급되면 안
# 된다. 파싱 자체가 실패한 경우만 명시적으로 막는다(fail-closed) — 파싱은
# 됐는데 tool_name이 그냥 없는/다른 경우는 기존과 동일하게 통과시킨다.
if ! TOOL_NAME=$(echo "$INPUT" | python3 -c "import json,sys; print(json.load(sys.stdin).get('tool_name',''))" 2>/dev/null); then
  block "훅 입력을 JSON으로 파싱하지 못함 — 안전을 위해 이 도구 호출을 막는다."
fi

case "$TOOL_NAME" in
  Artifact)
    FILE_PATH=$(echo "$INPUT" | python3 -c "import json,sys; print(json.load(sys.stdin).get('tool_input',{}).get('file_path',''))" 2>/dev/null)
    if [ -n "$FILE_PATH" ] && [ -f "$FILE_PATH" ]; then
      # mktemp로 예측 불가능한 경로에 만든다(2026-09-01 레드팀 발견: 이전엔
      # /tmp/guard-secrets-artifact.$$처럼 PID로 예측 가능한, 모두가 쓰기
      # 가능한 디렉터리 경로를 썼다 — 다중 사용자 환경에서 심볼릭 링크
      # 선점 공격에 노출될 수 있는 구도였다).
      ARTIFACT_ERR=$(mktemp)
      if ! python3 scripts/mask-sensitive-output.py "$FILE_PATH" --check 2>"$ARTIFACT_ERR"; then
        REASON=$(cat "$ARTIFACT_ERR"); rm -f "$ARTIFACT_ERR"
        block "발행 대상($FILE_PATH)에서 민감 패턴 발견 — $REASON — scripts/mask-sensitive-output.py로 직접 확인 후 다시 시도하라."
      fi
      rm -f "$ARTIFACT_ERR"
    fi
    ;;
  Bash)
    COMMAND=$(echo "$INPUT" | python3 -c "import json,sys; print(json.load(sys.stdin).get('tool_input',{}).get('command',''))" 2>/dev/null)
    if echo "$COMMAND" | grep -qE '\bgit\s+(commit|push)\b'; then
      GIT_CHECK_OUT=$(mktemp)
      if ! bash scripts/public-repo-check.sh >"$GIT_CHECK_OUT" 2>&1; then
        REASON=$(cat "$GIT_CHECK_OUT"); rm -f "$GIT_CHECK_OUT"
        block "git commit/push 직전 public-repo-check.sh가 민감 패턴을 발견했다:
$REASON
해당 파일을 고치거나 스테이징에서 빼고 다시 시도하라."
      fi
      rm -f "$GIT_CHECK_OUT"
    fi
    ;;
esac

exit 0
