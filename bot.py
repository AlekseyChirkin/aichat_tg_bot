import logging
import time
from pathlib import Path
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ContentType, Message, File
from config import TOKEN
import stt

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
    print('Recieved audio message!')
    voice = await message.voice.get_file()
    path = "files/voices"

    await handle_file(file=voice, file_name=f"{voice.file_id}.ogg", path=path)
    print('File successfully downloaded!')
    file_path = str(path) + '/' + str(voice.file_id) + '.ogg'
    logging.info(f'File {voice.file_id}.ogg saved to {file_path} at {time.asctime()}')

    await message.reply(stt.audio_to_text(file_path))
    print('Text sended to user!')

if __name__ == "__main__":
    try:
        executor.start_polling(dp, skip_updates=True)
    except (KeyboardInterrupt, SystemExit):
        print('Good bye!')
        pass
