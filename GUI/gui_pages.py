"""
-------------------------------
IMPORTS
-------------------------------
"""
import tkinter as tk
import gui_widgets

"""
-------------------------------
DEFINITIONS
-------------------------------
"""


class StartupPage(tk.Frame):
    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)
        label = tk.Label(self, text="Welcome to MagiChess").pack(pady=1)
        
        #startup widgets
        signinButton = gui_widgets.createButton(window=master, text="Sign in to Lichess", font="Comic Sans", size=12, weight="bold")
        signinButton.grid(row=1, column=0)
        
        exitButton = gui_widgets.createButton(window=master, function=exit, text="Exit", font="Comic Sans", size=12, weight="bold")
        exitButton.grid(row=2, column=0)

        
        

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