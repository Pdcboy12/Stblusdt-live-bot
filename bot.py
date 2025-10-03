import requests
import time

# ==================== Binance / CryptoCompare API ====================
# Binance free API sometimes blocks certain locations, fallback to CryptoCompare
symbol_binance = "XRPUSDT"   # Binance symbol
symbol_cc = "XRP"            # CryptoCompare symbol
fiat_cc = "USDT"

interval = 5   # minutes
limit = 10     # last 10 candles

# ==================== Telegram ====================
bot_token = "8191333539:AAF-XGRBPB2_gywymSz6VfUXlNIiWl50kMo"
chat_id = 1316245978

# ==================== Fetch Binance data ====================
url_binance = f"https://api.binance.com/api/v3/klines?symbol={symbol_binance}&interval=5m&limit={limit}"

try:
    r = requests.get(url_binance, timeout=10)
    data = r.json()
    if not data or isinstance(data, dict) and data.get("code"):
        raise Exception("No Binance data or API blocked, fallback to CryptoCompare")
    source = "Binance"
except Exception as e:
    # Fallback to CryptoCompare
    ts_to = int(time.time())
    url_cc = f"https://min-api.cryptocompare.com/data/v2/histominute?fsym={symbol_cc}&tsym={fiat_cc}&limit={limit-1}&aggregate={interval}"
    r = requests.get(url_cc, timeout=10)
    res = r.json()
    if res["Response"] != "Success":
        requests.get(f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text=No candle data received for {symbol_binance}")
        raise Exception(f"No data received: {res}")
    data = res["Data"]["Data"]
    source = "CryptoCompare"

# ==================== Parse candles ====================
candles = []
for candle in data:
    if source == "Binance":
        candles.append({
            "open": candle[1],
            "high": candle[2],
            "low": candle[3],
            "close": candle[4],
            "volume": candle[5]
        })
    else:  # CryptoCompare
        candles.append({
            "open": candle["open"],
            "high": candle["high"],
            "low": candle["low"],
            "close": candle["close"],
            "volume": candle["volumefrom"]
        })

# ==================== Send to Telegram ====================
message = f"Last {len(candles)} candles ({symbol_binance}):\n"
for c in candles:
    message += f"O={c['open']}, H={c['high']}, L={c['low']}, C={c['close']}, V={c['volume']}\n"

requests.get(f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={message}")
