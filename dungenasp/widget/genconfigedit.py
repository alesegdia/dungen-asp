
from Tkinter import *
from ttk import *

import tkFileDialog
import tkMessageBox

import json
import os

class TreeEditDialog:

	def __init__(self, master, tree, item, column, heading, validation):
		self.tree = tree
		self.item = item
		self.validation = validation
		self.column = column
		parent = master
		top = self.top = Toplevel(parent)
		Label(top, text=heading).pack()
		self.val = Entry(top)
		self.val.pack(padx=5)
		b = Button(top, text="OK", command=self.ok)
		b.pack(pady=5)

	def ok(self):
		if self.validation(self.val.get()):
			if self.column == "#0":
				self.tree.item(self.item, text=self.val.get())
			else:
				self.tree.set(self.item, column=self.column, value=self.val.get())
		else:
			tkMessageBox.showerror("Invalid value", "The value you entered is invalid for this field")
		self.top.destroy()

class GenConfigEdit:
	def __init__(self, master, parentw):
		self.parentw = Frame(parentw)
		parentw = self.parentw
		#parentw.pack(fill="both", expand=True)
		self.master = master
		b = Button(parentw, text="OK")
		self.tree = Treeview(parentw)
		self.tree['show'] = "headings"
		self.tree["columns"] = ("filepath", "roomname", "numrooms")
		self.tree.column("filepath", width=100)
		self.tree.column("roomname", width=100)
		self.tree.column("numrooms", width=100)
		self.tree.heading("filepath", text="File path")
		self.tree.heading("roomname", text="Room name")
		self.tree.heading("numrooms", text="Number of rooms")
		self.tree.pack(expand=True, fill=BOTH)
		self.tree.bind("<Double-1>", self.selectItem)
		self.newentrybutton = Button(parentw, text="New...", command=self.new_entry)
		self.newentrybutton.pack(side="left")
		self.deletebutton = Button(parentw, text="Delete...", command=self.new_entry)
		self.deletebutton.pack(side="left")
		self.loadbutton = Button(parentw, text="Load...", command=self.new_entry)
		self.loadbutton.pack(side="left")
		self.savebutton = Button(parentw, text="Save...", command=self.new_entry)
		self.savebutton.pack(side="left")
		self.clearbutton = Button(parentw, text="Clear...", command=self.new_entry)
		self.clearbutton.pack(side="left")

	def new_entry(self):
		file = tkFileDialog.askopenfile()
		filename, extension = os.path.splitext(file.name)
		print(extension)
		if extension == '.json':
			try:
				data = json.load(file)
				h = len(data[0])
				w = len(data)
				for x in range(0,w):
					for y in range(0,h):
						if not isinstance( data[x][y], int ):
							raise Exception("Invalid intern data!")
				rname = "room" + str(len(self.tree.get_children()))
				self.tree.insert("", 0, text="", values=(file.name, rname, "1"))
			except:
				tkMessageBox.showerror("Invalid file", "JSON contents is not valid for a room!")
		else:
			tkMessageBox.showerror("Invalid file", "Not a JSON file!")

		file.close()
		pass

	def selectItem(self, event):
		item = self.tree.selection()[0]
		c = self.tree.identify_column(event.x)
		if c == "#3":
			TreeEditDialog(self.master, self.tree, item, c, "replace-me", lambda x: x.isdigit())
		elif c == "#2":
			TreeEditDialog(self.master, self.tree, item, c, "replace-me", lambda x: not x[0].isdigit())

