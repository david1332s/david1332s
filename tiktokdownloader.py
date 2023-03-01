from TikTokApi import TikTokApi
import random

import telebot
from telebot.async_telebot import AsyncTeleBot
from telebot import types
import asyncio
import re
import nest_asyncio
nest_asyncio.apply()

#remove water NO
import subprocess

async def remove_watermark(file_directory):
    command = ['ffmpeg', '-y', '-i', file_directory, '-filter:v', 'crop=in_w:in_h-185', '-c:a', 'copy', '2.mp4']
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    process.communicate()

#params
fp = 'verify_lene87k0_nPuvOmfK_w5IP_4Gsa_8o7i_JiBdb4gEGY5Z'
did = str(random.randint(10000, 999999999))
api = TikTokApi(custom_verify_fp=fp, custom_device_id=did)

#bot
TOKEN = '5953810175:AAHAxZRZyogxtom_l9AcSLOC0_8B3ggcVfg'
bot = AsyncTeleBot(TOKEN,'html')

#filling
@bot.message_handler(content_types='text',func=lambda message: message.chat.type == 'private' or message.chat.id == -1001653038678)
async def new_message(message):
    if re.search(r'^https://.+tiktok.+',message.text):
        msg = (await bot.send_message(message.chat.id, "<b>Идёт обработка, ожидайте!</b>", reply_to_message_id=message.message_id))
        try:
            video = api.video(url=message.text)
            video_bytes = video.bytes()
            with open('1.mp4', 'wb') as f:
                f.write(video_bytes)
            await remove_watermark('1.mp4')
            info = video.info()
            await bot.delete_message(message.chat.id,msg.message_id)
            await bot.send_video(message.chat.id, open('2.mp4', 'rb'),caption=f"<b>{info['author']['uniqueId']}</b>: {info['contents'][0]['desc']}",reply_to_message_id=message.message_id)
        except Exception as e:
            print(e.args[0])
            await bot.send_message(message.chat.id, 'Ошибка')

#RUN
while True:
    try:
        asyncio.run(bot.polling(non_stop=True))
    except:
        pass