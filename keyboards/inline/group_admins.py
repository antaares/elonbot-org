from aiogram.types import InlineKeyboardMarkup,InlineKeyboardButton




async def info_admins(name: str, admin_id: int, hint: bool) -> InlineKeyboardMarkup:
    info = "Tasdiqlangan!"
    if not hint:
        info = "Qaytarilgan!"
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=info, callback_data="admininfo|{}|{}".format(name, admin_id))
                ]
    ]
    )

from loader import dp, bot

async def comment_client(user_id):
    username_ = await bot.get_me()
    username = username_.username
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Izoh qoldirish", url=f"https://t.me/{username}?start=comment_{user_id}")
            ]
        ]
    )