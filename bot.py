import requests
import time

# ==================== Coin setup ====================
COIN = "XRP"
QUOTE = "USDT"
LIMIT = 50
INTERVAL = 5  # minutes

# ==================== Telegram ====================
BOT_TOKEN = "8191333539:AAF-XGRBPB2_gywymSz6VfUXlNIiWl50kMo"
CHAT_ID = 1316245978

# ==================== CryptoCompare API ====================
url = "https://min-api.cryptocompare.com/data/v2/histominute"
params = {
    "fsym": COIN,
    "tsym": QUOTE,
    "limit": LIMIT-1,  # API returns limit+1
    "aggregate": INTERVAL
}

try:
    r = requests.get(url, params=params, timeout=10)
    data = r.json()
except Exception as e:
    requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text=Error fetching data: {e}")
    raise

# ==================== Parse candles ====================
candles = []
if data.get("Response") == "Success":
    for candle in data["Data"]["Data"]:
        candles.append({
            "open": candle["open"],
            "high": candle["high"],
            "low": candle["low"],
            "close": candle["close"],
            "volume": candle["volumefrom"]
        })

# ==================== Send to Telegram ====================
if candles:
    message = f"Last {LIMIT} candles ({COIN}-{QUOTE}):\n"
    for c in candles:
        message += f"O={c['open']}, H={c['high']}, L={c['low']}, C={c['close']}, V={c['volume']}\n"

    try:
        requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}", timeout=10)
    except Exception as e:
        print(f"Error sending message: {e}")
else:
    requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text=No candle data received for {COIN}-{QUOTE}")
