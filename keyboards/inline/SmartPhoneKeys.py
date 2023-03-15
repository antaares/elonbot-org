from aiogram.types import InlineKeyboardMarkup,InlineKeyboardButton

DEVICE_DOCS = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Bor", callback_data="Bor"),
            InlineKeyboardButton(text="Yo‘q", callback_data="Yoq")
        ]
    ]
)

DEVICE_BOX = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Bor", callback_data="Bor"),
            InlineKeyboardButton(text="Yo‘q", callback_data="Yoq")
        ]
    ]
)