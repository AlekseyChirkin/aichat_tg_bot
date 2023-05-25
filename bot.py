import logging
import time
from pathlib import Path
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ContentType, Message, File
import stt
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot)
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    filename="bot.log",
)


# Хэндлер на команду /start
@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    user_id = message.from_user.id
    user_full_name = message.from_user.full_name
    logging.info(f'{user_id=} {user_full_name=} {time.asctime()}')
    await message.reply(f"Hi, {user_full_name}, my captain!\nWaiting for orders...")


async def handle_file(file: File, file_name: str, path: str):
    Path(f"{path}").mkdir(parents=True, exist_ok=True)

    await bot.download_file(file_path=file.file_path, destination=f"{path}/{file_name}")


@dp.message_handler(content_types=[ContentType.VOICE])
async def voice_message_handler(message: Message):
    print('Received audio message!')
    voice = await message.voice.get_file()

    path_to_save_voices = "files/voices"
    voice_file_name = voice.file_id + '.ogg'
    path_to_saved_voice_file = str(path_to_save_voices) + '/' + voice_file_name

    await handle_file(file=voice, file_name=voice_file_name, path=path_to_save_voices)

    logging.info(f'File {voice_file_name} saved to {path_to_saved_voice_file} at {time.asctime()}')

    stt_obj = stt.STT()
    await message.reply(stt_obj.audio_to_text(path_to_saved_voice_file))


if __name__ == "__main__":
    try:
        executor.start_polling(dp, skip_updates=True)
    except (KeyboardInterrupt, SystemExit):
        print('Good bye!')
        pass
