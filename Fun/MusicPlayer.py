import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide" #This hides the pygame message. Annoying..
import pygame #Imports pygame to play sounds

#Initialize the mixer and set volume
pygame.mixer.init(44100)
pygame.mixer.music.set_volume(0.2)

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
