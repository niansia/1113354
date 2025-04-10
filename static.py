import csv, json, re, time, requests
from pathlib import Path
from typing import List, Dict
from bs4 import BeautifulSoup

HEADERS = {"User-Agent": "Mozilla/5.0 (GitHub Actions HW)"}
MAX_STOCKS = 600

LIST_URL = "https://www.twse.com.tw/exchangeReport/MI_INDEX?response=json&date={date}&type=ALL"
def get_stock_list(n: int) -> List[str]:
    yyyymmdd = time.strftime("%Y%m%d")
    data = requests.get(LIST_URL.format(date=yyyymmdd), timeout=15).json()
    codes = [row[0].strip() for row in data.get("data5", []) if re.match(r"^\d{4}$", row[0])]
    return codes[:n]

YAHOO = "https://tw.stock.yahoo.com/quote/{}.TW"
def fetch_quote(code: str) -> Dict:
    html = requests.get(YAHOO.format(code), headers=HEADERS, timeout=10).text
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
    if not rows:
        raise RuntimeError("抓不到任何股票資料，請檢查 API 或網路連線")

    Path("static.json").write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
    with open("static.csv", "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader(); writer.writerows(rows)

if __name__ == "__main__":
    main()
