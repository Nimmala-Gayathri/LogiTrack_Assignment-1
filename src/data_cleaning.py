from pathlib import Path
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
def run():
    raw=ROOT/"data/raw"; out=ROOT/"data/cleaned"; out.mkdir(parents=True,exist_ok=True)
    for p in raw.glob("*.csv"):
        df=pd.read_csv(p).drop_duplicates()
        df.columns=[c.strip().lower() for c in df.columns]
        for c in df.select_dtypes("object"): df[c]=df[c].astype("string").str.strip()
        for c in [x for x in df.columns if x.endswith("_dt") or x=="join_date"]: df[c]=pd.to_datetime(df[c],errors="coerce")
        df.to_csv(out/p.name,index=False); print(p.name,df.shape)
if __name__=="__main__": run()
