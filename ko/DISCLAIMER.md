# 고지문(Disclaimer) 템플릿

> 🌐 **[Read in English](../en/DISCLAIMER.md)**

이 파일은 [35-personal-oss-employer-confidentiality-separation.md](35-personal-oss-employer-confidentiality-separation.md)가
정리한 실무 관행(Google 공식 오픈소스 공개 가이드라인 확인 — "업무 관련
여부와 무관하게 사이드 프로젝트에도 필수 고지문을 포함한다")을 실제로
바로 쓸 수 있는 문구로 만든 것이다. 크리스탈 35가 "왜, 어떻게" 분리하는지의
방법론이라면, 이 파일은 그 방법론이 만들어내는 **산출물 하나**다 — 번호
매긴 크리스탈 목록에 넣지 않고 `README.md`/`BLUEPRINT.md`처럼 폴더
최상위에 별도로 둔 이유는, 이건 "배우는 기법"이 아니라 "그대로 게시할
문구"라서 35번 문서를 열어보지 않아도 바로 찾을 수 있어야 하기 때문이다.

## 이 폴더를 다른 프로젝트로 이식/공개할 때

아래 문구를 그 프로젝트의 최상위 `README.md`(또는 이 폴더가 저장소
루트가 됐다면 그 저장소의 루트 `README.md`) 맨 위에 넣는다 — 대괄호
부분만 채우면 된다:

> 이 [폴더/저장소]는 개인 프로젝트에서 도출된 운영 원칙 모음이며, [소속
> 조직명]의 공식 입장이 아니고 [소속 조직명]의 기밀·영업비밀을 포함하지
> 않는다.

**이 문구가 하는 일과 하지 않는 일 — 정직하게**:
- 하는 일: 독자에게 이 콘텐츠의 성격(개인 프로젝트, 비공식)을 정직하게
  알린다. Google 사례가 보여주듯, 업무 관련성과 무관하게 이 최소한의
  표시를 관행으로 두는 조직이 있다.
- 하지 않는 일: 이 문구 자체가 법적 방어막을 완성하지 않는다 — 실제로
  기밀이 섞여 있다면 고지문을 붙여도 그 사실 자체는 안 바뀐다. [35](35-personal-oss-employer-confidentiality-separation.md)의
  두 축 판단(콘텐츠 독자성 + 소속 관계상 허용 여부)과 `RISK-ANALYSIS.md`류
  문서의 실제 판단을 대체하지 않는다 — 그 판단이 끝난 뒤에 붙이는
  마지막 표시다.

## 새 프로젝트로 이식할 때

이 파일 자체는 [BLUEPRINT.md](BLUEPRINT.md) 7절이 "초기화 대상"으로
지정한 운영용 상태 파일(REFLECTION-CANDIDATES.md 등)과 다르다 — 이건
그 프로젝트의 실행 이력이 아니라 **빈칸만 채우면 되는 재사용 가능한
템플릿**이라 그대로 복사해도 안전하다(G2 통과). 대괄호 안의 조직명만
그 프로젝트에 맞게 채운다.

## 관련
- [35-personal-oss-employer-confidentiality-separation.md](35-personal-oss-employer-confidentiality-separation.md) —
  이 문구가 나온 방법론.
- `RISK-ANALYSIS.md` — 이 문구를 실제로 붙여도 되는지 판단하는 프로젝트별
  분석(이 파일과 달리 도메인 지식이 있는 명시적 예외).
