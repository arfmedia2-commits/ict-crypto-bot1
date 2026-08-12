"""
U diritaanka fariimaha Telegram - HTTP request toos ah (lib dheeraad ah looma baahna).
"""

import requests
import config as cfg


def send_message(text: str):
    url = f"https://api.telegram.org/bot{cfg.TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": cfg.TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": True,
    }
    try:
        resp = requests.post(url, data=payload, timeout=15)
        resp.raise_for_status()
        return True
    except Exception as e:
        print(f"[Telegram Error] {e}")
        return False


def format_signal_message(symbol, timeframe, direction, plan, decimals=2):
    emoji = "🟢" if direction == "LONG" else "🔴"
    fmt = lambda x: f"{x:,.{decimals}f}"

    tp_lines = "\n".join(
        f"   TP{i+1} ({r}R): <b>{fmt(tp)}</b>"
        for i, (tp, r) in enumerate(zip(plan["tps"], cfg.RR_TARGETS))
    )

    msg = (
        f"{emoji} <b>{direction} SIGNAL</b> - {symbol} ({timeframe})\n\n"
        f"Entry: <b>{fmt(plan['entry'])}</b>\n"
        f"SL: <b>{fmt(plan['sl'])}</b>\n"
        f"{tp_lines}\n\n"
        f"RSI: {plan['rsi']:.1f} | ATR: {fmt(plan['atr'])}\n"
        f"Leverage (tilmaan): {cfg.SUGGESTED_LEVERAGE}x\n"
        f"Waqti candle: {plan['candle_time']} UTC\n\n"
        f"⚠️ Signal-kan waa tilmaan tekniko oo keliya, ma aha ballan lacag la'aan khasaare. "
        f"Ku maamul risk-gaaga (isticmaal SL had iyo jeer, ha dhaafin 1-2% risk kadhig kasta)."
    )
    return msg
