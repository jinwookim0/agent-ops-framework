#!/usr/bin/env python3
"""agent-ops-framework-reflection-check.py — scans newly-added entries in
docs/directive-registry.md for a portable structural pattern from some
other project's (not agent-ops-framework's own) evolution that might be
worth reflecting back into agent-ops-framework, and accumulates
candidates in agent-ops-framework/REFLECTION-CANDIDATES.md.

The problem this solves: when a project that has adopted this folder
keeps evolving, it's easy to lose track of which of its new
directives/decisions are actually portable structural patterns worth
folding back into this shared collection — simply writing "let's reflect
this later" into a document doesn't prevent that from being forgotten
again (the same lesson BLUEPRINT.md section 4 already draws on). This
script automates the discovery half of that loop.

**What this script does NOT do (stated honestly)**: it never creates a
crystal automatically. agent-ops-framework/BLUEPRINT.md's admission
criteria (checking a primary source, minimizing domain knowledge, etc.)
are quality gates that require human or AI judgment — automating them
would make the gate itself meaningless. This script only automates
finding and accumulating candidates for "what needs review," never
deciding whether to admit one — the same detection/execution split this
repo's other checker scripts already follow.

Usage:
  ./scripts/agent-ops-framework-reflection-check.py           # scan only directives newer than the last checkpoint
  ./scripts/agent-ops-framework-reflection-check.py --rescan   # ignore the checkpoint and rescan everything (the candidate list is kept; duplicates are skipped)

Exit code: always 0 (advisory report).
"""
import argparse
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
REGISTRY = ROOT / "docs" / "directive-registry.md"
# These two files hold this repository's own operating history (not
# translatable content), so they live only under ko/ — consistent with
# the ko/en split the rest of this folder uses (ko is SSOT; see
# LANGUAGE-POLICY.md).
CHECKPOINT = ROOT / "ko" / ".reflection-checkpoint"
CANDIDATES = ROOT / "ko" / "REFLECTION-CANDIDATES.md"

# Signal words suggesting a portable structural pattern — signaling that a
# *process/rule itself* was newly created, not domain content (pricing,
# region names, etc.). Tolerates false positives and leaves filtering to
# human/AI judgment (better than missing a real one).
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

# Keywords for guessing a category — roughly matched against this folder's
# category list (see README.md). This is only a guess, so the result
# table also marks it "(guessed)".
CATEGORY_HINTS = {
    "거버넌스·의사결정": ["지시", "우선순위", "결정", "책임", "권한", "위임"],
    "품질·검증": ["eval", "검증", "루브릭", "품질", "회귀", "테스트"],
    "안전·보안": ["보안", "프라이버시", "가드레일", "대외비", "기밀", "레드팀"],
    "사고대응·복원력": ["사고", "포스트모템", "장애", "복원", "디버깅"],
    "관측·자가학습": ["관측", "로그", "메트릭", "trace", "자가학습", "휴리스틱"],
    "상호작용·문서화": ["문서", "용어", "가이드", "상호작용", "UX"],
    "구조·재사용": ["구조", "템플릿", "재사용", "스캐폴딩", "모듈"],
}

# Found during a self-audit: this regex used to require 5 columns (6
# pipes), which never matched docs/directive-registry.md's actual
# 4-column rows (| # | body | trigger | verbatim user directive |) — this
# scanner was silently a permanent no-op, always reporting "0 scanned."
# Now only the first two columns (number, body) are required and the rest
# are left free, so it keeps matching even if the registry table's later
# columns are added to or removed.
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
            continue  # entries about agent-ops-framework itself aren't candidates (already reflected)
        hit_keywords = [k for k in SIGNAL_KEYWORDS if k in body]
        if not hit_keywords:
            continue
        # num_str (verbatim, e.g. "12") is used for display/dedup — using
        # num_val (a float) directly would render "12" as "12.0", which
        # doesn't match directive-registry.md's actual numbering (a bug
        # found and fixed during a self-audit). num_val is only used for
        # sorting/threshold comparisons.
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
        help="ignore the checkpoint and rescan everything (duplicates are skipped automatically)",
    )
    args = ap.parse_args()

    if not REGISTRY.exists():
        print(f"[fatal] {REGISTRY} not found.", file=sys.stderr)
        return 1

    min_entry = -1.0 if args.rescan else load_checkpoint()
    rows = scan(min_entry)
    added = append_candidates(rows)

    max_seen = max((num_val for num_val, _, _, _ in rows), default=None)
    if max_seen is not None:
        save_checkpoint(max_seen)

    print(
        f"=== agent-ops-framework-reflection-check: {len(rows)} scanned, {added} new candidate(s) added ==="
    )
    if added:
        print(
            f"→ check {CANDIDATES.relative_to(ROOT)} — a human/AI should review rows marked '검토 대기' (pending review)"
        )
        print(
            "  and update their status to '반영됨(크리스탈 번호)' (adopted) or '반영 보류(이유)' (deferred, with reason)."
        )
    else:
        print(
            "No new candidates — no portable-pattern signal since the last checkpoint, or everything was already recorded."
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
