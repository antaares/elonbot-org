import asyncio
from aiogram import types
from states.menuStates import MainAuto
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

from keyboards.default.mainHomeKeys import CONFIRM
from keyboards.default.cancel_keys import CANCEL
from keyboards.default.mainMenu import MAIN_MENU
from keyboards.inline.mainHomeKeys import ADMIN_CONFIRM
from keyboards.inline.autoKeys import AUTO_POSITION, CAR_STATE, TRANSMISSION_BOX

from loader import dp, bot, db
from filters import IsPrivate
from data.config import ADMIN_GROUP
from utils.photograph import upload_photo






TEXT = {
    'start': ("Assalomu alaykum, Avtomobillar bo‘yicha reklama bo‘limiga xush kelibsiz!!!\n"
        "Iltimos arizangiz qabul qilinishi uchun barcha talablarni to‘g‘ri bajaring...\n"
        "Formani bekor qilish uchun /cancel buyrug'ini bering...\n\n\n"
        "Avtomobile modelini kiriting:"),
    'position': "Avtomobil pozitsiyasini belgilang",
    'color': "Avtomobil rangini yozing:",
    'now': "Avtomobilning hozirgi holati haqida qisqacha yozing:",
    'box': "Avtomobilning uzatish qutisi qanday?\nTanlang:",
    'phone': "Telefon raqam kiriting:",
    'city': "Qaysi shahardansiz?",
    'photo': "Iltimos Avtomobilning bir dona suratini yuboring:",
    'year': "Avtomobil ishlab chiqarilgan yilni kiriting",
    'distance': "Avtomobil umumiy yurib otgan masofasini kiriting:",
    'cost': "Avtomobilga taklif qiladigan narxni kiriting:"
}
















@dp.message_handler(IsPrivate(),Text(equals="🚔Avtomobil"))
async def startAutoForm(message: types.Message, state: FSMContext):
    text = TEXT['start']
    await message.answer(text=text, reply_markup= CANCEL)
    await MainAuto.model.set()





@dp.message_handler(state=MainAuto.model)
async def getAutoModel(message: types.Message, state: FSMContext):
    await message.answer(TEXT['position'], reply_markup=AUTO_POSITION)
    model = message.text
    await state.update_data(model=model)
    await MainAuto.position.set()
    try:
        await bot.delete_message(message.chat.id, message.message_id-1)
        await message.delete()
    except:
        pass


@dp.message_handler(state=MainAuto.manuYear)
async def getManuYear(message: types.Message, state: FSMContext):
    data = message.text
    await state.update_data(manuyear=data)
    await message.answer(TEXT['color'])
    await MainAuto.carColor.set()
    try:
        await bot.delete_message(message.chat.id, message.message_id-1)
        await message.delete()
    except:
        pass

@dp.message_handler(state=MainAuto.carColor)
async def getCarColor(message: types.Message, state: FSMContext):
    data = message.text
    await state.update_data(color=data)
    await message.answer(TEXT['now'])
    await MainAuto.carState.set()
    try:
        await bot.delete_message(message.chat.id, message.message_id-1)
        await message.delete()
    except:
        pass


@dp.message_handler(state=MainAuto.carState)
async def getCarState(message: types.Message, state: FSMContext):
    data = message.text
    await state.update_data(carstate=data)
    await message.answer(TEXT['distance'])
    await MainAuto.distance.set()
    try:
        await bot.delete_message(message.chat.id, message.message_id-1)
        await message.delete()
    except:
        pass







@dp.message_handler(state=MainAuto.distance)
async def getDistance(message: types.Message, state: FSMContext):
    distance = message.text
    await state.update_data(distance=distance)
    await message.answer(TEXT['box'], reply_markup=TRANSMISSION_BOX)
    await MainAuto.transBox.set()
    try:
        await bot.delete_message(message.chat.id, message.message_id-1)
        await message.delete()
    except:
        pass



@dp.message_handler(state=MainAuto.carCost)
async def getCarCost(message: types.Message, state: FSMContext):
    data = message.text
    await state.update_data(carcost=data)
    await message.answer(TEXT['phone'])
    await MainAuto.phoneNumber.set()
    try:
        await bot.delete_message(message.chat.id, message.message_id-1)
        await message.delete()
    except:
        pass

@dp.message_handler(state=MainAuto.phoneNumber)
async def getPhoneNumber(message: types.Message, state: FSMContext):
    data = message.text
    await state.update_data(number=data)
    await message.answer(TEXT['city'])             #######  "Qaysi shahardansiz?"
    await MainAuto.address.set()
    try:
        await bot.delete_message(message.chat.id, message.message_id-1)
        await message.delete()
    except:
        pass
@dp.message_handler(state=MainAuto.address)
async def getAddress(message: types.Message, state: FSMContext):
    address = message.text
    await state.update_data(address=address)
    await message.answer(TEXT['photo'])
    await MainAuto.carPhoto.set()
    try:
        await bot.delete_message(message.chat.id, message.message_id-1)
        await message.delete()
    except:
        pass

@dp.message_handler(content_types=types.ContentType.PHOTO, state=MainAuto.carPhoto)
async def getCarPhoto(message: types.Message, state: FSMContext):
    photo = message.photo[-1]
    link = await upload_photo(photo = photo)
    await state.update_data(photo = link)
    await message.delete()
    try:
        await bot.delete_message(message.chat.id, message.message_id-1)
    except:
        pass
    await confirmation(message, state)


@dp.message_handler(state=MainAuto.UserConfirm)
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












@dp.callback_query_handler(state=MainAuto.position)
async def callAutoModel(query: types.CallbackQuery, state: FSMContext):
    position = query.data[-1]
    await query.answer(cache_time=0)
    await state.update_data(position=position)
    await bot.send_message(query.message.chat.id, TEXT['year'])
    await MainAuto.manuYear.set()
    try:
        await bot.delete_message(query.message.chat.id, query.message.message_id)
    except:
        pass





@dp.callback_query_handler(state=MainAuto.transBox)
async def getTransBox(query: types.CallbackQuery, state: FSMContext):
    data = query.data
    await state.update_data(transbox=data)
    await query.answer(cache_time=0)
    await bot.send_message(query.message.chat.id, TEXT['cost'])
    await MainAuto.carCost.set()
    try:
        await bot.delete_message(query.message.chat.id, query.message.message_id)
    except:
        pass





async def returnDatas(state: FSMContext, unique_id: int):
    data = await state.get_data()
    model = data['model']
    position = data['position']
    year = data['manuyear']
    color = data['color']
    carstate = data['carstate']
    distance = data['distance']
    box = data['transbox']
    cost = data['carcost']
    number = data['number']
    address = data['address']
    text = f"#{address} #avto #{model.split()[0]}\t  #id{unique_id}\n"
    text += f"🚔 Avtomobil: {model}\n"
    text += f"➖ Yili: {year}\n"
    text += f"🏎 Pozitsiyasi: {position}\n"
    text += f"➖ Yurgan masofasi: {distance}\n"
    text += f"➖ Rangi: {color}\n"
    text += f"➖ Uzatmalar qutisi: {box}\n"
    text += f"➖ Avtomobil holati: {carstate}\n"
    text += f"➖ Narx: {cost}\n"
    text += f"☎️ Telefon: {number}\n"
    text += f"📍 Manzil: {address}\n\n"
    text += f"E'lonlaringizni @elonlartaxtasibot orqali yuboring!"
    return text


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
    await MainAuto.UserConfirm.set()
    msg_id = msg.message_id
    await state.update_data({'msg_id':msg_id})






async def save_to_db(data: FSMContext, user_id: int):
    data = await data.get_data()
    return db.add_auto(
        model=data['model'],
        position=data['position'],
        year=data['manuyear'],
        car_state=data['carstate'],
        distance=data['distance'],
        color=data['color'],
        number=data['number'],
        cost=data['carcost'],
        transbox=data['transbox'],
        address=data['address'],
        photo=data['photo'],
        user_id=user_id
    )
