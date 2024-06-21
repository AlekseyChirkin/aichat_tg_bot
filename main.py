import logging
import asyncio
from aiogram import Bot
from aiogram import Dispatcher
from aiogram import types
from aiogram.filters import CommandStart, Command
import config
import local_llama3_model


bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def start_message(message: types.Message):
    await message.answer(text=f"Приветствую, {message.from_user.full_name}, бот запущен.\nНапишите мне сообщение и я отвечу.")


@dp.message(Command("help"))
async def handle_help(message: types.Message):
    text = "Это MVP чат бот, использующий локальную версию llama3:8b\nНапишите мне сообщение"
    await message.answer(text=text)


@dp.message()
async def echo_message(message: types.Message):
    await bot.send_message(chat_id=message.chat.id,
                           text=f"Сообщение получено, {
                               message.from_user.full_name}, идет обработка",
                           reply_to_message_id=message.message_id)

    # await bot.send_message(
    #     chat_id=message.chat.id,
    #     text="Обрабатываю запрос..."
    # )

    await message.answer(
        text=local_llama3_model.get_response_from_ai(message.text)
    )

    # try:
    #     await message.send_copy(chat_id=message.chat.id)
    # except TypeError:
    #     await message.reply(text="Что-то новенькое, не могу ответить")


async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
