from Tkinter import *
import ttk
#from ttk import *

class TextLabel(Frame):

	def __init__(self, parentw, text):
		Frame.__init__(self, parentw, relief=RAISED, padx=5, pady=5, bd=2)

		#Label(self, text=text).pack(side="top")
		Button(self, text=text).pack(side="top")
		#ttk.Separator(self, orient=HORIZONTAL).pack(side="bottom", fill="x")
		Text(self, width=1, height=1).pack(side="bottom", expand=True, fill="both")




class GenProcess:

	def __init__(self, master, parentw):
		self.parentw = parentw
		self.master = master

		self.frame = parentw
		self.container = parentw

		TextLabel(self.container, "Generate code").pack(side="top", expand=True, fill="both")
		TextLabel(self.container, "Execute code").pack(side="bottom", expand=True, fill="both")

