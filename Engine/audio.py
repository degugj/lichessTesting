"""
    audio.py
    Module to provide audio for different actions that occur in MagiChess
    - uses pygame library to play different sound files (.wav, .mp3)
"""
import pygame
import time

# initialize pygame sound mixer
def init_mixer():
    pygame.mixer.init()


# game victory (checkmate, opponent resigns/aborts)
def sound_victory():
    pygame.mixer.music.load("Engine/audio_files/victory.mp3")
    pygame.mixer.music.play()


# game defeat (checkmate, user resigns/aborts)
def sound_defeat():
    pygame.mixer.music.load("Engine/audio_files/defeat.wav")
    pygame.mixer.music.play()


# chessboard move
def sound_move():
    pygame.mixer.music.load("Engine/audio_files/move.wav")
    pygame.mixer.music.play()


# successful move/user's turn
def sound_gamestart():
    pygame.mixer.music.load("Engine/audio_files/success.wav")
    pygame.mixer.music.play()


# error in move
def sound_error():
    pygame.mixer.music.load("Engine/audio_files/error.wav")
    pygame.mixer.music.play()


# button press in UI
def sound_button():
    pygame.mixer.music.load("Engine/audio_files/button_click.wav")
    pygame.mixer.music.play()
 

# background menu music
def sound_background():
    pygame.mixer.music.load("Engine/audio_files/background.mp3")
    pygame.mixer.music.play(-1, 0.0)
