# ProjectDRA

대체역사 TRPG 'Project Drachma' 워크스페이스. 게임 엔진 규칙과 SSOT는 `drachma_trpg/CLAUDE.md`.

## 평행우주
- **현재 진행: 평행우주 B** — 1976-06-09 시작, 주인공 드락 V. 에버하트(해군사관학교 1976기 수석). 콘솔과 모든 SSOT는 B 기준.
- **평행우주 A는 봉인된 기록 보관소**: `archive/universe_A/` (`universe_A.tar.gz` 원본 + `README.md` 요약). 진행·콘솔에 쓰지 않는다. 플레이어가 A를 물을 때만 README를 참고한다.

## 작업 라우팅 (`.claude/agents/`)
| 요청 | 에이전트 |
|---|---|
| 선택지·행동·대사 입력, `/roll` `/status` `/jump` — 게임 진행 | `drachma-gm` (응답을 그대로 플레이어에게 전달) |
| `/ask` 세계관 질의, 인물·경력 생성, 지휘관 교체, 연속성 감사 | `drachma-archivist` |
| 지휘 콘솔(`drachma_trpg/site`) 기능·버그·디자인 | `drachma-console-dev` |

## 진행 방식
- 게임 진행은 **이 대화에서** 한다. 콘솔 사이트는 기록을 보여 주는 읽기 전용 뷰어다.
- 플레이어 메시지가 `ㅁㅁ` 또는 `--`로 시작하면 단순 대화·질의다. 진행·판정·시간 경과·파일 반영 없이 바로 빠르게 답한다.
- 턴(또는 `/ask` 생성, 정합성 작업)이 끝나 `drachma_trpg/session.json`이나 SSOT가 바뀌면, 메인 대화가 아래를 수행한다.
  1. `python3 tools/build_org.py`
  2. Artifact 재게시
  3. 커밋·푸시
- 판정 결과와 서술은 `drachma-gm`의 응답을 그대로 플레이어에게 전달한다. 단, 응답 속도를 위해 일반 턴은 메인 대화가 GM 규칙(`drachma-gm.md` 서술 스타일)대로 직접 진행해도 된다.
- NPC 대사마다 `이름 [소속, 직책, 계급, 나이]`, 상태창엔 항상 나이·소속·보직·계급을 표기한다(플레이어 지시).
- 서술은 소설처럼 쉽고 짧게. 메타 설명·동기화 목록은 플레이어에게 늘어놓지 않는다.
- 인물은 모두 가상 인물로 만든다(실존 인물 이름 금지). 국가·기관·장비·지명·1976년까지의 세계사 사건은 실재를 따른다.

## 공통 규칙
- 조직 편제의 원본은 `tools/org_b.py`(평행우주 B, 1976). 콘솔 세계 데이터(인물 카드·관계·지도 지역/거점·연표·주인공 프리셋·전략 핵전력·병력 막대)의 원본은 `tools/universe_b.py`. `factions/*.md`와 `site/index.html`은 `python3 tools/build_org.py`로만 생성한다(콘솔의 `/* @@UNIVERSE_DATA_START */` 블록과 `const SESSION` 줄에 주입).
- 콘솔의 원본은 `drachma_trpg/site/console.fragment.html`. 재게시는 Artifact `https://claude.ai/artifact/VT2qJK7an7z2EAdQZ9Fm82`에 한다 (사이트는 Claude를 호출하지 않으므로 capability 없음).
