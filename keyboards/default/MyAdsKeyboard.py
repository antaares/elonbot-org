from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


MyAdsKeyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📝Mening e'lonlarim"),
            KeyboardButton(text="/cancel"),

        ],
    ],
    resize_keyboard= True
)