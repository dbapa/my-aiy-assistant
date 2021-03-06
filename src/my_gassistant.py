#!/usr/bin/env python3

import logging
import subprocess
import sys

import aiy.assistant.auth_helpers
import aiy.audio
import aiy.voicehat
from google.assistant.library import Assistant
from google.assistant.library.event import EventType

import RPi.GPIO as gpio
import time

import my_actions
import bot
# All the hotwords for custom actions listed below. detail handling of custom actions
# is implemented in my_actions module. Only action handler wrappers to be added in-line
PLAYSONG_HOTWORD = 'play song'
STOPSONG_HOTWORD = 'stop playing'
ROOMTEMP_HOTWORD = 'current room temperature'
PLAYNEWS_HOTWORD1 = 'play news from'
PLAYNEWS_HOTWORD2 = 'play top news from'
PLAYNEWSFEEDS_HOTWORD1 = 'news feeds'
PLAYNEWSFEEDS_HOTWORD2 = 'news sources'
PLAYNEWSHEADLINES_HOTWORDS = ['news','headlines']
START_CRYPTO_FEED = "start bitcoin feed"
STOP_CRYPTO_FEED = "stop bitcoin feed"
BEDROOM_LIGHT = "bedroom light"
LIVINGROOM_LIGHT = "living room light"
POWER_OFF = ['shutdown','power off']

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
)

# Custom action handler wrapper to start playing youtube songs using mpsyt and vlc player
def play_music(text,assistant,event):
    songName = text.replace(PLAYSONG_HOTWORD, '', 1)
    aiy.audio.say('Searching the song %s' % songName)
    my_actions.play_song(songName)

# this method does not work as the box doesnt get into listening mode while playing song
def stop_song():
    my_actions.stop_playing()


def play_news_feeds():
    src = my_actions.get_news_feeds()
    aiy.audio.say(str('I have new feeds from the following sources; %s ' % src))

def play_headlines():
    newsD = my_actions.get_news('The Washington Post')
    for key, val in newsD.items() :
        aiy.audio.say(key)
        aiy.audio.say('.')


def play_news(text):
    feedName1 = text.replace(PLAYNEWS_HOTWORD1, '', 1)
    newsD = my_actions.get_news(feedName1)
    for key, val in newsD.items() :
        aiy.audio.say(key)
        aiy.audio.say('.')
        aiy.audio.say(val)
        aiy.audio.say('..')

def power_off_pi():
    aiy.audio.say('Good bye!')
    subprocess.call('sudo shutdown now', shell=True)

def reboot_pi():
    aiy.audio.say('See you in a bit!')
    subprocess.call('sudo reboot', shell=True)

def say_ip():
    ip_address = subprocess.check_output("hostname -I | cut -d' ' -f1", shell=True)
    aiy.audio.say('My IP address is %s' % ip_address.decode('utf-8'))

def room_temp():
    temp = my_actions.get_room_temp()
    if 'na' in str(temp['temp']):
        aiy.audio.say('Am sorry, the temperature and humidity data is not currently available')
    else :
        strToSay = 'Current temperature is ' + str(temp['temp']) + 'degree centigrade'
        aiy.audio.say(strToSay)
        strToSay = 'The humidity in the room is ' + str(temp['humidity'])+ ' percent'
        aiy.audio.say(strToSay)

# This is the main event handler method from the google assistant source
def process_event(assistant, event):
    status_ui = aiy.voicehat.get_status_ui()
    print("in the process event:",event)
    if event.type == EventType.ON_START_FINISHED:
        status_ui.status('ready')
        if sys.stdout.isatty():
            print('Say "OK, Google" then speak, or press Ctrl+C to quit...')

    elif event.type == EventType.ON_CONVERSATION_TURN_STARTED:
        status_ui.status('listening')

    elif event.type == EventType.ON_RECOGNIZING_SPEECH_FINISHED and event.args:
        print('You said:', event.args['text'])
        text = event.args['text'].lower()
        if checkAnyHotwords(text,POWER_OFF):
            assistant.stop_conversation()
            power_off_pi()
        elif text == 'reboot':
            assistant.stop_conversation()
            reboot_pi()
        elif text == 'ip address':
            assistant.stop_conversation()
            say_ip()
        elif PLAYSONG_HOTWORD in text:
            assistant.stop_conversation()
            #print('text:',text)
            play_music(text,assistant,event)
        elif ROOMTEMP_HOTWORD in text:
            assistant.stop_conversation()
            room_temp()
        elif text == STOPSONG_HOTWORD:
            assistant.stop_conversation()
            stop_song()
        elif checkHotwords(text, PLAYNEWSHEADLINES_HOTWORDS):
            assistant.stop_conversation()
            play_headlines()
        elif PLAYNEWS_HOTWORD1 in text or PLAYNEWS_HOTWORD2 in text:
            assistant.stop_conversation()
            play_news(text)
        elif PLAYNEWSFEEDS_HOTWORD1 in text or PLAYNEWSFEEDS_HOTWORD2 in text:
            assistant.stop_conversation()
            play_news_feeds()
        elif START_CRYPTO_FEED in text:
            assistant.stop_conversation()
            my_actions.start_crypto_feeder()
        elif STOP_CRYPTO_FEED in text:
            assistant.stop_conversation()
            my_actions.stop_crypto_feeder()
        elif BEDROOM_LIGHT in text:
            assistant.stop_conversation()
            my_actions.bedroom_lights(text)
        elif LIVINGROOM_LIGHT in text:
            assistant.stop_conversation()
            my_actions.livingroom_lights(text)


    elif event.type == EventType.ON_END_OF_UTTERANCE:
        status_ui.status('thinking')

    elif event.type == EventType.ON_CONVERSATION_TURN_FINISHED:
        status_ui.status('ready')

    elif event.type == EventType.ON_ASSISTANT_ERROR and event.args and event.args['is_fatal']:
        sys.exit(1)

def main():
    credentials = aiy.assistant.auth_helpers.get_assistant_credentials()
    aiy.audio.say('Ok google will be activated in approximately one minute')
    bot.start_bot()
    # my_actions.initialize() # this is used to initialized HAT relay board PINS
    with Assistant(credentials) as assistant:
        for event in assistant.start():
            process_event(assistant, event)

# will return true if the text contains all the hotwords from the list HOTWORDS
def checkHotwords(text, HOTWORDS):
    flag = False
    for i in range(len(HOTWORDS)):
        if HOTWORDS[i] in text:
            flag = True
        else :
            flag = False
    return flag

# will return true if the text contains any of the hotwords from the list of HOTWORDS
def checkAnyHotwords(text, HOTWORDS):
    flag = False
    for i in range(len(HOTWORDS)):
        if HOTWORDS[i] in text:
            flag = True
            break
    return flag

if __name__ == '__main__':
    main()
