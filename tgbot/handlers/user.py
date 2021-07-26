import logging
import os

from aiogram import Dispatcher
from aiogram import types
from aiogram.types import InputFile

from tgbot.config import load_config
from tgbot.services.funcs import find_url, youtube_download

config = load_config()

async def user_start(message: types.Message):
    await message.reply("Salom, YouTube'dan menga hohlagan videoga ssilka bering ...")


async def user_text(message: types.Message):
    text = message.text
    is_url = await find_url(text)
    video_title = ''
    if is_url:
        link = is_url[0]
        video = await youtube_download(link)
        logging.info(video)
        keyword = video
        for fname in os.listdir(config.tg_bot.yt_path):
            if keyword in fname:
                video_title = fname
    if video_title:
        logging.info(video_title)
        await message.bot.send_video(message.chat.id, InputFile(f'{config.tg_bot.yt_path}{video_title}'),
                                     caption=f'@{config.tg_bot.bot_username}')


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"], state="*")
    dp.register_message_handler(user_text, content_types=types.ContentTypes.TEXT, state="*")
