import asyncio

from aiogram import Bot, Dispatcher
from aiogram import types

from db import get_statistics
from config import API_KEY

bot = Bot(API_KEY)
dp = Dispatcher(bot)


def get_main_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    button_1 = types.InlineKeyboardButton('Что я могу?', callback_data='what_i_can')
    button_2 = types.InlineKeyboardButton('Помогите', callback_data='help')
    button_3 = types.InlineKeyboardButton('Статистика', callback_data='statistics')
    keyboard.add(button_1)
    keyboard.add(button_2, button_3)
    return keyboard

def get_back_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    button_1 = types.InlineKeyboardButton('В главное меню', callback_data='back')
    keyboard.add(button_1)
    return keyboard


@dp.message_handler(commands='start')
async def start_handler(message: types.Message):
    if message.text == '/start':
        string = 'Привет! Я бот.'
        await message.delete()
        await message.answer(string, 'MARKDOWN', reply_markup=get_main_keyboard())


@dp.callback_query_handler()
async def messages_handler(call: types.CallbackQuery):
    try:
        if call.data == 'what_i_can':
            string = 'Пока ничего'
            await call.message.edit_text(string, 'MARKDOWN', reply_markup=get_back_keyboard())
        elif call.data == 'help':
            string = 'Если у Вас возникли какие-то вопросы, либо есть какие-то предложения, то вы можете написать в нашу тех поддержку: @mimbaw'
            await call.message.edit_text(string, 'MARKDOWN', reply_markup=get_back_keyboard())
        elif call.data == 'statistics':
            string = get_statistics()
            await call.message.edit_text(string, 'MARKDOWN', reply_markup=get_back_keyboard(), disable_web_page_preview=True)
        elif call.data == 'back':
            string = 'Привет! Я бот.'
            await call.message.edit_text(string, 'MARKDOWN', reply_markup=get_main_keyboard())
    except Exception as e:
        print(e)

async def start_bot():
    await dp.start_polling(bot)