import requests
import time

# ==================== SETTINGS ====================
# Coin pair ko yaha change karo (jaise 'BTC-USD', 'XRP-USD', etc.)
COIN = "XRP-USD"

# Telegram
BOT_TOKEN = "8191333539:AAF-XGRBPB2_gywymSz6VfUXlNIiWl50kMo"  # Bot token
CHAT_ID = 1316245978  # Numeric chat ID

# Candles config
INTERVAL = 5       # 5 minutes
NUM_CANDLES = 10   # last 10 candles

# ==================== FETCH DATA ====================
# TradingView URL (snapshot style)
timestamp_to = int(time.time())
timestamp_from = timestamp_to - (INTERVAL * 60 * NUM_CANDLES)

url = f"https://scanner.tradingview.com/crypto/scan"

payload = {
    "symbols": {"tickers": [f"BINANCE:{COIN}"], "query": {"types": []}},
    "columns": ["open", "high", "low", "close", "volume"]
}

try:
    r = requests.post(url, json=payload, timeout=10)
    data = r.json()
except Exception as e:
    requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text=Error fetching data: {e}")
    data = None

# ==================== PARSE CANDLES ====================
candles = []

try:
    if data and "data" in data and len(data["data"]) > 0:
        for c in data["data"][0]["d"][:NUM_CANDLES]:
            candles.append({
                "open": c[0],
                "high": c[1],
                "low": c[2],
                "close": c[3],
                "volume": c[4]
            })
except Exception as e:
    requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text=Error parsing data: {e}")
    candles = []

# ==================== SEND TO TELEGRAM ====================
if candles:
    message = f"Last {NUM_CANDLES} candles ({COIN}):\n"
    for c in candles:
        message += f"O={c['open']}, H={c['high']}, L={c['low']}, C={c['close']}, V={c['volume']}\n"
else:
    message = f"No candle data received for {COIN}"

requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}")
