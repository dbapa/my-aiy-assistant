import csv
import subprocess
import sys

# to be able to play youtube music need to install the following
# pip install mps-youtube, youtube-dl
# and sudo apt-get vlc - use sudo apt-get update before installing vlc
# after that, issue this: mpsyt set player vlc

playshell = None

def play_song(songName):
    global playshell   
    
    if (playshell == None):
        playshell = subprocess.Popen(["/usr/local/bin/mpsyt","/ ",songName,"\n 1 \n"])
        #playshell = subprocess.Popen(["/usr/local/bin/mpsyt",""],stdin=subprocess.PIPE,stdout=subprocess.PIPE)
    playshell.stdin.write(bytes('/' + songName + '\n 1 \n', 'utf-8'))
    playshell.stdin.flush()

play_song('guns and roses')

