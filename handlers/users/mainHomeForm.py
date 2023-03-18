import asyncio
from aiogram import types
from keyboards.default.cancel_keys import CANCEL
from keyboards.default.mainHomeKeys import CONFIRM
from keyboards.default.mainMenu import MAIN_MENU
from states.menuStates import MainHome
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

from loader import dp, bot, db
from filters import IsPrivate

from data.config import ADMIN_GROUP

from keyboards.inline.mainHomeKeys import ADMIN_CONFIRM, YES_AND_NO
from utils.photograph import upload_photo





TEXT = {
    'start': ("Assalomu alaykum, Kop qavatli uylar boyicha reklama bolimiga xush kelibsiz!!!\n"
        "Iltimos arizangiz qabul qilinishi uchun barcha talablarni togri bajaring...\n"
        "Formani bekor qilish uchun /cancel buyrug'ini bering...\n\n\n"
        "Binodagi jami qavatlar sonini kiriting: Masalan: 8"),
    'floor': "Qaysi qavatda turasiz? (masalan: 3 yoki 6):",
    'rooms': "Uydagi xonalar sonini kiriting: (masalan: 3 ta):",
    'things': "Uyning jihozlari bormi? Masalan: Bor, yo'q yoki Televizor, shkaf, muzlatgich",
    'cost': 'Uyga qanday narx taklif qilasiz? Masalan $30,000, $40,000',
    'conven': 'Uyning qulayliklari qanday? Masalan: Gaz, chiroq, suv, hakazo, internet',
    'phone': 'Boglanish uchun bitta telefon raqam qoldiring: Masalan: +998 90 123 45 67',
    'city': 'Qaysi shaharda yashaysiz? Masalan: Toshkent, Samarqand, Namangan',
    'photo': "Iltimos uyning bir dona suratini yuboring",
    'holat': "Uyning holati qanday? Masalan: Yangi, eskirmagan, yorilmagan...",
}












@dp.message_handler(IsPrivate(),Text(equals="🏬 Kop qavatli uylar"), state="*")
async def startHomeForm(message: types.Message, state: FSMContext):
    text = TEXT['start']
    await message.answer(text=text, reply_markup=CANCEL)
    await MainHome.totalFloor.set()





@dp.message_handler(state=MainHome.totalFloor)
async def getTotalFloor(message: types.Message, state: FSMContext):    
    await message.answer(TEXT['floor'])
    data = message.text
    await state.update_data(floor = data)
    await MainHome.currentFloor.set()
    try:
        await bot.delete_message(message.chat.id, message.message_id-1)
        await message.delete()
    except:
        pass


@dp.message_handler(state=MainHome.currentFloor)
async def getCurrentFloor(message: types.Message, state: FSMContext):
    await message.answer(TEXT['rooms'])
    data = message.text
    await state.update_data(current = data)
    await MainHome.countRooms.set()
    try:
        await bot.delete_message(message.chat.id, message.message_id-1)
        await message.delete()
    except:
        pass
    


@dp.message_handler(state=MainHome.countRooms)
async def getCountRooms(message: types.Message, state: FSMContext):
    data = message.text
    await state.update_data(rooms = data)
    await message.answer(TEXT['things'], reply_markup=YES_AND_NO)
    await MainHome.household.set()
    try:
        await bot.delete_message(message.chat.id, message.message_id-1)
        await message.delete()
    except:
        pass



@dp.message_handler(state=MainHome.household)
async def getHousehold(message: types.Message, state: FSMContext):
    data = message.text
    await state.update_data(household = data)
    await message.answer(TEXT['holat'])
    await MainHome.homeState.set()
    try:
        await bot.delete_message(message.chat.id, message.message_id-1)
        await message.delete()
    except:
        pass





@dp.message_handler(state=MainHome.homeState)
async def getHomeState(message: types.Message, state: FSMContext):
    data = message.text
    await state.update_data(homestate = data)
    await message.answer(TEXT['cost'])
    await MainHome.homeCost.set()
    try:
        await bot.delete_message(message.chat.id, message.message_id-1)
        await message.delete()
    except:
        pass


@dp.message_handler(state=MainHome.homeCost)
async def getHomeCost(message: types.Message, state: FSMContext):
    data = message.text
    await state.update_data(cost = data)
    await message.answer(TEXT['conven'])
    await MainHome.homeconven.set()
    try:
        await bot.delete_message(message.chat.id, message.message_id-1)
        await message.delete()
    except:
        pass

@dp.message_handler(state=MainHome.homeconven)
async def getHomeConven(message: types.Message, state: FSMContext):
    data = message.text
    await state.update_data(conven = data)
    await message.answer(TEXT['phone'])
    await MainHome.homePhoneNumber.set()
    try:
        await bot.delete_message(message.chat.id, message.message_id-1)
        await message.delete()
    except:
        pass


@dp.message_handler(state=MainHome.homePhoneNumber)
async def getHomeNumber(message: types.Message, state: FSMContext):
    data = message.text
    await state.update_data(number = data)
    await message.answer(TEXT['city'])
    await MainHome.address.set()
    try:
        await bot.delete_message(message.chat.id, message.message_id-1)
        await message.delete()
    except:
        pass

@dp.message_handler(state=MainHome.address)
async def getAddress(message: types.Message, state: FSMContext):
    data = "#" + message.text.replace(" ", " #")
    await state.update_data(address = data)
    await message.answer(TEXT['photo'])
    await MainHome.getHomePhoto.set()
    try:
        await bot.delete_message(message.chat.id, message.message_id-1)
        await message.delete()
    except:
        pass



@dp.message_handler(content_types='photo', state=MainHome.getHomePhoto)
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






@dp.message_handler(state=MainHome.UserConfirm)
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
    
















async def returnDatas(state: FSMContext, unique_id: int):
    data = await state.get_data()
    floors = data['floor']
    current = data['current']
    rooms = data['rooms']
    housuhold = data['household']
    homestate = data['homestate']
    conven = data['conven']
    cost = data['cost']
    number = data['number']
    address = data['address']
    text = f"<b>🏬 #Kvartira #id{unique_id}</b>\n"\
    f"<b>✅ Umumiy qavatlar:</b> {floors}\n"\
    f"<b>✅ Uyning joylashuv qavati:</b> {current}\n"\
    f"<b>✅ Umumiy xonalar:</b> {rooms}\n"\
    f"<b>✅ Uyning jihozlari:</b> {housuhold}\n"\
    f"<b>✅ Uyning holati: </b> {homestate}\n"\
    f"<b>🔗 Qoʻshimcha ma’lumotlar:</b> {conven}\n"\
    f"<b>💰 Uyning narxi:</b> {cost}\n"\
    f"<b>☎️ Telefon: </b>{number}\n"\
    f"<b>🚩 Manzil:</b> {address}\n\n"\
    f"<a href=\"https://t.me/BorBor_Bot\">Bor Bor | Bepul e’lon joylang!</a>"
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
    await MainHome.UserConfirm.set()
    msg_id = msg.message_id
    await state.update_data(msg_id = msg_id)
    









async def save_to_db(data: FSMContext, user_id: int):
    data = await data.get_data()
    floors = data['floor']
    current = data['current']
    rooms = data['rooms']
    things = data['things']
    homestate = data['homestate']
    cost = data['cost']
    number = data['number']
    address = data['address']
    photo = data['photo']

    db.add_home(
        user_id=user_id,
        total_floors=floors,
        rooms=rooms,
        current_floor=current,
        conven=things,
        home_state=homestate,
        cost=cost,
        number=number,
        address=address,
        photo=photo
        )
