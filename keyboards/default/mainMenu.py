from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


MAIN_MENU = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🚔Avtomobil"),
            KeyboardButton(text="🛠Xizmatlar🪜")
        ],
        [
            KeyboardButton(text="🏡Hovlili uylar"),
            KeyboardButton(text="🏬 Kop qavatli uylar")
        ],
        [
            KeyboardButton(text="Boshqa turdagi e'lonlar"),
            # own ads button
            KeyboardButton(text="📝E'lonlarim")
        ]
    ],
    resize_keyboard=True,
    selective=True
)