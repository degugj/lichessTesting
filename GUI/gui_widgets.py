"""
-------------------------------
IMPORTS
-------------------------------
"""
from tkinter import *
import tkinter.font

"""
-------------------------------
FUNCTIONS
-------------------------------
"""

"""
Create button widget
params: window, buttonText, font, fontSize, fontWeight
return: button object
"""
def createButton(window=None, function=None, buttonText=None, font=None, fontSize=None,
                 fontWeight=None):
    buttonFont = tkinter.font.Font(family=font, size=fontSize, weight=fontWeight);
    button = Button(window, command=function, text=buttonText, font=buttonFont);
    return button

