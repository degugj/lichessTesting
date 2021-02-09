"""
    audio.py
    Module to provide audio for different actions that occur in MagiChess
    - uses pygame library to play different sound files (.wav, .mp3)
"""
import pygame

pygame.mixer.init()

# game victory (checkmate, opponent resigns/aborts)
def sound_victory():
    pygame.mixer.music.load("audio_files/victory.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        continue

# game defeat (checkmate, user resigns/aborts)
def sound_defeat():
    pygame.mixer.music.load("audio_files/defeat.wav")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        continue

# chessboard move
def sound_move():
    pygame.mixer.music.load("audio_files/move.wav")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        continue

# successful move/user's turn
def sound_success():
    pygame.mixer.music.load("audio_files/success.wav")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        continue

# error in move
def sound_error():
    pygame.mixer.music.load("audio_files/error.wav")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        continue
    
# button press in UI
def sound_button():
    pygame.mixer.music.load("audio_files/button_click.wav")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        continue
