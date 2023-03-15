from aiogram.types import ReplyKeyboardMarkup, KeyboardButton





async def all_ads_keyboard(all_ads: list):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=3)
    
    keyboard.add(*[KeyboardButton(ad) for ad in all_ads])
    keyboard.add(KeyboardButton("/cancel"))
    return keyboard