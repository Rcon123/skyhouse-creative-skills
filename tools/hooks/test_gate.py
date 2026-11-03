#!/usr/bin/env python3
"""Runs gate.check on the fixture and asserts the exact kill ids per hook. python3 tools/hooks/test_gate.py"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import gate  # noqa: E402

EXPECT = {1: ["SC-1"], 2: ["SC-1"], 3: ["SC-2"], 4: ["WS-1"], 5: ["SC-8", "WS-2"], 6: [], 7: ["SC-10"], 8: ["SC-8"], 9: ["SC-8"]}  # SC-8: no core word (Liver, bloodwork...); SC-10 (10-29): never open on the authority (Dr./Vet/43-year)


def main():
    fx = HERE / "fixtures" / "short-cold-fixture.md"
    res = gate.check(fx.read_text(), str(fx))
    bad = 0
    for h in res["hooks"]:
        want = EXPECT[h["n"]]
        got = h["fails"]
        ok = got == want
        bad += 0 if ok else 1
        print(f"{'ok ' if ok else 'BAD'} {h['n']}. want {want} got {got}  {h['text'][:50]}")
    star = next(h for h in res["hooks"] if h["n"] == 9)
    if not star["star"]:
        print("BAD 9. star not parsed"); bad += 1
    if not any("SC-5" in s for s in res["set_fails"]):
        print("BAD set: expected SC-5 fail (9 drafted < 25)"); bad += 1
    else:
        print("ok  set: " + res["set_fails"][0])
    # header guards
    for name, text in [
        ("no header", "1. hook\n"),
        ("missing reader", "---\noffer: cloud9\nlane: short-cold\nround: 1\nangle: x\nsources: none\n---\n1. hook\n"),
        ("forbidden source", "---\noffer: cloud9\nlane: short-cold\nround: 1\nangle: x\nreader: y\nsources: strategist-references/hook-laws.md\n---\n1. hook\n"),
        ("unknown lane", "---\noffer: cloud9\nlane: yapper\nround: 1\nangle: x\nreader: y\nsources: none\n---\n1. hook\n"),
    ]:
        try:
            gate.check(text)
            print(f"BAD guard: {name} was accepted"); bad += 1
        except gate.GateError as e:
            print(f"ok  guard: {name} -> {e}")
    print("ALL AS EXPECTED" if not bad else f"{bad} PROBLEMS")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
