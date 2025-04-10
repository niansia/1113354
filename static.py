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
2353 2354 2355 2356 2357 2358 2359 2360 2362 2363 2364 2365 2367 2368 2369 2371
2373 2374 2375 2376 2377 2379 2380 2382 2383 2385 2387 2388 2390 2392 2393 2395
2397 2399 2401 2402 2404 2405 2406 2408 2409 2412 2413 2414 2415 2417 2419 2420
2421 2423 2424 2425 2426 2427 2428 2429 2430 2431 2433 2434 2436 2438 2439 2440
2441 2442 2443 2444 2448 2449 2450 2451 2453 2454 2455 2456 2457 2458 2459 2460
2461 2462 2464 2465 2466 2467 2468 2471 2472 2474 2476 2477 2478 2480 2481 2482
2483 2484 2485 2486 2488 2489 2491 2492 2493 2495 2496 2497 2498 2501 2504 2505
2506 2509 2511 2514 2515 2516 2520 2524 2527 2528 2530 2534 2535 2536 2537 2538
2539 2540 2542 2543 2545 2546 2547 2548 2597 2601 2603 2605 2606 2607 2608 2609
2610 2611 2612 2613 2614 2615 2616 2617 2618 2701 2702 2704 2705 2706 2707 2801
2809 2812 2816 2820 2823 2832 2834 2836 2838 2841 2845 2849 2850 2851 2852 2855
2867 2880 2881 2882 2883 2884 2885 2886 2887 2888 2889 2890 2891 2892 2897 2901
2903 2904 2905 2906 2908 2910 2912 2913 2915 2923 2929 2936 2937 2939 3002 3003
3004 3005 3006 3008 3010 3011 3013 3014 3015 3016 3017 3018 3019 3021 3022 3023
3024 3025 3026 3027 3028 3029 3030 3031 3032 3033 3034 3035 3036 3037 3038 3040
3041 3042 3043 3044 3045 3046 3047 3048 3049 3050 3051 3052 3054 3055 3056 3057
3058 3059 3060 3062 3064 3066 3071 3073 3078 3081 3083 3086 3088 3089 3090 3092
3093 3094 3095 3097 3099 3105 3107 3114 3115 3118 3122 3128 3129 3130 3131 3138
3141 3149 3152 3156 3162 3163 3164 3167 3169 3171 3176 3178 3189 3207 3211 3213
3217 3218 3219 3221 3224 3226 3227 3228 3230 3231 3232 3234 3236 3252 3257 3260
3264 3265 3266 3272 3276 3282 3287 3288 3290 3293 3294 3296 3297 3305 3308 3309
3311 3312 3313 3317 3318 3321 3322 3323 3324 3325 3332 3338 3346 3349 3354 3356
3357 3360 3362 3372 3373 3374 3376 3379 3380 3383 3402 3413 3416 3419 3432 3434
3437 3441 3443 3450 3454 3455 3458 3481 3483 3484 3489 3490 3491 3492 3494 3498
3499 3501 3504 3508 3511 3512 3515 3518 3520 3521 3522 3523 3526 3527 3528 3529
3530 3532 3533 3535 3537 3540 3543 3545 3546 3548 3550 3552 3555 3556 3557 3563
3576 3579 3580 3581 3583 3587 3591 3593 3596 3605 3607 3609 3611 3615 3622 3645
3653 3661 3664 3665 3669 3673 3675 3678 3680 3684 3685 3686 3687 3689 3691 3693
3694 3698 3701 3702 3703 3704 3705 3706 3707 3708 3711 3712 3714 3715 4104 4105
4106 4107 4108 4114 4119 4120 4121 4123 4126 4127 4128 4133 4137 4141 4142 4144
4147 4153 4160 4161 4162 4163 4173 4174 4180 4183 4205 4207 4303 4304 4306 4401
4402 4406 4414 4420 4426 4429 4430 4432 4433 4434 4438 4439 4440 4442 4443 4444
4446 4449 4450 4451 4452 4455 4502 4503 4506 4510 4513 4523 4526 4527 4528 4529
4530 4532 4533 4534 4535 4536 4537 4540 4541 4542 4543 4545 4549 4550 4551 4552
4555 4557 4558 4560 4561 4562 4563 4564 4566 4568 4571 4572 4576 4577 4581 4583
4720 4721 4722 4725 4726 4728 4729 4736 4737 4739 4741 4743 4744 4745 4746 4747
4749 4755 4763 4764 4766 4767 4768 4769 4770 4771 4772 4803 4804 4806 4807 4904
4906 4912 4915 4916 4919 4923 4924 4927 4930 4933 4934 4935 4938 4939 4942 4943
4952 4958 4960 4961 4966 4971 4976 4977 4987 4994 4999
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

    Path("static.json").write_text(
        json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")

    with open("static.csv", "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

if __name__ == "__main__":
    main()
