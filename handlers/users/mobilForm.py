from aiogram.dispatcher.filters import Text
from aiogram import types
from aiogram.dispatcher.storage import FSMContext

from keyboards.default.cancel_keys import CANCEL
from keyboards.default.mainHomeKeys import CONFIRM
from keyboards.default.mainMenu import MAIN_MENU

from filters import IsPrivate
from keyboards.inline.SmartPhoneKeys import DEVICE_BOX, DEVICE_DOCS
from loader import dp, bot, db 
from data.config import ADMIN_GROUP, ADMINS

from keyboards.inline.mainHomeKeys import ADMIN_CONFIRM

from states.menuStates import MainSmartphone
from utils.photograph import upload_photo





TEXT = {
    'start': ("Assalomu alaykum, Smartphonelar bo‘yicha reklama bo‘limiga xush kelibsiz!!!\n"
        "Iltimos arizangiz qabul qilinishi uchun barcha talablarni to‘g‘ri bajaring...\n"
        "Formani bekor qilish uchun /cancel buyrug'ini bering...\n\n\n"
        "Smartphonening modelini kiriting:"),
    'memory': "SmartPhone xotirasini kiriting,\nMasalan: 64GB/4GB",
    'document': "Qurilmaning hujjatlari bormi?",
    'cost': "Qurilmaga qanday narx taklif qilasiz:",
    'phone': "Bog‘lanish uchun telefon raqam kiriting: ",
    'address': "Manzilni/shaharni kiriting",
    'photo': "Iltimos Telefoningizni bir dona suratini yuklang...",
    'box': "Qurilmaning qutisi bormi?",
    'holat': "Qurilmaning holati qanday?"
}


















@dp.message_handler(IsPrivate(),Text(equals="📱Smartphone"))
async def startMobilForm(message: types.Message, state: FSMContext):
    await message.answer(text="Vaqtinchalik bu bo'lim ishlamaydi")


@dp.message_handler(state=MainSmartphone.mdoel)
async def getPhoneModel(message: types.Message, state: FSMContext):
    model = message.text
    
    await message.answer(TEXT["memory"])
    await state.update_data(model=model)
    await MainSmartphone.totalMemory.set()
    try:
        await bot.delete_message(message.chat.id, message.message_id-1)
        await message.delete()
    except:
        pass


@dp.message_handler(state=MainSmartphone.totalMemory)
async def getPhoneMemory(message: types.Message, state: FSMContext):
    await message.answer(text=TEXT["document"], reply_markup=DEVICE_DOCS)
    memory = message.text
    await state.update_data(memory = memory)
    await MainSmartphone.documents.set()
    try:
        await bot.delete_message(message.chat.id, message.message_id-1)
        await message.delete()
    except:
        pass


@dp.message_handler(state=MainSmartphone.phoneState)
async def getDefaultBox(message: types.Message, state: FSMContext):
    
    await message.answer(TEXT["cost"])
    phone_state = message.text
    await state.update_data(phone_state=phone_state)
    await MainSmartphone.phoneCost.set()
    try:
        await bot.delete_message(message.chat.id, message.message_id-1)
        await message.delete()
    except:
        pass


@dp.message_handler(state=MainSmartphone.phoneCost)
async def getPhoneCost(message: types.Message, state: FSMContext):
    await message.answer(TEXT['phone'])
    cost = message.text
    await state.update_data(cost=cost)
    await MainSmartphone.phoneNumber.set()
    try:
        await bot.delete_message(message.chat.id, message.message_id-1)
        await message.delete()
    except:
        pass

@dp.message_handler(state=MainSmartphone.phoneNumber)
async def getPhoneNumber(message: types.Message, state: FSMContext):
    number = message.text
    await state.update_data(number=number)
    await message.answer(TEXT['address'])
    await MainSmartphone.address.set()

@dp.message_handler(state=MainSmartphone.address)
async def getAddress(message: types.Message, state: FSMContext):
    data = message.text
    await state.update_data(address=data)
    # await confirmation(message, state)
    await message.answer(TEXT['photo'])
    await MainSmartphone.getPhonePhoto.set()
    try:
        await bot.delete_message(message.chat.id, message.message_id-1)
        await message.delete()
    except:
        pass

@dp.message_handler(content_types=types.ContentType.PHOTO, state=MainSmartphone.getPhonePhoto)
async def getPhonePhoto(message: types.Message, state: FSMContext):
    photo = message.photo[-1]
    link = await upload_photo(photo = photo)
    await state.update_data(photo = link)
    await confirmation(message, state)


@dp.message_handler(state=MainSmartphone.UserConfirm)
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
    model = data['model']
    memory = data['memory']
    holati = data['phone_state']
    cost = data['cost']
    number = data['number']
    box = data['box']
    docs = data['docs']
    address = data['address']
    address = "#"+address.replace(" "," #")
    text = f"#Smartphone \n"
    text += f"📱 Model: {model}\n"
    text += f"💾 Xotirasi: {memory}\n"
    text += f"🛠 Holati: {holati}\n"
    text += f"💰 Narxi: {cost}\n"
    text += f"📦 Qurilma qutisi: {box}\n"
    text += f"🗂 Qurilmaning hujjatlari: {docs}\n"
    text += f"☎️ Telefon raqam: {number}\n"
    text += f"📍 Manzil: {address}"
    return text












@dp.callback_query_handler(state=MainSmartphone.documents)
async def getDocs(query: types.CallbackQuery, state: FSMContext):
    docs = query.data
    await state.update_data(docs = docs)
    await query.answer(text="Qabul qilindi...", cache_time=0)
    await bot.send_message(chat_id=query.message.chat.id, text=TEXT['box'], reply_markup=DEVICE_BOX)
    await MainSmartphone.defaultBox.set()
    try:
        await bot.delete_message(query.message.chat.id, query.message.message_id)
    except:
        pass

@dp.callback_query_handler(state=MainSmartphone.defaultBox)
async def getDefaultBox(query: types.CallbackQuery, state: FSMContext):
    box = query.data
    await state.update_data(box=box)
    await query.answer(text="Qabul qilindi...", cache_time=0)
    await bot.send_message(chat_id=query.message.chat.id, text=TEXT['holat'])
    await MainSmartphone.phoneState.set()
    try:
        await bot.delete_message(query.message.chat.id, query.message.message_id)
    except:
        pass           

async def confirmation(message: types.Message, state: FSMContext):
    await message.answer("Siz yuborgan ma'lumotlar to‘g‘ri ekanligiga ishonchingiz komilmi?")
    data = await state.get_data()
    photo = data['photo']
    text = await returnDatas(state)
    ##
    msg = await message.answer_photo(
        photo=photo,
        caption=text, 
        reply_markup = CONFIRM)
        ##
    await MainSmartphone.UserConfirm.set()
    msg_id = msg.message_id
    await state.update_data(msg_id=msg_id)













async def save_to_db(data: FSMContext, user_id: int):
    data = await data.get_data()
    model = data['model']
    memory = data['memory']
    holati = data['phone_state']
    cost = data['cost']
    number = data['number']
    box = data['box']
    docs = data['docs']
    address = data['address']
    photo = data['photo']

    db.add_smartphone(
        user_id=user_id,
        model=model,
        memory=memory,
        phone_state=holati,
        cost=cost,
        number=number,
        box=box,
        docs=docs,
        address=address,
        photo=photo
        )
