#!/usr/bin/env bash
# 이 저장소가 지금 이 순간 퍼블릭으로 전환돼도 문제없는지 훑는 저비용 스캐너.
#
# 사용법: ./public-repo-check.sh
# git으로 추적되는 파일만 검사한다 (추적 안 되는 로컬 전용 파일은 애초에 push 안 되므로 제외).
#
# 완벽한 탐지는 불가능하다 — 이건 "명백한 실수를 걸러내는 안전망"이지 보안 감사의 전체가
# 아니다. 걸린 게 없어도 사람이 한 번 더 훑어보는 걸 대체하지 않는다.
#
# 이 스크립트는 경고만 한다(사람이 직접 고쳐야 함). 실제로 치환(마스킹)까지 필요하면
# mask-sensitive-output.py를 쓴다 — 둘은 같은 패턴을 공유하니 한쪽을 고치면
# 다른 쪽도 같이 검토한다. 원천 차단(애초에 못 읽게)은 settings.json의
# permissions.deny 참고.

set -uo pipefail
cd "$(git rev-parse --show-toplevel)"

FOUND=0
# --cached: 이미 git에 추가된 파일 / --others --exclude-standard: 아직 add 안 했지만
# .gitignore에 안 걸려서 커밋하면 들어갈 파일. 즉 "지금 커밋하면 포함될 모든 파일"을 본다.
# -z(NUL 구분)로 받아 임시 파일에 저장한다 — 일반 셸 변수는 NUL을 담지
# 못해서 값으로 캡처하면 못 쓴다. mktemp로 예측 불가능한 경로에 만들고
# EXIT 시 정리한다.
FILELIST=$(mktemp)
trap 'rm -f "$FILELIST"' EXIT
git ls-files -z --cached --others --exclude-standard > "$FILELIST"

check() {
  local label="$1" pattern="$2"
  local hits
  # 2026-09-01 레드팀 발견: 예전엔 파일 목록을 공백 구분 문자열로 xargs에
  # 넘겨서, 파일명에 공백이 있으면(예: "secret file.txt") word-splitting
  # 때문에 조용히 검사에서 빠졌다(라이브 재현 확인됨) — xargs -0 + NUL
  # 구분 목록으로 파일명에 공백/개행이 있어도 항상 통째로 한 인자가 되게
  # 고쳤다.
  hits=$(xargs -0 grep -InE "$pattern" < "$FILELIST" 2>/dev/null || true)
  # 터미널/ANSI 이스케이프 주입 방어(2026-09-01 레드팀 발견): 매칭된 줄은
  # 스캔 대상 파일의 내용을 그대로 담고 있어, 공격자가 제어한 파일이 ESC
  # 바이트를 포함하면 이 경고 자체가 화면에서 변조/은폐될 수 있다. \t·\n은
  # 남기고 그 외 C0 제어문자만 지운다.
  hits=$(printf '%s' "$hits" | LC_ALL=C tr -d '\000-\010\013-\037\177')
  if [ -n "$hits" ]; then
    echo "⚠️  $label"
    echo "$hits" | sed 's/^/    /'
    echo
    FOUND=1
  fi
}

echo "=== public-repo-check: $(date '+%Y-%m-%d') ==="
echo

check "홈 디렉토리 절대경로 (/Users/<이름>/ 또는 /home/<이름>/)" '/(Users|home)/[A-Za-z0-9_.-]+/'
check "이메일 주소" '[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}'
# 참고: 전화번호처럼 자릿수가 정해진 숫자열 패턴은 SEC EDGAR 문서 ID·뉴스 기사 ID처럼
# 더 긴 숫자열 중간의 부분 일치로 오탐이 잦다 — 경계 없이 매칭하면 "0001018724..." 같은
# 문자열 안에서도 걸린다. 실제 전화번호(양옆이 숫자가 아닌 독립된 토큰)만 잡히도록
# 앞뒤에 비-숫자 경계를 반드시 둔다(아래는 한국 휴대폰 번호 형식 예시 — 자신의
# 국가/형식에 맞게 바꿔 쓴다).
check "한국식 휴대폰 번호 패턴 (010-xxxx-xxxx, 공백/점 구분자 포함)" '(^|[^0-9])01[0-9][-. ]?[0-9]{3,4}[-. ]?[0-9]{4}([^0-9]|$)'
# 구분자는 하이픈/점/공백 중 하나를 필수로 요구한다(완전 생략은 허용 안 함)
# — 생략까지 허용해보니 저장소 안의 무관한 13자리 숫자열(리드베리 상수 등)에
# 실제로 오탐이 나서(2026-09-01 레드팀 자체검증), 탐지력보다 오탐 비용이
# 커지는 지점에서 멈췄다.
check "주민등록번호 패턴 (xxxxxx-x......, 하이픈/점/공백 구분자)" '(^|[^0-9])[0-9]{6}[-. ][1-4][0-9]{6}([^0-9]|$)'
check "흔한 시크릿 키 패턴 (api_key/secret/token/password = ...)" '(api[_-]?key|secret|token|password)[[:space:]]*[:=][[:space:]]*[\"'"'"']?[A-Za-z0-9_/+=-]{8,}'
# PEM 개인키 블록 — 레이블+구분자 방식인 위 패턴이 구조적으로 못 잡는,
# 유출 피해가 가장 큰 시크릿 유형(2026-09-01 레드팀 발견). BEGIN 마커
# 한 줄만 있어도 파일 안에 개인키가 있다는 뜻이라 줄 단위 grep으로 충분하다.
check "PEM 개인키 블록 시작 마커 (-----BEGIN ... PRIVATE KEY-----)" '\-\-\-\-\-BEGIN [A-Z ]*PRIVATE KEY\-\-\-\-\-'
check "클라우드/서비스 토큰 패턴 (AWS/OpenAI/Stripe/GitHub/Slack)" '(AKIA[0-9A-Z]{16}|sk-[A-Za-z0-9]{20,}|sk_live_[A-Za-z0-9]{16,}|pk_live_[A-Za-z0-9]{16,}|gh[pousr]_[A-Za-z0-9]{20,}|xox[baprs]-[A-Za-z0-9-]{10,})'
# 정직한 한계: 위는 알려진 몇몇 벤더 형식만 잡는다 — GCP/Azure 자격증명,
# connection-string(scheme://user:pass@host) 형식, 영어가 아닌 시크릿
# 레이블은 여전히 못 잡는다(완전한 목록을 목표로 하지 않음).

if [ "$FOUND" -eq 0 ]; then
  echo "✅ 특별한 패턴 없음. (사람이 한 번 더 훑어보는 걸 대체하진 않는다.)"
  exit 0
else
  echo "위 항목을 확인하고, 실제로 민감하면 값을 빼거나 일반화한 뒤 다시 실행하라."
  exit 1
fi
