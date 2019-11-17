import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide" #This hides the pygame message. Annoying..
import pygame #Imports pygame to play sounds

def setSong(): #Initializes the music player, loads a song, sets volume and plays it
    pygame.mixer.init()
    pygame.mixer.music.load('sounds/sound.mp3')
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play()

def setSong2():
    pygame.mixer.init()
    pygame.mixer.music.set_volume(0.2)    
    pygame.mixer.music.load('sounds/sound2.mp3')
    pygame.mixer.music.play()

def setSong3():
    pygame.mixer.init()
    pygame.mixer.music.set_volume(0.2)    
    pygame.mixer.music.load('sounds/sound3.mp3')
    pygame.mixer.music.play()

def stopMusic(): #stops the music
    pygame.mixer.init()
    pygame.mixer.music.stop()