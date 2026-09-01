#!/usr/bin/env python3
"""agent-ops-framework-version-check.py — verifies each ko/ crystal's
stored content hash still matches its actual content, with no git history
required at all.

2026-09-01 신설, 같은 날 재설계. 처음엔 git -G(diff-content 검색)로 "버전
줄이 마지막으로 바뀐 시점 이후 파일이 또 바뀌었는가"를 감지했다 — 동작은
했지만 이 저장소의 git 이력에 의존했다. "버저닝이 세맨틱하거나 유니크한
해시여야 하지 않을까"라는 지적을 받아, 각 크리스탈 헤더에 **콘텐츠
해시**(sha256, 본문 기준)를 직접 박아넣는 방식으로 바꿨다 — 이제 이
스크립트는 git을 전혀 안 쓴다: 저장된 해시와 지금 이 순간 파일 본문을
다시 해시한 값이 같은지만 비교한다. **이 저장소 밖으로 크리스탈 파일을
복사-붙여넣기한 프로젝트도 자기 자신의 사본에 대해 이 스크립트를 그대로
돌릴 수 있다** — git 이력이 전혀 필요 없기 때문이다(BLUEPRINT.md 7절의
"이식" 시나리오와 정확히 맞는 설계).

해시가 안 맞으면 = 헤더의 버전 번호를 안 올린 채로 본문이 바뀌었다는
뜻이다(사람이 실수로 버전을 안 올렸거나, 스탬프 스크립트를 안 거치고
직접 고쳤거나). 이것도 신호일 뿐이다 — 실제로 버전을 올릴 만큼 실질적인
변경인지는 사람/AI가 판단한다(발견은 자동, 판단은 사람 — BLUEPRINT.md
4절과 같은 원칙). 버전을 올리려면 agent-ops-framework-version-stamp.py를
쓴다.

**정직한 한계 — 이건 무결성(tamper-proofing) 장치가 아니라 자기일관성
(self-consistency) 검사다(2026-09-01 레드팀 감사로 명확화)**: 이 해시가
잡는 건 "본문은 바뀌었는데 헤더의 해시/버전은 그대로 남은" 경우뿐이다.
내용을 **고의로** 바꾸고 나서 agent-ops-framework-version-stamp.py를
그대로 돌려 새 해시를 다시 맞춰 넣는 사람은 이 검사를 그냥 통과한다 —
해시 알고리즘도, 그걸 계산하는 스탬프 도구도 전부 이 저장소 안에
공개돼 있어서, 아무 비밀도 필요 없이 "맞는 해시"를 누구나 다시 만들 수
있기 때문이다(체크섬과 서명의 차이와 같은 구도 — 이 해시엔 서명이
증명하는 "누가·왜 승인했는지"가 없다). 그러니 "해시 일치 = ✅"는
"버전을 깜빡하지 않고 스탬프 절차를 거쳤다"는 뜻이지 "이 변경이
검토·승인됐다"는 뜻이 아니다 — 실제 검토는 여전히 사람/AI의 몫이다.

사용법:
  ./scripts/agent-ops-framework-version-check.py

종료 코드: 항상 0 (조언용 리포트).
"""
import hashlib
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
KO_DIR = ROOT / "ko"

VERSION_RE = re.compile(r"^\*\*버전\*\*:\s*(\d+\.\d+\.\d+)\s*$", re.MULTILINE)
HASH_RE = re.compile(
    r"^\*\*콘텐츠 해시\*\*:\s*sha256:([0-9a-f]{12})\s*\(.*\)\s*$", re.MULTILINE
)

EXCLUDE = {
    "README.md",
    "BLUEPRINT.md",
    "USAGE-GUIDE.md",
    "DISCLAIMER.md",
    "LANGUAGE-POLICY.md",
    "RISK-ANALYSIS.md",
    "REFLECTION-CANDIDATES.md",
    "GLOSSARY.md",
}


def check_file(relpath: str, f: pathlib.Path):
    text = f.read_text(encoding="utf-8", errors="replace")
    lines = text.split("\n")
    v_idx = h_idx = None
    for i, line in enumerate(lines):
        if VERSION_RE.match(line):
            v_idx = i
        if HASH_RE.match(line):
            h_idx = i
    if v_idx is None or h_idx is None:
        return ("unmarked", relpath, None)

    stored_hash = HASH_RE.match(lines[h_idx]).group(1)
    version = VERSION_RE.match(lines[v_idx]).group(1)
    body = "\n".join(l for i, l in enumerate(lines) if i not in (v_idx, h_idx))
    computed_hash = hashlib.sha256(body.encode("utf-8")).hexdigest()[:12]

    if computed_hash != stored_hash:
        return ("mismatch", relpath, (version, stored_hash, computed_hash))

    # 2026-09-01 레드팀 발견: BLUEPRINT.md가 "검증 강도 표시 없는 크리스탈은
    # 존재할 수 없다"고 규정하지만, 실제로 8개 크리스탈이 본문에 🟢/🟡가
    # 전혀 없었다(README.md 집계표에만 있었음) — 단일 파일로 복사됐을 때
    # 그 정보가 통째로 사라지는 gap. 매번 사람이 눈으로 훑어 잡는 대신
    # 기계적으로 재발을 막는다.
    # ⚪는 검증 강도 등급이 아니다(BLUEPRINT.md 1절 — 유효 등급은 🟢/🟡뿐) —
    # "확인 필요/미검증"을 표시하는 별개 기호로 크리스탈 본문 여기저기서
    # 쓰이므로, 이걸 유효 배지로 인정하면 실제로 🟢/🟡가 없는 크리스탈도
    # (본문에 무관하게 등장하는 ⚪ 때문에) 이 검사를 통과하게 된다.
    if not ("🟢" in body or "🟡" in body):
        return ("no_badge", relpath, version)
    return ("ok", relpath, version)


def main() -> int:
    targets = []
    for f in sorted(KO_DIR.glob("*.md")):
        if f.name in EXCLUDE:
            continue
        targets.append((f.relative_to(ROOT).as_posix(), f))
    # 코드가 딸린 크리스탈(NN-이름/README.md 형식, 지금은 07-prompt-
    # guardrails/뿐)을 전부 찾는다 — 예전엔 "07-prompt-guardrails"
    # 경로를 하드코딩해서, 같은 패턴의 새 크리스탈 서브디렉터리가 생겨도
    # 여기 한 줄을 추가로 기억해서 고쳐야만 검사 대상에 들어갔다(2026-09-01
    # 레드팀 발견 — guardrails README 자신이 경고하는 "한쪽만 고치고 짝을
    # 잊는" 실패 패턴과 같은 종류).
    for subdir_readme in sorted(KO_DIR.glob("[0-9][0-9]-*/README.md")):
        targets.append((subdir_readme.relative_to(ROOT).as_posix(), subdir_readme))

    mismatches, unmarked, no_badge, ok = [], [], [], []
    for relpath, f in targets:
        status, rel, detail = check_file(relpath, f)
        if status == "mismatch":
            mismatches.append((rel, detail))
        elif status == "unmarked":
            unmarked.append(rel)
        elif status == "no_badge":
            no_badge.append(rel)
        else:
            ok.append((rel, detail))

    print("=== agent-ops-framework-version-check ===")
    if mismatches:
        print(
            f"\n🟡 저장된 해시와 실제 내용이 안 맞는 항목 {len(mismatches)}건 "
            "(버전을 안 올린 채로 본문이 바뀜 — 실질적 변경이면 version-stamp.py로 버전을 올릴 것):"
        )
        for rel, (version, stored, computed) in mismatches:
            print(
                f"  {rel}  (헤더는 v{version}/sha256:{stored}, 실제 본문은 sha256:{computed})"
            )
    else:
        print(f"\n✅ 저장된 해시가 전부 실제 내용과 일치함 ({len(ok)}개 확인).")

    if unmarked:
        print(f"\n⚪ 버전/해시 헤더 없음 {len(unmarked)}건:")
        for u in unmarked:
            print(f"  {u}")

    if no_badge:
        print(
            f"\n🔴 본문에 검증 강도(🟢/🟡/⚪) 표시가 전혀 없는 항목 {len(no_badge)}건 "
            "(BLUEPRINT.md 1절 위반 — README.md 집계표에만 등급이 있으면 파일 단독 복사 시 사라진다):"
        )
        for rel in no_badge:
            print(f"  {rel}")

    print(
        "\n참고: 해시 불일치는 git 이력과 무관하게 100% 기계적으로 검증된다"
        " — 이 크리스탈 파일 하나만 복사해서 다른 프로젝트로 가져간 경우에도"
        " 똑같이 쓸 수 있다. 다만 '버전을 올릴 만큼 실질적인 변경인가'는"
        " 여전히 사람/AI 판단이다(오타 수정처럼 사소한 경우 그냥 재-스탬프만"
        " 해도 됨)."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
