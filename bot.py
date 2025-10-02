import requests

# Binance API URL (5-min candle, last 10 candles)
url = "https://api.binance.com/api/v3/klines?symbol=STBLUSDT&interval=5m&limit=10"

# Telegram info
bot_token = "8191333539:AAF-XGRBPB2_gywymSz6VfUXlNIiWl50kMo"
chat_id = 1316245978

try:
    data = requests.get(url, timeout=10).json()
except Exception as e:
    requests.get(f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text=Error fetching Binance data: {e}")
    raise

# Debug: check Binance data
print("Data received:", data)

candles = []
for candle in data:
    if isinstance(candle, list) and len(candle) >= 6:
        candles.append({
            "open": candle[1],
            "high": candle[2],
            "low": candle[3],
            "close": candle[4],
            "volume": candle[5]
        })

# Debug: check parsed candles
print("Candles parsed:", candles)

# Prepare message
if candles:
    chunk_size = 10  # 10 candles per message
    for i in range(0, len(candles), chunk_size):
        chunk = candles[i:i+chunk_size]
        message = f"Candles {i+1} to {i+len(chunk)}:\n"
        for c in chunk:
            message += f"Open={c['open']}, High={c['high']}, Low={c['low']}, Close={c['close']}, Vol={c['volume']}\n"
        try:
            requests.get(f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={message}", timeout=10)
        except Exception as e:
            print(f"Error sending message to Telegram: {e}")
else:
    # Send debug message if no candles
    requests.get(f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text=No candle data received from Binance")
