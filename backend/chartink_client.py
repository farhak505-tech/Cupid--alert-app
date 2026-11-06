"""
Chartink public screener reader.

Uses the publicly visible screener page to obtain a fresh CSRF token/session,
then submits the user's own scan clause to Chartink's /screener/process endpoint.
This endpoint is undocumented and may change or be rate-limited. Use only at a
modest cadence and only if consistent with Chartink's terms and policies.
"""
import requests
from bs4 import BeautifulSoup

SCREENER_URL = "https://chartink.com/screener/cupid-129"
PROCESS_URL = "https://chartink.com/screener/process"

# Reconstructed from the user's supplied scanner text and screenshot.
# Market Cap < 104000 is intentionally excluded because its toggle was OFF.
SCAN_CLAUSE = r"""( {cash} ( ( {cash} ( daily close > 52 weeks ago high and daily close >= 100 and daily close > daily max ( 250 , daily high ) * 0.99 and daily volume > 6000000 and daily close > 1 day ago high ) ) and daily close > daily ema ( daily close , 20 ) and daily ema ( daily close , 20 ) > daily ema ( daily close , 50 ) and daily ema ( daily close , 50 ) > daily sma ( daily close , 200 ) and daily rsi ( 14 ) >= 62 and daily rsi ( 14 ) <= 75 and weekly rsi ( 14 ) > 65 and weekly close > weekly sma ( daily close , 30 ) and weekly sma ( daily close , 30 ) > 5 weeks ago sma ( daily close , 30 ) and daily ^3899('length'='21','output'='val')^ > 15.8 and daily ema ( daily close , 5 ) > daily ema ( daily close , 10 ) and daily ema ( daily close , 10 ) > daily ema ( daily close , 20 ) and daily mfi ( 14 ) > 72 and daily volume > 1 day ago volume and daily cci ( 20 ) >= 100 ) )"""

def fetch_results():
    session = requests.Session()
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; NSEBreakoutAlert/0.1)",
        "X-Requested-With": "XMLHttpRequest",
    }
    page = session.get(SCREENER_URL, headers=headers, timeout=20)
    page.raise_for_status()
    soup = BeautifulSoup(page.text, "html.parser")
    token_tag = soup.select_one('meta[name="csrf-token"]')
    if not token_tag or not token_tag.get("content"):
        raise RuntimeError("Chartink page did not provide a CSRF token; page format may have changed.")
    headers["X-CSRF-TOKEN"] = token_tag["content"]
    headers["Content-Type"] = "application/x-www-form-urlencoded; charset=UTF-8"
    response = session.post(
        PROCESS_URL,
        headers=headers,
        data={"scan_clause": SCAN_CLAUSE},
        timeout=30,
    )
    response.raise_for_status()
    payload = response.json()
    rows = payload.get("data")
    if not isinstance(rows, list):
        raise RuntimeError("Unexpected Chartink response; no results array returned.")
    cleaned = []
    for row in rows:
        symbol = (row.get("nsecode") or "").strip().upper()
        if not symbol:
            continue
        cleaned.append({
            "symbol": symbol,
            "name": row.get("name") or symbol,
            "price": row.get("close"),
            "change_percent": row.get("per_chg"),
            "volume": row.get("volume"),
        })
    return cleaned
