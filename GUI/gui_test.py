"""
-------------------------------
IMPORTS
-------------------------------
"""
import tkinter as tk
import gui_widgets
import gui_pages as pages

"""
-------------------------------
VARIABLES
-------------------------------
"""
#frames dictionary
frames = {}

"""
-------------------------------
FUNCTIONS
-------------------------------
"""

class MainApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        
        #frame of window
        container = tk.Frame(self)
        container.pack(side="top")
        
        #centralize container
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        #dictionary of frames
        
        self.frames = {}
        
        for F in (pages.StartupPage, pages.SigninPage, pages.MainMenuPage, pages.PlayBotPage, pages.PlayRandomPage,
                  pages.PlayFriendPage):
            
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
    def show_frame(self, page):
        frame = self.frames[page]
        frame.tkraise()
    

"""
-------------------------------
MAIN
-------------------------------
"""
def main():
    
    #GUI window
    mainWindow = MainApp()
    mainWindow.title("MagiChess")
    mainWindow.geometry("600x400")   #main window dimensions



    mainWindow.mainloop()


if __name__ == '__main__':
    main();
# program will terminate and close GUI if no loop (terminal only)

