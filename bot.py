import logging
import time
from pathlib import Path
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ContentType, Message, File
import stt
from dotenv import load_dotenv
import os
from art import tprint
import g4f_responce

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot)
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    filename="bot.log",
)

stt_obj = stt.STT()
logging.info(f'Object {stt_obj=} created successfull!')
tprint("Working...")


# Хэндлер на команду /start
@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    user_id = message.from_user.id
    user_full_name = message.from_user.full_name
    logging.info(f'{user_id=} {user_full_name=} {time.asctime()}')
    await message.reply(f"Hi, {user_full_name}, my captain!\nWaiting for orders...")


# На текст пользователя отвечает сразу нейросетью
@dp.message_handler(content_types="text")
async def echo_from_g4f(message: types.Message):
    await message.answer(g4f_responce.get_responce(message.text))


### Здесь должена быть обработка сообщения, если к нему приложено видео с ютуб ###
# @dp.message_handler(content_types=[ContentType.TEXT])
# async def voice_message_handler(message: Message):
#     text_from_user = message.text
#     if 'youtube.com/watch?v=' in text_from_user:
#         youtube_id = text_from_user[:-11]
#         await message.reply(text_from_youtube.transcript_from_yt_video(youtube_id))

# Обработка голосового сообщения
@dp.message_handler(content_types=[ContentType.VOICE])
async def voice_message_handler(message: Message):
    voice = await message.voice.get_file()
    path_voices_tmp = "files/voices"
    voice_file_name = voice.file_id + '.ogg'
    path_to_voice = str(path_voices_tmp) + '/' + voice_file_name

    # Save audio message to file
    await handle_file(file=voice, file_name=voice_file_name, path=path_voices_tmp)
    logging.info(f"File {voice_file_name} saved to {path_to_voice} at {time.asctime()}")
    text_from_message = stt_obj.audio_to_text(path_to_voice)
    logging.info(f"Распознанный текст запроса: \n{text_from_message}\n")
    # Получаем ответ нейросети
    # response = g4f_responce.get_responce(text_from_message)
    # await message.reply(response)
    await message.reply(text_from_message)

if __name__ == "__main__":
    # polling bot
    try:
        executor.start_polling(dp, skip_updates=True)
    except (KeyboardInterrupt, SystemExit):
        tprint('Good bye!')
        pass
