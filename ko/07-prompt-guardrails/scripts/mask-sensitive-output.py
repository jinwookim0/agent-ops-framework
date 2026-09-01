#!/usr/bin/env python3
"""mask-sensitive-output.py — 프롬프트/외부 전송 직전 능동 마스킹 도구.

`public-repo-check.sh`는 커밋 대상 파일에서 민감 패턴을 **발견하면 경고만**
한다(사람이 직접 고쳐야 함). 이 스크립트는 같은 패턴 탐지 로직을
재사용하되, 외부 발행·붙여넣을 콘텐츠·그 밖에 "이 파일 내용을 그대로
프롬프트/외부로 내보내기 직전"처럼 즉시 치환이 필요한 경우를 위해
**실제로 치환(마스킹)까지** 한다.

**이 도구가 하는 것과 안 하는 것 (정직하게 밝힘)**:
- 한다: `public-repo-check.sh`와 동일한 정규식 패턴(이메일·휴대폰번호·
  주민등록번호·홈디렉토리 경로·시크릿 키·클라우드 자격증명·PEM 개인키
  블록)을 실제 치환해 마스킹된 사본을 만든다.
- 안 한다: 완벽한 PII 탐지가 아니다 — 정규식 기반이라 패턴에 안 걸리는
  민감정보(예: 사람 이름, 주소, 서술형 개인정보)는 못 잡는다. 사람의
  최종 확인을 대체하지 않는다(public-repo-check.sh와 동일한 면책).
  구체적으로 알려진 한계(2026-09-01 레드팀 감사로 확인, 완전 해소는
  불가능해서 문서화만 함): 이메일 주소를 "골뱅이"·"at"처럼 풀어쓰거나
  유니코드 유사자형(homoglyph)으로 바꿔 쓰면 안 걸린다, `password`/
  `secret`/`token`/`api_key` 같은 영어 라벨이 아니라 한글 변수명이나
  `pwd`/`cred` 같은 축약형으로 쓰인 비밀값은 안 걸린다, `scheme://
  user:pass@host` 형태처럼 라벨 없이 URL에 박힌 자격증명은 안 걸린다.

사용법:
  python3 mask-sensitive-output.py <파일경로>          # 마스킹 결과를 표준출력
  python3 mask-sensitive-output.py <파일경로> --out <출력경로>
  cat 파일 | python3 mask-sensitive-output.py -        # 표준입력도 지원
  python3 mask-sensitive-output.py <파일경로> --report # 마스킹 요약만(개수) 표준에러로
  python3 mask-sensitive-output.py <파일경로> --check  # 내용은 출력 안 함,
                                                        # 걸리면 exit 1(훅에서 사용)
"""
import argparse
import re
import sys

# public-repo-check.sh와 동일한 탐지 로직 — 패턴을 한쪽만 고치고 다른 쪽을
# 잊어버리는 걸 막기 위해, 이 두 파일을 고칠 때는 항상 같이 검토한다.
# 순서가 중요하다(2026-09-01 레드팀 테스트로 실제 버그 확인 후 재정렬):
# mask()가 같은 텍스트 버퍼에 패턴을 순서대로 연속 치환하기 때문에, 폭이
# 좁은 숫자열 패턴(전화번호/주민등록번호)이 먼저 실행되면 토큰/시크릿 문자열
# 중간에 우연히 낀 숫자 구간만 잘라먹고 "[MASKED:...]"로 바꿔버려서, 그
# 뒤에 실행되는 더 구체적인 패턴(클라우드 토큰 등)이 더는 연속 문자열로
# 인식 못 하고 매칭에 실패하는 사례를 실측했다 — 그 결과 진짜 시크릿의
# 앞뒤 조각이 마스킹 안 된 평문으로 그대로 출력에 남는 사고가 났다(예:
# GitHub PAT 안에 우연히 낀 10자리 숫자열이 "휴대폰 번호"로 먼저
# 마스킹되면서 `ghp_...` 전체를 가려야 할 "클라우드/서비스 토큰" 패턴이
# 더는 매칭 못 함). 그래서 구조적으로 더 넓고 특정적인 패턴(PEM 블록·
# 클라우드 토큰·레이블 기반 시크릿 키)을 먼저 치환해 자리를 "선점"하고,
# 남는 텍스트에 대해서만 폭 좁은 숫자열 패턴(전화번호·주민등록번호)이
# 돌게 한다.
PATTERNS = [
    ("홈 디렉토리 경로", re.compile(r"/(Users|home)/[A-Za-z0-9_.-]+/")),
    ("이메일 주소", re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")),
    (
        "시크릿 키",
        re.compile(
            r"(api[_-]?key|secret|token|password)[\s]*[:=][\s]*[\"']?[A-Za-z0-9_/+=-]{8,}",
            re.IGNORECASE,
        ),
    ),
    # PEM 형식 개인키 블록 — 실제 유출 피해가 가장 큰 시크릿 유형인데
    # 위 "시크릿 키" 패턴(레이블+구분자 방식)은 이 형식을 구조적으로 못 잡는다
    # (2026-09-01 레드팀 발견 — DOTALL로 여러 줄에 걸친 블록 전체를 매칭).
    (
        "PEM 개인키 블록",
        re.compile(
            r"-----BEGIN [A-Z ]*PRIVATE KEY-----.*?-----END [A-Z ]*PRIVATE KEY-----",
            re.DOTALL,
        ),
    ),
    (
        "클라우드/서비스 토큰",
        re.compile(
            r"(AKIA[0-9A-Z]{16}"  # AWS access key ID
            r"|sk-[A-Za-z0-9]{20,}"  # OpenAI-style
            r"|sk_live_[A-Za-z0-9]{16,}"  # Stripe live secret key
            r"|pk_live_[A-Za-z0-9]{16,}"  # Stripe live publishable key
            r"|gh[pousr]_[A-Za-z0-9]{20,}"  # GitHub PAT (ghp_/gho_/ghu_/ghs_/ghr_)
            r"|xox[baprs]-[A-Za-z0-9-]{10,})"  # Slack token
        ),
    ),
    (
        "휴대폰 번호",
        re.compile(r"(?<![0-9])01[0-9][-. ]?[0-9]{3,4}[-. ]?[0-9]{4}(?![0-9])"),
    ),
    # 구분자를 하이픈뿐 아니라 점·공백도 허용하고, 전화번호 패턴과 동일한
    # 숫자 경계(앞뒤가 숫자가 아니어야 함)를 추가함 — 하이픈 대신 점/공백을
    # 쓰는 실제 표기가 예전엔 빠져나갔다(2026-09-01 레드팀 발견, 적대적
    # 우회가 아니라 흔한 표기 차이였음). 구분자는 그대로 **필수**로 남겨둔다
    # (완전히 생략 가능하게 하지 않음) — 한 번 생략 가능하게 바꿔서 직접
    # 테스트해보니, 저장소 안의 무관한 13자리 숫자열(리드베리 상수 등
    # 과학 상수 리터럴)에 오탐이 실제로 발생했다(2026-09-01 레드팀
    # 자체검증) — RRN 없이 13개 연속 숫자가 나오는 경우까지 잡으려 하면
    # 오탐 비용이 실제 탐지력 향상보다 커서, 그 케이스는 의도적으로 포기.
    ("주민등록번호", re.compile(r"(?<![0-9])[0-9]{6}[-. ][1-4][0-9]{6}(?![0-9])")),
]
# 정직한 한계(2026-09-01 레드팀): 위 패턴은 알려진 몇몇 벤더 형식의 접두사만
# 잡는다 — GCP 서비스계정 JSON, Azure 연결 문자열/SAS 토큰, connection-string
# 형식(scheme://user:pass@host)처럼 레이블이 없는 자격증명, 영어가 아닌
# 언어의 시크릿 레이블(예: 한국어 "비밀번호"류 변수명)은 여전히 못 잡는다 —
# 벤더 토큰 형식을 전부 따라잡는 건 끝나지 않는 경쟁이라 완전한 목록을
# 목표로 하지 않는다(이 파일 상단의 "안 하는 것" 절 참고).


def mask(text: str) -> tuple[str, dict[str, int]]:
    counts: dict[str, int] = {}
    for label, pattern in PATTERNS:
        text, n = pattern.subn(f"[MASKED:{label}]", text)
        if n:
            counts[label] = n
    return text, counts


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("input", help="마스킹할 파일 경로, 또는 '-'(표준입력)")
    ap.add_argument("--out", help="마스킹 결과를 쓸 파일 경로(생략 시 표준출력)")
    ap.add_argument(
        "--report",
        action="store_true",
        help="마스킹 요약(라벨별 개수)만 표준에러로 출력",
    )
    ap.add_argument(
        "--check",
        action="store_true",
        help="내용을 어디에도 출력하지 않고, 패턴이 하나라도 걸리면 exit 1"
        "(exit 0=깨끗함) — 훅(hook)처럼 내용을 로그에 남기면 안 되는 곳에서 사용",
    )
    args = ap.parse_args()

    raw = (
        sys.stdin.read()
        if args.input == "-"
        else open(args.input, encoding="utf-8").read()
    )
    masked, counts = mask(raw)

    if args.check:
        if counts:
            summary = ", ".join(f"{label} {n}건" for label, n in counts.items())
            print(f"⚠️  민감정보 패턴 발견: {summary}", file=sys.stderr)
            return 1
        return 0

    if counts:
        summary = ", ".join(f"{label} {n}건" for label, n in counts.items())
        print(f"⚠️  마스킹됨: {summary}", file=sys.stderr)
    else:
        print(
            "✅ 마스킹 대상 패턴 없음(완벽한 탐지는 아님 — 사람 확인 대체 안 함).",
            file=sys.stderr,
        )

    if args.report:
        return 0

    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(masked)
        print(f"→ {args.out}에 저장", file=sys.stderr)
    else:
        print(masked)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
