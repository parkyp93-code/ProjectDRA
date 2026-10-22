# ProjectDRA

대체역사 TRPG 'Project Drachma' 워크스페이스. 게임 엔진 규칙과 SSOT는 `drachma_trpg/CLAUDE.md`.

## 작업 라우팅 (`.claude/agents/`)
| 요청 | 에이전트 |
|---|---|
| 분기점 선택, 선택지·행동·대사 입력, `/roll` `/status` `/jump` — 게임 진행 | `drachma-gm` (응답을 그대로 플레이어에게 전달) |
| 플레이어 메시지가 `--`로 시작 = 단순 질의·정보 요청 (진행·판정·시간 경과 없음). `/ask` 세계관 질의, 인물·경력 생성, 지휘관 교체, 연속성 감사, GM이 남긴 `[아카이비스트 동기화 필요]` | `drachma-archivist` |
| 지휘 콘솔(`drachma_trpg/site`) 기능·버그·디자인 | `drachma-console-dev` |

## 진행 방식
- 게임 진행(분기 선택, 선택지·자유 행동, 판정, 상태창, 시간 점프, `/ask`)은 **이 대화에서** 한다. 콘솔 사이트는 기록을 보여 주는 읽기 전용 뷰어다.
- 턴(또는 `/ask` 생성, 정합성 작업)이 끝나 `drachma_trpg/session.json`이나 SSOT가 바뀌면, 메인 대화가 아래를 수행한다.
  1. `python3 tools/build_org.py`
  2. Artifact 재게시
  3. 커밋·푸시
- 판정 결과와 서술은 `drachma-gm`의 응답을 그대로 플레이어에게 전달한다. 단, 응답 속도를 위해 일반 턴은 메인 대화가 GM 규칙(`drachma-gm.md` 서술 스타일)대로 직접 진행해도 된다.
- 서술은 소설처럼 쉽고 짧게. 메타 설명·동기화 목록은 플레이어에게 늘어놓지 않는다.

## 공통 규칙
- 조직 편제의 원본은 `tools/org_data.py`. `factions/*.md`와 `site/index.html`은 `python3 tools/build_org.py`로만 생성한다.
- 콘솔의 원본은 `drachma_trpg/site/console.fragment.html`. 재게시는 Artifact `https://claude.ai/artifact/VT2qJK7an7z2EAdQZ9Fm82`에 한다 (사이트는 더 이상 Claude를 호출하지 않으므로 capability 없음).
