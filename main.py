"""
Telegram Crypto Scalping Signal Bot
=====================================
Wuxuu si joogto ah u eegaa BTCUSDT / ETHUSDT / SOLUSDT (5m & 15m),
haddii signal cusub la helo (EMA crossover + RSI + MACD), wuxuu
Telegram u diraa fariin leh Entry / SL / TP (2R & 3R).

Run: python3 main.py
"""

import time
import traceback
from datetime import datetime, timezone

import config as cfg
from binance_client import get_klines
from indicators import add_all_indicators
from strategy import detect_signal, build_trade_plan
from telegram_sender import send_message, format_signal_message

# la socodka signal-yadii ugu dambeeyay si aan loo soo celin isla mid (spam)
# key: (symbol, timeframe) -> (candle_time, direction)
last_signal_state = {}

# tirinta signal-yada maalinka - si aad u ogaato imisa maanta la diray
daily_signal_count = 0
current_day = datetime.now(timezone.utc).date()


def _reset_daily_counter_if_new_day():
    global daily_signal_count, current_day
    today = datetime.now(timezone.utc).date()
    if today != current_day:
        current_day = today
        daily_signal_count = 0
        print(f"[{datetime.now(timezone.utc)}] Maalin cusub - counter-ka signal-yada dib ayaa loo dejiyay.")


def check_symbol_timeframe(symbol: str, timeframe: str):
    df = get_klines(symbol, timeframe, limit=200)
    df = add_all_indicators(df, cfg)

    direction = detect_signal(df)
    if direction is None:
        return

    last_closed_time = df.iloc[-2]["close_time"]
    key = (symbol, timeframe)
    prev_state = last_signal_state.get(key)

    # Signal-ka isla candle-ka mar kale ha la dirin
    if prev_state == (last_closed_time, direction):
        return

    plan = build_trade_plan(df, direction)
    decimals = 4 if plan["entry"] < 10 else 2
    msg = format_signal_message(symbol, timeframe, direction, plan, decimals)

    if send_message(msg):
        global daily_signal_count
        daily_signal_count += 1
        print(f"[{datetime.now(timezone.utc)}] Signal sent: {symbol} {timeframe} {direction} "
              f"(signal #{daily_signal_count} maanta)")
        last_signal_state[key] = (last_closed_time, direction)


def run_forever():
    print("Bot-ku wuu socdaa... (Ctrl+C si aad u joojiso)")
    send_message("✅ Signal Bot wuu bilaabmay. Symbols: "
                 f"{', '.join(cfg.SYMBOLS)} | Timeframes: {', '.join(cfg.TIMEFRAMES)}")

    while True:
        _reset_daily_counter_if_new_day()
        for symbol in cfg.SYMBOLS:
            for tf in cfg.TIMEFRAMES:
                try:
                    check_symbol_timeframe(symbol, tf)
                except Exception as e:
                    print(f"[Error] {symbol} {tf}: {e}")
                    traceback.print_exc()
        time.sleep(cfg.POLL_SECONDS)


if __name__ == "__main__":
    run_forever()
