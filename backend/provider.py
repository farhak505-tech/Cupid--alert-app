from typing import Protocol

class MarketDataProvider(Protocol):
    async def get_nse_cash_universe(self) -> list[str]:
        """Return NSE cash symbols."""
        ...
    async def get_indicator_snapshot(self, symbol: str) -> dict:
        """
        Return normalized daily/weekly OHLCV history and indicator values.
        Must include:
          close, high, volume, prev_day_high, prev_day_volume,
          high_250d, high_52w_ago,
          ema5, ema10, ema20, ema50, sma200,
          daily_rsi14, weekly_rsi14, weekly_close,
          weekly_sma30, weekly_sma30_5w_ago,
          custom_3899_len21, daily_mfi14, daily_cci20.
        All values must be timestamp-aligned to the same completed candle.
        """
        ...

class DemoProvider:
    async def get_nse_cash_universe(self) -> list[str]:
        return []

    async def get_indicator_snapshot(self, symbol: str) -> dict:
        raise RuntimeError("Demo provider has no live market data")
