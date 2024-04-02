
from aiogram import types
from aiogram import Dispatcher
from aiogram import Bot
from dotenv import load_dotenv
import os
import logging
import asyncio

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message()
async def echo_message(message: types.message):
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
    if message.text:
        await message.reply(text=message.text)
    elif message.sticker:
        await message.reply_sticker(sticker=message.sticker.file_id)

    else:
        await message.reply(text="Something new 😀")


async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
