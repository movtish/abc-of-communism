import requests, sys, os, urllib3, pandas as pd
urllib3.disable_warnings(); sys.stdout.reconfigure(encoding="utf-8")
S = requests.Session(); S.headers["User-Agent"] = "Mozilla/5.0"
B = "https://rosstat.gov.ru/free_doc/new_site/perepis2010/croc/Documents/"
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "sources", "census2010")
os.makedirs(OUT, exist_ok=True)
for f in ["Vol4/pub-04-14.xlsx", "Vol4/pub-04-13.xlsx", "Vol3/pub-03-01.xlsx", "Vol4/pub-04-10.xlsx"]:
    p = os.path.join(OUT, os.path.basename(f))
    if not os.path.exists(p):
        r = S.get(B + f, verify=False, timeout=300); open(p, "wb").write(r.content)
    print(f, os.path.getsize(p))
    x = pd.ExcelFile(p); print("  sheets:", x.sheet_names[:12], "..." if len(x.sheet_names) > 12 else "")
    df = x.parse(x.sheet_names[0], header=None)
    print("  shape", df.shape)
    for i in range(min(14, len(df))): print("   ", [str(v)[:28] for v in df.iloc[i, :10].tolist()])
