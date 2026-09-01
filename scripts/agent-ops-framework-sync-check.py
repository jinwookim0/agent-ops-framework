#!/usr/bin/env python3
"""agent-ops-framework-sync-check.py — 크리스탈이 추출된 원본 문서가 크리스탈
자신보다 더 최근에 바뀌었는지 확인한다.

2026-09-01 신설. 계기: 사용자 지적 "왜 내가 언급해야만 그제야 빈자리나
허점을 찾는가?" — `agent-ops-framework-reflection-check.py`는 `docs/
directive-registry.md`에 새로 쌓인 지시만 스캔하는데, 이건 (a) 내가 그
스크립트를 실제로 돌려야만 작동하고, (b) 원본 문서를 고쳤다고 해서 그 즉시
대응 크리스탈을 다시 보라는 신호를 안 준다. 오늘 실제로 `docs/auto-mode-
operating-principles.md`에 ScheduleWakeup 기본동작 규칙을 추가해놓고도,
그 대응 크리스탈(05번)에 반영해야 한다는 걸 사용자가 세 번째로 물어볼
때까지 스스로 못 챙겼다 — 이 스크립트는 그 구멍을 메우는 쪽이다.

**이 스크립트가 하지 않는 것(정직하게)**: "원본 문서가 크리스탈보다 최근에
바뀌었다"는 신호일 뿐, "그러니 크리스탈을 고쳐야 한다"는 결론이 아니다.
append-only 로그류 문서(예: directive-registry.md 자신)는 내용이 계속
늘어나도 그 문서가 크리스탈에 담긴 "패턴 자체"는 안 바뀔 수 있다 — 실제로
이 스크립트 첫 실행에서 directive-registry.md가 STALE로 잡혔지만 직접 열어
대조해보니 크리스탈(02번)의 "비대화 방지" 절 내용은 여전히 정확했다(새
행이 쌓인 것뿐, 표 형식·정책 자체는 안 바뀜). 발견(자동)과 "실제로 반영이
필요한가" 판단(사람/AI)을 분리하는 이 폴더의 기존 설계(`BLUEPRINT.md` 4절)
와 같은 원칙이다.

사용법:
  ./scripts/agent-ops-framework-sync-check.py

종료 코드: 항상 0 (조언용 리포트).
"""
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

# 크리스탈 번호 → (원본 문서, 최초 추출 근거)
# 이 저장소는 agent-ops-framework 자신을 담은 독립 공개 저장소라, 크리스탈이
# 뽑혀 나온 "원본 프로젝트 문서"가 없다(크리스탈 자체가 콘텐츠의 최종
# 형태). 이 맵은 원래 "이 프레임워크를 이식받은 프로젝트가 자기 자신의
# 원본 문서 목록으로 다시 채우는" 용도다(BLUEPRINT.md 7절) — 이 저장소를
# 포크해 자신의 프로젝트에 이식한 뒤, 크리스탈을 새로 뽑을 때마다 여기
# "크리스탈 파일명": "그 프로젝트 안의 원본 문서 경로" 한 줄을 추가한다.
ORIGIN_MAP = {}

CRYSTAL_DIR = ROOT / "ko"


def last_commit_ts(relpath: str) -> int | None:
    out = subprocess.run(
        ["git", "log", "-1", "--format=%ct", "--", relpath],
        cwd=ROOT,
        capture_output=True,
        text=True,
    ).stdout.strip()
    return int(out) if out else None


def main() -> int:
    stale = []
    skipped = []
    for crystal_name, origin_relpath in sorted(ORIGIN_MAP.items()):
        crystal_relpath = f"agent-ops-framework/ko/{crystal_name}"
        if not (ROOT / crystal_relpath).exists():
            skipped.append((crystal_relpath, "크리스탈 파일 없음"))
            continue
        if not (ROOT / origin_relpath).exists():
            skipped.append((crystal_relpath, f"원본 {origin_relpath} 없음"))
            continue
        o_ts = last_commit_ts(origin_relpath)
        c_ts = last_commit_ts(crystal_relpath)
        if o_ts is None or c_ts is None:
            skipped.append((crystal_relpath, "git 이력 없음"))
            continue
        if o_ts > c_ts:
            hours = (o_ts - c_ts) / 3600
            stale.append((crystal_relpath, origin_relpath, hours))

    print("=== agent-ops-framework-sync-check ===")
    if stale:
        print(
            f"\n🔴 원본이 크리스탈보다 최근에 바뀐 항목 {len(stale)}건 "
            "(반영 필요 여부는 직접 열어 판단할 것 — 자동 결론 아님):"
        )
        for crystal_relpath, origin_relpath, hours in stale:
            print(
                f"  {crystal_relpath}  <  {origin_relpath}  (원본이 {hours:.0f}시간 더 최근)"
            )
    else:
        print("\n✅ 원본보다 오래된 크리스탈 없음.")

    if skipped:
        print(f"\n⚪ 건너뜀 {len(skipped)}건:")
        for path, reason in skipped:
            print(f"  {path}: {reason}")

    print(
        "\n참고: '원본이 더 최근'은 신호일 뿐이다. append-only 로그류 원본은"
        " 내용이 늘어도 문서화된 패턴 자체는 안 바뀔 수 있다 — 실제로 반영이"
        " 필요한지는 열어서 판단한다."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
