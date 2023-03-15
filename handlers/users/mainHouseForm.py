import asyncio
from aiogram.dispatcher.filters import Text
from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from data.config import ADMIN_GROUP


from filters import IsPrivate
from keyboards.default.cancel_keys import CANCEL
from keyboards.default.mainHomeKeys import CONFIRM
from keyboards.inline.mainHomeKeys import ADMIN_CONFIRM
from keyboards.default.mainMenu import MAIN_MENU
from loader import dp,db, bot

from utils.photograph import upload_photo




TEXT = {
    'start': ("Assalomu alaykum, Hovlili uylar bo‘yicha reklama bo‘limiga xush kelibsiz!!!\n"
        "Iltimos arizangiz qabul qilinishi uchun barcha talablarni to‘g‘ri bajaring...\n\n"
        "Formani bekor qilish uchun /cancel buyrug'ini bering...\n\n\n"
        "Uyning umumiy maydonini kiriting:"),
    'rooms': "Yashash xonalari soni qancha?",
    'qulay': "Qulayliklar haqida yozing(gaz, chiroq, suv va hakazo...):",
    'holat': "Uyning holati haqida qisqacha yozing:",
    'cost': "Uyga taklif qiladigan narxingizni yozing:",
    'phone': "Bog‘lanish uchun telefon raqam kiriting:",
    'city': "Uyning manzilini kiriting(masalan: Toshkent, Samarqand, Urgut) :",
    'photo': "Uyingizning bir dona suratini yuboring:"
    }





from states.menuStates import MainHouse

@dp.message_handler(IsPrivate(),Text(equals="🏡Hovlili uylar"), state="*")
async def startHouseForm(message: types.Message, state: FSMContext):
    text = TEXT['start'] 
    await message.answer(text=text, reply_markup=CANCEL)
    await MainHouse.totalArea.set()




@dp.message_handler(state=MainHouse.totalArea)
async def getTotalArea(message: types.Message, state: FSMContext):
    data = message.text
    await state.update_data(area = data)
    await message.answer(TEXT['rooms'])
    await MainHouse.countRooms.set()
    try:
        await bot.delete_message(message.chat.id, message.message_id-1)
        await message.delete()
    except:
        pass

@dp.message_handler(state=MainHouse.countRooms)
async def getRooms(message: types.Message, state: FSMContext):
    data = message.text
    await state.update_data(rooms = data)
    await message.answer(TEXT['qulay'])
    await MainHouse.conveniences.set()
    try:
        await bot.delete_message(message.chat.id, message.message_id-1)
        await message.delete()
    except:
        pass

@dp.message_handler(state=MainHouse.conveniences)
async def getConveniences(message: types.Message, state: FSMContext):
    data = message.text
    await state.update_data(conven = data)
    await message.answer(text=TEXT['holat'])
    await MainHouse.houseState.set()
    try:
        await bot.delete_message(message.chat.id, message.message_id-1)
        await message.delete()
    except:
        pass

@dp.message_handler(state=MainHouse.houseState)
async def getHomeState(message: types.Message, state: FSMContext):
    await message.answer(TEXT['cost'])
    await MainHouse.houseCost.set()
    data = message.text
    await state.update_data(homestate = data)
    try:
        await bot.delete_message(message.chat.id, message.message_id-1)
        await message.delete()
    except:
        pass


@dp.message_handler(state=MainHouse.houseCost)
async def getHouseCost(message: types.Message, state: FSMContext):
    data = message.text
    await state.update_data(cost = data)
    await message.answer(TEXT['phone'])
    await MainHouse.housePhoneNumber.set()
    try:
        await bot.delete_message(message.chat.id, message.message_id-1)
        await message.delete()
    except:
        pass

@dp.message_handler(state=MainHouse.housePhoneNumber)
async def getHomeCost(message: types.Message, state: FSMContext):
    data = message.text
    await state.update_data(number = data)
    await message.answer(TEXT['city'])
    await MainHouse.address.set()
    try:
        await bot.delete_message(message.chat.id, message.message_id-1)
        await message.delete()
    except:
        pass

@dp.message_handler(state=MainHouse.address)
async def getHouseCost(message: types.Message, state: FSMContext):
    data = "#" + message.text.replace(" "," #")
    await state.update_data(address = data)
    await message.answer(TEXT['photo'])
    await MainHouse.getHousePhoto.set()
    try:
        await bot.delete_message(message.chat.id, message.message_id-1)
        await message.delete()
    except:
        pass

@dp.message_handler(content_types='photo', state=MainHouse.getHousePhoto)
async def getPhoto(message: types.Message, state: FSMContext):
    photo = message.photo[-1]
    link = await upload_photo(photo = photo)
    await state.update_data(photo = link)
    try:
        await bot.delete_message(message.chat.id, message.message_id-1)
        await message.delete()
    except:
        pass
    await confirmation(message, state)



@dp.message_handler(state=MainHouse.UserConfirm)
async def userConfirm(message: types.Message, state: FSMContext):
    data = message.text
    if data == "To‘g‘ri":
        data = await state.get_data()
        await bot.copy_message(ADMIN_GROUP, message.chat.id, data['msg_id'], reply_markup=ADMIN_CONFIRM(message.from_user.id))
        
        await message.answer("Siz yaratgan ariza adminlarga yuborildi.")

        await save_to_db(state, message.chat.id)
        await state.finish()
    else:
        await bot.delete_message(message.chat.id, message.message_id-2)
        await bot.delete_message(message.chat.id, message.message_id-1)
        await message.delete()
        await state.finish()
    await bot.send_message(chat_id=message.chat.id, text="Kerakli bo'limni tanlang!", reply_markup=MAIN_MENU)

async def returnDatas(state: FSMContext):
    data = await state.get_data()
    area = data['area']
    rooms = data['rooms']
    conven = data['conven']
    homestate = data['homestate']
    cost = data['cost']
    number = data['number']
    address = data['address']
    text = f"🏘 Uyning umumiy maydoni: {area}\n"\
        f"🏗 Yashash xonalar soni: {rooms}\n"\
        f"🏖 Uydagi qulayliklar: {conven}\n"\
        f"🏠 Uyning holati: {homestate}\n"\
        f"🏦 Uyga taklif qilingan narx: {cost}\n"\
        f"☎️ Telefon raqam: {number}\n"\
        f"📍 Uyning manzili: {address}\n\n"\
        f"E'lonlaringizni @elonlartaxtasibot orqali yuboring!"
    return text














async def confirmation(message: types.Message, state: FSMContext):
    await message.answer("Siz yuborgan ma'lumotlar to‘g‘ri ekanligiga ishonchingiz komilmi?")
    data = await state.get_data()
    photo = data['photo']
    text = await returnDatas(state)
    ##
    await asyncio.sleep(0.5)
    msg = await message.answer_photo(
        photo=photo,
        caption=text, 
        reply_markup = CONFIRM)
    ##
    await MainHouse.UserConfirm.set()
    msg_id = msg.message_id
    await state.update_data(msg_id=msg_id)
    








async def save_to_db(data: FSMContext, user_id: int):
    data = await data.get_data()
    db.add_house(
        area=data['area'],
        rooms=data['rooms'],
        conven=data['conven'],
        house_state=data['homestate'],
        cost=data['cost'],
        number=data['number'],
        address=data['address'],
        photo=data['photo'],
        user_id=user_id
    )