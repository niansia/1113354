#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
static.py  (3 stocks)
抓取 Yahoo 奇摩股市即時報價：2330、2317、2454
"""
import json, csv, re, time, requests
from pathlib import Path
from bs4 import BeautifulSoup

HEADERS = {"User-Agent": "Mozilla/5.0 (GitHub Actions HW)"}
STOCKS  = ["2330", "2317", "2454"]
URL     = "https://tw.stock.yahoo.com/quote/{}.TW"

def fetch(code):
    html = requests.get(URL.format(code), headers=HEADERS, timeout=10).text
    m    = re.search(r'"regularMarketPrice":\{"raw":([\d.]+)', html)
    price = float(m.group(1)) if m else None
    soup  = BeautifulSoup(html, "lxml")
    chg   = soup.select_one('span[data-field=\"regularMarketChange\"]')
    vol   = soup.find("span", string=re.compile("成交量"))
    return {
        "股票代號": code,
        "即時價格": price,
        "漲跌": chg.text.strip() if chg else "",
        "成交量": vol.find_next("span").text if vol else "",
        "擷取時間": time.strftime("%Y-%m-%d %H:%M:%S")
    }

rows = [fetch(s) for s in STOCKS]
Path("static.json").write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
with open("static.csv", "w", newline="", encoding="utf-8-sig") as f:
    csv.DictWriter(f, fieldnames=rows[0].keys()).writerows(rows)
