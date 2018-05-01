# pylint: disable=C0111
import time
import random
import datetime
import telepot
from telepot.loop import MessageLoop
import aiy.audio
import aiy.voicehat
import my_locker as locker

def play_message(sender, command):
    msgTxt = command.replace("/msg", '', 1)
    aiy.audio.play_wave('/home/pi/misc/dollar.wav')
    aiy.audio.say(sender+" says: ")
    aiy.audio.say(msgTxt)

def handle(msg):
    sender_id = msg['chat']['id']
    sender_name = msg['chat']['first_name']
    command = msg['text']
    # content_type, chat_type, chat_id = telepot.glance(msg)
    # print(content_type, chat_type, chat_id)
    
    if "hi" in str(command).lower():
        bot.sendMessage(sender_id, "Hello there, my local time is:"+ str(datetime.datetime.now()))
    elif "/msg" in command:
        play_message(sender_name, command)

def start_bot():
    if locker.get_content("telegram","enabled") == "1":
        global bot
        bot = telepot.Bot(locker.get_content("telegram","key"))
        print(bot.getMe())
        MessageLoop(bot, handle).run_as_thread()
        print('Bot started listening ...')
        #while True:
        #    time.sleep(10)
    else:
        print("Telegram bot is disabled")

if __name__ == '__main__' :
    start_bot()
