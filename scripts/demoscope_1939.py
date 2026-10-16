"""Scrape Demoscope's 1939 census tables (RGAE f.1562 op.336 d.607, 640) for RSFSR regions:
illiterate population and total population by sex x age x urban/rural -> literacy by cohort.
Output: data/census1939_literacy_by_region_age_sex.csv"""
import sys, re, time, csv, os, urllib.request, urllib.parse, html
sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); D = f"{ROOT}/data"
BASE = "http://www.demoscope.ru/weekly/ssp/"
def get(url, tries=4):
    for k in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            raw = urllib.request.urlopen(req, timeout=90).read()
            try: return raw.decode("cp1251")
            except UnicodeDecodeError: return raw.decode("utf-8", errors="replace")
        except Exception as e:
            if k == tries - 1: raise
            time.sleep(2 + 2*k)
def key(n):
    n = n.lower().replace("в том числе", "").replace("ё", "е")
    n = re.sub(r"\(.*?\)", "", n)
    return re.sub(r"[^а-я]", "", n)
def strip(s): return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s))).strip()
def biggest_table_rows(h):
    tables = re.findall(r"<table.*?</table>", h, re.S | re.I)
    big = max(tables, key=len)
    rows = []
    for r in re.findall(r"<tr.*?</tr>", big, re.S | re.I):
        cells = [strip(c) for c in re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>", r, re.S | re.I)]
        if cells: rows.append(cells)
    return rows
def num(s):
    s = s.replace(" ", "").replace("\xa0", "")
    return int(s) if re.fullmatch(r"-?\d+", s) else None
def norm_age(lab):
    l = lab.lower().replace("—", "-").replace("–", "-").strip()
    if "неизв" in l or "не указан" in l: return "unknown"
    if l in ("итого", "всего"): return "TOTAL"
    if "до одного" in l or l in ("0", "0 лет"): return "0"
    if "до 5" in l: return "0-5"
    m = re.fullmatch(r"(\d+)\s*(?:лет|года|год)?", l)
    if m: return m.group(1)
    m = re.fullmatch(r"(\d+)\s*-\s*(\d+)\s*(?:лет|года)?", l)
    if m: return f"{m.group(1)}-{m.group(2)}"
    m = re.fullmatch(r"(\d+)\s*(?:лет)?\s*и\s*(?:старше|более)", l)
    if m: return f"{m.group(1)}+"
    return l

# region lists
h_ill = get(BASE + "rus_ill_39.php")
ill_regs = [(int(v), strip(t)) for v, t in re.findall(r"<option[^>]*value=['\"]?(\d+)['\"]?[^>]*>(.*?)</option>", h_ill, re.S | re.I) if strip(t) and "выберите" not in strip(t)]
h_age = get(BASE + "rus_age_39.php")
form = re.search(r"<select name=\"reg\".*?</select>", h_age, re.S | re.I).group(0)
age_regs = [(int(v), strip(t)) for v, t in re.findall(r"<option[^>]*value=['\"]?(\d+)['\"]?[^>]*>(.*?)</option>", form, re.S | re.I) if strip(t) and "выберите" not in strip(t)]
age_by_name = {n: v for v, n in age_regs}
print("illiterate-table regions:", len(ill_regs), "| age-table regions:", len(age_regs))

out = []
missing = []
for rid, name in ill_regs:
    aid = age_by_name.get(name)
    if aid is None:
        cand = [n for n in age_by_name if key(n) == key(name)]
        if not cand:
            cand = [n for n in age_by_name if key(name)[:8] and key(n).startswith(key(name)[:8])]
        aid = age_by_name.get(cand[0]) if cand else None
    if aid is None:
        missing.append(name); continue
    try:
        rows_ill = biggest_table_rows(get(BASE + f"rus_ill_39.php?reg={rid}"))
        pop = {}
        for gor, area in ((3, "total"), (1, "urban"), (2, "rural")):
            rows = biggest_table_rows(get(BASE + f"rus_age_39.php?reg={aid}&gor={gor}"))
            for r in rows:
                if len(r) >= 4 and num(r[1]) is not None:
                    pop[(area, norm_age(r[0]))] = (num(r[1]), num(r[2]))
            time.sleep(0.2)
    except Exception as e:
        print("ERR", name, e); missing.append(name); continue
    # illiterate table: cols urban M,F,both | rural M,F,both | all M,F,both
    ill = {}
    for r in rows_ill:
        if len(r) >= 10 and (num(r[1]) is not None or num(r[7]) is not None):
            a = norm_age(r[0])
            ill[("urban", a)] = (num(r[1]), num(r[2])); ill[("rural", a)] = (num(r[4]), num(r[5])); ill[("total", a)] = (num(r[7]), num(r[8]))
    # population: "0-5" = ages 0..5; five-year bands 20-24 ... 65-69; "70+" = ages >= 70 (illiterate table uses these)
    def ok(s): return s and all(x is not None and x[0] is not None and x[1] is not None for x in s)
    for area in ("total", "urban", "rural"):
        s = [pop.get((area, str(a))) for a in range(0, 6)]
        if ok(s):
            pop[(area, "0-5")] = (sum(x[0] for x in s), sum(x[1] for x in s))
        for lo in range(20, 70, 5):
            s = [pop.get((area, str(a))) for a in range(lo, lo+5)]
            if ok(s):
                pop[(area, f"{lo}-{lo+4}")] = (sum(x[0] for x in s), sum(x[1] for x in s))
        s = [v for (ar, a), v in pop.items() if ar == area and (a.isdigit() and int(a) >= 70 or a.endswith("+"))
             and v[0] is not None and v[1] is not None]
        if s:
            pop[(area, "70+")] = (sum(x[0] for x in s), sum(x[1] for x in s))
    n = 0
    for (area, a), (im, if_) in ill.items():
        p = pop.get((area, a))
        if p is None: continue
        for sex, pv, iv in (("M", p[0], im), ("F", p[1], if_)):
            if pv is None or iv is None: continue
            out.append(dict(region_1939=name, area=area, sex=sex, age=a, population=pv, illiterate=iv, literate=pv - iv,
                            literacy_rate=round(100*(pv - iv)/pv, 2) if pv else None)); n += 1
    print(f"{name:45s} cells={n}")
    time.sleep(0.2)
with open(f"{D}/census1939_literacy_by_region_age_sex.csv", "w", newline="", encoding="utf-8-sig") as f:
    w = csv.DictWriter(f, fieldnames=["region_1939", "area", "sex", "age", "population", "illiterate", "literate", "literacy_rate"], delimiter=";")
    w.writeheader(); w.writerows(out)
print("rows:", len(out), "| unmatched regions:", missing)
