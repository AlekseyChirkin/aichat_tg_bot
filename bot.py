import logging
import time
from pathlib import Path
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ContentType, Message, File
import stt
from dotenv import load_dotenv
import os
from art import tprint
import ai_llama2, g_translate

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot)
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    filename="bot.log",
    encoding='utf-8'
)

stt_obj = stt.STT()
logging.info(f'Object {stt_obj=} created successfull!')
tprint("ON AIR")

async def handle_file(file: File, file_name: str, path: str):
    Path(f"{path}").mkdir(parents=True, exist_ok=True)

    await bot.download_file(file_path=file.file_path, destination=f"{path}/{file_name}")

# Хэндлер на команду /start
@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    user_id = message.from_user.id
    user_full_name = message.from_user.full_name
    logging.info(f'{user_id=} {user_full_name=} {time.asctime()}')
    await message.reply(f"Hi, {user_full_name}, my captain!\nWaiting for orders...")


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
    # Получаем ответ нейросети
    await message.reply(ai_response(text_from_message))


# Отвечаем на текс пользователя
@dp.message_handler(content_types="text")
async def text_reply(message: types.Message):
    await message.answer(ai_response(message.text))

# Ответ нейросети здесь
def ai_response(request_str: str):
    request_in_eng = g_translate.translate_rus_to_eng(request_str)
    logging.info(f"Request to AI: \n{request_in_eng}\n")   
    answer_from_ai = ai_llama2.get_answer(request_in_eng)
    logging.info(f"Answer from AI: \n{answer_from_ai}\n")   
    answer_from_ai = g_translate.translate_eng_to_rus(answer_from_ai)
    return answer_from_ai


### Здесь должена быть обработка сообщения, если к нему приложено видео с ютуб ###
# @dp.message_handler(content_types=[ContentType.TEXT])
# async def voice_message_handler(message: Message):
#     text_from_user = message.text
#     if 'youtube.com/watch?v=' in text_from_user:
#         youtube_id = text_from_user[:-11]
#         await message.reply(text_from_youtube.transcript_from_yt_video(youtube_id))


if __name__ == "__main__":
    # polling bot
    try:
        executor.start_polling(dp, skip_updates=True)
    except (KeyboardInterrupt, SystemExit):
        tprint('Good bye!')
        pass
