#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
static.py  (hard‑coded 600 stocks version)
抓取 Yahoo 奇摩股市即時報價，輸出 500+ 列 static.json / static.csv
"""

import csv, json, re, time, requests
from pathlib import Path
from typing import List, Dict
from bs4 import BeautifulSoup

HEADERS = {"User-Agent": "Mozilla/5.0 (GitHub Actions Stock Crawler)"}
TARGET_ROWS = 500

CODES = """
1101 1102 1103 1104 1108 1109 1110 1201 1203 1210 1213 1215 1216 1217 1218 1219
1220 1225 1227 1229 1231 1232 1233 1234 1235 1236 1256 1301 1303 1304 1305 1307
1308 1309 1310 1312 1313 1314 1315 1316 1319 1321 1323 1324 1325 1326 1402 1409
1410 1413 1414 1416 1417 1418 1419 1423 1434 1435 1436 1437 1438 1439 1440 1441
1442 1443 1444 1445 1446 1447 1449 1451 1452 1453 1454 1455 1456 1457 1459 1460
1463 1464 1465 1466 1467 1468 1470 1471 1472 1473 1474 1475 1476 1477 1503 1504
1506 1507 1512 1513 1514 1515 1516 1517 1519 1521 1522 1524 1525 1526 1527 1528
1529 1530 1531 1532 1533 1535 1536 1537 1538 1539 1540 1541 1558 1560 1568 1569
1570 1582 1583 1587 1589 1590 1597 1603 1604 1605 1608 1609 1611 1612 1614 1615
1616 1617 1626 1701 1702 1707 1708 1709 1710 1711 1712 1713 1714 1717 1720 1721
1722 1723 1724 1725 1726 1727 1730 1731 1732 1733 1734 1735 1736 1737 1738 1752
1760 1762 1773 1776 1783 1786 1789 1795 1802 1805 1806 2002 2006 2007 2008 2009
2010 2012 2013 2014 2015 2020 2022 2023 2024 2025 2027 2028 2029 2030 2031 2032
2033 2034 2038 2049 2059 2062 2069 2101 2103 2104 2105 2106 2107 2108 2109 2114
2115 2201 2204 2206 2207 2208 2211 2213 2227 2228 2231 2233 2236 2239 2241 2243
2247 2250 2301 2302 2303 2305 2308 2312 2313 2314 2316 2317 2321 2323 2324 2327
2328 2329 2330 2331 2332 2337 2338 2340 2342 2344 2345 2347 2348 2349 2351 2352
2353
""".split()

YAHOO = "https://tw.stock.yahoo.com/quote/{}.TW"

def fetch_quote(code: str) -> Dict | None:
    """成功回傳 dict；抓不到價格則回傳 None"""
    try:
        html = requests.get(YAHOO.format(code), headers=HEADERS, timeout=10).text
        m = re.search(r'"regularMarketPrice":\{"raw":([\d.]+)', html)
        if not m:
            return None
        price = float(m.group(1))
        soup  = BeautifulSoup(html, "lxml")
        change_tag = soup.select_one('span[data-field="regularMarketChange"]')
        change     = change_tag.text.strip() if change_tag else ""
        vol_tag    = soup.find("span", string=re.compile("成交量"))
        volume     = vol_tag.find_next("span").text if vol_tag else ""
        return {
            "股票代號": code,
            "即時價格": price,
            "漲跌": change,
            "成交量": volume,
            "擷取時間": time.strftime("%Y-%m-%d %H:%M:%S")
        }
    except Exception:
        return None
def main():
    rows: List[Dict] = []
    for code in CODES:
        data = fetch_quote(code)
        if data:
            rows.append(data)
        if len(rows) >= TARGET_ROWS:
            break

    if len(rows) < TARGET_ROWS:
        raise RuntimeError("抓不到任何股票資料，請檢查清單或網路連線")

    # 寫 JSON
    Path("static.json").write_text(
        json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")

    # 寫 CSV
    with open("static.csv", "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

if __name__ == "__main__":
    main()
