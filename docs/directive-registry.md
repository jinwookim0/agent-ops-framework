# Directive Registry

이 저장소 자신의 결정·지시를 누적 색인하는 문서 — 형식과 원칙은
[`ko/02-directive-registry.md`](../ko/02-directive-registry.md) 크리스탈을
따른다. 아직 이 저장소를 관리하며 내린 결정이 없어 표가 비어 있다 —
새 결정이 생길 때마다 아래 표에 한 행씩 추가한다(번호는 영구 ID, 낮은
번호가 항상 우선한다는 뜻은 아니다 — 자세한 충돌 처리 규칙은 크리스탈
02번 참고).

`scripts/agent-ops-framework-reflection-check.py`가 이 표를 스캔해
`ko/REFLECTION-CANDIDATES.md`에 편입 후보를 자동으로 쌓는다.

| # | 지시/원칙 내용(굵게) + 실제로 뭘 했는지 | 재적용 트리거 | 사용자 지시 원문 |
|---|---|---|---|
| 1 | **history-rewriting(squash/rebase) 작업 뒤에는 반드시 `translated-from` 커밋해시 스탬프의 도달가능성(`git merge-base --is-ancestor`)을 재검사하고, 깨진 스탬프를 즉시 별도 커밋으로 복구한다** — 이번 세션 중 두 차례 squash 뒤 실제로 en/ 44개 중 37개의 스탬프가 도달 불가능한(orphan) 커밋을 가리키고 있었음을 발견. `git log -1 --format=%ct <해시>`는 로컬에 아직 gc되지 않은 dangling 커밋에도 "성공"해 조용히 통과하는 문제가 있어, `scripts/agent-ops-framework-translation-sync-check.py`에 `is_reachable()`(merge-base 기반) 검사와 `--repair` 옵션을 추가해 37건을 SSOT 파일의 실제 최신 커밋 해시로 재포인트함. | history를 재작성(squash/rebase/filter-branch/BFG)하는 모든 작업 직후 | "최근에 커밋 병합 작업들을 하다 보니 파일에 명시된 커밋 해시가 깨지는 이슈가 있을 것 같다. 그러한가? 해결하고, 이를 어떻게 방지할지 고도화 필요하다" |
