import requests
import time

# ==================== Coin setup ====================
COIN = "STBL"
QUOTE = "USDT"
LIMIT = 50
INTERVAL = 5  # minutes

# ==================== Telegram ====================
BOT_TOKEN = "8191333539:AAF-XGRBPB2_gywymSz6VfUXlNIiWl50kMo"
CHAT_ID = 1316245978

# ==================== CryptoCompare API ====================
url = "https://min-api.cryptocompare.com/data/v2/histominute"

# ---------- 5 Minute candles ----------
params_5m = {
    "fsym": COIN,
    "tsym": QUOTE,
    "limit": LIMIT-1,
    "aggregate": INTERVAL
}

try:
    r5 = requests.get(url, params=params_5m, timeout=10)
    data_5m = r5.json()
except Exception as e:
    requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text=Error fetching 5m data: {e}")
    raise

candles_5m = []
if data_5m.get("Response") == "Success":
    for candle in data_5m["Data"]["Data"]:
        candles_5m.append({
            "open": candle["open"],
            "high": candle["high"],
            "low": candle["low"],
            "close": candle["close"],
            "volume": candle["volumefrom"]
        })

# ---------- 30 Minute candles ----------
params_30m = {
    "fsym": COIN,
    "tsym": QUOTE,
    "limit": LIMIT-1,
    "aggregate": 30
}

try:
    r30 = requests.get(url, params=params_30m, timeout=10)
    data_30m = r30.json()
except Exception as e:
    requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text=Error fetching 30m data: {e}")
    raise

candles_30m = []
if data_30m.get("Response") == "Success":
    for candle in data_30m["Data"]["Data"]:
        candles_30m.append({
            "open": candle["open"],
            "high": candle["high"],
            "low": candle["low"],
            "close": candle["close"],
            "volume": candle["volumefrom"]
        })

# ==================== Send to Telegram ====================
message = ""

# 5m data
if candles_5m:
    message += f"Last {LIMIT} candles (5m - {COIN}-{QUOTE}):\n"
    for c in candles_5m:
        message += f"O={c['open']}, H={c['high']}, L={c['low']}, C={c['close']}, V={c['volume']}\n"
else:
    message += f"No 5m candle data for {COIN}-{QUOTE}\n"

# 30m data
if candles_30m:
    message += f"\nLast {LIMIT} candles (30m - {COIN}-{QUOTE}):\n"
    for c in candles_30m:
        message += f"O={c['open']}, H={c['high']}, L={c['low']}, C={c['close']}, V={c['volume']}\n"
else:
    message += f"No 30m candle data for {COIN}-{QUOTE}\n"

try:
    requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}", timeout=10)
except Exception as e:
    print(f"Error sending message: {e}")
