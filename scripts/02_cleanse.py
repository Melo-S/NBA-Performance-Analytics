
import pandas as pd
from pathlib import Path

INP = Path("data/staging/nba_reduced.csv")
OUT = Path("data/staging/nba_cleansed.csv")
if OUT.exists(): OUT.unlink()

def normalize_team_name(s):
    return str(s).strip() if pd.notna(s) else "Unknown Team"

first = True
for ch in pd.read_csv(INP, chunksize=200_000, low_memory=False):
    ch["player_name"] = ch["player_name"].astype(str).str.strip()
    ch["team"] = ch["team"].apply(normalize_team_name)
    ch["season"] = pd.to_numeric(ch["season"], errors="coerce").astype("Int64")

    for c in ["points","rebounds","assists","turnovers","fg_pct"]:
        ch[c] = pd.to_numeric(ch[c], errors="coerce").fillna(0.0).astype(float)
    ch["minutes"] = pd.to_numeric(ch["minutes"], errors="coerce").fillna(0).astype(int)

    ch.loc[ch["fg_pct"] > 1.0, "fg_pct"] = ch["fg_pct"] / 100.0
    ch = ch[(ch["fg_pct"] >= 0.0) & (ch["fg_pct"] <= 1.0)]

    ch = ch.dropna(subset=["player_name","team","season"])
    ch = ch.drop_duplicates(subset=["player_name","team","season"])

    ch.to_csv(OUT, mode="w" if first else "a", index=False, header=first)
    first = False
print("wrote", OUT)
