from Tkinter import *
import ttk
from datetime import datetime

from dungenasp.widget.tilemapwidget import TilemapWidget
from dungenasp.widget.genconfigedit import GenConfigEdit

from dungenasp.asp.generator import asp_map_size, asp_room_entry

from dungenasp.asp.clingo import clingo_spawn

from dungenasp.maputil.tilemap import Tilemap

import json

class TextLabel(Frame):

	def __init__(self, parentw, text):
		Frame.__init__(self, parentw, relief=RAISED, padx=5, pady=5, bd=2)

		#Label(self, text=text).pack(side="top")
		Button(self, text=text).pack(side="top")
		#ttk.Separator(self, orient=HORIZONTAL).pack(side="bottom", fill="x")
		Text(self, width=1, height=1).pack(side="bottom", expand=True, fill="both")

class NoTreeChildrenException(Exception):
	pass

class GenOptions(Frame):

	def __init__(self, parent):
		Frame.__init__(self, parent)

		self.parent = parent
		self.top_frame = Frame(self)
		self.top_frame.pack(side="top")
		self.bot_frame = Frame(self)
		self.bot_frame.pack(side="top", fill="both", expand=True)

		self.mapsizebut = Label(self.top_frame, text="Map size")
		self.mapsizetext = Text(self.top_frame, height=1, width=21)
		self.genmap = Button(self.top_frame, text="Generate!", command=self.generate, background="purple", foreground="white")

		self.notebook = ttk.Notebook(self.bot_frame, width=1, height=1)

		self.tab3 = Frame(self.notebook)
		self.notebook.add(self.tab3, text="Console log")
		self.logtxt = Text(self.tab3)
		self.logtxt.config(state="disabled")
		self.logtxt.pack(fill="both", expand=True)

		# generation tab
		self.tab1 = Frame(self.notebook)
		self.notebook.add(self.tab1, text="ASP generated code")
		self.gentxt = Text(self.tab1)
		self.gentxt.config(state="disabled")
		self.gentxt.pack(fill="both", expand=True)

		self.tab2 = Frame(self.notebook)
		self.notebook.add(self.tab2, text="Clingo output")
		self.solvetxt = Text(self.tab2)
		self.solvetxt.config(state="disabled")
		self.solvetxt.pack(fill="both", expand=True)

		self.notebook.pack(fill="both", expand=True)

		self.mapsizebut.pack(side="left")
		self.mapsizetext.pack(side="left")
		self.genmap.pack(side="left")

	def generate(self):
		try:
			print(int(self.mapsizetext.get("1.0", END)))
			tree = self.parent.gc.tree
			if len(tree.get_children()) == 0:
				raise NoTreeChildrenException
			code = asp_map_size(int(self.mapsizetext.get("1.0", END)))
			for c in tree.get_children():
				cdata = tree.set(c)
				tm = Tilemap(1,1)
				f = open(cdata['filepath'], 'r')
				tm.tilemap = json.load(f)
				f.close()
				code = code + asp_room_entry(tm, cdata['roomname'], cdata['numrooms'])

			f = open("asp/sample-gen.lp", "r")
			generator_asp = f.read()
			f.close()
			code = code + generator_asp 

			self.write_to_txt(self.gentxt, code)
			output_code = clingo_spawn(code)
			self.write_to_txt(self.solvetxt, output_code)

			self.parent.parent.resultingmap.load_asp_tilemap(output_code)

		except ValueError:
			self.log("invalid map size")
		except NoTreeChildrenException:
			self.log("no rooms to use")

	def log(self, txt):
		self.write_to_txt(self.logtxt, txt)

	def write_to_txt(self, txtwidget, txt):
		date = datetime.now().strftime('[%02H:%02M:%02S]')
		txtwidget.config(state="normal")
		txtwidget.insert(END, date + " " + txt + "\n")
		txtwidget.config(state="disabled")

class GenConfig(PanedWindow):

	def __init__(self, parent, master, pparent):

		PanedWindow.__init__(self, parent, orient=VERTICAL, sashwidth=8, bg="gray")

		self.parent = pparent

		self.gc = GenConfigEdit(master, self)
		self.go = GenOptions(self)

		self.add(self.gc.parentw)
		self.add(self.go)

		self.paneconfigure(self.gc.parentw, minsize=260)


class GenProcess:

	def __init__(self, master, parentw):
		self.parentw = parentw
		self.master = master

		self.panedw = PanedWindow(parentw, orient=HORIZONTAL, bg="gray", sashwidth=8)

		self.config = GenConfig(self.panedw, master, self)
		self.config.pack(expand=True, fill="both")

		#self.gc.parentw.pack(side="top", expand=True, fill="both")

		self.resultingmap = TilemapWidget(master, self.panedw)
		self.resultingmap.tilesize = 10
		self.resultingmap.new_tilemap(100, 100)


		self.panedw.pack(fill="both", expand=True)

		self.panedw.add(self.config)
		self.panedw.add(self.resultingmap.canvasframe)


