#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
static.py  (100 stocks via Yahoo Quote API)
一次抓 100 檔台股即時行情，輸出 static.json / static.csv
"""

import json, csv, time, requests
from pathlib import Path

# ---- 1. 100 檔熱門上市股代號 ----
CODES = [
    "2330","2317","2454","2603","2881","2303","2891","2882","2886","2884",
    "2609","2379","2885","2880","2311","5880","3034","2412","2605","2353",
    "1301","1303","1304","1305","2883","2890","2892","1101","1102","1103",
    "1104","1108","1109","1216","1210","1213","1215","1218","2301","2308",
    "2312","2313","2314","2316","2324","2327","2329","2337","2340","2345",
    "2347","2352","2354","2356","2357","2358","2359","2360","2362","2363",
    "2376","2382","2383","2385","2395","2397","2401","2404","2408","2409",
    "2413","2414","2415","2417","2420","2421","2458","2460","2474","2476",
    "2492","2498","2606","2607","2608","2615","2618","2801","2809","2812",
    "2820","2834","2836","2838","2845","2850","2867","2897","2912","3008",
    "3017","3035","3037","3045","3711"
]

BATCH = 20   # Yahoo API 最長可一次 50 檔，保險起見分批 20

def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i+n]

def fetch_batch(symbols):
    url = "https://query1.finance.yahoo.com/v7/finance/quote"
    qs  = ",".join(f"{s}.TW" for s in symbols)
    r   = requests.get(url, params={"symbols": qs}, timeout=10)
    return r.json()["quoteResponse"]["result"]

rows = []
for part in chunks(CODES, BATCH):
    for q in fetch_batch(part):
        rows.append({
            "股票代號": q["symbol"].replace(".TW",""),
            "即時價格": q.get("regularMarketPrice"),
            "漲跌": q.get("regularMarketChange"),
            "成交量": q.get("regularMarketVolume"),
            "擷取時間": time.strftime("%Y-%m-%d %H:%M:%S")
        })

# ---- 4. 輸出 ----
Path("static.json").write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
with open("static.csv", "w", newline="", encoding="utf-8-sig") as f:
    csv.DictWriter(f, fieldnames=rows[0].keys()).writerows(rows)
