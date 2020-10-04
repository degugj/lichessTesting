"""
-------------------------------
IMPORTS
-------------------------------
"""
import tkinter as tk
import gui_pages
import gui_widgets

"""
-------------------------------
GUI app
-------------------------------
"""
class MainApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        
        #frame of window
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        
        #centralize container
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        #dictionary of frames
        self.frames = {}
        
        #create startup page frame and update frame dictionary
        startupFrame = gui_pages.StartupPage
        frame = startupFrame(container, self)
        self.frames[startupFrame] = frame
        
        #grid the frame
        frame.grid(row=0, column=0, sticky="nsew")
        
        #show startup page frame
        self.show_frame(startupFrame)
        
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
    mainWindow.geometry("600x200")   #main window dimensions
    

    mainWindow.mainloop()


if __name__ == '__main__':
    main();
# program will terminate and close GUI if no loop (terminal only)

