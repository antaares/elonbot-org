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



async def comment_client(user_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Izoh qoldirish", url="https://t.me/elonlartaxtasibot?start=comment_{}".format(user_id))
            ]
        ]
    )