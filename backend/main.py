import json
import os
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo

from fastapi import FastAPI
from pydantic import BaseModel
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from chartink_client import fetch_results

app = FastAPI(title="NSE Breakout Alert Pro")
scheduler = AsyncIOScheduler(timezone="Asia/Kolkata")
STATE_FILE = Path(os.getenv("STATE_FILE", "scanner_state.json"))
state = {
    "enabled": False,
    "last_checked": None,
    "last_error": None,
    "current_symbols": [],
    "alerts": [],
}

def load_seen():
    if STATE_FILE.exists():
        try:
            return set(json.loads(STATE_FILE.read_text()).get("seen_symbols", []))
        except Exception:
            pass
    return set()

seen_symbols = load_seen()

def save_seen():
    STATE_FILE.write_text(json.dumps({"seen_symbols": sorted(seen_symbols)}))

def market_is_open():
    now = datetime.now(ZoneInfo("Asia/Kolkata"))
    # NSE regular cash session, weekdays only. Holiday calendar should be added for production.
    return now.weekday() < 5 and (now.hour, now.minute) >= (9, 15) and (now.hour, now.minute) < (15, 30)

async def scan_job():
    if not state["enabled"] or not market_is_open():
        return
    try:
        rows = fetch_results()
        symbols = {r["symbol"] for r in rows}
        new_symbols = symbols - seen_symbols
        # Alert once when a symbol first appears. It can alert again only after it
        # disappears from results and later re-enters (tracked by current set).
        for row in rows:
            if row["symbol"] in new_symbols:
                alert = {**row, "detected_at": datetime.now(ZoneInfo("Asia/Kolkata")).isoformat()}
                state["alerts"].insert(0, alert)
                print("NEW STOCK ALERT:", alert, flush=True)
        # Remove symbols that have left the scanner so a later re-entry can alert again.
        seen_symbols.intersection_update(symbols)
        seen_symbols.update(symbols)
        save_seen()
        state["current_symbols"] = sorted(symbols)
        state["last_checked"] = datetime.now(ZoneInfo("Asia/Kolkata")).isoformat()
        state["last_error"] = None
    except Exception as exc:
        state["last_error"] = str(exc)
        print("SCAN ERROR:", repr(exc), flush=True)

class Toggle(BaseModel):
    enabled: bool

@app.on_event("startup")
async def startup():
    scheduler.add_job(scan_job, "interval", minutes=5, id="chartink_scan", replace_existing=True)
    scheduler.start()

@app.on_event("shutdown")
async def shutdown():
    scheduler.shutdown(wait=False)

@app.get("/health")
async def health():
    return {"ok": True, "provider": "Chartink public screener reader", "live_notifications": "not configured"}

@app.post("/scanner")
async def set_scanner(body: Toggle):
    state["enabled"] = body.enabled
    return {"enabled": state["enabled"]}

@app.get("/scanner/status")
async def status():
    return {**state, "interval_minutes": 5, "market_hours_only": True}

@app.post("/scan-once")
async def scan_once():
    await scan_job()
    return await status()
