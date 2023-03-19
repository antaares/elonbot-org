from aiogram.types import InlineKeyboardMarkup,InlineKeyboardButton

from data.config import CHANNEL_LINK
SUBSCRIBE = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Bor Bor", url=CHANNEL_LINK)],
        [InlineKeyboardButton(text="✅ Tekshirish", callback_data="Checksub")]
    ]
)