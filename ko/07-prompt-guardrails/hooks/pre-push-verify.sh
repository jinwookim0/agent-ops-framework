#!/usr/bin/env bash
# 네이티브 git pre-push 훅 — Claude Code를 거치지 않고 사람이 터미널에서
# 직접 `git push`를 실행해도 작동한다(guard-secrets.sh는 Claude Code의
# Bash 도구 호출을 가로채는 PreToolUse 훅이라 그 경계 밖은 못 본다 —
# 이 훅은 그 경계 밖, "실제로 원격에 나가기 직전"이라는 마지막 지점 하나를
# 추가로 지킨다. 3단 방어(README.md "왜 3단인가")에 4단째를 더하는 셈).
#
# 이 훅이 막는 것 두 가지, 서로 다른 이유로 분리해서 검사한다:
# 1. **커밋 대상 파일 내용**: `public-repo-check.sh`를 그대로 재사용한다
#    (같은 패턴을 여기 또 베끼지 않는다 — 파일 내용 검사는 이미 그 스크립트의
#    책임이고, 이 훅은 그걸 "push 직전"이라는 새 시점에 다시 호출할 뿐이다).
# 2. **지금 막 push되는 커밋들의 메시지 자체**: 파일 내용과는 다른 채널이라
#    별도로 검사해야 한다 — 예를 들어 세션 링크·로컬 절대경로처럼 파일에는
#    안 나오지만 커밋 메시지 본문에만 섞여 들어갈 수 있는 값들이 있다.
#
# 설치(이 폴더를 프로젝트에 이식할 때):
#   git config core.hooksPath .githooks
#   (.githooks/pre-push가 이 파일을 가리키게 심볼릭 링크하거나 복사)
# `.git/hooks/`는 git이 버전관리하지 않아 클론마다 따로 설정해야 한다 —
# `core.hooksPath`로 버전관리되는 디렉터리를 가리키게 하는 쪽이 매번 수동
# 복사를 안 해도 돼서 더 안전하다(설치를 잊는 실패 모드 자체를 없앤다).
#
# 정직한 한계: 이 훅도 `.git/hooks/`가 아니라 `core.hooksPath`를 통해서만
# 작동한다 — 그 git 설정 자체를 새 클론에서 한 번 실행하는 걸 잊으면 이
# 훅은 조용히 작동 안 한다(문서화된 규칙이 실행을 잊으면 무력하다는, 이
# 폴더가 다른 곳에서도 반복하는 교훈과 같다). `--no-verify`로 이 훅
# 자체를 건너뛰는 것도 항상 가능하다 — 이건 안전망이지 강제가 아니다.

set -uo pipefail
cd "$(git rev-parse --show-toplevel)"

ZERO_SHA="0000000000000000000000000000000000000000"
BLOCK=0

# 커밋 메시지 채널 전용 패턴 — 파일 내용용 패턴(public-repo-check.sh가
# 이미 담당)과 굳이 다시 합치지 않고, 커밋 메시지에서 실제로 문제가 됐던
# 것 위주로 최소한만 둔다.
#
# 2026-09-02 라이브로 발견한 오탐: 이 훅 자체를 추가한 커밋의 메시지가
# "이 훅은 'Claude-Session:'을 잡는다"처럼 그 패턴을 설명하느라 문자열
# 자체를 인용해서, 실제 유출이 아닌데도 걸렸다 — 첫 실제 push에서 바로
# 재현됨. 실제 트레일러는 항상 뒤에 URL이 붙으므로, 그 URL 형태까지
# 요구해 "설명하는 문장"과 "진짜 유출"을 구분한다.
check_message() {
  local sha="$1" msg hits
  msg=$(git log -1 --format=%B "$sha")
  hits=$(printf '%s' "$msg" | grep -inE 'claude-session:\s*https://claude\.ai/code/session_|/(Users|home)/[A-Za-z0-9_.-]+/|-----BEGIN [A-Z ]*PRIVATE KEY-----' || true)
  if [ -n "$hits" ]; then
    echo "🚫 커밋 $sha 메시지에 금지 패턴:"
    echo "$hits" | sed 's/^/    /'
    BLOCK=1
  fi
}

# git이 pre-push 훅 stdin으로 주는 줄 형식: "로컬ref 로컬sha 원격ref 원격sha"
while read -r local_ref local_sha remote_ref remote_sha; do
  [ "$local_sha" = "$ZERO_SHA" ] && continue # 브랜치/태그 삭제 — 검사 대상 없음
  if [ "$remote_sha" = "$ZERO_SHA" ]; then
    range="$local_sha" # 새 브랜치 최초 push — 그 브랜치의 커밋 전체
  else
    range="$remote_sha..$local_sha"
  fi
  for sha in $(git rev-list "$range" -- 2>/dev/null); do
    check_message "$sha"
  done
done

if [ "$BLOCK" -eq 1 ]; then
  echo "" >&2
  echo "위 커밋 메시지를 고친 뒤(예: git filter-branch --msg-filter, 또는" >&2
  echo "아직 origin에 없는 최근 커밋이면 git commit --amend) 다시 push하라." >&2
  exit 1
fi

# 파일 내용 검사는 기존 스크립트를 그대로 재사용 — 같은 패턴을 여기 또
# 베끼지 않는다. public-repo-check.sh는 "현재 커밋되면 포함될 파일 전체"를
# 보므로, push 시점에 다시 돌리면 지금 push하려는 상태와 사실상 같은
# 내용을 검사하는 셈이다.
#
# 경로가 두 갈래인 이유: 이식된 프로젝트는 설치 안내대로 이 스크립트가
# `scripts/public-repo-check.sh`에 있지만, 이 크리스탈을 만든 원본
# 저장소(agent-ops-framework) 자신은 `ko/07-prompt-guardrails/`
# 아래 원본 그대로 둔 채로 쓴다 — 두 레이아웃 다 지원한다.
if [ -f scripts/public-repo-check.sh ]; then
  CHECK_SCRIPT=scripts/public-repo-check.sh
else
  CHECK_SCRIPT=ko/07-prompt-guardrails/scripts/public-repo-check.sh
fi
if ! bash "$CHECK_SCRIPT"; then
  echo "" >&2
  echo "public-repo-check.sh가 위 항목을 발견했다 — push를 막는다." >&2
  exit 1
fi

exit 0
