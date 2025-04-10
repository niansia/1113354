#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
static.py
抓取 Yahoo 奇摩股市（靜態 HTML）即時報價並輸出 static.json / static.csv
"""
import json, re, time, csv
from pathlib import Path
from typing import List, Dict
import requests
from bs4 import BeautifulSoup

HEADERS = {"User-Agent": "Mozilla/5.0 (GitHub Classroom HW)"}
STOCKS  = ["2330", "2317", "2454"]          # ← 想抓別的股票直接改這裡
URL_TPL = "https://tw.stock.yahoo.com/quote/{}.TW"

def parse_stock(code: str) -> Dict:
    """回傳單一股票的即時資訊 dict"""
    url   = URL_TPL.format(code)
    html  = requests.get(url, headers=HEADERS, timeout=10).text
    soup  = BeautifulSoup(html, "lxml")

    # Yahoo 會把即時價格塞進一段 <script> JSON；用正規式直接抓
    m = re.search(r'"regularMarketPrice":\{"raw":([\d.]+),"fmt":"([\d.,]+)"\}', html)
    price = float(m.group(1)) if m else None

    change_tag = soup.select_one('span[data-field="regularMarketChange"]')
    change     = change_tag.text.strip() if change_tag else ""

    volume_tag = soup.find("span", string=re.compile("成交量"))
    volume     = volume_tag.find_next("span").text if volume_tag else ""

    return {
        "股票代號": code,
        "即時價格": price,
        "漲跌": change,
        "成交量": volume,
        "擷取時間": time.strftime("%Y-%m-%d %H:%M:%S")
    }

def main():
    rows: List[Dict] = [parse_stock(s) for s in STOCKS]

    # 輸出 JSON
    Path("static.json").write_text(json.dumps(rows, ensure_ascii=False, indent=2))

    # 輸出 CSV
    with open("static.csv", "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader(); writer.writerows(rows)

if __name__ == "__main__":
    main()
