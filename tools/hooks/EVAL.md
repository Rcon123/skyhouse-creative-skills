# hook-writer eval

One row per run. `pass` = the gate passed the hook and none of the extra checks fired (see `eval_score.py`). Rerun the same five inputs after every skill edit; keep the edit only if the number moves and nothing else got worse.

| date | run | pass | per offer | what failed |
|---|---|---|---|---|
| 2026-11-06 | baseline, skill as of 11-06 | **144/156 (92%)** | akka 34/34 · cloud9 29/32 · olavita 23/30 · osteoshield 28/30 · prodenta 30/30 | SC-12 12 |
| 2026-11-06 | baseline, stranger read (63-year-old on her phone) | **16/50 stopped her** | akka 3/10 · cloud9 2/10 · olavita 5/10 · osteoshield 4/10 · prodenta 2/10 | reread 13/50 |
