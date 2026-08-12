# Telegram Crypto Scalping Signal Bot

Bot Telegram ah oo si joogto ah u eegaa BTCUSDT, ETHUSDT, SOLUSDT (5m & 15m) oo
u diraa signals (LONG/SHORT) marka istiraatiijiyadu is dhigto — EMA crossover +
RSI filter + MACD confirmation, leh SL/TP oo ku dhisan ATR (2R & 3R).

## ⚠️ Ogeysiis Muhiim ah

- **Ma jiro win-rate go'an (60% iwm) oo la hubin karo** — nidaamkan waa tilmaan
  tekniko oo aan la backtest-gareyn. Kahor isticmaalka lacag dhab ah, ku tijaabi
  **demo/paper trading** ugu yaraan 2-4 toddobaad, oo eeg natiijada dhabta ah.
- **Leverage trading (futures)** waxay kordhin kartaa khasaaraha si degdeg ah.
  Ha isticmaalin lacag aadan awoodin inaad lumiso.
- Koodhkan **kuma fulinayo trades** — wuxuu diraa oo keliya fariimo signal ah.

## 1. Isku diyaarinta

```bash
cd telegram_signal_bot
pip install -r requirements.txt
```

## 2. Qeexida Token-ka (muhiim - ammaan)

Koobiye `.env.example` una beddel magaca `.env`, ka buuxi qiimayaashaada:

```bash
cp .env.example .env
```

`.env` file:
```
TELEGRAM_BOT_TOKEN=<token-kaaga>
TELEGRAM_CHAT_ID=<chat id-kaaga>
```

**La socod:** hadda `.env.example` wuxuu ka kooban yahay token/chat id-gaaga
si aad u aragto qaabka. Marka aad `.env` sameyso, `.env` ha ku darin git/GitHub
(ku dar `.env` faylka `.gitignore`).

### Sida loo helo Chat ID (haddii aad rabto mid kale)
1. Ku qor bot-kaaga fariin (`/start`)
2. Booqo: `https://api.telegram.org/bot<TOKEN>/getUpdates`
3. Raadi `"chat":{"id": ...}` — taasi waa chat ID-gaaga

## 3. Isku day (test) ka hor inta aadan run garayn joogtada ah

```bash
python3 -c "from telegram_sender import send_message; send_message('Test ✅')"
```

Haddii aad fariinta ka aragto Telegram, dhammaan wuu shaqeynayaa.

## 4. Bilaabidda Bot-ka

```bash
python3 main.py
```

Bot-ku wuxuu si joogto ah u socon doonaa (`Ctrl+C` si aad u joojiso), oo
isla mar ahaantaana hubinaya candle-yada cusub (30 ilbiriqsi kasta by default).

## 5. In loo beddelo istiraatiijiyada / settings

Dhammaan qiimayaasha (symbols, timeframes, RSI/EMA/MACD periods, ATR
multiplier, R-targets, leverage tilmaanta) waxaa lagu beddeli karaa
`config.py`.

## 6. Sida loo run-geliyo si joogto ah (server/VPS)

Server-ka (ama VPS 24/7 ah) ku isticmaal `screen` ama `systemd` si bot-ku
uusan u istaagin marka terminal-ka la xiro:

```bash
screen -S signalbot
python3 main.py
# Ctrl+A ka dib D si aad uga baxdo screen-ka isagoo bot-ku socda
```

## 7. Talooyin kordhinta mustaqbalka

- **Backtesting**: ka hor inta aad rumaysan tahay istiraatiijiyada, isku day
  xogta hore (historical data) si aad u aragto natiijada dhabta ah.
- **Auto-execute trades**: haddii aad mustaqbalka rabto in bot-ku si toos ah
  u fuliyo trades (order placement) Binance Futures, waxaad u baahan doontaa
  Binance API Key + Secret oo leh futures permission — waa qayb kale oo
  dheeraad ah, khatar sarena leh (waa la iga codsan karaa).
