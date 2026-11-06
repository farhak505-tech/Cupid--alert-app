# Live deployment checklist

- Deploy this backend to an always-on server; do not rely on the Android app remaining open.
- Add an authenticated API and persistent database for scanner state and alert deduplication.
- Add a five-minute scheduler restricted to NSE market hours (Asia/Kolkata).
- Add Firebase Cloud Messaging for Android push notifications.
- Implement a licensed provider adapter in `provider.py`; never place provider secrets in the Android APK.
- Add retries, rate-limit handling, market holiday calendar, stale-data checks, and audit logs.
- Verify indicator calculations against the user's Chartink scanner on the same completed candles before enabling alerts.
- Keep alert-only behavior. Do not add order placement without a separate explicit request and safeguards.
