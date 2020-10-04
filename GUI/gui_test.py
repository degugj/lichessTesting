"""
-------------------------------
IMPORTS
-------------------------------
"""
from tkinter import *
import tkinter.font
import gui_windows
import gui_widgets

"""
-------------------------------
FUNCTIONS
-------------------------------
"""

"""
-------------------------------
MAIN
-------------------------------
"""
def main():
    
    #GUI window
    mainWindow = Tk()
    mainWindow.title('MagiChess')
    mainWindow.geometry("600x200")   #main window dimensions
    newlabel = Label(mainWindow, text="MagiChess Main Menu").pack(pady=5)
    
    #create buttons
    exitButton = gui_widgets.createButton(window=mainWindow, function=exit, buttonText="Exit",
                              font="Comic Sans", fontSize=12, fontWeight="bold")
    exitButton.pack(pady=2)
    #exitButton.grid(row=1, column=0)
    
    signinButton = gui_widgets.createButton(window=mainWindow, function=lambda: gui_windows.createNewWindow(mainWindow),
                                buttonText="Sign in to Lichess", font="Comic Sans",
                                fontSize=12, fontWeight="bold")
    signinButton.pack(pady=2)
    #signinButton.grid(row=2, column=0)
    
    
    mainWindow.mainloop()


if __name__ == '__main__':
    main();
# program will terminate and close GUI if no loop (terminal only)

