import re, sys, copy
sys.path.insert(0, "/home/user/ProjectDRA/tools")
from org_data import ORG
from org_billets import BILLETS

def num(s):
    if "관리" in s: return None
    m = re.search(r"(\d[\d,]*(?:\.\d+)?)\s*(만)?", s)
    if not m: return None
    v = float(m.group(1).replace(",", ""))
    return int(round(v * (10000 if m.group(2) else 1)))

def cap(n):  # 기존 n 우선, 단 "비공개"는 BILLETS 추정치 사용
    b = BILLETS[n["t"]][0]
    return b if not n.get("n") or b.startswith(n["n"] + "(") else n["n"]

over, checked = [], 0
def walk(nodes, path):
    global checked
    for n in nodes:
        p = f"{path} > {n['t']}"
        kids = n.get("c", [])
        pv = num(cap(n))
        if kids and pv is not None:
            for br in ("B", "C"):
                if n.get("only") and br not in n["only"]: continue
                tot = 0
                for k in kids:
                    if k.get("only") and br not in k["only"]: continue
                    s = cap(k)
                    if "중복" in s: continue
                    v = num(s)
                    if v: tot += v
                checked += 1
                if tot > pv: over.append((p, br, tot, pv))
        walk(kids, p)
for key, tab in ORG.items(): walk(tab["c"], key)
print(f"[정원] 부모-분기 쌍 {checked}건 검사 · 하위 합 > 상위: {len(over)}건")
for o in over: print("  OVER", o)

# 보임-지휘관 계급 검사
R = {"국가원수":12,"총리급":11,"부총리급":10.5,"원수":10,"장관급":9,"대장":9,"차관급":8,"중장":8,
     "고위공무원 가급":7,"소장":7,"고위공무원 나급":6,"준장":6,"3급":5,"대령":5,"4급":4,"중령":4,
     "5급":3,"소령":3,"대위":2,"중위":1.5,"소위":1,"준위":0.5}
pat = re.compile("|".join(sorted(map(re.escape, R), key=len, reverse=True)))
bad, exc, ok = [], [], 0
def heads(h):
    if not h: return []
    if "B" in h or "C" in h: return [(k, v) for k, v in h.items()]
    return [("공통", h)]
def walk2(nodes, path):
    global ok
    for n in nodes:
        g = BILLETS[n["t"]][1]
        main, _, paren = g.partition("(")
        vals = [R[x] for x in pat.findall(main)]
        for br, h in heads(n.get("h")):
            rk = [h[k] for k in ("mil", "civ") if h.get(k)]
            if not rk: continue
            if vals and any(min(vals) <= R[r] <= max(vals) for r in rk): ok += 1
            elif any(r in pat.findall(paren) for r in rk): exc.append((n["t"], br, rk, g))
            else: bad.append((n["t"], br, rk, g))
        walk2(n.get("c", []), path)
for key, tab in ORG.items(): walk2(tab["c"], key)
print(f"[보임] 지휘관 판정 {ok + len(exc) + len(bad)}건 · 기준 범위 내 {ok} · 괄호 예외 표기 {len(exc)} · 불일치 {len(bad)}")
for e in exc: print("  EXC", e)
for b in bad: print("  BAD", b)
