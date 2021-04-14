"""
-------------------------------
IMPORTS
-------------------------------
"""
import tkinter as tk
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
def createButton(window, function, text, bgcolor=None):
    buttonFont = tkinter.font.Font(family="arial", size=12, weight="bold");
    button = tk.Button(window, command=function, text=text, font=buttonFont, bg=bgcolor);
    return button

"""
Create label widget
params: window, labelText, font, fontSize, fontWeight
return: label object
"""
def createLabel(window, text, font, fontsize, fontweight):
    labelFont = tkinter.font.Font(family=font, size=fontsize, weight=fontweight);
    label = tk.Label(window, text=text, font=labelFont)
    return label

"""
Create entry widget
params: window, bgcolor, show 
return: entry object
"""
def createEntry(window, bgcolor, show=None):
    if show != None:
        entry = tk.Entry(window, bg=bgcolor, show=show)
    else:
        entry = tk.Entry(window, bg=bgcolor)
    return entry

"""
Create radio button widget
params: window
return: radio button object
"""
def createRadioButton(window, text, var, value):
    radioButton = tk.Radiobutton(window, text=text, var=var, value=value)
    return radioButton

"""
Create scrollbar
"""
def createScrollbar(window):
    scrollbar = tk.Scrollbar(window, orient=tk.VERTICAL)
    return scrollbar

"""
Create listbox
"""
def createListbox(window, width, yscrollcommand):
    return tk.Listbox(window, width=width, yscrollcommand=yscrollcommand)