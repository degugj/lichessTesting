"""
-------------------------------
IMPORTS
-------------------------------
"""
import tkinter as tk
import signal, os

from Engine.GUI import gui_widgets as widgets
from Engine import gui_pages as pages, audio

"""
-------------------------------
VARIABLES AND DEFINITIONS
-------------------------------
"""
os.environ['SDL_VIDEO_CENTERED'] = '1'

# width and height of gui window
WIDTH = 500
HEIGHT = 300


"""
-------------------------------
FUNCTIONS
-------------------------------
"""

class MainApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        
        #tk.Tk.iconbitmap(self, default="Engine/GUI/icon.bmp")

        #frame of window
        container = tk.Frame(self)
        container.pack(side="top")
        
        #centralize container
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        #dictionary of frames
        self.frames = {}
        
        for F in (pages.StartupPage, pages.SigninPage, pages.MainMenuPage, pages.PlayBotPage, pages.PlayRandomPage,
                  pages.ChallengePage, pages.ChallengeDeniedPage):
            
            #create startup page frame and update frame dictionary
            frame = F(container, self)
            self.frames[F] = frame
            
            #grid the frame
            frame.grid(row=0, column=0, sticky="nsew")
            
    
        #show startup page frame
        self.show_frame(pages.StartupPage)
        
    """
    show desired frame, 'page'
    params: page
    """    
    def show_frame(self, page, user=""):

        frame = self.frames[page]
        #checks for username input
        if user != "":
            #main menu frame functions
            frame.welcomeHeader(user)
            frame.menuButtons(self)
            
        frame.tkraise()
    

"""
-------------------------------
MAIN
-------------------------------
"""
def main():
    
    # initialize sound mixer
    audio.init_mixer()
    # initialize background music
    audio.sound_background()

    if 0:
        pages.test()
    else:
        #GUI window
        mainWindow = MainApp()
        mainWindow.title("MagiChess")
        
        positionRight = int(mainWindow.winfo_screenwidth()/2 - WIDTH/2)
        positionDown = int(mainWindow.winfo_screenheight()/2 - HEIGHT/2)
        # mainWindow.attributes('-fullscreen', True)   #main window dimensions
        mainWindow.geometry("{}x{}+{}+{}".format(WIDTH, HEIGHT, positionRight, positionDown))

        # map closing 'window closing' event to quit_program function
        mainWindow.protocol("WM_DELETE_WINDOW", pages.quit_program)

        # program will terminate and close GUI if no loop (terminal only)
        mainWindow.after(50, lambda: check(mainWindow))
        mainWindow.mainloop()

def check(mainWindow):
    mainWindow.after(50, lambda: check(mainWindow))

if __name__ == '__main__':
    main();

