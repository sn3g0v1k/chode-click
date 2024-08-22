import asyncio
import logging
import sys
import sqlite3 as sq
from os import getenv
import os
from aiogram.client.session.aiohttp import AiohttpSession
from db_logic import new_user, boosters
from aiogram import Bot, Dispatcher, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, FSInputFile, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ContentType, PreCheckoutQuery, WebAppInfo
from parse import profile_photo

# Bot token can be obtained via https://t.me/BotFather
TOKEN = "7294965050:AAG9JlzFOCWodh1-6hOR42JoSATcSSWqns4"
# All handlers should be attached to the Router (or Dispatcher)

dp = Dispatcher()

conn = sq.connect("database.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS users (user_id BIGINT, score INTEGER, name TEXT, booster INTEGER, photo TEXT)")
conn.commit()

cursor.execute("CREATE TABLE IF NOT EXISTS costs (cost INTEGER, name TEXT, booster INTEGER)")
conn.commit()

cursor.execute("CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY AUTOINCREMENT, text TEXT, reward INTEGER, url TEXT)")
conn.commit()

cursor.execute("CREATE TABLE IF NOT EXISTS user_task (user_id BIGINT, undone_tasks_ids TEXT)")
conn.commit()

boosters(conn, cursor)


def keyboard(id: str):
    button = [InlineKeyboardButton(text="Go here", web_app=WebAppInfo(url=f"https://v0hnxss7-5000.euw.devtunnels.ms/clicking/{id}"))]
    return InlineKeyboardMarkup(inline_keyboard=[button])

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    id = str(message.from_user.id)
    photo = await message.bot.get_user_profile_photos(message.from_user.id, 0, 1)
    try:
        photo_id = photo.photos[0][0].file_id
    except IndexError:
        new_user(conn, cursor, name=message.from_user.full_name, id=id, url="https://ach-raion.gosuslugi.ru/netcat_files/9/260/MUZhChINA_2.jpg")
        await message.answer(f"Hello, {message.from_user.full_name}", reply_markup=keyboard(id))
        return
    url = profile_photo(photo_id, TOKEN)
    new_user(conn, cursor, name=message.from_user.full_name, id=id, url=url)
    await message.answer(f"Hello, {message.from_user.full_name}", reply_markup=keyboard(id))



@dp.message(Message)
async def echo_handler(message: Message):
    try:
        await message.answer(message.text)
    except:
        await message.answer("Good try")




async def main() -> None:   
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(token=TOKEN)

    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
