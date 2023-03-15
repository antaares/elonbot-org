import sqlite3
from aiogram import executor

from loader import dp, db
import filters, handlers

async def on_startup(dispatcher):
    try:
        db.create_table_users()
        db.create_auto_ads()
        db.create_smartphone_ads()
        db.create_home_ads()
        db.create_house_ads()
        db.create_status_table()
        db.create_services_table()
    except sqlite3.IntegrityError as error:
        print(error)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
