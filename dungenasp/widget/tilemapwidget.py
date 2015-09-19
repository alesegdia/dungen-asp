from Tkinter import *

from dungenasp.maputil.tilemap import Tilemap
from dungenasp.widget.tileconfig import TileConfig

class TilemapWidget:
	def __init__(self, master, parentw):

		self.tilesize = TileConfig.tilesize
		self.master = master
		self.parentw = parentw

		self.canvasframe = Frame(parentw, width=1, height=1)
		self.canvasframe.pack(fill=BOTH, expand=True)
		self.canvas = Canvas(self.canvasframe, width=1, height=1)

		self.hbar = Scrollbar(self.canvasframe, orient=HORIZONTAL)
		self.hbar.pack(side=BOTTOM, fill=X)
		self.hbar.config(command=self.canvas.xview)

		self.vbar = Scrollbar(self.canvasframe, orient=VERTICAL)
		self.vbar.pack(side=RIGHT, fill=Y)
		self.vbar.config(command=self.canvas.yview)

		self.canvas.config(xscrollcommand=self.hbar.set, yscrollcommand=self.vbar.set)
		self.canvas.pack(side=LEFT, fill=BOTH, expand=True)

	def update_canvas(self):
		self.canvas.delete("all")
		self.tilemap.foreach(self.update_canvas_)

	def fit_canvas_to_tilemap(self):
		canvas_width = self.tilemap.w() * self.tilesize
		canvas_height = self.tilemap.h() * self.tilesize
		self.canvas.width = canvas_width
		self.canvas.height = canvas_height
		self.canvas.config(scrollregion=(0,0,canvas_width, canvas_height), xscrollcommand=self.hbar.set, yscrollcommand=self.vbar.set, width = 300, height = 300 )

	def load_tilemap(self, tm):
		self.tilemap.tilemap = tm
		self.fit_canvas_to_tilemap()
		self.update_canvas()

	def new_tilemap(self,w,h):
		self.tilemap = Tilemap(w,h)
		self.fit_canvas_to_tilemap()
		self.update_canvas()

	def update_canvas_(self, x, y, tile):
		tilesize = self.tilesize
		x1 = x * tilesize
		y1 = y * tilesize
		x2 = (x + 1) * tilesize
		y2 = (y + 1) * tilesize
		self.canvas.create_rectangle( x1, y1, x2, y2, fill = TileConfig.tilecolor[tile])
