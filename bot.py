import requests

# Binance API URL (5-min candle, last 50 candles)
url = "https://api.binance.com/api/v3/klines?symbol=STBLUSDT&interval=5m&limit=50"
data = requests.get(url).json()

# Extract candles
candles = []
for candle in data:
    candles.append({
        "open": candle[1],
        "high": candle[2],
        "low": candle[3],
        "close": candle[4],
        "volume": candle[5]
    })

# Telegram bot info
bot_token = "8191333539:AAF-XGRBPB2_gywymSz6VfUXlNIiWl50kMo"  # Rahul5555_bot token
chat_id = 1316245978                                         # तुम्हारा numeric chat ID

# Prepare messages in chunks to avoid Telegram limit
chunk_size = 10  # 10 candles per message
for i in range(0, len(candles), chunk_size):
    chunk = candles[i:i+chunk_size]
    message = f"Candles {i+1} to {i+len(chunk)}:\n"
    for c in chunk:
        message += f"Open={c['open']}, High={c['high']}, Low={c['low']}, Close={c['close']}, Vol={c['volume']}\n"
    requests.get(f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={message}")
