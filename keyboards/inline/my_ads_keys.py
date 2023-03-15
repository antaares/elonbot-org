from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton



# inline button for activate or deactivate and delete ad
async def ad_methods(ad_id: int):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text='aktivatsiya', callback_data=f'myactivate|{ad_id}'))
    markup.add(InlineKeyboardButton(text='deaktivatsiya', callback_data=f'mydeactivate|{ad_id}'))
    markup.add(InlineKeyboardButton(text="o'chirish", callback_data=f'mydelete|{ad_id}'))
    markup.add(InlineKeyboardButton(text='orqaga', callback_data='myback'))
    return markup
