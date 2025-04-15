
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from datetime import datetime, timedelta
import asyncio

API_TOKEN = '8151839888:AAFSKa2K6Ns8wAG8wLhJY1JbUIFmz1ylkgk'

CURRENCY_NAME = "كوين"
DAILY_REWARD = 5
users_data = {}

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

main_kb = ReplyKeyboardMarkup(resize_keyboard=True)
main_kb.add(KeyboardButton("رصيدي"), KeyboardButton("مكافأة يومية"))
main_kb.add(KeyboardButton("رابط الإحالة"))

def get_user(user_id):
    if user_id not in users_data:
        users_data[user_id] = {"balance": 0, "last_claim": None}
    return users_data[user_id]

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    get_user(message.from_user.id)
    await message.answer("أهلاً بك في بوت الربح من كوين!", reply_markup=main_kb)

@dp.message_handler(lambda message: message.text == "رصيدي")
async def balance(message: types.Message):
    user = get_user(message.from_user.id)
    await message.answer(f"رصيدك: {user['balance']} {CURRENCY_NAME}")

@dp.message_handler(lambda message: message.text == "مكافأة يومية")
async def daily_reward(message: types.Message):
    user = get_user(message.from_user.id)
    now = datetime.utcnow()
    if not user['last_claim'] or (now - user['last_claim']) > timedelta(hours=24):
        user['balance'] += DAILY_REWARD
        user['last_claim'] = now
        await message.answer(f"أخذت {DAILY_REWARD} {CURRENCY_NAME} اليوم!")
    else:
        await message.answer("رجع باچر تاخذ مكافأتك!")

@dp.message_handler(lambda message: message.text == "رابط الإحالة")
async def referral_link(message: types.Message):
    user_id = message.from_user.id
    await message.answer(f"رابط إحالتك:
t.me/YOUR_BOT_USERNAME?start={user_id}")

if __name__ == '__main__':
    asyncio.run(dp.start_polling())
