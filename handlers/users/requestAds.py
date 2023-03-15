from aiogram import types
from data.config import CHANNELS
from keyboards.inline.group_admins import comment_client, info_admins

from states.AdminStates import Comment

from aiogram.dispatcher.storage import FSMContext
from aiogram.dispatcher.filters import Text


from loader import dp, bot 


@dp.callback_query_handler(Text(startswith='admin'))
async def CallBackReceive(query: types.CallbackQuery, state: FSMContext):
    data = query.data
    user = data.split("|")[-1]
    admin_name = data.split("|")[-2]
    admin_id = data.split("|")[-1]
    if data.startswith("admininfo"):
        return await query.answer(
            text="Ma'lumot:\nAdmin ismi:{}\nadmin id:{}".format(admin_name, admin_id), 
            show_alert=True,
            cache_time=0
            )
    
    if data.startswith("adminconfirm"):
        admin_id = query.from_user.id
        admin_name = query.from_user.full_name
        txt = f"Sizning arizangiz qabul qilindi va tez orada kanalga joylanadi. https://t.me/elonlartahtasi"
        await bot.send_message(chat_id=int(user), text=txt)
        await query.message.edit_reply_markup(
            reply_markup= await info_admins(name=admin_name, admin_id=admin_id, hint=True)
            )
        await state.finish()

    else:
        admin_id = query.from_user.id
        admin_name = query.from_user.full_name
        await query.message.edit_reply_markup(
            reply_markup=await info_admins(name=admin_name, admin_id=admin_id, hint=False)
            )
        await query.message.answer("Arizachiga izoh qoldirishingiz mumkin!", reply_markup=await comment_client(user_id=user))
        await bot.send_message(chat_id=int(user), text="Sizning arizangiz qabul qilinmadi!,\nQaytadan urinib ko'ring.")
        await state.finish()