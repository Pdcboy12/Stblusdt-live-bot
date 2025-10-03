import requests
import time

# ==================== Settings ====================
symbol = "BINANCE:BTCUSDT"   # pair TradingView se
resolution = "5"             # 5 min candles
limit = 10                   # candles count

bot_token = "8191333539:AAF-XGRBPB2_gywymSz6VfUXlNIiWl50kMo"  # Tumhara bot token
chat_id = 1316245978  # Tumhara chat id

# ==================== Time Range ====================
end = int(time.time())
start = end - (limit * 5 * 60)  # 10 candles * 5 min each

# ==================== TradingView API ====================
url = f"https://tvc4.forexpros.com/989a1a112233445566/history?symbol={symbol}&resolution={resolution}&from={start}&to={end}"

try:
    r = requests.get(url, timeout=10)
    data = r.json()
except Exception as e:
    requests.get(
        f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text=Error: {e}"
    )
    raise

# ==================== Parse & Send ====================
if "c" in data:
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
