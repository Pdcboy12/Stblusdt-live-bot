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
bot_token = "Rahul5555_bot"   # अपने bot token डालो
chat_id = "@pdcboy"       # अपने chat id डालो

# Prepare message
message = "Last 50 candles:\n"
for c in candles:
    message += f"Open={c['open']}, High={c['high']}, Low={c['low']}, Close={c['close']}, Vol={c['volume']}\n"

# Send message
requests.get(f"https://api.telegram.org/bot{bot_token}/sendMesstextchat_id={chat_id}&text={message}")
