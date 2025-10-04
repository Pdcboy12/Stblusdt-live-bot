import requests
import json
import base64
import time

# ==================== Config ====================
COIN = "STBL"
QUOTE = "USDT"
LIMIT = 50
INTERVALS = [5, 30]  # 5 min and 30 min

# ==================== Telegram ====================
BOT_TOKEN = "8191333539:AAF-XGRBPB2_gywymSz6VfUXlNIiWl50kMo"
CHAT_ID = 1316245978

# ==================== GitHub ====================
GITHUB_TOKEN = "<YOUR_GITHUB_TOKEN>"  # Replace with your GitHub personal token
GITHUB_USER = "<YOUR_GITHUB_USERNAME>"
GITHUB_REPO = "<YOUR_REPO_NAME>"
GITHUB_FILE_PATH = "candles_data.json"

# ==================== CryptoCompare API ====================
URL = "https://min-api.cryptocompare.com/data/v2/histominute"

# ==================== Functions ====================

def fetch_candles(interval):
    params = {
        "fsym": COIN,
        "tsym": QUOTE,
        "limit": LIMIT-1,
        "aggregate": interval
    }
    try:
        r = requests.get(URL, params=params, timeout=10)
        data = r.json()
        if data.get("Response") == "Success":
            candles = []
            for candle in data["Data"]["Data"]:
                candles.append({
                    "O": candle['open'],
                    "H": candle['high'],
                    "L": candle['low'],
                    "C": candle['close'],
                    "V": candle['volumefrom']
                })
            return candles
        else:
            return []
    except Exception as e:
        print(f"Error fetching {interval}m data: {e}")
        return []

def send_telegram(text):
    for i in range(0, len(text), 3900):
        chunk = text[i:i+3900]
        try:
            requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                         params={"chat_id": CHAT_ID, "text": chunk}, timeout=10)
        except Exception as e:
            print(f"Telegram send error: {e}")

def upload_to_github(data):
    url = f"https://api.github.com/repos/{GITHUB_USER}/{GITHUB_REPO}/contents/{GITHUB_FILE_PATH}"
    # Get current file SHA
    sha = None
    try:
        r = requests.get(url, headers={"Authorization": f"token {GITHUB_TOKEN}"})
        if r.status_code == 200:
            sha = r.json()["sha"]
    except:
        pass

    payload = {
        "message": "Update candles",
        "content": base64.b64encode(json.dumps(data).encode()).decode(),
    }
    if sha:
        payload["sha"] = sha
    try:
        r = requests.put(url, headers={"Authorization": f"token {GITHUB_TOKEN}"}, json=payload)
        if r.status_code in [200, 201]:
            print("GitHub updated successfully")
        else:
            print("GitHub update failed:", r.json())
    except Exception as e:
        print("GitHub upload error:", e)

# ==================== Main Loop ====================
def main():
    while True:
        all_data = {}
        telegram_msg = ""
        for interval in INTERVALS:
            candles = fetch_candles(interval)
            all_data[f"{interval}m"] = candles
            telegram_msg += f"📊 Last {LIMIT} candles ({interval}m - {COIN}-{QUOTE}):\n"
            for c in candles:
                telegram_msg += f"O={c['O']}, H={c['H']}, L={c['L']}, C={c['C']}, V={c['V']}\n"
            telegram_msg += "\n"

        # Send to Telegram
        send_telegram(telegram_msg)

        # Upload to GitHub
        upload_to_github(all_data)

        # Wait 5 minutes before next fetch
        time.sleep(300)

if __name__ == "__main__":
    main()
