from Tkinter import *
import tkFileDialog
import json

from dungenasp.widget.tilemapwidget import TilemapWidget
from dungenasp.maputil.tileconfig import TileConfig

class RequestSizeDialog:

	def __init__(self, master, callback):
		parent = master
		self.callback = callback
		top = self.top = Toplevel(parent)
		Label(top, text="X").pack()
		self.ex = Entry(top)
		self.ex.pack(padx=5)
		Label(top, text="Y").pack()
		self.ey = Entry(top)
		self.ey.pack(padx=5)
		b = Button(top, text="OK", command=self.ok)
		b.pack(pady=5)

	def ok(self):
		self.callback(self.ex.get(), self.ey.get())
		self.top.destroy()


class TilemapEdit:
	def __init__(self, master, parentw):
		self.master = master
		self.parentw = parentw

		self.tilemapwidget = TilemapWidget(master, parentw)
		self.selectedTile = StringVar(self.parentw)
		self.tileOption = apply( OptionMenu, (self.parentw, self.selectedTile) + tuple(TileConfig.tileoptions.keys()) )
		self.tileOption.pack()
		self.tilemapwidget.canvas.bind("<B1-Motion>", self.motion)

		self.tilemapwidget.new_tilemap(6,8)

	def request_new_size(self):
		def edit_size_cb(x, y):
			self.tilemapwidget.new_tilemap(int(x), int(y))
		d = RequestSizeDialog(self.master, edit_size_cb)
		self.master.wait_window(d.top)

	def save_json(self):
		file = tkFileDialog.asksaveasfile()
		json.dump(self.tilemapwidget.tilemap.tilemap, file)
		file.close()

	def load_json(self):
		file = tkFileDialog.askopenfile()
		self.tilemapwidget.load_tilemap(json.load(file))
		file.close()

	def motion(self, event):
		canvas = event.widget
		x = canvas.canvasx(event.x)
		y = canvas.canvasy(event.y)
		tilesize = TileConfig.tilesize
		tilex = int(x / tilesize)
		tiley = int(y / tilesize)
		self.tilemapwidget.tilemap.tilemap[tiley][tilex] = TileConfig.tileoptions[self.selectedTile.get()]
		self.tilemapwidget.update_canvas()


