#!/usr/bin/env python3
"""agent-ops-framework-reflection-check.py — docs/directive-registry.md에 새로 쌓인
지시 중, agent-ops-framework가 아닌 다른 프로젝트(tasks/prototypes/products)의
고도화가 agent-ops-framework에 반영할 만한 이식 가능한 구조적 패턴을 담고 있는지
후보를 찾아 agent-ops-framework/REFLECTION-CANDIDATES.md에 누적한다.

2026-08-29 신설. 사용자 지시: "agent-ops-framework가 아닌 다른 프로젝트가 고도화될
때 마찬가지로 agent-ops-framework에 반영 가능한 고도화해나갈 수 있는 부분을
고도화하는 작업 반영이 자동화되어야 한다." — `docs/auto-mode-operating-
principles.md` §3.7(레포 비대화 대응)이 이미 실측으로 확인한 교훈("문서에
적어두는 것만으로는 재발을 못 막는다")을 그대로 적용해, 이것도 §3.8로
매 틱 확인 목록에 박아넣는다.

**이 스크립트가 하지 않는 것(정직하게)**: 크리스탈을 자동으로 만들지 않는다.
`agent-ops-framework/BLUEPRINT.md`의 편입 기준(1차 자료 확인, 도메인 지식 최소화
검증 등)은 사람 또는 AI의 판단이 필요한 품질 게이트라, 자동화하면 그 게이트
자체가 무의미해진다. 이 스크립트는 "무엇을 검토해야 하는지" 후보를 놓치지
않게 발견·누적하는 것까지만 자동화한다 — 발견(detection)과 실행(execution)을
분리하는 이 레포의 기존 원칙(quality-regression-check.py, eval-staleness-
check.sh와 동일 설계)을 그대로 따른다.

사용법:
  ./scripts/agent-ops-framework-reflection-check.py           # 체크포인트 이후 새 지시만 스캔
  ./scripts/agent-ops-framework-reflection-check.py --rescan   # 체크포인트 무시하고 전체 재스캔(후보 목록은 유지, 중복 항목만 건너뜀)

종료 코드: 항상 0 (조언용 리포트 — repo-growth-check.py와 동일 정책).
"""
import argparse
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
REGISTRY = ROOT / "docs" / "directive-registry.md"
# 2026-09-01: agent-ops-framework 전체가 ko/en 대칭 구조로 재편되며 이동
# (SSOT는 ko/ — LANGUAGE-POLICY.md 참고). 이 두 파일은 원본 프로젝트 자신의
# 실행 이력이라 번역 대상이 아니므로 ko/ 안에만 존재한다.
CHECKPOINT = ROOT / "ko" / ".reflection-checkpoint"
CANDIDATES = ROOT / "ko" / "REFLECTION-CANDIDATES.md"

# 이식 가능한 구조적 패턴을 시사하는 신호어 — 도메인 콘텐츠(가격, 지역명 등)가
# 아니라 "프로세스/규칙 자체"를 새로 만들었다는 신호. 과탐(false positive)을
# 허용하고 사람/AI 판단으로 거르는 쪽을 택한다(놓치는 것보다 나음).
SIGNAL_KEYWORDS = [
    "원칙",
    "규칙",
    "체계",
    "기준",
    "가드레일",
    "절차",
    "방법론",
    "게이트",
    "프레임워크",
    "표준",
    "패턴",
    "매트릭스",
    "루브릭",
    "검증 강도",
    "자동화",
    "파이프라인",
]

# 카테고리 추정용 키워드 — agent-ops-framework/README.md의 7개 카테고리와 대략 매칭.
# 추정일 뿐이니 결과 표에도 "추정"이라고 표시한다.
CATEGORY_HINTS = {
    "거버넌스·의사결정": ["지시", "우선순위", "결정", "책임", "권한", "위임"],
    "품질·검증": ["eval", "검증", "루브릭", "품질", "회귀", "테스트"],
    "안전·보안": ["보안", "프라이버시", "가드레일", "대외비", "기밀", "레드팀"],
    "사고대응·복원력": ["사고", "포스트모템", "장애", "복원", "디버깅"],
    "관측·자가학습": ["관측", "로그", "메트릭", "trace", "자가학습", "휴리스틱"],
    "상호작용·문서화": ["문서", "용어", "가이드", "상호작용", "UX"],
    "구조·재사용": ["구조", "템플릿", "재사용", "스캐폴딩", "모듈"],
}

# 2026-09-01 발견: 예전엔 5컬럼(6개 파이프)을 강제해 docs/directive-
# registry.md의 실제 4컬럼(| # | 내용 | 트리거 | 사용자 지시 원문 |) 행과
# 하나도 안 맞았다 — 이 스캐너가 언제나 "0건 스캔"만 내는 무한 무동작
# 상태였다는 뜻. 앞의 두 컬럼(번호, 본문)만 강제하고 나머지는 자유롭게
# 둬서, 레지스트리 표에 컬럼이 추가/삭제돼도 계속 매치되게 한다.
ROW_RE = re.compile(r"^\|\s*([0-9]+(?:\.[0-9]+)?)\s*\|\s*(.+?)\s*\|.*$")


def load_checkpoint():
    if CHECKPOINT.exists():
        try:
            return float(CHECKPOINT.read_text().strip())
        except ValueError:
            return -1.0
    return -1.0


def save_checkpoint(value):
    CHECKPOINT.write_text(f"{value}\n")


def guess_category(text):
    best, best_score = "미분류(직접 검토 필요)", 0
    for cat, hints in CATEGORY_HINTS.items():
        score = sum(1 for h in hints if h in text)
        if score > best_score:
            best, best_score = cat, score
    return best


def already_listed(entry_num_str):
    if not CANDIDATES.exists():
        return False
    return f"| {entry_num_str} |" in CANDIDATES.read_text()


def scan(min_entry):
    rows = []
    for line in REGISTRY.read_text(encoding="utf-8").splitlines():
        m = ROW_RE.match(line)
        if not m:
            continue
        num_str, body = m.group(1), m.group(2)
        try:
            num_val = float(num_str)
        except ValueError:
            continue
        if num_val <= min_entry:
            continue
        if "agent-ops-framework" in body or "agent-ops-framework" in line:
            continue  # agent-ops-framework 자신에 대한 항목은 대상 아님(이미 반영됨)
        hit_keywords = [k for k in SIGNAL_KEYWORDS if k in body]
        if not hit_keywords:
            continue
        # num_str(원문 그대로, 예: "12")을 표시·중복확인에 쓴다 — num_val
        # (float)을 그대로 쓰면 "12"가 "12.0"으로 표시돼 directive-
        # registry.md의 실제 번호 표기와 안 맞는 문제(2026-09-01 발견)가
        # 있었다. 정렬·임계값 비교에만 num_val을 쓴다.
        rows.append((num_val, num_str, body, hit_keywords))
    return rows


def append_candidates(rows):
    if not CANDIDATES.exists():
        CANDIDATES.write_text(
            "# agent-ops-framework 반영 후보 — 자동 발견, 사람/AI 검토 필요\n\n"
            "`scripts/agent-ops-framework-reflection-check.py`가 `docs/directive-"
            "registry.md`에서 이식 가능해 보이는 새 구조적 패턴을 자동으로 "
            "찾아 여기 누적한다. **크리스탈을 자동으로 만들지 않는다** — "
            "여기 있는 각 행은 검토 대상 후보일 뿐이다. `agent-ops-framework/"
            "BLUEPRINT.md`의 편입 기준을 통과해야만 실제 크리스탈이 된다.\n\n"
            "| 지시번호 | 요약(directive-registry 원문 발췌) | 신호어 | 추정 카테고리 | 상태 |\n"
            "|---|---|---|---|---|\n"
        )
    new_lines = []
    for num_val, num_str, body, keywords in rows:
        if already_listed(num_str):
            continue
        excerpt = body[:160] + ("…" if len(body) > 160 else "")
        excerpt = excerpt.replace("|", "\\|")
        category = guess_category(body)
        kw = ", ".join(keywords[:3])
        new_lines.append(
            f"| {num_str} | {excerpt} | {kw} | {category}(추정) | 검토 대기 |"
        )
    if new_lines:
        with open(CANDIDATES, "a", encoding="utf-8") as f:
            f.write("\n".join(new_lines) + "\n")
    return len(new_lines)


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument(
        "--rescan",
        action="store_true",
        help="체크포인트 무시하고 전체 재스캔(중복은 자동 건너뜀)",
    )
    args = ap.parse_args()

    if not REGISTRY.exists():
        print(f"[fatal] {REGISTRY}가 없습니다.", file=sys.stderr)
        return 1

    min_entry = -1.0 if args.rescan else load_checkpoint()
    rows = scan(min_entry)
    added = append_candidates(rows)

    max_seen = max((num_val for num_val, _, _, _ in rows), default=None)
    if max_seen is not None:
        save_checkpoint(max_seen)

    print(
        f"=== agent-ops-framework-reflection-check: {len(rows)}건 스캔, {added}건 신규 후보 추가 ==="
    )
    if added:
        print(
            f"→ {CANDIDATES.relative_to(ROOT)} 확인 — '검토 대기' 상태인 행을 사람/AI가 검토해"
        )
        print("  '반영됨(크리스탈 번호)' 또는 '반영 보류(이유)'로 상태를 갱신할 것.")
    else:
        print(
            "신규 후보 없음 — 체크포인트 이후 이식 가능한 패턴 신호가 없었거나 전부 이미 기록됨."
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
