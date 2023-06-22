from pyrogram import Client, filters
from pyrogram.types import Message
from aiogram import Bot

from config import api_id, api_hash, API_KEY
from db import add_new_spam

app = Client("my_account", api_id, api_hash)
bot = Bot(API_KEY)


@app.on_message(filters.text)
async def hello(client, message: Message):
        if not message.from_user.is_bot:
            count = await app.get_chat_history_count(message.chat.id)
            if count:
                if message.text:
                    if 'http' in message.text:
                        string = f'*Новое сообщние от неизвестного пользователя:*\n\n{message.text}\n\n*Внимание! Скорее всего, это сообщение является спамом!*'
                        await bot.send_message(app.me.id, string, 'MARKDOWN', disable_web_page_preview=True)
                        await app.block_user(message.chat.id)
                        add_new_spam(message.chat.id, message.from_user.first_name, message.text)
                    elif message.entities:
                        if any(i.url for i in message.entities):
                            string = message.text
                            data = []
                            for i in message.entities:
                                if i.url:
                                    data.append((message.text[i.offset: i.offset+i.length], i.url))
                            for i in data:
                                string = string.replace(i[0], f'[{i[0]}]({i[1]})')
                            string = f'*Новое сообщние от неизвестного пользователя:*\n\n{string}\n\n*Внимание! Скорее всего, это сообщение является спамом!*'
                            await bot.send_message(app.me.id, string, 'MARKDOWN', disable_web_page_preview=True)
                            await app.block_user(message.chat.id)
                        add_new_spam(message.chat.id, message.from_user.first_name, message.text)