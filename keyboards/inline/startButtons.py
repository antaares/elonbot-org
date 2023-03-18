from aiogram.types import InlineKeyboardMarkup,InlineKeyboardButton

from data.config import CHANNEL_LINK
SUBSCRIBE = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Channel", url=CHANNEL_LINK)],
        [InlineKeyboardButton(text="Check", callback_data="Checksub")]
    ]
)