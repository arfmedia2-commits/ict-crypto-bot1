"""
Config-ka Bot-ka Telegram Signals
==================================
Buuxi qiimayaasha hoose. Token-ka BotFather waa qarsoodi - HA la wadaagin cid kale.
Waxaa la talinayaa in aad token-ka ku shubto .env file halkii aad koodhka ku qori lahayd
si toos ah (fiiri README.md).
"""

import os
from dotenv import load_dotenv

load_dotenv()  # akhrisa .env file haddii uu jiro

# ---- Telegram ----
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8622338917:AAHN93x-n8tM55x7taNpduqkxrSA5fpZUF0")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "93372553")

# ---- Symbols-ka la eegayo (Binance Futures perpetual) ----
# Kordhiyay ilaa 10 coin si signals-ka loo badiyo (frequency > sida 3-da hore)
SYMBOLS = [
    "BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT", "XRPUSDT",
    "ADAUSDT", "DOGEUSDT", "AVAXUSDT", "LINKUSDT", "DOTUSDT",
]

# ---- Timeframe-yada (Binance format) ----
TIMEFRAMES = ["5m", "15m"]

# ---- Indicator settings ----
EMA_FAST = 9
EMA_SLOW = 21
RSI_PERIOD = 14
RSI_LONG_MIN, RSI_LONG_MAX = 40, 70      # signal LONG loo ansixiyo
RSI_SHORT_MIN, RSI_SHORT_MAX = 30, 60    # signal SHORT loo ansixiyo
MACD_FAST, MACD_SLOW, MACD_SIGNAL = 12, 26, 9
ATR_PERIOD = 14

# ---- Risk / SL-TP settings ----
ATR_SL_MULTIPLIER = 1.5     # SL = entry -/+ (ATR * multiplier)
RR_TARGETS = [2, 3]         # TP1 = 2R, TP2 = 3R (R = masaafada SL)

# ---- Leverage (tilmaan/muujin oo keliya - user ayaa go'aansada) ----
SUGGESTED_LEVERAGE = 5      # tilmaan aan matoor ahayn - khatar sare leh in la kordhiyo

# ---- Bot loop ----
POLL_SECONDS = 30           # inta jeer bot-ku hubiyo candle-ka cusub
