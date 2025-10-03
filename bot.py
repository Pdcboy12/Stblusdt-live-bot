import requests
import time

# ==================== Settings ====================
symbol = "BINANCE:BTCUSDT"   # Pair
resolution = "5"             # 5 min
limit = 10                   # candles count

bot_token = "8191333539:AAF-XGRBPB2_gywymSz6VfUXlNIiWl50kMo"
chat_id = 1316245978

# ==================== Time Range ====================
end = int(time.time())
start = end - (limit * 5 * 60)

# ==================== TradingView Public Proxy ====================
url = f"https://api.tradingview.com/history?symbol={symbol}&resolution={resolution}&from={start}&to={end}"

try:
    r = requests.get(url, timeout=10)
    print("HTTP:", r.status_code)
    print("Raw:", r.text[:200])
    data = r.json()
except Exception as e:
    requests.get(
        f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text=Error: {e}"
    )
    raise

# ==================== Parse & Send ====================
if "c" in data and data["c"]:
    closes = data["c"]
    opens = data["o"]
    highs = data["h"]
    lows = data["l"]

    message = f"Last {len(closes)} candles ({symbol}):\n"
    for i in range(len(closes)):
        message += f"O={opens[i]}, H={highs[i]}, L={lows[i]}, C={closes[i]}\n"

    requests.get(
        f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={message}"
    )
else:
    requests.get(
        f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text=No candle data from TradingView"
    )
