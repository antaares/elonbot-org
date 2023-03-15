from aiogram import types
from aiogram.dispatcher import FSMContext
from keyboards.default.mainMenu import MAIN_MENU

from loader import dp
from filters import IsPrivate

@dp.message_handler(IsPrivate(), commands=['cancel'], state="*")
async def CancelDef(message: types.Message, state: FSMContext):
    try:
        await state.finish()
    except:
        pass
    await message.answer("Siz bosh menudasiz!!!", reply_markup=MAIN_MENU)