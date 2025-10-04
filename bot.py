import os
import requests
import subprocess

# ==================== Auto Install Missing Libraries ====================
try:
    import pandas as pd
except ImportError:
    subprocess.run(["pip", "install", "pandas", "requests"], check=True)
    import pandas as pd

# ==================== Config ====================
COIN = "STBL"
QUOTE = "USDT"
LIMIT = 50
INTERVALS = [5, 30]   # 5min + 30min chart dono

# ==================== Telegram ====================
BOT_TOKEN = "8191333539:AAF-XGRBPB2_gywymSz6VfUXlNIiWl50kMo"
CHAT_ID = 1316245978

# ==================== API ====================
URL = "https://min-api.cryptocompare.com/data/v2/histominute"

def fetch_candles(interval):
    params = {
        "fsym": COIN,
        "tsym": QUOTE,
        "limit": LIMIT - 1,
        "aggregate": interval
    }
    try:
        r = requests.get(URL, params=params, timeout=10)
        data = r.json()
        if data.get("Response") == "Success":
            candles = []
            for candle in data["Data"]["Data"]:
                candles.append(
                    f"O={candle['open']}, H={candle['high']}, L={candle['low']}, "
                    f"C={candle['close']}, V={candle['volumefrom']}"
                )
            return candles
        else:
            return [f"Error: API returned {data.get('Message', 'unknown error')}"]
    except Exception as e:
        return [f"Error fetching {interval}m data: {e}"]

def send_message(text):
    # Split message if too long (Telegram limit)
    for i in range(0, len(text), 3900):
        chunk = text[i:i + 3900]
        try:
            requests.get(
                f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                params={"chat_id": CHAT_ID, "text": chunk},
                timeout=10
            )
        except Exception as e:
            print(f"Error sending message: {e}")

# ==================== Build + Send ====================
full_message = ""
for interval in INTERVALS:
    candles = fetch_candles(interval)
    full_message += f"📊 Last {LIMIT} candles ({interval}m - {COIN}-{QUOTE}):\n" + "\n".join(candles) + "\n\n"

send_message(full_message)
