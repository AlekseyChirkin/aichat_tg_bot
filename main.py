import asyncio
from aiogram import types
from aiogram import Dispatcher
from aiogram import Bot
from dotenv import load_dotenv
import os

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
