import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from datetime import datetime, timedelta

API_TOKEN = '8151839888:AAFSKa2K6Ns8wAG8wLhJY1JbUIFmz1ylkgk'

# إعدادات
CURRENCY_NAME = "كوين"
DAILY_REWARD = 5
REFERRAL_REWARD = 2

users_data = {}

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

main_kb = ReplyKeyboardMarkup(resize_keyboard=True)
main_kb.add(KeyboardButton("رصيدي"), KeyboardButton("مكافأة يومية"))
main_kb.add(KeyboardButton("رابط الإحالة"))

def get_user(user_id):
    if user_id not in users_data:
        users_data[user_id] = {"balance": 0, "last_claim": None, "referrals": []}
    return users_data[user_id]

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    user = get_user(message.from_user.id)
    await message.answer("أهلاً بك! استخدم الأزرار للبدء.", reply_markup=main_kb)

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
        await message.answer(f"أخذت {DAILY_REWARD} {CURRENCY_NAME}!")
    else:
        await message.answer("رجع باچر تاخذ مكافأتك!")

@dp.message_handler(lambda message: message.text == "رابط الإحالة")
async def referral_link(message: types.Message):
    user_id = message.from_user.id
    await message.answer(f"رابط إحالتك:
t.me/Queenn00_bot?start={user_id}")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
