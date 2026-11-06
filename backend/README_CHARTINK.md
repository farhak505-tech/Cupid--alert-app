# Chartink public-screener polling prototype

This version adds a five-minute backend poller for Cupid-129, using the scan
clause supplied by the user. It does not require Groww login or Chartink Premium
credentials in this prototype.

## Important limitations
- `/screener/process` is an undocumented Chartink endpoint, not a supported public API.
  Chartink may change it, block automated requests, or restrict its use. Confirm
  Chartink's current terms and obtain permission if required before deploying.
- The page itself is public, but automated polling is not guaranteed to be allowed
  or stable. This code does not bypass login, paywalls, or access controls.
- The 5-minute scheduler runs on a server, not reliably on Android in the background.
- This prototype logs new-symbol alerts to the backend console and exposes them in
  `/scanner/status`. Firebase push notifications and a persistent alert database
  are not yet configured.
- The scanner is reconstructed from the user's text and screenshot. Validate the
  exact ROC Gopal function name and weekly/daily candle interpretation against the
  Chartink page before relying on it.
- Chartink free data is delayed; this is not a real-time feed.
- The market-hours check excludes weekends but does not yet include NSE holidays.

## Run
```bash
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```
Open `/docs` for the API controls. Start with `POST /scanner` body `{"enabled": true}`.
Use `GET /scanner/status` to see the latest symbols and alerts.
