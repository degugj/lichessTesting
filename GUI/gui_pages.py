"""
-------------------------------
IMPORTS
-------------------------------
"""
import tkinter as tk
import gui_widgets as widgets
import gui_test

"""
-------------------------------
DEFINITIONS
-------------------------------
"""


class StartupPage(tk.Frame):
    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)
        header = widgets.createLabel(self, text="MagiChess", font="times", fontsize=14, fontweight="bold")
        header.pack(padx=10, pady=10)
        
        #startup buttons
        signinButton = widgets.createButton(self, function=lambda: controller.show_frame(SigninPage),
                                           text="Sign in to LiChess.org")
        signinButton.pack()
        
        exitButton = widgets.createButton(self, function=exit,
                                          text="Exit")    
        exitButton.pack()


class SigninPage(tk.Frame):
    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)
        header = widgets.createLabel(self, text="Sign in to LiChess", font="times", fontsize=14, fontweight="bold")
        header.pack(padx=10, pady=10)
        
        """ username/password entries """
        usernameLabel = widgets.createLabel(self, text="Username", font="times", fontsize=11, fontweight="normal")
        usernameLabel.pack()
        usernameEntry = widgets.createEntry(self, bgcolor="beige")
        usernameEntry.pack()
        
        passwordLabel = widgets.createLabel(self, text="Password", font="times", fontsize=11, fontweight="normal")
        passwordLabel.pack()
        passEntry = widgets.createEntry(self, bgcolor="beige", show="*")
        passEntry.pack()
        
        
        """ buttons """
        loginButton = widgets.createButton(self, function=lambda: controller.show_frame(MainMenuPage),
                                           text="Login", bgcolor="sky blue")
        loginButton.pack(pady=4)
        
        returnButton = widgets.createButton(self, function=lambda: controller.show_frame(StartupPage),
                                            text="Return", bgcolor="sky blue")
        returnButton.pack(pady=7)
        

class MainMenuPage(tk.Frame):
    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)
        header = widgets.createLabel(self, text="Welcome to MagiChess", font="times", fontsize=14, fontweight="bold")
        header.pack(padx=10, pady=10)
        
        """ main menu options """
        playbotButton = widgets.createButton(self, function=lambda: controller.show_frame(PlayBotPage),
                                             text="Play Bot", bgcolor="sky blue")
        playbotButton.pack(pady=5)
        
        playrandButton = widgets.createButton(self, function=lambda: controller.show_frame(PlayRandomPage),
                                             text="Seek an Opponent", bgcolor="sky blue")
        playrandButton.pack(pady=5)
        
        playfriendButton = widgets.createButton(self, function=lambda: controller.show_frame(PlayFriendPage),
                                             text="Challenge a Friend", bgcolor="sky blue")
        playfriendButton.pack(pady=5)
        
        exitButton = widgets.createButton(self, function=exit,
                                             text="Exit MagiChess", bgcolor="seashell3")
        exitButton.pack(pady=5)
        
        
        
""" main menu pages """
class PlayBotPage(tk.Frame):
    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)
        header = widgets.createLabel(self, text="Play a Bot", font="times", fontsize=14, fontweight="bold")
        header.pack(padx=10, pady=10)
        
        returnButton = widgets.createButton(self, function=lambda:controller.show_frame(MainMenuPage),
                                            text="Return to Main Menu", bgcolor="sky blue")
        returnButton.pack()
        
class PlayRandomPage(tk.Frame):
    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)
        header = widgets.createLabel(self, text="Seeking Opponent...", font="times", fontsize=14, fontweight="bold")
        header.pack(padx=10, pady=10)
        
        returnButton = widgets.createButton(self, function=lambda:controller.show_frame(MainMenuPage),
                                            text="Return to Main Menu", bgcolor="sky blue")
        returnButton.pack()
        
        
class PlayFriendPage(tk.Frame):
    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)
        header = widgets.createLabel(self, text="Search Opponent Name", font="times", fontsize=14, fontweight="bold")
        header.pack(padx=10, pady=10)
        
        returnButton = widgets.createButton(self, function=lambda:controller.show_frame(MainMenuPage),
                                            text="Return to Main Menu", bgcolor="sky blue")
        returnButton.pack()
        
        
"""
-------------------------------
FUNCTIONS
-------------------------------
"""

