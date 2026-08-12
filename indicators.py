"""
Xisaabinta Indicators-ka: EMA, RSI, MACD, ATR
Waxaa loo isticmaalay pandas/numpy oo keliya (lib dheeraad ah looma baahna).
"""

import pandas as pd
import numpy as np


def ema(series: pd.Series, period: int) -> pd.Series:
    return series.ewm(span=period, adjust=False).mean()


def rsi(series: pd.Series, period: int = 14) -> pd.Series:
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.ewm(alpha=1 / period, min_periods=period, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1 / period, min_periods=period, adjust=False).mean()

    rs = avg_gain / avg_loss.replace(0, np.nan)
    rsi_val = 100 - (100 / (1 + rs))
    return rsi_val.fillna(50)


def macd(series: pd.Series, fast=12, slow=26, signal=9):
    ema_fast = ema(series, fast)
    ema_slow = ema(series, slow)
    macd_line = ema_fast - ema_slow
    signal_line = ema(macd_line, signal)
    hist = macd_line - signal_line
    return macd_line, signal_line, hist


def atr(df: pd.DataFrame, period: int = 14) -> pd.Series:
    high, low, close = df["high"], df["low"], df["close"]
    prev_close = close.shift(1)
    tr = pd.concat([
        high - low,
        (high - prev_close).abs(),
        (low - prev_close).abs()
    ], axis=1).max(axis=1)
    return tr.ewm(alpha=1 / period, min_periods=period, adjust=False).mean()


def add_all_indicators(df: pd.DataFrame, cfg) -> pd.DataFrame:
    df = df.copy()
    df["ema_fast"] = ema(df["close"], cfg.EMA_FAST)
    df["ema_slow"] = ema(df["close"], cfg.EMA_SLOW)
    df["rsi"] = rsi(df["close"], cfg.RSI_PERIOD)
    df["macd"], df["macd_signal"], df["macd_hist"] = macd(
        df["close"], cfg.MACD_FAST, cfg.MACD_SLOW, cfg.MACD_SIGNAL
    )
    df["atr"] = atr(df, cfg.ATR_PERIOD)
    return df
