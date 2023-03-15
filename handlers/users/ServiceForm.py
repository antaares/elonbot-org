import asyncio
from aiogram.dispatcher.filters import Text
from aiogram import types
from aiogram.dispatcher.storage import FSMContext

from keyboards.default.cancel_keys import CANCEL
from keyboards.default.mainHomeKeys import CONFIRM
from keyboards.default.mainMenu import MAIN_MENU

from filters import IsPrivate

from loader import dp, bot, db 
from data.config import ADMIN_GROUP, ADMINS

from keyboards.inline.mainHomeKeys import ADMIN_CONFIRM

from states.menuStates import ServiceMenu
from utils.photograph import upload_photo





TEXT = {
    'start': ("Assalomu alaykum, Xizmatlar bo‘yicha reklama bo‘limiga xush kelibsiz!!!\n"\
              "Iltimos arizangiz qabul qilinishi uchun barcha talablarni to‘g‘ri bajaring...\n"\
                "Formani bekor qilish uchun /cancel buyrug'ini bering...\n\n\n"\
                "Xizmatlaringizni turini yozing:"),
    'description': "Xizmatlaringiz haqida to'liqroq izoh yozing  {1000 ta belgi kiritishingiz mumkin!}:",
    'regions': "Xizmatlaringizni qaysi hududlarda faoliyat ko'rsatadi:",
    'number': "Bog'lanish uchun elefon raqamingizni kiriting:",
    'photo': "Iltimos xizmatlaringizni ifodalaydigan bir dona suratni yuklang...",
}









@dp.message_handler(IsPrivate(),Text(equals="🛠Xizmatlar🪜"))
async def startServiceForm(message: types.Message, state: FSMContext):
    text = TEXT['start']
    await message.answer(text=text, reply_markup= CANCEL)
    await ServiceMenu.service_type.set()




@dp.message_handler(IsPrivate(), state=ServiceMenu.service_type)
async def serviceType(message: types.Message, state: FSMContext):
    text = TEXT['description']
    await message.answer(text=text, reply_markup= CANCEL)
    await state.update_data(service_type=message.text)
    await ServiceMenu.description.set()
    try:
        await bot.delete_message(message.chat.id, message.message_id-1)
        await message.delete()
    except Exception as e:
        print(e)


@dp.message_handler(IsPrivate(), state=ServiceMenu.description)
async def serviceDescription(message: types.Message, state: FSMContext):
    text = TEXT['regions']
    await message.answer(text=text, reply_markup= CANCEL)
    await state.update_data(description=message.text)
    await ServiceMenu.regions.set()
    try:
        await bot.delete_message(message.chat.id, message.message_id-1)
        await message.delete()
    except Exception as e:
        print(e)


@dp.message_handler(IsPrivate(), state=ServiceMenu.regions)
async def serviceRegions(message: types.Message, state: FSMContext):
    text = TEXT['number']
    await message.answer(text=text, reply_markup= CANCEL)
    await state.update_data(regions=message.text)
    await ServiceMenu.number.set()
    try:
        await bot.delete_message(message.chat.id, message.message_id-1)
        await message.delete()
    except Exception as e:
        print(e)



@dp.message_handler(IsPrivate(), state=ServiceMenu.number)
async def serviceNumber(message: types.Message, state: FSMContext):
    text = TEXT['photo']
    await message.answer(text=text, reply_markup= CANCEL)
    await state.update_data(number=message.text)
    await ServiceMenu.photo.set()
    try:
        await bot.delete_message(message.chat.id, message.message_id-1)
        await message.delete()
    except Exception as e:
        print(e)



@dp.message_handler(IsPrivate(), content_types = types.ContentType.PHOTO,state=ServiceMenu.photo)
async def servicePhoto(message: types.Message, state: FSMContext):
    await message.answer(text="Iltimos kuting...", reply_markup= CANCEL)
    photo = message.photo[-1]
    link = await upload_photo(photo = photo)
    await state.update_data(photo = link)
    await message.delete()
    try:
        await bot.delete_message(message.chat.id, message.message_id-1)
    except Exception as e:
        print(e)
    await confirmation(message, state)





@dp.message_handler(IsPrivate(), state=ServiceMenu.UserConfirm)
async def userConfirm(message: types.Message, state: FSMContext):
    state1 = await state.get_data()
    data = message.text
    if data == "To‘g‘ri":
        data = await state.get_data()
        await bot.copy_message(ADMIN_GROUP, message.chat.id, data['msg_id'], reply_markup=ADMIN_CONFIRM(message.from_user.id))
        
        await message.answer("Siz yaratgan ariza adminlarga yuborildi.")

        # await save_to_db(state, message.chat.id)
        await state.finish()
    else:
        await bot.delete_message(message.chat.id, message.message_id-2)
        await bot.delete_message(message.chat.id, message.message_id-1)
        await message.delete()
        db.delete_ad(message.chat.id, state1['unique_id'])
        await state.finish()
        
    await bot.send_message(chat_id=message.chat.id, text="Kerakli bo'limni tanlang!", reply_markup=MAIN_MENU)









async def confirmation(message: types.Message, state: FSMContext):
    await message.answer("Siz yuborgan ma'lumotlar to‘g‘ri ekanligiga ishonchingiz komilmi?")
    data = await state.get_data()
    photo = data['photo']
    id = await save_to_db(state, message.chat.id)
    await state.update_data(unique_id=id)
    text = await returnDatas(state, id)
    ##
    await asyncio.sleep(0.5)
    msg = await message.answer_photo(
        photo=photo,
        caption=text, 
        reply_markup = CONFIRM)
    ##
    await ServiceMenu.UserConfirm.set()
    msg_id = msg.message_id
    await state.update_data(msg_id=msg_id)





async def returnDatas(state: FSMContext, unique_id: int):
    data = await state.get_data()
    service_type = data['service_type']
    description = data['description']
    regions = data['regions']
    number = data['number']
    photo = data['photo']
    text = f"#Xizmatlar   #id{unique_id}\n\n"\
            f"Xizmat turi: {service_type}\n"\
            f"Xizmat haqida: {description}\n"\
            f"Xizmat faoliyat hududlari: {regions}\n"\
            f"Xizmatlarga bog'lanish uchun raqam: {number}\n\n"\
            f"E'lonlaringizni @elonlartaxtasibot orqali yuboring!"
    return text
            




async def save_to_db(state: FSMContext, user_id):
    data = await state.get_data()
    return db.add_service(
        user_id = user_id,
        service_name = data['service_type'],
        description = data['description'],
        regions = data['regions'],
        number = data['number'],
        photo = data['photo']
    )



