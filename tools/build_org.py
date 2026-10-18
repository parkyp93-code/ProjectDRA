# -*- coding: utf-8 -*-
"""org_data.py → console.fragment.html(ORG 블록) + session.json → console.fragment.html(SESSION 블록)
+ index.html(완전 문서) + factions/*.md 재생성.

SESSION_JSON 환경변수로 session.json 경로를 바꿀 수 있다(테스트용).
"""
import json, os, re, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from org_data import ORG, TABS

ROOT = pathlib.Path(__file__).resolve().parent.parent / "drachma_trpg"
FRAG = ROOT / "site" / "console.fragment.html"
INDEX = ROOT / "site" / "index.html"
SESSION_JSON = pathlib.Path(os.environ.get("SESSION_JSON") or (ROOT / "session.json"))

def head_txt(h):
    def one(x):
        s = x["nm"]
        bits = [b for b in (x.get("svc"), x.get("mil"), x.get("civ"), x.get("st")) if b]
        if bits: s += " (" + " · ".join(bits) + ")"
        return s
    if not h: return ""
    if "B" in h or "C" in h:
        b, c = h.get("B"), h.get("C")
        if b and c and one(b) == one(c): return one(c)
        return " / ".join(f"{k}: {one(v)}" for k, v in (("B", b), ("C", c)) if v)
    return one(h)

def md_tree(nodes, depth=0):
    out = []
    for n in nodes:
        line = "  " * depth + f"- **{n['t']}**"
        if n.get("only"): line += f" `분기 {'/'.join(n['only'])} 한정`"
        meta = [x for x in (head_txt(n.get("h")), n.get("n") and f"인원 {n['n']}", n.get("loc") and f"📍{n['loc']}") if x]
        if meta: line += " — " + " · ".join(meta)
        if n.get("note"): line += f"  \n" + "  " * depth + f"  _{n['note']}_"
        out.append(line)
        out += md_tree(n.get("c", []), depth + 1)
    return out

def md_section(key):
    o = ORG[key]
    return [f"## {o['t']}", f"> {o['sub']}", ""] + md_tree(o["c"]) + [""]

HDR = "> last_sync: Turn 0 · 자동 생성: `python3 tools/build_org.py` (원본 `tools/org_data.py`) — 직접 수정 금지\n> 표기: 단일 값은 B·C 공통, `B: … / C: …`는 분기별 상이. 분기점 A(1998-02-14)에는 연방 편제가 존재하지 않음.\n"

RANK_MD = """## 계급 체계 (대한민국 국군 편제 동기화)
| 구분 | 계급 |
|---|---|
| 장성 | 원수 · 대장 · 중장 · 소장 · 준장 |
| 영관 | 대령 · 중령 · 소령 |
| 위관 | 대위 · 중위 · 소위 · 준위 |
| 부사관 | 원사 · 상사 · 중사 · 하사 |
| 병 | 병장 · 상병 · 일병 · 이병 |

## 공무원 계급 (대한민국 공무원 편제 동기화)
| 구분 | 계급 | 군 상응(의전·대우 참고) |
|---|---|---|
| 정무직 | 국가원수(총통) | — |
| 정무직 | 총리급 · 부총리급 | 원수 |
| 정무직 | 장관급 | 대장 |
| 정무직 | 차관급 | 중장 |
| 고위공무원단 | 가급 (구 1급) | 소장 |
| 고위공무원단 | 나급 (구 2급) | 준장 |
| 일반직 | 3급 부이사관 | 대령 |
| 일반직 | 4급 서기관 | 중령 |
| 일반직 | 5급 사무관 | 소령 |
| 일반직 | 6급 주사 | 대위 |
| 일반직 | 7급 주사보 | 중위 · 소위 |
| 일반직 | 8급 서기 | 준위 · 상사 |
| 일반직 | 9급 서기보 | 중사 · 하사 |
"""

files = {
 "factions/government.md": ["# 국가 최고기구 · 연방 행정부", HDR] + md_section("state") + md_section("gov") + [RANK_MD.split("## 공무원")[0] and "## 공무원" + RANK_MD.split("## 공무원")[1]],
 "factions/military.md": ["# 드라크마 연방군 (Federal Armed Forces)", HDR, RANK_MD.split("## 공무원")[0]] + md_section("mil"),
 "factions/intelligence.md": ["# 정보기관 · 군 정보·방첩", HDR] + md_section("intel") + md_section("milintel"),
 "factions/praetorian.md": ["# 흑수리 친위군", HDR] + md_section("guard") + ["_국가비상동원위원회·최고감찰원은 `government.md` 참조._", ""],
}
for rel, lines in files.items():
    (ROOT / rel).write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")

# console.fragment.html ORG 블록 교체
src = FRAG.read_text(encoding="utf-8")
js = "const ORG = " + json.dumps(ORG, ensure_ascii=False) + ";\nconst ORG_TABS = " + json.dumps(TABS, ensure_ascii=False) + ";\n"
src, k = re.subn(r"const ORG = .*?\n(?=const SESSION = |const DAM = \[)", lambda m: js + "\n", src, count=1, flags=re.S)
assert k == 1, "ORG block not found"

# console.fragment.html SESSION 블록 교체 (없으면 ORG 블록 바로 뒤에 삽입)
SESSION = json.loads(SESSION_JSON.read_text(encoding="utf-8"))
SESSION = {k: v for k, v in SESSION.items() if k != "_doc"}
sjs = "const SESSION = " + json.dumps(SESSION, ensure_ascii=False).replace("</", "<\\/") + ";\n"
src, k = re.subn(r"^const SESSION = .*\n", lambda m: sjs, src, count=1, flags=re.M)
if k == 0:
    src, k = re.subn(r"(?=const DAM = \[)", lambda m: sjs + "\n", src, count=1)
assert k == 1, "SESSION insertion point not found"
FRAG.write_text(src, encoding="utf-8")

# index.html (완전 문서) 생성
head, body = src.split("</style>", 1)
INDEX.write_text(
    '<!doctype html>\n<html lang="ko">\n<head>\n<meta charset="utf-8">\n'
    '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
    '<style>[hidden]{display:none!important}img{max-width:100%}</style>\n'
    + head + "</style>\n</head>\n<body>" + body.rstrip() + "\n</body>\n</html>\n", encoding="utf-8")
print("built:", ", ".join(files), "+ site/index.html")
print(f"session: {SESSION_JSON} · branch {SESSION.get('branch') or '-'} · turn {SESSION.get('turn', 0)} · history {len(SESSION.get('history') or [])}건")
