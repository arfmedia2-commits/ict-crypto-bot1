"""
Istiraatiijiyada Signal-ka: EMA crossover + RSI filter + MACD confirmation
Xisaabinta SL/TP waxay ku dhisan tahay ATR (volatility-based).

MUHIIM: Nidaamkan ma aha mid la iska hubiyay (backtested) suuq dhab ah.
Kahor inta aad lacag dhab ah ku isticmaalin, ku tijaabi paper-trading
ama demo account muddo dheer.
"""

import config as cfg


def detect_signal(df):
    """
    df waa DataFrame leh indicators (fiiri indicators.add_all_indicators).
    Waxay soo celisaa: "LONG", "SHORT", ama None
    """
    if len(df) < max(cfg.EMA_SLOW, cfg.MACD_SLOW, cfg.RSI_PERIOD) + 2:
        return None

    prev = df.iloc[-3]
    last = df.iloc[-2]  # candle-ka ugu dambeeyay ee la xiray (closed candle)

    ema_cross_up = prev["ema_fast"] <= prev["ema_slow"] and last["ema_fast"] > last["ema_slow"]
    ema_cross_down = prev["ema_fast"] >= prev["ema_slow"] and last["ema_fast"] < last["ema_slow"]

    macd_bullish = last["macd_hist"] > 0
    macd_bearish = last["macd_hist"] < 0

    rsi_ok_long = cfg.RSI_LONG_MIN <= last["rsi"] <= cfg.RSI_LONG_MAX
    rsi_ok_short = cfg.RSI_SHORT_MIN <= last["rsi"] <= cfg.RSI_SHORT_MAX

    if ema_cross_up and macd_bullish and rsi_ok_long:
        return "LONG"
    if ema_cross_down and macd_bearish and rsi_ok_short:
        return "SHORT"
    return None


def build_trade_plan(df, direction: str):
    """
    Xisaabisa entry, SL, iyo TP levels (2R, 3R) iyadoo la adeegsanayo ATR.
    """
    last = df.iloc[-2]
    entry = last["close"]
    atr_val = last["atr"]
    sl_distance = atr_val * cfg.ATR_SL_MULTIPLIER

    if direction == "LONG":
        sl = entry - sl_distance
        tps = [entry + sl_distance * r for r in cfg.RR_TARGETS]
    else:  # SHORT
        sl = entry + sl_distance
        tps = [entry - sl_distance * r for r in cfg.RR_TARGETS]

    return {
        "entry": entry,
        "sl": sl,
        "tps": tps,
        "atr": atr_val,
        "rsi": last["rsi"],
        "candle_time": last["close_time"],
    }
