
# import aiogram classes
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher import FSMContext

# import filters
from filters.privateChat import IsPrivate
from filters.isMember import IsMember

#  import buttons
from keyboards.default.mainMenu import MAIN_MENU
from keyboards.inline.startButtons import SUBSCRIBE

#  immport global variables of bot
from loader import dp, db, bot
from states.AdminStates import Comment


# reply on /start command, if user not joined channel
@dp.message_handler(IsPrivate(), IsMember(), CommandStart(), state="*")
async def bot_start(message: types.Message, state: FSMContext):
    args = message.get_args()
    if args.split('_')[0]=="comment":
        await message.answer("Arizachiga yuborish uchun izoh yozing!")
        await Comment.GetComment.set()
        return await state.update_data(user_id=args.split('_')[1])
    await message.answer(f"Salom, {message.from_user.full_name}!"\
                         "Siz bizning bot yyordamida @BorBorRasmiy kanalimizga turli xildagi e'lonlar joylashtirishingiz mumkin.")
    await message.answer("Iltimos, botdan to‘liq foydalanish uchun kanalimizga a'zo bo‘ling", reply_markup=SUBSCRIBE)
    try:
        db.add_user(
            id=message.from_user.id,
            name=message.from_user.full_name,
            language=message.from_user.language_code
            )
    except Exception as error:
       print(error)


# reply on /start command.
@dp.message_handler(IsPrivate(), CommandStart(), state="*")
async def bot_start(message: types.Message, state: FSMContext):
    args = message.get_args()
    if args.split('_')[0]=="comment":
        await message.answer("Arizachiga yuborish uchun izoh yozing!")
        await Comment.GetComment.set()
        return await state.update_data(user_id=args.split('_')[1])

    text = "Kerakli bo'limni tanlang!!!"
    await message.answer(f"Salom, {message.from_user.full_name}!")
    await message.answer(text=text, reply_markup=MAIN_MENU)
    try:
        db.add_user(
            id=message.from_user.id,
            name=message.from_user.full_name,
            language=message.from_user.language_code
            )
    except Exception as error:
       print(error)





@dp.message_handler(state=Comment.GetComment)
async def get_comment(message: types.Message, state: FSMContext):
    data = await state.get_data()
    user_id = data.get("user_id")
    await bot.send_message(chat_id=int(user_id), text=message.text)
    await message.answer("Izoh yuborildi!")
    await state.finish()