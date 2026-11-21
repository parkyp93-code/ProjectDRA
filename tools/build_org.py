# -*- coding: utf-8 -*-
"""평행우주 B 빌드: tools/org_b.py(ORG) + tools/universe_b.py(세계 데이터) + drachma_trpg/session.json
→ site/console.fragment.html(주입) + site/index.html(완전 문서) + factions/*.md.

주입 지점(console.fragment.html):
  /* @@UNIVERSE_DATA_START */ ... /* @@UNIVERSE_DATA_END */  ← universe_b.py 상수 + ORG/ORG_TABS/ORG_SIDES
  const SESSION = ...;                                       ← session.json
SESSION_JSON 환경변수로 session.json 경로를 바꿀 수 있다(테스트용).
평행우주 A의 원본은 archive/universe_A/universe_A.tar.gz 에 봉인되어 있다.
"""
import json, os, re, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from org_b import ORG, TABS
import universe_b as U

ROOT = pathlib.Path(__file__).resolve().parent.parent / "drachma_trpg"
FRAG = ROOT / "site" / "console.fragment.html"
INDEX = ROOT / "site" / "index.html"
SESSION_JSON = pathlib.Path(os.environ.get("SESSION_JSON") or (ROOT / "session.json"))

def j(v): return json.dumps(v, ensure_ascii=False).replace("</", "<\\/")

# ── factions/*.md ──
def head_txt(h):
    if not h: return ""
    s = h["nm"]; bits = [b for b in (h.get("svc"), h.get("mil"), h.get("civ")) if b]
    if h.get("b"): bits.append(f"{h['b']}년생")
    return s + (" (" + " · ".join(bits) + ")" if bits else "")

def md_tree(nodes, depth=0):
    out = []
    for n in nodes:
        line = "  " * depth + f"- **{n['t']}**"
        meta = [x for x in (head_txt(n.get("h")), n.get("n") and f"정원 {n['n']}", n.get("g") and f"보임 {n['g']}", n.get("loc") and f"📍{n['loc']}") if x]
        if meta: line += " — " + " · ".join(meta)
        if n.get("note"): line += "  \n" + "  " * depth + f"  _{n['note']}_"
        out.append(line); out += md_tree(n.get("c", []), depth + 1)
    return out

def md_section(key):
    o = ORG[key]
    return [f"## {o['t']}", f"> {o['sub']}", ""] + md_tree(o["c"]) + [""]

HDR = "> 평행우주 B · 1976-06 기준 · 자동 생성: `python3 tools/build_org.py` (원본 `tools/org_b.py`) — 직접 수정 금지. 인물은 가상, 기관·지명은 실재.\n"
FILES = {
 "factions/government.md": ["# 백악관·행정부·의회 (평행우주 B, 1976)", HDR] + md_section("state") + md_section("gov"),
 "factions/military.md": ["# 미군 — 합참·통합사령부·해군 (평행우주 B, 1976)", HDR] + md_section("mil") + md_section("navy"),
 "factions/intelligence.md": ["# 정보기관 (평행우주 B, 1976)", HDR] + md_section("intel"),
 "factions/soviet.md": ["# 소비에트 연방 — 주적 (평행우주 B, 1976)", HDR] + md_section("ussr"),
}
fdir = ROOT / "factions"
for old in fdir.glob("*.md"):
    if f"factions/{old.name}" not in FILES: old.unlink()
for rel, lines in FILES.items():
    (ROOT / rel).write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")

# ── 콘솔 주입 ──
names = ["UNIVERSE", "BORN", "BRANCH", "FAC_NAME", "PEOPLE", "EDGES", "REG", "PTS", "EVENTS", "TIMELINE", "STATS", "HP_MOD", "GRADE", "STACK", "STRATEGIC", "OPENING"]
block = "".join(f"const {k} = {j(getattr(U, k))};\n" for k in names)
block += f"const ORG = {j(ORG)};\nconst ORG_TABS = {j(TABS)};\nconst ORG_SIDES = {{}};\n"
src = FRAG.read_text(encoding="utf-8")
src, k = re.subn(r"/\* @@UNIVERSE_DATA_START \*/.*?/\* @@UNIVERSE_DATA_END \*/",
                 lambda m: "/* @@UNIVERSE_DATA_START */\n" + block + "/* @@UNIVERSE_DATA_END */", src, count=1, flags=re.S)
if k != 1: raise SystemExit("console.fragment.html에 /* @@UNIVERSE_DATA_START */ … /* @@UNIVERSE_DATA_END */ 블록이 없습니다.")
SESSION = json.loads(SESSION_JSON.read_text(encoding="utf-8"))
SESSION = {k: v for k, v in SESSION.items() if k != "_doc"}
src, k = re.subn(r"^const SESSION = .*\n", lambda m: f"const SESSION = {j(SESSION)};\n", src, count=1, flags=re.M)
if k != 1: raise SystemExit("const SESSION 줄을 찾지 못했습니다.")
FRAG.write_text(src, encoding="utf-8")

head, body = src.split("</style>", 1)
INDEX.write_text('<!doctype html>\n<html lang="ko">\n<head>\n<meta charset="utf-8">\n'
    '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
    '<style>[hidden]{display:none!important}img{max-width:100%}</style>\n'
    + head + "</style>\n</head>\n<body>" + body.rstrip() + "\n</body>\n</html>\n", encoding="utf-8")

def count(nodes): return sum(1 + count(n.get("c", [])) for n in nodes)
print("built:", ", ".join(FILES), "+ site/index.html")
print(f"org: 노드 {sum(count(t['c']) for t in ORG.values())}개 · 탭 {len(TABS)}")
print(f"session: {SESSION_JSON.name} · universe {SESSION.get('universe')} · turn {SESSION.get('turn', 0)} · history {len(SESSION.get('history') or [])}건")
