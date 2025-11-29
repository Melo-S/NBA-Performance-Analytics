
import pandas as pd, json
from pathlib import Path
import re

INP = Path("data/staging/nba_cleansed.csv")
OUT = Path("data/curated/nba_ready.jsonl")

OUT.parent.mkdir(parents=True, exist_ok=True)
if OUT.exists(): OUT.unlink()

def slug(s):
    s = re.sub(r"[^a-z0-9]+", "-", str(s).lower())
    return s.strip("-")

with open(OUT, "w", encoding="utf-8") as f:
    for ch in pd.read_csv(INP, chunksize=200_000, low_memory=False):
        for _, r in ch.iterrows():
            rec = {
                "player_id": slug(r["player_name"]),
                "player_name": r["player_name"],
                "season": int(r["season"]),
                "team": r["team"],
                "stats": {
                    "points": float(r["points"]),
                    "rebounds": float(r["rebounds"]),
                    "assists": float(r["assists"]),
                    "turnovers": float(r["turnovers"]),
                    "minutes": int(r["minutes"]),
                    "fg_pct": float(r["fg_pct"]),
                    "plus_minus": 0.0
                }
            }
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
print("wrote", OUT)
