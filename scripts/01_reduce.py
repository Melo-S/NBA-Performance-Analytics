import pandas as pd
from pathlib import Path

RAW = Path("data/raw/nba_raw.csv")
OUT = Path("data/staging/nba_reduced.csv")
OUT.parent.mkdir(parents=True, exist_ok=True)
if OUT.exists(): OUT.unlink()

usecols = [
    "player","team","season","pts_per_game","trb_per_game",
    "ast_per_game","tov_per_game","mp_per_game","fg_percent"
]

def process_chunk(ch):
    ch = ch[usecols].copy()
    ch = ch.rename(columns={
        "player":"player_name",
        "pts_per_game":"points",
        "trb_per_game":"rebounds",
        "ast_per_game":"assists",
        "tov_per_game":"turnovers",
        "mp_per_game":"minutes",
        "fg_percent":"fg_pct"
    })
    ch["season"] = pd.to_numeric(ch["season"], errors="coerce").astype("Int64")
    ch = ch[ch["season"].between(2010, 2024)]
    ch = ch.drop_duplicates(subset=["player_name","team","season"])
    return ch

first = True
for chunk in pd.read_csv(RAW, chunksize=200_000, usecols=usecols, low_memory=False):
    out = process_chunk(chunk)
    if not out.empty:
        out.to_csv(OUT, mode="w" if first else "a", index=False, header=first)
        first = False
print("wrote", OUT)
