REQUIRED_FIELDS = {
    "close", "volume", "prev_day_high", "prev_day_volume",
    "high_250d", "high_52w_ago", "ema5", "ema10", "ema20",
    "ema50", "sma200", "daily_rsi14", "weekly_rsi14",
    "weekly_close", "weekly_sma30", "weekly_sma30_5w_ago",
    "custom_3899_len21", "daily_mfi14", "daily_cci20"
}

def qualifies(x: dict) -> tuple[bool, list[str]]:
    missing = REQUIRED_FIELDS - x.keys()
    if missing:
        return False, [f"Missing provider fields: {', '.join(sorted(missing))}"]

    # Fail closed until the semantics of Chartink custom indicator #3899 are confirmed.
    if x["custom_3899_len21"] is None:
        return False, ["Custom indicator #3899 is not configured"]

    checks = [
        ("Daily close > 52-week-ago high", x["close"] > x["high_52w_ago"]),
        ("Daily close >= 100", x["close"] >= 100),
        ("Within 1% of 250-day high", x["close"] > x["high_250d"] * 0.99),
        ("Daily volume > 6,000,000", x["volume"] > 6_000_000),
        ("Daily close > previous day's high", x["close"] > x["prev_day_high"]),
        ("Daily close > EMA 20", x["close"] > x["ema20"]),
        ("EMA 20 > EMA 50", x["ema20"] > x["ema50"]),
        ("EMA 50 > SMA 200", x["ema50"] > x["sma200"]),
        ("Daily RSI(14) >= 62", x["daily_rsi14"] >= 62),
        ("Daily RSI(14) <= 75", x["daily_rsi14"] <= 75),
        ("Weekly RSI(14) > 65", x["weekly_rsi14"] > 65),
        ("Weekly close > weekly SMA(30)", x["weekly_close"] > x["weekly_sma30"]),
        ("Weekly SMA(30) rising", x["weekly_sma30"] > x["weekly_sma30_5w_ago"]),
        ("Custom indicator #3899 > 15.8", x["custom_3899_len21"] > 15.8),
        ("EMA 5 > EMA 10", x["ema5"] > x["ema10"]),
        ("EMA 10 > EMA 20", x["ema10"] > x["ema20"]),
        ("MFI(14) > 72", x["daily_mfi14"] > 72),
        ("Volume > previous day's volume", x["volume"] > x["prev_day_volume"]),
        ("CCI(20) >= 100", x["daily_cci20"] >= 100),
    ]
    failed = [name for name, passed in checks if not passed]
    return not failed, failed
