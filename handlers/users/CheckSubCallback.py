from aiogram import types
import data
from keyboards.default.mainMenu import MAIN_MENU

from loader import dp, bot

@dp.callback_query_handler(text="Checksub")
async def checkCallUser(query: types.CallbackQuery):
    User = query.from_user
    MSG = query.message
    status = await bot.get_chat_member(data.config.CHANNELS[0], User.id)
    all_status = ['creator','administrator','member']
    if status.status in all_status:
        await query.answer(text="Ok, have a good day", cache_time=0)
        await bot.delete_message(User.id, query.message.message_id)
        await bot.send_message(User.id, "Kanallarga azoligingiz tasdiqlandi...\n\n✅✅✅")
        await bot.send_message(chat_id=MSG.chat.id, text="Kerakli bo'limni tanlang!", reply_markup=MAIN_MENU)
    else:
        await query.answer(text="Iltimos kanallarga azo bo'lmasangiz bot siz uchun ishlamaydi.",
        show_alert=True, cache_time=0)