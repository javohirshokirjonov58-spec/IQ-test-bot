"""
Telegram IQ Test Bot - Asosiy fayl.
Render.com va serverlarda ishlashga to'liq moslashtirilgan.
Aiogram 3.x va aiohttp (health-check / web service) bilan ishlaydi.
"""

import asyncio
import logging
import sys
from typing import Dict, Any

from aiohttp import web
from aiogram import Bot, Dispatcher, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.client.default import DefaultBotProperties

import config
import database
from questions import QUESTIONS, calculate_iq
import keyboards

# Loglarni sozlash
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("IQTestBot")

# Bot va Dispatcher obyektlari
bot = Bot(
    token=config.BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()

# Foydalanuvchilarning faol test sessiyalari (In-Memory)
# active_tests[user_id] = {
#     "current_idx": int,
#     "score": int,
#     "mistakes": list,
#     "message_id": int
# }
active_tests: Dict[int, Dict[str, Any]] = {}


def generate_progress_bar(current: int, total: int) -> str:
    """Progress bar emojisi yaratish (Masalan: [🟩🟩🟩⬜⬜⬜⬜⬜] 3/15)."""
    blocks = 10
    filled = int((current / total) * blocks)
    bar = "🟩" * filled + "⬜" * (blocks - filled)
    return f"[{bar}] {current}/{total}"


def format_question_text(q_data: dict, current_idx: int, total: int) -> str:
    """Savol matnini chiroyli formatda tayyorlash."""
    progress = generate_progress_bar(current_idx + 1, total)
    category = q_data.get("category", "💡 Mantiq")
    
    text = (
        f"<b>{category}</b>\n"
        f"📊 <i>Jarayon: {progress}</i>\n"
        f"━━━━━━━━━━━━━━━━━━\n\n"
        f"<b>❓ {current_idx + 1}-savol:</b>\n"
        f"{q_data['question']}\n\n"
        f"<i>Quyidagi javoblardan birini tanlang 👇</i>"
    )
    return text


# ===================== KOMANDALAR =====================

@dp.message(CommandStart())
async def cmd_start(message: Message):
    """Start komandasi - foydalanuvchini ro'yxatga olish va salomlashish."""
    user = message.from_user
    database.register_user(
        telegram_id=user.id,
        username=user.username,
        full_name=user.full_name
    )

    welcome_text = (
        f"Assalomu alaykum, <b>{user.full_name}</b>! 🧠👋\n\n"
        f"<b>IQ Test Bot</b>ga xush kelibsiz!\n"
        f"Ushbu bot sizning mantiqiy, analitik va fazoviy fikrlash qobiliyatingizni "
        f"sinab ko'rish hamda IQ darajangizni aniqlash uchun maxsus ishlab chiqilgan.\n\n"
        f"📌 <b>Test haqida:</b>\n"
        f"• Savollar soni: <b>{len(QUESTIONS)} ta</b>\n"
        f"• Yo'nalishlar: <i>Ketma-ketlik, Analitika, Matematik mantiq, Fazoviy tasavvur</i>\n"
        f"• Test yakunida: <b>Aniq IQ bali</b> va <b>xatolar tahlili</b> beriladi!\n\n"
        f"O'z intellektingizni sinab ko'rishga tayyormisiz? Unda quyidagi tugmani bosing:"
    )

    await message.answer(
        text=welcome_text,
        reply_markup=keyboards.get_main_menu_keyboard()
    )


@dp.message(F.text == "🎯 Testni boshlash")
@dp.message(Command("test"))
async def start_iq_test(message: Message):
    """Testni boshlash funksiyasi."""
    user_id = message.from_user.id
    
    # Sessiyani tozalash / yangilash
    active_tests[user_id] = {
        "current_idx": 0,
        "score": 0,
        "mistakes": [],
        "last_results": None
    }

    first_q = QUESTIONS[0]
    text = format_question_text(first_q, 0, len(QUESTIONS))
    markup = keyboards.get_question_keyboard(first_q["id"], first_q["options"])

    sent_msg = await message.answer(text=text, reply_markup=markup)
    active_tests[user_id]["message_id"] = sent_msg.message_id


@dp.message(F.text == "📊 Mening natijalarim")
@dp.message(Command("stats"))
async def show_user_stats(message: Message):
    """Foydalanuvchining shaxsiy statistikasini ko'rsatish."""
    user_id = message.from_user.id
    stats = database.get_user_stats(user_id)

    if not stats:
        await message.answer(
            "Siz hali biron marta IQ test topshirmagansiz! 🧐\n"
            "Hoziroq '🎯 Testni boshlash' tugmasini bosing va o'z intellektingizni sinang!",
            reply_markup=keyboards.get_main_menu_keyboard()
        )
        return

    text = (
        f"📊 <b>Sizning IQ statistikangiz:</b>\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"🎯 Urinishlar soni: <b>{stats['attempts']} ta</b>\n"
        f"🏆 Eng yuqori IQ: <b>{stats['best_iq']}</b>\n"
        f"⭐️ Eng yaxshi ball: <b>{stats['best_score']} / {len(QUESTIONS)}</b>\n"
        f"📈 O'rtacha ball: <b>{stats['avg_score']}</b>\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"Oxirgi natija: IQ <b>{stats['last_iq']}</b> ({stats['last_score']}/{len(QUESTIONS)})\n"
        f"Sana: <i>{stats['last_date']}</i>"
    )
    await message.answer(text=text, reply_markup=keyboards.get_main_menu_keyboard())


@dp.message(F.text == "🏆 Top reyting")
@dp.message(Command("leaderboard"))
async def show_leaderboard(message: Message):
    """Eng yuqori IQ egalari reytingi."""
    top_users = database.get_top_leaderboard(limit=10)
    total_count = database.get_total_users_count()

    if not top_users:
        await message.answer(
            "Hozircha reyting jadvali bo'sh. Birinchi bo'lib testni topshiring!",
            reply_markup=keyboards.get_main_menu_keyboard()
        )
        return

    medals = ["🥇", "🥈", "🥉"]
    text = "🏆 <b>Eng yuqori IQ ko'rsatkichli bilimdonlar:</b>\n━━━━━━━━━━━━━━━━━━\n"

    for i, u in enumerate(top_users):
        rank = medals[i] if i < 3 else f"<b>{i+1}.</b>"
        name = u["full_name"] or "Foydalanuvchi"
        if u["username"]:
            name = f"@{u['username']}"
        text += f"{rank} {name} — IQ <b>{u['max_iq']}</b> ({u['max_score']}/{len(QUESTIONS)})\n"

    text += f"\n👥 Jami ishtirokchilar: <b>{total_count} kishi</b>"

    await message.answer(text=text, reply_markup=keyboards.get_main_menu_keyboard())


@dp.message(F.text == "ℹ️ Bot haqida")
@dp.message(Command("about"))
async def show_about(message: Message):
    """Bot haqida ma'lumot."""
    about_text = (
        "🤖 <b>IQ Test Bot haqida:</b>\n"
        "━━━━━━━━━━━━━━━━━━\n"
        "Ushbu bot xalqaro intellekt koeffitsiyenti (IQ) metodologiyalari asosida tuzilgan.\n\n"
        "🔬 <b>Test nimani aniqlaydi?</b>\n"
        "• Mantiqiy xulosalar chiqarish qobiliyati\n"
        "• Sonlar va shakllar orasidagi ketma-ketliklarni ilg'ash\n"
        "• Tahliliy fikrlash tezligi\n\n"
        "📊 <b>IQ shkalasi:</b>\n"
        "• 140+ — Daho (Genius)\n"
        "• 120-139 — Juda yuqori intellekt\n"
        "• 110-119 — O'rtachadan yuqori\n"
        "• 90-109 — O'rtacha intellekt\n"
        "• 80-89 — O'rtachadan past\n\n"
        "⚡️ Do'stlaringizga ham ulashing va kim zukkorroq ekanini aniqlang!"
    )
    await message.answer(text=about_text, reply_markup=keyboards.get_main_menu_keyboard())


@dp.message(F.text == "❓ Qoidalar")
@dp.message(Command("rules"))
async def show_rules(message: Message):
    """Qoidalar haqida ma'lumot."""
    rules_text = (
        "📋 <b>Test qoidalari:</b>\n"
        "━━━━━━━━━━━━━━━━━━\n"
        "1. Test 15 ta savoldan iborat.\n"
        "2. Har bir savolda faqat 1 ta to'g'ri javob mavjud.\n"
        "3. Javobni tanlaganingizdan so'ng, uni o'zgartirib bo'lmaydi.\n"
        "4. Hech qanday shoshilish shart emas — diqqatni jamlab o'ylang.\n"
        "5. Test yakunida xatolaringiz va ularning yechimlari ko'rsatiladi!\n\n"
        "Boshlash uchun '🎯 Testni boshlash' tugmasini bosing."
    )
    await message.answer(text=rules_text, reply_markup=keyboards.get_main_menu_keyboard())


# ===================== CALLBACK HANDLERS =====================

@dp.callback_query(F.data.startswith("ans:"))
async def process_answer(callback: CallbackQuery):
    """Foydalanuvchi variant tanlaganda ishlovchi funksiya."""
    user_id = callback.from_user.id
    _, q_id_str, opt_idx_str = callback.data.split(":")
    q_id = int(q_id_str)
    selected_option = int(opt_idx_str)

    if user_id not in active_tests:
        await callback.answer("Faol test topilmadi. Qaytadan boshlang.", show_alert=True)
        return

    session = active_tests[user_id]
    current_idx = session["current_idx"]
    current_question = QUESTIONS[current_idx]

    # Javob to'g'riligini tekshirish
    is_correct = (selected_option == current_question["correct"])
    if is_correct:
        session["score"] += 1
    else:
        session["mistakes"].append({
            "q_idx": current_idx + 1,
            "question": current_question["question"],
            "user_choice": current_question["options"][selected_option],
            "correct_choice": current_question["options"][current_question["correct"]],
            "explanation": current_question["explanation"]
        })

    session["current_idx"] += 1

    # Keyingi savol bormi yoki test tugadimi?
    if session["current_idx"] < len(QUESTIONS):
        next_idx = session["current_idx"]
        next_q = QUESTIONS[next_idx]
        text = format_question_text(next_q, next_idx, len(QUESTIONS))
        markup = keyboards.get_question_keyboard(next_q["id"], next_q["options"])

        await callback.message.edit_text(text=text, reply_markup=markup)
        await callback.answer()
    else:
        # Test yakunlandi! Natijalarni hisoblash
        score = session["score"]
        total = len(QUESTIONS)
        result_data = calculate_iq(score, total)

        # Bazaga yozish
        database.save_result(
            telegram_id=user_id,
            score=score,
            total=total,
            iq=result_data["iq"]
        )

        session["last_results"] = result_data

        stars = "⭐️" * max(1, min(5, (score * 5) // total))
        result_text = (
            f"🎉 <b>TEST YAKUNLANDI!</b> 🎉\n"
            f"━━━━━━━━━━━━━━━━━━\n\n"
            f"👤 Foydalanuvchi: <b>{callback.from_user.full_name}</b>\n"
            f"🎯 To'g'ri javoblar: <b>{score} / {total}</b> ({result_data['percentage']}%)\n"
            f"🧠 Sizning IQ ko'rsatkichingiz: <b>{result_data['iq']} ball</b>\n"
            f"Daraja: <b>{result_data['title']}</b> {stars}\n\n"
            f"💬 <i>{result_data['desc']}</i>\n\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"Pastdagi tugmalar orqali xatolarni tahlil qilishingiz yoki testni qayta topshirishingiz mumkin 👇"
        )

        has_mistakes = len(session["mistakes"]) > 0
        await callback.message.edit_text(
            text=result_text,
            reply_markup=keyboards.get_result_keyboard(has_errors=has_mistakes)
        )
        await callback.answer("Natijangiz hisoblandi! 🏆")


@dp.callback_query(F.data == "test:cancel")
async def cancel_test_prompt(callback: CallbackQuery):
    """Testni to'xtatish so'rovi."""
    await callback.message.edit_text(
        "Haqiqatan ham testni to'xtatmoqchimisiz? Joriy natijalar saqlanmaydi.",
        reply_markup=keyboards.get_cancel_confirm_keyboard()
    )
    await callback.answer()


@dp.callback_query(F.data == "test:confirm_cancel")
async def cancel_test_confirm(callback: CallbackQuery):
    """Testni bekor qilishni tasdiqlash."""
    user_id = callback.from_user.id
    if user_id in active_tests:
        del active_tests[user_id]
    await callback.message.edit_text("Test bekor qilindi. Bosh menyudan foydalanishingiz mumkin.")
    await callback.answer("Test to'xtatildi")


@dp.callback_query(F.data == "test:resume")
async def resume_test(callback: CallbackQuery):
    """To'xtatilgan testni davom ettirish."""
    user_id = callback.from_user.id
    if user_id not in active_tests:
        await callback.message.edit_text("Sessiya tugagan. Yangi test boshlang.")
        return

    session = active_tests[user_id]
    idx = session["current_idx"]
    q_data = QUESTIONS[idx]
    text = format_question_text(q_data, idx, len(QUESTIONS))
    markup = keyboards.get_question_keyboard(q_data["id"], q_data["options"])

    await callback.message.edit_text(text=text, reply_markup=markup)
    await callback.answer()


@dp.callback_query(F.data == "test:restart")
async def restart_test_callback(callback: CallbackQuery):
    """Testni qaytadan boshlash."""
    user_id = callback.from_user.id
    active_tests[user_id] = {
        "current_idx": 0,
        "score": 0,
        "mistakes": [],
        "last_results": None
    }
    first_q = QUESTIONS[0]
    text = format_question_text(first_q, 0, len(QUESTIONS))
    markup = keyboards.get_question_keyboard(first_q["id"], first_q["options"])

    await callback.message.edit_text(text=text, reply_markup=markup)
    await callback.answer("Yangi test boshlandi!")


@dp.callback_query(F.data == "test:review")
async def review_mistakes_callback(callback: CallbackQuery):
    """Xatolar tahlili va yechimlarni ko'rsatish."""
    user_id = callback.from_user.id
    session = active_tests.get(user_id)

    if not session or not session.get("mistakes"):
        await callback.answer("Xatolar topilmadi yoki test yakunlanmagan!", show_alert=True)
        return

    mistakes = session["mistakes"]
    report = "🔍 <b>Xatolar va to'g'ri javoblar tahlili:</b>\n━━━━━━━━━━━━━━━━━━\n\n"

    for item in mistakes[:8]:  # Telegram xabar uzunligi chegarasi uchun
        report += (
            f"<b>{item['q_idx']}-savol:</b>\n"
            f"❌ Sizning javobingiz: <i>{item['user_choice']}</i>\n"
            f"✅ To'g'ri javob: <b>{item['correct_choice']}</b>\n"
            f"💡 Tushuntirish: {item['explanation']}\n\n"
        )

    if len(mistakes) > 8:
        report += f"<i>...va yana {len(mistakes) - 8} ta savol.</i>\n\n"

    report += "Mantiqiy fikrlashni rivojlantirish uchun qayta sinab ko'ring!"

    await callback.message.answer(
        text=report,
        reply_markup=keyboards.get_result_keyboard(has_errors=False)
    )
    await callback.answer()


@dp.callback_query(F.data == "action:leaderboard")
async def callback_leaderboard(callback: CallbackQuery):
    """Inline tugma orqali reytingni ko'rsatish."""
    top_users = database.get_top_leaderboard(limit=10)
    medals = ["🥇", "🥈", "🥉"]
    text = "🏆 <b>Eng yuqori IQ egalari reytingi:</b>\n━━━━━━━━━━━━━━━━━━\n"

    for i, u in enumerate(top_users):
        rank = medals[i] if i < 3 else f"<b>{i+1}.</b>"
        name = u["full_name"] or "Foydalanuvchi"
        if u["username"]:
            name = f"@{u['username']}"
        text += f"{rank} {name} — IQ <b>{u['max_iq']}</b>\n"

    await callback.message.answer(text=text)
    await callback.answer()


# ===================== RENDER WEB SERVER =====================

async def health_check_handler(request: web.Request) -> web.Response:
    """Render port health check uchun endpoint."""
    return web.json_response({
        "status": "healthy",
        "service": "Telegram IQ Test Bot",
        "version": "1.0.0"
    })


async def start_web_server():
    """Render uchun aiohttp HTTP serverini fonda ishga tushirish."""
    app = web.Application()
    app.router.add_get("/", health_check_handler)
    app.router.add_get("/health", health_check_handler)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", config.PORT)
    await site.start()
    logger.info(f"Render HTTP Web Server 0.0.0.0:{config.PORT} da ishga tushirildi.")


# ===================== ASOSIY ISHGA TUSHIRISH =====================

async def main():
    """Asosiy ishga tushirish funksiyasi."""
    logger.info("IQ Test Bot ishga tushmoqda...")
    
    # Bazani ishga tushirish
    database.init_db()

    # Render uchun HTTP serverini ishga tushirish
    await start_web_server()

    # Telegram bot pollingni boshlash
    logger.info("Telegram Polling boshlandi...")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot to'xtatildi.")
