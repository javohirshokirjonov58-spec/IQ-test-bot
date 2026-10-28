# 🧠 IQ Test Telegram Bot

Telegram orqali foydalanuvchilarning mantiqiy, analitik, fazoviy va matematik fikrlash qobiliyatlarini tekshiruvchi, individual IQ ballini hisoblab beruvchi va xatolar tahlilini taqdim etuvchi zamonaviy Telegram bot.

Loyihada **Render.com** bepul bulutli platformasiga bir zumda deploy qilish uchun barcha sozlamalar (`render.yaml`, `Procfile`, aiohttp health check) to'liq tayyorlangan.

---

## 🌟 Asosiy imkoniyatlari

- 🎯 **15 ta professional IQ savollari**:
  - Ketma-ketliklar (raqamlar va naqshlar)
  - Analitik mantiq va analogiyalar
  - Fazoviy tasavvur masalalari
  - Matematik va nostandart topishmoqlar
- 📊 **Progress Bar**: Har bir savolda foydalanuvchiga testning qaysi bosqichida ekani ko'rsatiladi.
- 🧮 **Haqiqiy IQ hisob-kitobi**: Test natijasi 70 dan 145+ gacha bo'lgan rasmiy IQ shkalasi asosida baholanadi (Daho, Yuqori, O'rtacha va h.k.).
- 🔍 **Xatolar tahlili**: Test yakunlangach, foydalanuvchi qayerda xato qilgani va to'g'ri javobning izohini ko'rishi mumkin.
- 🏆 **Top reyting (Leaderboard)**: Eng yuqori IQ natijasiga erishgan foydalanuvchilar ro'yxati.
- 📈 **Shaxsiy statistika**: Foydalanuvchining urinishlari soni, eng yaxshi va o'rtacha natijalari.
- ☁️ **Render.com ga to'liq mos**: Render Web Service talab qiladigan `$PORT` bo'yicha HTTP server integratsiyasi mavjud bo'lib, bot hech qanday xatoliksiz uzluksiz ishlaydi.

---

## 🚀 Texnologiyalar

- **Python 3.10+**
- **Aiogram 3.x** (Asinxron va tezkor Telegram Bot freymvorki)
- **Aiohttp** (Render portini tekshirish uchun HTTP server)
- **SQLite3** (Foydalanuvchilar va natijalar bazasi)

---

## 💻 Mahalliy kompyuterda ishga tushirish

1. Ushbu omborni klonlang yoki loyiha papkasiga kiring:
   ```bash
   git clone https://github.com/javohirshokirjonov58-spec/IQ-test-bot.git
   cd IQ-test-bot
   ```

2. Virtual muhit yaratish va kutubxonalarni o'rnatish:
   ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # Linux / macOS:
   source venv/bin/activate

   pip install -r requirements.txt
   ```

3. `.env` faylida Telegram bot tokenini sozlang:
   ```env
   BOT_TOKEN=9007180538:AAFLnPX4WznaX9kI6o3CaQPwq9guajQKQjU
   PORT=10000
   ```

4. Botni ishga tushiring:
   ```bash
   python bot.py
   ```

---

## 🌐 Render.com ga deploy qilish bo'yicha qo'llanma

Bot Render.com da 24/7 rejimida bepul ishlashi uchun barcha kerakli fayllar sozlangan:

1. [https://render.com](https://render.com) saytiga kiring va ro'yxatdan o'ting (yoki GitHub orqali kiring).
2. **"New +"** tugmasini bosing va **"Web Service"** ni tanlang.
3. GitHub hisobingizdan ushbu omborni tanlang:
   `https://github.com/javohirshokirjonov58-spec/IQ-test-bot.git`
4. Sozlamalarni tekshiring:
   - **Name**: `iq-test-bot` (yoki ixtiyoriy nom)
   - **Language**: `Python`
   - **Branch**: `main`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python bot.py`
   - **Instance Type**: `Free`
5. **Environment Variables** (Muhit o'zgaruvchilari) bo'limida:
   - `BOT_TOKEN`: `9007180538:AAFLnPX4WznaX9kI6o3CaQPwq9guajQKQjU`
   - `PORT`: `10000`
6. **"Deploy Web Service"** tugmasini bosing!
7. Render avtomatik ravishda kutubxonalarni o'rnatadi, HTTP portni ochadi va Telegram botingiz ishga tushadi! ✅

---

## 📂 Loyiha tuzilishi

```text
├── bot.py             # Asosiy bot logikasi va Render HTTP serveri
├── questions.py       # 15 ta IQ test savollari va natijani baholash funksiyasi
├── database.py        # SQLite ma'lumotlar bazasi (foydalanuvchilar va natijalar)
├── keyboards.py       # Telegram tugmalari (menyu, variantlar, xatolar tahlili)
├── config.py          # Sozlamalar va muhit o'zgaruvchilari
├── requirements.txt   # Kerakli Python kutubxonalari
├── Procfile           # Render/Heroku ishga tushirish buyrug'i
├── render.yaml        # Render 1-click avtomatik konfiguratsiyasi
├── .env.example       # Token va port namunasi
└── README.md          # Loyiha qo'llanmasi
```
