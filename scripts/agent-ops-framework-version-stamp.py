#!/usr/bin/env python3
"""agent-ops-framework-version-stamp.py — bumps a ko/ crystal's semantic
version and recomputes its content hash.

2026-09-01 신설. 계기: "버저닝이 세맨틱하거나 커밋이 있는 등 유니크한
해시여야 하지 않을까" — 처음 만든 순정수 버전(`**버전**: 1`)은 (a) 변경의
성격(사소한 수정 vs 근본적 변경)을 전달 못하고, (b) 사람이 버전을 실제로
올렸는지 기계적으로 검증할 방법이 없었다. 그래서 둘을 합친다:

- **세맨틱 버전**(major.minor.patch) — 사람/AI의 판단이 필요한 축. 이
  크리스탈을 이식해 쓰는 다른 프로젝트에게 "이 변경이 재검토할 만큼
  중요한가"를 전달한다.
  - major: 원칙 자체가 바뀌거나 뒤집힘(드묾)
  - minor: 새 메커니즘/절이 추가됨(원칙은 그대로, 범위가 넓어짐)
  - patch: 표현·오타·링크 수정(의미 변화 없음)
- **콘텐츠 해시**(sha256, 본문 기준) — 판단이 필요 없는 축, 기계적으로
  100% 재현 가능하다. **이 저장소의 git 이력과 무관하게** 계산되므로,
  이 크리스탈 파일 하나를 복사-붙여넣기해서 다른 프로젝트로 가져간
  경우에도(BLUEPRINT.md 7절의 "이식") 그 사본이 원본과 바이트 단위로
  같은지 대조할 수 있다 — git 커밋 해시 기반 스탬프(translated-from)가
  이 저장소 밖에서는 무의미해지는 문제를 정확히 이걸로 보완한다.

해시 대상: 버전/해시 헤더 두 줄을 제외한 나머지 전체 본문(자기 자신을
참조하는 해시가 되지 않도록).

사용법:
  ./scripts/agent-ops-framework-version-stamp.py <파일> --bump=major|minor|patch
  ./scripts/agent-ops-framework-version-stamp.py <파일> --recompute-hash-only
     (버전은 그대로 두고 해시만 다시 계산 — 해시가 안 맞을 때 대조용)

이 스크립트는 무엇을 "실질적 변경"으로 볼지 판단하지 않는다 — bump 수준은
호출하는 사람/AI가 매번 명시적으로 골라야 한다(기본값 없음, 침묵하는
자동판단을 만들지 않는다).
"""
import argparse
import hashlib
import pathlib
import re
import sys

VERSION_RE = re.compile(r"^\*\*버전\*\*:\s*(\d+)\.(\d+)\.(\d+)\s*$", re.MULTILINE)
HASH_RE = re.compile(
    r"^\*\*콘텐츠 해시\*\*:\s*sha256:([0-9a-f]{12})\s*\(.*\)\s*$", re.MULTILINE
)


def compute_hash(body: str) -> str:
    return hashlib.sha256(body.encode("utf-8")).hexdigest()[:12]


def strip_header(text: str) -> tuple[list[str], int | None, int | None]:
    """Returns (lines, v_idx, h_idx) — lines is the file split on "\n", and
    v_idx/h_idx are the indices of the **버전**/**콘텐츠 해시** lines
    (None if not found), used both to locate them for replacement and to
    exclude them from the hash input.

    Raises SystemExit if either pattern matches more than once — silently
    keeping "last match wins" would let a second, unrelated line that
    happens to match (e.g. a worked-example header quoted elsewhere in the
    file) get bumped/hashed instead of the real header."""
    lines = text.split("\n")
    v_idx = h_idx = None
    v_count = h_count = 0
    for i, line in enumerate(lines):
        if VERSION_RE.match(line):
            v_idx = i
            v_count += 1
        if HASH_RE.match(line):
            h_idx = i
            h_count += 1
    if v_count > 1 or h_count > 1:
        print(
            f"오류: **버전**/**콘텐츠 해시** 패턴이 파일 안에 2번 이상 나타남 "
            f"(버전 {v_count}회, 해시 {h_count}회) — 어느 줄이 진짜 헤더인지 "
            "기계적으로 판단할 수 없다. 중복을 없앤 뒤 다시 시도할 것.",
            file=sys.stderr,
        )
        sys.exit(1)
    return lines, v_idx, h_idx


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("file", type=pathlib.Path)
    group = ap.add_mutually_exclusive_group(required=True)
    group.add_argument("--bump", choices=["major", "minor", "patch"])
    group.add_argument("--recompute-hash-only", action="store_true")
    args = ap.parse_args()

    text = args.file.read_text(encoding="utf-8")
    lines, v_idx, h_idx = strip_header(text)
    if v_idx is None or h_idx is None:
        print(
            f"오류: {args.file}에서 **버전**/**콘텐츠 해시** 줄을 못 찾음 — 먼저 헤더를 만들어야 한다.",
            file=sys.stderr,
        )
        return 1

    m = VERSION_RE.match(lines[v_idx])
    major, minor, patch = int(m.group(1)), int(m.group(2)), int(m.group(3))

    if args.bump == "major":
        major, minor, patch = major + 1, 0, 0
    elif args.bump == "minor":
        minor, patch = minor + 1, 0
    elif args.bump == "patch":
        patch += 1

    # body = everything except the two header lines
    body_lines = [l for i, l in enumerate(lines) if i not in (v_idx, h_idx)]
    body = "\n".join(body_lines)
    new_hash = compute_hash(body)

    lines[v_idx] = f"**버전**: {major}.{minor}.{patch}"
    lines[h_idx] = f"**콘텐츠 해시**: sha256:{new_hash} (본문 기준, 이 두 줄 제외)"

    args.file.write_text("\n".join(lines), encoding="utf-8")
    print(f"{args.file}: v{major}.{minor}.{patch}, sha256:{new_hash}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
