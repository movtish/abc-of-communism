"""Stata (stata/output/stata_results.csv) vs Python (results/paper_numbers.json), key by key -> stata/output/comparison.csv"""
import os, sys, json, numpy as np, pandas as pd
sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NUM = json.load(open(f"{ROOT}/results/paper_numbers.json", encoding="utf-8"))["NUM"]
s = pd.read_csv(f"{ROOT}/stata/output/stata_results.csv", sep=";")
rows = []
for k, b, se in zip(s.key, s.b, s.se):
    if k not in NUM: rows.append(dict(key=k, b_stata=b, se_stata=se, status="key not in paper_numbers")); continue
    bp = NUM[k][0]; sp = NUM[k + ".se"][0] if k + ".se" in NUM else np.nan
    if bp != bp and b == 0 and se == 0: rows.append(dict(key=k, b_python=bp, b_stata=b, se_python=sp, se_stata=se, status="not identified in either (omitted by Stata)")); continue
    db = abs(b - bp); dse = abs(se - sp) / sp if sp and not np.isnan(sp) and sp > 0 else np.nan
    ok_b = db <= 1e-4 * max(1.0, abs(bp)); ok_se = np.isnan(dse) or dse <= 0.03
    rows.append(dict(key=k, b_python=bp, b_stata=b, se_python=sp, se_stata=se, diff_b=db, rel_diff_se=dse, status="ok" if ok_b and ok_se else ("coefficient differs" if not ok_b else "standard error differs")))
c = pd.DataFrame(rows); c.to_csv(f"{ROOT}/stata/output/comparison.csv", sep=";", index=False, encoding="utf-8-sig")
print("coefficients compared:", len(c), "| identical:", int((c.status == "ok").sum()))
print(c.status.value_counts().to_string())
bad = c[~c.status.isin(["ok", "not identified in either (omitted by Stata)"])]
if len(bad):
    pd.set_option("display.width", 220); pd.set_option("display.max_rows", 200)
    print(bad.round(4).to_string(index=False))
else:
    print("largest difference in a coefficient:", f"{c.diff_b.max():.2e}", "| largest relative difference in a standard error:", f"{c.rel_diff_se.max():.2e}")
