"""
Binance Futures public API client - soo qaadista OHLCV candles.
Endpoint-kani waa PUBLIC - API key looma baahna wax signals ah.
"""

import requests
import pandas as pd

BASE_URL = "https://fapi.binance.com/fapi/v1/klines"


def get_klines(symbol: str, interval: str, limit: int = 200) -> pd.DataFrame:
    """
    symbol: tusaale 'BTCUSDT'
    interval: '5m', '15m', '1h' iwm (Binance format)
    """
    params = {"symbol": symbol, "interval": interval, "limit": limit}
    resp = requests.get(BASE_URL, params=params, timeout=15)
    resp.raise_for_status()
    raw = resp.json()

    cols = [
        "open_time", "open", "high", "low", "close", "volume",
        "close_time", "quote_volume", "trades",
        "taker_buy_base", "taker_buy_quote", "ignore"
    ]
    df = pd.DataFrame(raw, columns=cols)
    for c in ["open", "high", "low", "close", "volume"]:
        df[c] = df[c].astype(float)
    df["open_time"] = pd.to_datetime(df["open_time"], unit="ms")
    df["close_time"] = pd.to_datetime(df["close_time"], unit="ms")
    return df
