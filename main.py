from threading import Thread
import asyncio

from userbot import app
from bot import start_bot


Thread(target=asyncio.run, args=(start_bot(),)).start()
app.run()