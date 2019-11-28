import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide" #This hides the pygame message. Annoying..
import pygame #Imports pygame to play sounds

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

def setSong(): #Loads a song and plays it
    pygame.mixer.music.load('sounds/sound.mp3')
    pygame.mixer.music.play()

def setSong2():
    pygame.mixer.music.load('sounds/sound2.mp3')
    pygame.mixer.music.play()

def setSong3():
    pygame.mixer.music.load('sounds/sound3.mp3')
    pygame.mixer.music.play()

def stopMusic(): #stops the music
    pygame.mixer.music.stop()
