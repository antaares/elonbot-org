from aiogram.dispatcher.filters import Text
from aiogram import types
from aiogram.dispatcher.storage import FSMContext

from keyboards.default.cancel_keys import CANCEL


from filters import IsPrivate



from data.config import ADMIN_GROUP
from loader import dp, bot, db 

from keyboards.default.MyAdsKeyboard import MyAdsKeyboard
from keyboards.default.all_ads_keyboard import all_ads_keyboard

from keyboards.inline.my_ads_keys import ad_methods

from states.menuStates import MyAdsMenu






TEXT = {
    'start': "Assalomu alaykum, Mening e'lonlarim bo‘limiga xush kelibsiz!!!\n"\
              "bajarmoqchi bo'lgan amalni tanlang:",
    'myads': 'Sizning e\'lonlaringiz:',
}







@dp.message_handler(IsPrivate(),Text(equals="📝E'lonlarim"))
async def startMobilForm(message: types.Message, state: FSMContext):
    await message.answer(text=TEXT['start'], reply_markup= MyAdsKeyboard)
    await MyAdsMenu.myAdsMenu.set()








@dp.message_handler(IsPrivate(),Text(equals="📝Mening e'lonlarim"), state=MyAdsMenu.myAdsMenu)
async def startMyAdsForm(message: types.Message, state: FSMContext):
    ads = db.get_my_ads(message.from_user.id)
    if ads:
        ads = [f"#{i[0]}" for i in ads]
        await message.answer(text=TEXT['myads'], reply_markup= await all_ads_keyboard(ads))
        await MyAdsMenu.zed.set()
    else:
        await message.answer("Sizda hech qanday e'lon yo'q!!!", reply_markup=CANCEL)



@dp.message_handler(IsPrivate(), state=MyAdsMenu.zed)
async def startMyAdsForm(message: types.Message, state: FSMContext):
    ad_id = int(message.text[1::])
    ad = db.find_ad(ads_id=ad_id, user_id=message.from_user.id)
    ad, ad_type = ad[0], ad[1]
    if ad:
        await send_my_ads(message, ad_id, ad_type)
        await state.finish()





async def send_my_ads(message: types.Message, ad_id: int, ad_type: int,):
    ad = db.find_ad(ads_id=ad_id, user_id=message.from_user.id)
    ad, ad_type = ad[0], ad[1]
    if ad:
        if ad_type == 1:
            text = await return_auto_text(ad, ad_id)
            photo = ad[12]
            await message.answer_photo(photo=photo, caption=text)
        elif ad_type == 2:
            text = await return_home_text(ad, ad_id)
            photo = ad[10]
            await message.answer_photo(photo=photo, caption=text)
        elif ad_type == 3:
            text = await return_house_text(ad, ad_id)
            photo = ad[9]
            await message.answer_photo(photo=photo, caption=text)
        elif ad_type == 4:
            text = await return_service_text(ad, ad_id)
            photo = ad[6]
            await message.answer_photo(photo=photo, caption=text)
        await message.answer(f"Bu #id{ad_id} raqamli e'loningiz. Siz bu e'lonni vaqtinchalik deaktivatsiya qilishingiz mumkin, "\
                            f"bu holatda adminlar kanaldagi e'lonni o'chirib turishadi. Keyinchalik qayta aktivatsiya qilsangiz, adminlar "\
                            f"shu e'lonni yana kanalga tashlaydilar. Agar siz \"o'chirish\" tugmasini bossangiz, ushbu e'lon "\
                            f"tizim bazasidan o'chib ketadi!""", reply_markup=await ad_methods(ad_id))
        await MyAdsMenu.red.set()
        







@dp.callback_query_handler(Text(startswith="my") ,state="*")
async def all_query_handler(query: types.CallbackQuery, state: FSMContext):
    data = query.data.split('|')
    # print("data private: ", data)
    if data[0] == 'mydelete':
        db.delete_ad(user_id=query.from_user.id,ads_id=int(data[1]))
        await query.answer("E'lon o'chirildi!", show_alert=True)
        # wwwwwwwwww
        await bot.send_message(
            chat_id=ADMIN_GROUP, 
            text=f"{query.from_user.id} foydalanuvchisi #id{data[1]} raqamli e'lonni o'chirishni so'radi, e'lon tizimdan ham o'chirildi!"
            )
        # wwwwwwwwww

        ads = db.get_my_ads(query.from_user.id)
        if ads:
            ads = [f"#{i[0]}" for i in ads]
            await query.message.answer(text=TEXT['myads'], reply_markup= await all_ads_keyboard(ads))
            await MyAdsMenu.zed.set()
        else:
            await query.message.answer("Sizda hech qanday e'lon yo'q!!!", reply_markup=CANCEL)
    elif data[0] == 'mydeactivate':
        ad_id = int(data[1])
        db.update_status(ad_id, 'deactive')
        await query.answer("E'lon deaktivatsiya qilindi!", show_alert=True)
        # adminlarga yuborish
        await bot.send_message(
            chat_id=ADMIN_GROUP, 
            text=f"{query.from_user.id} foydalanuvchisi #id{data[1]} raqamli e'lonni deaktivatsiya qilishni so'radi, e'lon tizimdan deaktivatsiya qilindi!"
            )
        # wwwwwwwwww


        # wwwwwwwwww
    elif data[0] == 'myactivate':
        ad_id = int(data[1])
        db.update_status(ad_id, 'active')
        await query.answer("E'lon aktivatsiya qilindi!", show_alert=True)
        # adminlarga yuborish
        await bot.send_message(
            chat_id=ADMIN_GROUP, 
            text=f"{query.from_user.id} foydalanuvchisi #id{data[1]} raqamli e'lonni aktivatsiya qilishni so'radi, e'lon tizimda activatsiya qilindi!"
            )
        # wwwwwwwwww


        # wwwwwwwwww
    else:
        await query.message.delete()
        ads = db.get_my_ads(query.from_user.id)
        if ads:
            ads = [f"#{i[0]}" for i in ads]
            await query.message.answer(text=TEXT['myads'], reply_markup= await all_ads_keyboard(ads))
            await MyAdsMenu.zed.set()
        else:
            await query.message.answer("Sizda hech qanday e'lon yo'q!!!", reply_markup=CANCEL)



















async def return_auto_text(ad: tuple, unique_id: int):
    model = ad[2]
    position = ad[4]
    year = ad[3]
    color = ad[9]
    carstate = ad[5]
    distance = ad[8]
    box = ad[7]
    cost = ad[6]
    number = ad[10]
    address = ad[11]
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
    text += f"📍 Manzil: {address}"
    return text



async def return_home_text(ad: tuple, unique_id: int):
    floors = ad[2]
    current = ad[3]
    rooms = ad[4]
    things = ad[7]
    homestate = ad[5]
    cost = ad[6]
    number = ad[8]
    address = ad[9]
    text = f"🏬 #{address} #uy\t#id{unique_id}\n"\
    f"🏗 Jami qavatlar: {floors}\n"\
    f"🚡 Nechanchi qavat: {current}\n"\
    f"⛩ Xonalar soni: {rooms}\n"\
    f"🎡 Uydagi jihozlar: {things}\n"\
    f"🏛 Uyning holati: {homestate}\n"\
    f"🏦 Taklif qilingan narx: {cost}\n"\
    f"☎️ Boglanish uchun raqam: {number}\n"\
    f"📍 Uyning manzili: {address}\n"
    return text






async def return_house_text(ad: tuple, unique_id: int):
    area = ad[2]
    rooms = ad[3]
    conven = ad[6]
    homestate = ad[4]
    cost = ad[5]
    number = ad[7]
    address = ad[8]
    text = f"#{address} #uy\t#id{unique_id}\n"\
        f"🏘 Uyning umumiy maydoni: {area}\n"\
        f"🏗 Yashash xonalar soni: {rooms}\n"\
        f"🏖 Uydagi qulayliklar: {conven}\n"\
        f"🏠 Uyning holati: {homestate}\n"\
        f"🏦 Uyga taklif qilingan narx: {cost}\n"\
        f"☎️ Telefon raqam: {number}\n"\
        f"📍 Uyning manzili: {address}"
    return text


async def return_service_text(ad: tuple, unique_id: int):
    service_type = ad[2]
    service_description = ad[3]
    regions = ad[4]
    number = ad[5]
    text = f"#Xizmatlar\t#id{unique_id}\n"\
        f"🛠 Xizmat turi: {service_type}\n"\
        f"📝 Xizmat haqida: {service_description}\n"\
        f"📍 Xizmat faoliyati hududlari: {regions}\n"\
        f"☎️Xizmatlarga bog'lanish uchun raqam: {number}\n\n"\
        f"E'lonlaringizni @elonlartaxtasibot orqali yuboring!"
    return text