"""
Loyihaning asosiy konfiguratsiya parametrlari.
"""

import os
from dotenv import load_dotenv

load_dotenv()

# Telegram Bot Token (Foydalanuvchi bergan token)
BOT_TOKEN = os.getenv("BOT_TOKEN", "9007180538:AAFLnPX4WznaX9kI6o3CaQPwq9guajQKQjU")

# Render yoki server porti
PORT = int(os.getenv("PORT", "10000"))

# Webhook manzili (ixtiyoriy, agar ko'rsatilmasa polling rejimida ishlaydi)
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "")
