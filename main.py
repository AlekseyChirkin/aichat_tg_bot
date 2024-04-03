import os
import logging
import asyncio

from dotenv import load_dotenv
from aiogram import Bot
from aiogram import Dispatcher
from aiogram import types
from aiogram.filters import CommandStart, Command

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def start_message(message: types.Message):
    await message.answer(text=f"Hello, {message.from_user.full_name}")


@dp.message(Command("help"))
async def handle_help(message: types.Message):
    text = "I'm an echo bot\nSend me any message!"
    await message.answer(text=text)


@dp.message()
async def echo_message(message: types.Message):
    await bot.send_message(
        chat_id=message.chat.id,
        text="Start processing..."
    )
    await bot.send_message(
        chat_id=message.chat.id,
        text="Detected message...",
        reply_to_message_id=message.message_id,
    )
    await message.answer(
        text="Wait a second, please!"
    )
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.reply(text="Something new!")


async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
