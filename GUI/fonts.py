from tkinter import Tk
import tkinter.font
Tk()
for name in sorted(tkinter.font.families()):
    print(name)