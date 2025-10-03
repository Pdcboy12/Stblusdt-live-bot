import requests
import time

# ==================== Settings ====================
symbol = "BTC-USD"      # Coin pair for Yahoo Finance
interval = "5m"          # 5-minute candles
limit = 10               # last 10 candles

bot_token = "8191333539:AAF-XGRBPB2_gywymSz6VfUXlNIiWl50kMo"
chat_id = 1316245978

# ==================== Fetch Yahoo Finance data ====================
url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?interval={interval}&range=1d"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

try:
    r = requests.get(url, headers=headers, timeout=10)
    print("HTTP:", r.status_code)
    if r.status_code == 429:
        requests.get(f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text=Rate limit hit (429). Retry later.")
        raise Exception("Rate limit hit (429)")
    data = r.json()
except Exception as e:
    requests.get(f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text=Error fetching Yahoo data: {e}")
    raise

# ==================== Parse candles ====================
try:
    result = data['chart']['result'][0]
    timestamps = result['timestamp'][-limit:]
    ohlc = result['indicators']['quote'][0]
    opens = ohlc['open'][-limit:]
    highs = ohlc['high'][-limit:]
    lows = ohlc['low'][-limit:]
    closes = ohlc['close'][-limit:]
    volumes = ohlc['volume'][-limit:]
except Exception as e:
    requests.get(f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text=Error parsing data: {e}")
    raise

# ==================== Send to Telegram ====================
message = f"Last {limit} candles ({symbol}):\n"
for i in range(limit):
    message += f"O={opens[i]}, H={highs[i]}, L={lows[i]}, C={closes[i]}, V={volumes[i]}\n"

try:
    requests.get(f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={message}", timeout=10)
except Exception as e:
    print(f"Error sending message to Telegram: {e}")
