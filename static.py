"""
static.py  v2
抓取 Yahoo 奇摩股市即時報價
自動擷取台灣上市股票前 N 檔，輸出 static.json / static.csv
"""
import csv, json, re, time
from pathlib import Path
from typing import List, Dict
import requests
from bs4 import BeautifulSoup

HEADERS   = {"User-Agent": "Mozilla/5.0 (GitHub Actions HW)"}
MAX_STOCKS = 600 

ISIN_URL = "https://isin.twse.com.tw/isin/C_public.jsp?strMode=2"

def get_stock_list(n: int) -> List[str]:
    html = requests.get(ISIN_URL, headers=HEADERS, timeout=15).text
    codes = re.findall(r"<td>(\d{4})\u3000", html)
    return codes[:n]

YAHOO = "https://tw.stock.yahoo.com/quote/{}.TW"

def fetch_quote(code: str) -> Dict:
    url  = YAHOO.format(code)
    html = requests.get(url, headers=HEADERS, timeout=10).text
    m = re.search(r'"regularMarketPrice":\{"raw":([\d.]+)', html)
    price = float(m.group(1)) if m else None
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

def main():
    codes = get_stock_list(MAX_STOCKS)
    rows  = [fetch_quote(c) for c in codes]

    Path("static.json").write_text(
        json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
    with open("static.csv", "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader(); writer.writerows(rows)

if __name__ == "__main__":
    main()
