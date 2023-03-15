from aiogram.types import InlineKeyboardMarkup,InlineKeyboardButton

AUTO_POSITION = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="1", callback_data="position1"),
            InlineKeyboardButton(text="2", callback_data="position2"),
            InlineKeyboardButton(text="3", callback_data="position3"),
            InlineKeyboardButton(text="4", callback_data="position4")
        ]
    ]
)
CAR_STATE = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="kraska bor", callback_data='Kraska bor'),
            InlineKeyboardButton(text='Kraska toza', callback_data='Kraska toza')
        ]
    ]
)
TRANSMISSION_BOX = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Avtomat", callback_data="avtomatik"),
            InlineKeyboardButton(text="Mexanika", callback_data="mexanika")
        ]
    ]
)