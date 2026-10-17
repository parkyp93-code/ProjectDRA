# ProjectDRA

대체역사 TRPG 'Project Drachma' 워크스페이스. 게임 엔진 규칙과 SSOT는 `drachma_trpg/CLAUDE.md`.

## 작업 라우팅 (`.claude/agents/`)
| 요청 | 에이전트 |
|---|---|
| 분기점 선택, 선택지·행동·대사 입력, `/roll` `/status` `/jump` — 게임 진행 | `drachma-gm` (응답을 그대로 플레이어에게 전달) |
| `/ask` 세계관 질의, 인물·경력 생성, 지휘관 교체, 연속성 감사, GM이 남긴 `[아카이비스트 동기화 필요]` | `drachma-archivist` |
| 지휘 콘솔(`drachma_trpg/site`) 기능·버그·디자인 | `drachma-console-dev` |

## 공통 규칙
- 조직 편제의 원본은 `tools/org_data.py`. `factions/*.md`와 `site/index.html`은 `python3 tools/build_org.py`로만 생성한다.
- 콘솔의 원본은 `drachma_trpg/site/console.fragment.html`. 재게시는 Artifact `https://claude.ai/artifact/VT2qJK7an7z2EAdQZ9Fm82`에 `capabilities: {sample: {}}`를 유지한 채 한다.
