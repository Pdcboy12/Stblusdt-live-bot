import requests
import time

# ==================== Settings ====================
symbol = "XRP-USD"  # Yaha coin change kar sakte ho (BTC-USD, XRP-USD...)
interval = "5"       # 5-min candles
limit = 10           # last 10 candles

bot_token = "8191333539:AAF-XGRBPB2_gywymSz6VfUXlNIiWl50kMo"
chat_id = 1316245978

# ==================== Fetch data from Yahoo Finance ====================
url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?interval={interval}m&range=1d"
try:
    r = requests.get(url, timeout=10)
    data = r.json()
except Exception as e:
    requests.get(f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text=Error fetching data: {e}")
    raise

# ==================== Parse candles ====================
try:
    result = data["chart"]["result"][0]
    timestamps = result["timestamp"][-limit:]
    ohlc = result["indicators"]["quote"][0]
    opens = ohlc["open"][-limit:]
    highs = ohlc["high"][-limit:]
    lows = ohlc["low"][-limit:]
    closes = ohlc["close"][-limit:]
    volumes = ohlc["volume"][-limit:]
except Exception as e:
    requests.get(f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text=Error parsing data: {e}")
    raise

# ==================== Prepare Telegram message ====================
message = f"Last {limit} candles ({symbol}):\n"
for i in range(limit):
    message += f"O={opens[i]}, H={highs[i]}, L={lows[i]}, C={closes[i]}, V={volumes[i]}\n"

# ==================== Send message ====================
try:
    requests.get(f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={message}", timeout=10)
except Exception as e:
    print(f"Error sending message to Telegram: {e}")
