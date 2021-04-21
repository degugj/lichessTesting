import tkinter as tk
from tkinter import messagebox

def messagebox_question(title, msg):
	return messagebox.askquestion(title, msg)

def messagebox_alert(title, msg)
	return messagebox.showinfo(title, msg)

class MultiMsgBox(tk.Toplevel):
	def __init__(self):
		tk.Toplevel.__init__(self)



	def destroy_msgbox(self):
		self.destroy()