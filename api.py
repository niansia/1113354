#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
api.py  (12 months × 3 stocks)
呼叫 TWSE STOCK_DAY API，抓最近 12 個月每日行情，輸出 api.csv
"""
import csv, datetime, requests
from pathlib import Path

STOCKS = ["2330", "2317", "2454"]
API_TPL = ("https://www.twse.com.tw/exchangeReport/STOCK_DAY"
           "?response=json&date={date}&stockNo={code}")

def yyyymm_dates(months_back=12):
    today = datetime.date.today().replace(day=1)
    for i in range(months_back):
        d = today - datetime.timedelta(days=30*i)
        yield d.strftime("%Y%m01")

rows = []
for code in STOCKS:
    for yyyymm in yyyymm_dates(12):
        data = requests.get(API_TPL.format(date=yyyymm, code=code), timeout=15).json()
        for row in data.get("data", []):
            rows.append([code] + row[:9])

header = ["股票代號", "日期", "成交股數", "成交金額", "開盤價",
          "最高價", "最低價", "收盤價", "漲跌價差", "成交筆數"]
with open("api.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f); writer.writerow(header); writer.writerows(rows)
