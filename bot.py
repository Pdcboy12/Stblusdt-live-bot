import requests

# Telegram info
bot_token = "8191333539:AAF-XGRBPB2_gywymSz6VfUXlNIiWl50kMo"
chat_id = 1316245978

# Simple test message
message = "Test: Bot is working ✅"

# Send message
requests.get(f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={message}")
