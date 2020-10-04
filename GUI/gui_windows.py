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
create new window
params: window
"""
def createNewWindow(currentWindow):
    newWindow = Toplevel(currentWindow)
    newWindow.title("New Window")