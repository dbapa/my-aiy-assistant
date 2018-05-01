import logging
import subprocess
import sys
import RPi.GPIO as gpio
import time
import _thread
import quandl as qd
import requests
import my_news_reader as news
import my_locker as locker
import aiy.assistant.auth_helpers
import aiy.audio
import aiy.voicehat
from google.assistant.library import Assistant
from google.assistant.library.event import EventType


ROOMCLIMATE_FILE = locker.getContent("roomsensor","current")

BCM_FOR_HAT_RELAY_PIN1 = 4 # Driver 0 on HAT board
BCM_FOR_HAT_RELAY_PIN2 = 17 # Driver 1 on HAT board

def initialize():
    gpio.setmode(gpio.BCM)
    gpio.setup(BCM_FOR_HAT_RELAY_PIN1,gpio.OUT) #,initial=0)
    gpio.setup(BCM_FOR_HAT_RELAY_PIN2,gpio.OUT) #,initial=0)


#returns a data set tuple e.g. {'temp':50, 'humidity':100 }
def get_room_temp():
    f = open(ROOMCLIMATE_FILE,'r')
    ln1 = f.readline()
    ln = ln1.split(':')
    dataSet = {}
    dataSet['temp']=ln[1]
    ln1 = f.readline()
    ln = ln1.split(':')
    dataSet['humidity']=ln[1]
    f.close()
    return dataSet

playshell = None
def play_song_new_thread(pshell,songName):
    if (pshell == None):
        pshell = subprocess.Popen(["/usr/local/bin/mpsyt",""],stdin=subprocess.PIPE,stdout=subprocess.PIPE)
    pshell.stdin.write(bytes('/' + songName + '\n 1 \n', 'utf-8'))
    pshell.stdin.flush()
    # Waits for button to be pressed and hold for 1 second to kill the player
    gpio.setmode(gpio.BCM)
    gpio.setup(23, gpio.IN)
    while gpio.input(23):
         time.sleep(1)
    pkill = subprocess.Popen(["/usr/bin/pkill","vlc"],stdin=subprocess.PIPE)

# Wrapper method to the play_song_new_thread by initiating a new thread
def play_song(songName):
    global playshell
    _thread.start_new_thread(play_song_new_thread,(playshell,songName))

# kills the mpsyt and vlc player processes thereby stopping the player
def stop_playing():
    global playshell
    subprocess.Popen(["/usr/bin/pkill","vlc"],stdin=subprocess.PIPE)
    if playshell != None:
        subprocess.Popen(["/usr/bin/pkill","mpsyt"],stdin=subprocess.PIPE)
        playshell = None

def get_news(feedName):
    c = news.DBNewsReader()
    keys = c.get_news_sources()
    #print ('searching news for:',feedName)
    if len(feedName) != 0:
        feedName = feedName.lower()
    feedKey = ''
    for i in range(len(keys)):
        #print('key:',str(keys[i]))
        v = (str(keys[i])).lower().find(feedName)
        #print ('index of search string:',v)
        if v > 0 :
            feedKey = keys[i]
            break
        else:
            feedKey = keys[0] # feedKey can be set to the first source outside of for player if no feedName matched
    #print('getting news for: ',feedKey)
    newsD  = c.get_news(feedKey)

    return newsD


def get_news_feeds():
    c = news.DBNewsReader()
    src = c.get_news_sources_as_text()
    #print (src)
    return src

def start_crypto_feeder():
    pass

def stop_crypto_feeder():
    pass

def bedroom_lights(textStr):
    k = locker.getContent("ifttt","key")
    if "off" in textStr:
        r = requests.post("https://maker.ifttt.com/trigger/lightoff/with/key/"+k)
    elif "on" in textStr:
        r = requests.post("https://maker.ifttt.com/trigger/lighton/with/key/"+k)

def voicehat_driver_pin(bcm_pin,on_off):
    gpio.setmode(gpio.BCM)
    gpio.setup(bcm_pin,gpio.OUT) # ,initial=0)
    gpio.output(bcm_pin,on_off)

def livingroom_lights(textStr):
    if "off" in textStr:
        voicehat_driver_pin(BCM_FOR_HAT_RELAY_PIN1,1)
    elif "on" in textStr:
        voicehat_driver_pin(BCM_FOR_HAT_RELAY_PIN1,0)


def song_test():
    x = play_song('guns and roses')

if __name__ == '__main__':
    song_test()
