# Project Drachma

하드코어 대체역사 TRPG 엔진 워크스페이스.

- `drachma_trpg/` — GM 단일 진실 공급원(SSOT) 마크다운 DB (`CLAUDE.md`, `timeline.md`, `state.md`, `characters/`, `factions/`, `lore/`)
- `drachma_trpg/site/index.html` — 인터랙티브 지휘 콘솔 (브라우저로 바로 열기, 외부 의존성은 Google Fonts뿐)
  - 원본은 `console.fragment.html`. 조직 편제는 `tools/org_data.py`가 단일 원본이며 `python3 tools/build_org.py`로 페이지와 `factions/*.md`를 함께 재생성
  - 작전 콘솔: 플레이어는 선택지 A·B·C 또는 자유 입력만 하고, 판정 여부·스탯·보정·DC·결과 서술은 GM이 결정 (claude.ai에서 열면 Claude가 GM, 로컬 파일은 규칙 엔진)
  - 작전 지도: 지역/거점 클릭 → 브리핑 → 인물·연표 딥링크, 세계/북미/수도권/유럽 줌, 다모클레스 궤도 레이어
  - 연표 · 인물 관계도(노화 시뮬레이터) · 조직 편제(6개 기관 탭·검색, 군/공무원 계급별 현역 해당자, 병력 배분) · 다모클레스(궤도·타격 시뮬레이터) · d20 판정기/상태창
  - 상단 분기점 A/B/C 스위치가 모든 화면의 나이·계급·정세·위성 가동 수를 동기화
