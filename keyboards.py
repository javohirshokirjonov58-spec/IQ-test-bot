"""
Telegram klaviaturalari va inline tugmalar.
"""

from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)


def get_main_menu_keyboard() -> ReplyKeyboardMarkup:
    """Asosiy menyu tugmalari."""
    keyboard = [
        [
            KeyboardButton(text="🎯 Testni boshlash")
        ],
        [
            KeyboardButton(text="📊 Mening natijalarim"),
            KeyboardButton(text="🏆 Top reyting")
        ],
        [
            KeyboardButton(text="ℹ️ Bot haqida"),
            KeyboardButton(text="❓ Qoidalar")
        ]
    ]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        input_field_placeholder="Quyidagi bo'limlardan birini tanlang:"
    )


def get_question_keyboard(question_id: int, options: list) -> InlineKeyboardMarkup:
    """Savol uchun 4 ta variant tugmalari."""
    keyboard = []
    letters = ["A", "B", "C", "D"]
    for idx, opt in enumerate(options):
        prefix = letters[idx] if idx < len(letters) else str(idx + 1)
        keyboard.append([
            InlineKeyboardButton(
                text=f"{prefix}) {opt}",
                callback_data=f"ans:{question_id}:{idx}"
            )
        ])
    
    # Bekor qilish tugmasi
    keyboard.append([
        InlineKeyboardButton(
            text="🛑 Testni to'xtatish",
            callback_data="test:cancel"
        )
    ])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_result_keyboard(has_errors: bool = True) -> InlineKeyboardMarkup:
    """Natija chiqqandan keyingi inline menyu."""
    buttons = [
        [
            InlineKeyboardButton(
                text="🔄 Qaytadan topshirish",
                callback_data="test:restart"
            )
        ]
    ]
    if has_errors:
        buttons.append([
            InlineKeyboardButton(
                text="🔍 Xatolar va tushuntirishlar",
                callback_data="test:review"
            )
        ])
    buttons.append([
        InlineKeyboardButton(
            text="🏆 Top reyting",
            callback_data="action:leaderboard"
        ),
        InlineKeyboardButton(
            text="📤 Do'stlarga ulashish",
            switch_inline_query="Men IQ testimni topshirdim! Siz ham o'z aqlingizni sinab ko'ring 🧠👇"
        )
    ])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_cancel_confirm_keyboard() -> InlineKeyboardMarkup:
    """Testni to'xtatishni tasdiqlash klaviaturasi."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Ha, to'xtatilsin", callback_data="test:confirm_cancel"),
                InlineKeyboardButton(text="❌ Davom etish", callback_data="test:resume")
            ]
        ]
    )
