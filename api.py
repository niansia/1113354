#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
api.py
呼叫 TWSE STOCK_DAY API 取得當月逐日行情，輸出 api.csv
"""
import requests, csv, time
from pathlib import Path
from typing import List

API_TPL = ("https://www.twse.com.tw/exchangeReport/STOCK_DAY"
           "?response=json&date={date}&stockNo={code}")
STOCKS  = ["2330", "2317", "2454"]          # ← 想抓別的股票直接改這裡

def fetch_month(code: str) -> List[List[str]]:
    """回傳某股票當月每日資料 (list of list)"""
    yyyymm = time.strftime("%Y%m") + "01"    # e.g. 20250301
    url    = API_TPL.format(date=yyyymm, code=code)
    data   = requests.get(url, timeout=10).json()
    return [[code] + row[:9]                 # 加上股票代號欄
            for row in data.get("data", [])]

def main():
    rows: List[List[str]] = []
    for code in STOCKS:
        rows += fetch_month(code)

    header = ["股票代號", "日期", "成交股數", "成交金額", "開盤價",
              "最高價", "最低價", "收盤價", "漲跌價差", "成交筆數"]
    with open("api.csv", "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f); writer.writerow(header); writer.writerows(rows)

if __name__ == "__main__":
    main()
