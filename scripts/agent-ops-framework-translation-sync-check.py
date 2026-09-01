#!/usr/bin/env python3
"""agent-ops-framework-translation-sync-check.py — checks translation sync
between agent-ops-framework/ko/ (the default SSOT) and agent-ops-framework/en/
in BOTH directions, so a contribution that lands directly in en/ (e.g. from
an English-speaking contributor who doesn't read Korean) isn't silently
discarded the next time ko/ changes. Also covers a handful of root-level
pairs outside that mirrored-folder structure (see EXTRA_PAIRS below) — so
far just the top-level landing-page README.md/README.ko.md pair, which
lives at the repo root instead of under ko//en/ so README.md can render as
GitHub's default repo homepage.

Renamed 2026-09-01 from agent-ops-framework-translation-staleness-check.py
(one-directional only) — a "-> ko/ 재편 + 진정한 오픈소스가 되려면 영문->한글
흐름도 지원해야 한다" 지시에 대응. Same detection-only philosophy as every
other checker in this family (BLUEPRINT.md 4절): flags a signal, a human/AI
still judges what to do about it.

Stamp format (first line of a translated file):
  <!-- translated-from: <commit-hash> -->
Whichever file HAS this stamp is the derived translation; whichever file
lacks it is that file's SSOT. Normally ko/NN.md has no stamp and en/NN.md
does (ko is SSOT). A file's ownership CAN be flipped per-file (rare — e.g.
a crystal originated as an English contribution) by moving the stamp onto
the ko/ file instead; this script handles either direction the same way.

Two distinct signals, not conflated:

1. STALE — the SSOT changed after the translation was stamped. Normal,
   low-stakes: re-translate from the current SSOT and re-stamp.
2. DIVERGED — the translation's own body was edited by some commit AFTER
   the commit that last set its current stamp value, without updating
   that stamp. This is the fingerprint of a direct edit landing in the
   translation (e.g. an English contributor's PR) that bypassed the
   normal "re-translate from SSOT, then re-stamp" ritual. Higher-stakes:
   this content must NOT be silently overwritten by blindly re-translating
   from the SSOT (that would discard a real contribution) — a human/AI
   must reconcile it: port the substantive change into the SSOT file,
   then re-translate SSOT -> translation and re-stamp. See
   agent-ops-framework/ko/BLUEPRINT.md section 7 for the full protocol.

Honest limitation on DIVERGED (2026-09-01 red-team review, confirmed by
direct reproduction in an isolated scratch repo): stamp_last_set_ts() only
tracks "when did the stamp *line* last change," not "was that change
actually produced by re-translating from the current SSOT." A commit that
edits *only* the stamp line — re-pointing `translated-from:` at a newer
commit hash without doing any real translation work — resets
stamp_last_set_ts to "now" and silently clears an already-correct DIVERGED
signal, while whatever unreviewed content triggered it in the first place
is left untouched and now invisible to this checker. This is not a
theoretical concern — it was reproduced end to end while auditing this
script. Deliberately not "fixed" by binding the stamp to a content hash
instead of a bare commit hash: that would raise the bar but not close the
gap, since the same untrusted party doing the re-stamping is the one who'd
need to have done the honest re-translation in the first place — so this
is documented as a known limitation of a non-cryptographic, non-signed
stamp rather than treated as a solvable bug. Treat a DIVERGED->clean
transition as informative, not as proof the underlying content was ever
actually reconciled — when in doubt, diff the translation against its SSOT
by hand rather than trusting the signal alone.

Usage:
  ./scripts/agent-ops-framework-translation-sync-check.py

Exit code: always 0 (advisory report).
"""
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
FRAMEWORK_DIR = ROOT
KO_DIR = FRAMEWORK_DIR / "ko"
EN_DIR = FRAMEWORK_DIR / "en"

STAMP_RE = re.compile(r"<!--\s*translated-from:\s*([0-9a-f]{7,40})\s*-->")
STAMP_LINE_PATTERN = r"translated-from: [0-9a-f]{7,40}"


def commit_ts(rev: str) -> int | None:
    out = subprocess.run(
        ["git", "log", "-1", "--format=%ct", rev],
        cwd=ROOT,
        capture_output=True,
        text=True,
    ).stdout.strip()
    return int(out) if out else None


def last_touch_ts(relpath: str) -> int | None:
    """Timestamp of the most recent commit that touched this path at all."""
    out = subprocess.run(
        ["git", "log", "-1", "--format=%ct", "--", relpath],
        cwd=ROOT,
        capture_output=True,
        text=True,
    ).stdout.strip()
    return int(out) if out else None


def stamp_last_set_ts(relpath: str) -> int | None:
    """Timestamp of the most recent commit that changed the stamp line's
    VALUE (added/removed a line matching the pattern) — not just any commit
    that touched the file. Uses -G (diff-content regex search), not -S,
    because the string "translated-from:" itself never changes — only the
    hash after it does, which -S's occurrence-count logic would miss."""
    out = subprocess.run(
        ["git", "log", "-1", "--format=%ct", "-G", STAMP_LINE_PATTERN, "--", relpath],
        cwd=ROOT,
        capture_output=True,
        text=True,
    ).stdout.strip()
    return int(out) if out else None


def pair_relpaths(en_file: pathlib.Path) -> tuple[str, str]:
    rel = en_file.relative_to(EN_DIR)
    ko_file = KO_DIR / rel
    return (
        ko_file.relative_to(ROOT).as_posix(),
        en_file.relative_to(ROOT).as_posix(),
    )


# Root-level pairs outside the ko//en/ mirrored-folder structure -- so far
# just the top-level landing-page README, which was split into README.md
# (English) / README.ko.md (Korean) rather than living under ko//en/ like
# every other document, since it needs to render as GitHub's default repo
# homepage. pair_relpaths() can't derive this one from a shared relative
# path, so it's listed explicitly instead. Same stamp convention applies:
# whichever file has the `translated-from` comment is the translation.
EXTRA_PAIRS = [
    ("README.md", "README.ko.md"),
]


def process_pair(rel_a: str, rel_b: str, buckets: dict) -> None:
    """Runs the STALE/DIVERGED check for one (path, path) pair -- order
    doesn't matter, since ownership (which side is the SSOT) is determined
    from which file actually carries the `translated-from` stamp, not from
    argument position. Appends results into the shared `buckets` dict so
    every pair (both the ko//en/ mirrored ones and EXTRA_PAIRS) reports
    through the same STALE/DIVERGED/unstamped/missing_pair/ok accounting."""
    file_a, file_b = ROOT / rel_a, ROOT / rel_b
    text_a = (
        file_a.read_text(encoding="utf-8", errors="replace") if file_a.exists() else ""
    )
    text_b = (
        file_b.read_text(encoding="utf-8", errors="replace") if file_b.exists() else ""
    )
    first_a = text_a.splitlines()[0] if text_a.splitlines() else ""
    first_b = text_b.splitlines()[0] if text_b.splitlines() else ""

    has_a = STAMP_RE.search(first_a)
    has_b = STAMP_RE.search(first_b)

    if has_b and not has_a:
        ssot_relpath, translation_relpath, stamp_match = (rel_a, rel_b, has_b)
    elif has_a and not has_b:
        ssot_relpath, translation_relpath, stamp_match = (rel_b, rel_a, has_a)
    elif not has_a and not has_b:
        buckets["unstamped"].append(rel_b)
        return
    else:
        # both stamped — ambiguous ownership, needs a human to fix by hand
        buckets["unstamped"].append(f"{rel_b} (양쪽 다 스탬프 있음 — 소유권 불명확)")
        return

    if not (ROOT / ssot_relpath).exists():
        buckets["missing_pair"].append((translation_relpath, ssot_relpath))
        return

    ssot_ts = last_touch_ts(ssot_relpath)
    translation_ts = last_touch_ts(translation_relpath)
    stamp_target_ts = commit_ts(stamp_match.group(1))
    stamp_set_ts = stamp_last_set_ts(translation_relpath)

    if (
        ssot_ts is None
        or translation_ts is None
        or stamp_target_ts is None
        or stamp_set_ts is None
    ):
        buckets["unstamped"].append(translation_relpath + " (커밋 조회 실패)")
        return

    is_stale = ssot_ts > stamp_target_ts
    is_diverged = translation_ts > stamp_set_ts

    if is_diverged:
        # DIVERGED takes priority even if SSOT also moved on (is_stale
        # true at the same time) -- checked first, not elif'd after
        # STALE, precisely so a real un-reconciled translation edit is
        # never silently reported as "just STALE, re-translate" (see
        # module docstring: STALE and DIVERGED must not be conflated).
        hours = (translation_ts - stamp_set_ts) / 3600
        buckets["diverged"].append((translation_relpath, ssot_relpath, hours, is_stale))
    elif is_stale:
        hours = (ssot_ts - stamp_target_ts) / 3600
        buckets["stale"].append((translation_relpath, ssot_relpath, hours))
    else:
        buckets["ok"].append(translation_relpath)


def main() -> int:
    if not EN_DIR.exists():
        print("=== agent-ops-framework-translation-sync-check ===")
        print("\n⚪ agent-ops-framework/en/ 없음 — 아직 번역이 없다. 검사할 게 없다.")
        return 0

    buckets = {
        "stale": [],
        "diverged": [],
        "unstamped": [],
        "missing_pair": [],
        "ok": [],
    }

    for en_file in sorted(EN_DIR.rglob("*.md")):
        rel_ko, rel_en = pair_relpaths(en_file)
        process_pair(rel_ko, rel_en, buckets)

    for rel_a, rel_b in EXTRA_PAIRS:
        if (ROOT / rel_a).exists() or (ROOT / rel_b).exists():
            process_pair(rel_a, rel_b, buckets)

    stale, diverged = buckets["stale"], buckets["diverged"]
    unstamped, missing_pair, ok = (
        buckets["unstamped"],
        buckets["missing_pair"],
        buckets["ok"],
    )

    print("=== agent-ops-framework-translation-sync-check ===")

    if stale:
        print(
            f"\n🔴 STALE — SSOT가 번역 시점보다 최근에 바뀐 항목 {len(stale)}건 "
            "(재번역 필요 여부는 직접 대조해 판단할 것):"
        )
        for translation_relpath, ssot_relpath, hours in stale:
            print(
                f"  {translation_relpath}  <  {ssot_relpath}  (SSOT가 {hours:.0f}시간 더 최근)"
            )

    if diverged:
        print(
            f"\n🟠 DIVERGED — 번역 파일이 스탬프 갱신 없이 직접 수정된 항목 {len(diverged)}건 "
            "(무단 재번역으로 덮어쓰지 말 것 — 반드시 사람이 반영 여부를 판단):"
        )
        for translation_relpath, ssot_relpath, hours, also_stale in diverged:
            note = (
                " — SSOT도 그 사이 추가로 바뀌었다(STALE 조건도 동시에 참)"
                if also_stale
                else ""
            )
            print(
                f"  {translation_relpath}  (스탬프 설정 이후 {hours:.0f}시간 뒤 직접 수정됨, "
                f"SSOT: {ssot_relpath}){note} — 이 변경을 SSOT로 먼저 반영한 뒤 재번역·재스탬프할 것"
            )

    if not stale and not diverged:
        print(f"\n✅ STALE도 DIVERGED도 없음 ({len(ok)}개 확인).")

    if unstamped:
        print(f"\n⚪ 스탬프 판정 불가 {len(unstamped)}건:")
        for f in unstamped:
            print(f"  {f}")

    if missing_pair:
        print(f"\n⚠️ 대응 파일이 없는 항목 {len(missing_pair)}건:")
        for translation_relpath, ssot_relpath in missing_pair:
            print(f"  {translation_relpath} -> {ssot_relpath} 없음")

    print(
        "\n참고: STALE·DIVERGED 둘 다 신호일 뿐이다 — 실제로 반영이 필요한지는"
        " 무엇이 바뀌었는지 열어서 판단한다. STALE은 보통 그냥 재번역하면 되지만,"
        " DIVERGED는 번역 쪽에 남은 실제 기여를 먼저 SSOT로 이식하지 않으면 그"
        " 기여가 사라진다 — 두 신호를 같은 방식으로 처리하지 않는다."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
