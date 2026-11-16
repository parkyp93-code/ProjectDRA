# -*- coding: utf-8 -*-
"""2080-12 드라크마 연합 편제 갱신 (Turn 44, /jump 10년).
연합(union) 진영에만 적용: 서사 교체(EXPLICIT) + 정년 자동 교체(org_2060과 같은 규칙, YEAR=2080, seed 2080).
"""
import random, re
import org_2060 as base

YEAR = 2080

def H(nm, b, svc=None, mil=None, civ=None):
    d = {"nm": nm, "b": b}
    for k, v in (("svc", svc), ("mil", mil), ("civ", civ)):
        if v: d[k] = v
    return d

EXPLICIT = {
 "대통령": dict(h=H("아마라 오코예", 2026, civ="국가원수"), note="2075 2대 대통령(통일 후 세대 첫 당선, 49세). 구 제국 노동·재건성 대신 새뮤얼 오코예의 손녀. 2080-12-19 채터누가 청사 테러로 중상"),
 "진실·화해위원회": dict(t="[활동 종료 2075] 진실·화해위원회", n="—",
   note="2071-02 전 황제 증언 — '제로는 나였다'. 2074 최종 보고서: 노동교화소·세니 학살·86·존슨 관저 국가 책임 인정. 2072 전 황제 기소 → 2076 사망으로 공소기각"),
 "합참 차장": dict(h=H("이선 마로", 2021, "연합 육군", "대장"), note="전 고스트대대장(2058)·특수전사령관. 교차 보임 — 구 제국 출신"),
 "특수전사령부": dict(h=H("그레타 포크너", 2027, "연합 육군", "소장"), note="2078 마로 합참 차장 승진 후. 고스트대대 유지"),
 "고스트대대": dict(c=[{"t": "A중대 '레이스'", "h": H("제이든 모로", 2049, "연합 육군", "대위"), "n": "36", "g": "중대장 (대위)",
                        "note": "2049 세니 노동교화소 출생 — 노아 한이 받은 아기. 이름은 윌리엄에게 신장을 준 제이든 모리스에서. 전 황제가 남긴 노아의 편지 24통 상속"}]),
}

def apply(ORG_SIDES):
    u = ORG_SIDES["union"]; rng = random.Random(YEAR)
    used, succ = set(), {}
    def collect(n):
        if n.get("h"): used.add(base._base(n["h"]["nm"]))
        for c in n.get("c", []): collect(c)
    for side in ORG_SIDES.values():
        for t in side["org"].values():
            if t: [collect(n) for n in t["c"]]
    def newname():
        while True:
            nm = rng.choice(base.FIRST) + " " + rng.choice(base.LAST)
            if nm not in used: used.add(nm); return nm
    def walk(n):
        ex = EXPLICIT.get(n["t"])
        if ex:
            for k, v in ex.items(): n[k] = v
        else:
            h = n.get("h")
            if h and h.get("b"):
                lim, tgt = base._limit(h)
                if lim and YEAR - h["b"] > lim:
                    b0 = base._base(h["nm"])
                    if b0 not in succ: succ[b0] = (newname(), YEAR - tgt - rng.randint(0, 2))
                    nm, b = succ[b0]
                    nh = dict(h); nh["nm"] = nm + base._suffix(h["nm"]); nh["b"] = b
                    n["h"] = nh
                    n["note"] = ((n.get("note") + " · ") if n.get("note") else "") + f"2080 기준 후임 (전임 {b0})"
        for c in n.get("c", []): walk(c)
    for t in u["org"].values(): [walk(n) for n in t["c"]]
    u["sub"] = "통일 국가 · 2080-12 기준"
    u["forceTitle"] = "연합군 병력 배분 · 현역 약 75만 (2072 감군 완료, 모병제)"
    u["force"] = [["gulf", "연합 육군", 39, "var(--c-stars)"], ["norfolk", "연합 해군·해병", 20, "var(--c-navy)"],
                  ["pentagon", "공군·우주군", 13, "var(--c-mil)"], ["gulf", "해안경비대·특수전", 3.4, "var(--c-pra)"]]
    u["doctrine"].append(["2070년대", "2071 전 황제 증언 → 2074 진실·화해위 최종 보고 → 2076 전 황제 사망. 2072 남부 수호회 찰스턴 폭탄(31명). 2075 오코예 대통령 — 통일 후 세대. 2077 소코부 데탕트"])
    return succ
