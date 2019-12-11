import os, sys
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide" #This hides the pygame message. Annoying..
import pygame #Imports pygame to play sounds

APP_FOLDER = os.path.dirname(os.path.realpath(sys.argv[0]))

#Initialize the mixer and set volume
pygame.mixer.init(44100)
volume = 0.1
pygame.mixer.music.set_volume(volume)


def volumeUP():
    global volume
    if volume >= 1.0:
        volume = 1.0
    else:
        volume += 0.1
        pygame.mixer.music.set_volume(volume)

def volumeDOWN():
    global volume
    if volume <= 0.0:
        volume = 0.0
    else:
        volume -= 0.1
        pygame.mixer.music.set_volume(volume)

def setSong1(): #Loads a song and plays it
    full_path = os.path.join(APP_FOLDER, "sound1.mp3")
    mixer.music.load(full_path)
    pygame.mixer.music.play(-1) #(-1) means that song is repeated

def setSong2():
    full_path = os.path.join(APP_FOLDER, "sound2.mp3")
    mixer.music.load(full_path)
    pygame.mixer.music.play(-1)

def setSong3():
    full_path = os.path.join(APP_FOLDER, "sound3.mp3")
    mixer.music.load(full_path)
    pygame.mixer.music.play(-1)

def setCountdown():
    full_path = os.path.join(APP_FOLDER, "countdown.mp3")
    mixer.music.load(full_path)
    pygame.mixer.music.play()

def stopMusic(): #stops the music
    pygame.mixer.music.stop()
