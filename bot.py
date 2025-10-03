import requests
import time

# ==================== Binance API ====================
API_KEY = "YOUR_API_KEY"       # ← अपने Binance API key डालो
API_SECRET = "YOUR_API_SECRET" # ← अपने Binance secret डालो

symbol = "STBLUSDT"            # Coin pair
interval = "5m"                 # 5-minute candles
limit = 10                      # last 10 candles (change as needed)

# ==================== Telegram ====================
bot_token = "8191333539:AAF-XGRBPB2_gywymSz6VfUXlNIiWl50kMo"  # Telegram bot token
chat_id = 1316245978                                         # Numeric chat_id

# ==================== Fetch Binance data ====================
timestamp = int(time.time() * 1000)
url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}&timestamp={timestamp}"
headers = {"X-MBX-APIKEY": API_KEY}

try:
    r = requests.get(url, headers=headers, timeout=10)
    print("HTTP status:", r.status_code)
    print("Raw response:", r.text)  # 🔍 Debug line
    data = r.json()
except Exception as e:
    err_msg = f"Error fetching Binance data: {e}"
    print(err_msg)
    requests.get(f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={err_msg}")
    raise

# ==================== Parse candles ====================
candles = []
if isinstance(data, list):
    for candle in data:
        if isinstance(candle, list) and len(candle) >= 6:
            candles.append({
                "open": candle[1],
                "high": candle[2],
                "low": candle[3],
                "close": candle[4],
                "volume": candle[5]
            })

print("Candles parsed:", candles)

# ==================== Send to Telegram ====================
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
    msg = f"No candle data received from Binance.\nRaw reply: {data}"
    print(msg)
    requests.get(f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={msg}")
