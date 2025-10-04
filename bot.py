import requests
import pandas as pd
import numpy as np

# ==================== Config ====================
COIN = "STBL"
QUOTE = "USDT"
LIMIT = 100
INTERVALS = [5, 30]
BOT_TOKEN = "8191333539:AAF-XGRBPB2_gywymSz6VfUXlNIiWl50kMo"
CHAT_ID = 1316245978
URL = "https://min-api.cryptocompare.com/data/v2/histominute"

# ==================== Core Functions ====================

def fetch_candles(interval):
    params = {"fsym": COIN, "tsym": QUOTE, "limit": LIMIT-1, "aggregate": interval}
    try:
        r = requests.get(URL, params=params, timeout=10)
        data = r.json()
        if data.get("Response") == "Success":
            df = pd.DataFrame(data["Data"]["Data"])
            df["time"] = pd.to_datetime(df["time"], unit="s")
            return df
    except Exception as e:
        print(f"Error fetching {interval}m data: {e}")
    return pd.DataFrame()

def calc_indicators(df):
    df["EMA12"] = df["close"].ewm(span=12, adjust=False).mean()
    df["EMA26"] = df["close"].ewm(span=26, adjust=False).mean()
    df["MACD"] = df["EMA12"] - df["EMA26"]
    df["Signal"] = df["MACD"].ewm(span=9, adjust=False).mean()
    
    delta = df["close"].diff()
    gain = np.where(delta > 0, delta, 0)
    loss = np.where(delta < 0, -delta, 0)
    avg_gain = pd.Series(gain).rolling(14).mean()
    avg_loss = pd.Series(loss).rolling(14).mean()
    rs = avg_gain / avg_loss
    df["RSI"] = 100 - (100 / (1 + rs))
    
    return df

def generate_signal(df):
    last = df.iloc[-1]
    if last["MACD"] > last["Signal"] and last["RSI"] < 70:
        return "BUY"
    elif last["MACD"] < last["Signal"] and last["RSI"] > 30:
        return "SELL"
    else:
        return "WAIT"

def send_message(text):
    for i in range(0, len(text), 3900):
        try:
            requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                         params={"chat_id": CHAT_ID, "text": text[i:i+3900]}, timeout=10)
        except Exception as e:
            print(f"Error sending message: {e}")

# ==================== Main ====================
messages = []
for interval in INTERVALS:
    df = fetch_candles(interval)
    if df.empty:
        continue
    df = calc_indicators(df)
    signal = generate_signal(df)
    
    last = df.iloc[-1]
    summary = {
        "pair": f"{COIN}-{QUOTE}",
        "interval": f"{interval}m",
        "price": round(float(last['close']), 6),
        "RSI": round(float(last['RSI']), 2),
        "MACD": round(float(last['MACD']), 6),
        "SignalLine": round(float(last['Signal']), 6),
        "Trend": signal
    }
    messages.append(summary)

# ==================== Send JSON Summary ====================
import json
send_message("📊 Signal Update:\n" + json.dumps(messages, indent=2))
