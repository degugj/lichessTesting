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
def createButton(window=None, function=None, text=None, font=None, size=None, weight=None):
    buttonFont = tkinter.font.Font(family=font, size=size, weight=weight);
    button = Button(window, command=function, text=text, font=buttonFont);
    return button

"""
Create label widget
params: window, labelText, font, fontSize, fontWeight
return: label object
"""
def createLabel(window, text, **font):
    return

