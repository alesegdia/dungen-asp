from Tkinter import *
from ttk import *
import tkFileDialog
import tkMessageBox
import math
import json
import os

from maputil.tilemap import Tilemap
from asp.clingo import clingo_spawn
from asp.generator import asp_room_entry, asp_map_size

class TileConfig:
    tilecolor = {
        0 : "blue",
        1 : "red",
    }
    tileoptions = {
        "" : 0,
        "solid" : 1,
        "free " : 0,
    }
    tilesize = 64


class RequestSizeDialog:

    def __init__(self, app):
        self.app = app
        parent = app.master
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
        self.app.new_tilemap(int(self.ex.get()), int(self.ey.get()))
        self.top.destroy()

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
        self.parentw = parentw
        self.master = master
        self.tree = Treeview(parentw)
        self.tree["columns"] = ("roomname", "numrooms")
        self.tree.column("roomname", width=100)
        self.tree.column("numrooms", width=100)
        self.tree.heading("roomname", text="Room Name")
        self.tree.heading("numrooms", text="Number of rooms")
        self.tree.pack(expand=True, fill=BOTH)
        self.tree.bind("<Double-1>", self.selectItem)
        self.newentrybutton = Button(parentw, text="New...", command=self.new_entry)
        self.newentrybutton.pack()

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
                self.tree.insert("", 0, text=file.name, values=("1", "1"))
            except:
                tkMessageBox.showerror("Invalid file", "JSON contents is not valid for a room!")
        else:
            tkMessageBox.showerror("Invalid file", "Not a JSON file!")

        file.close()
        pass

    def selectItem(self, event):
        item = self.tree.selection()[0]
        c = self.tree.identify_column(event.x)
        if c != "#0":
            TreeEditDialog(self.master, self.tree, item, c, "replace-me", lambda x: x.isdigit())


class TilemapEdit:
    def __init__(self, master, parentw):
        self.master = master
        self.parentw = parentw

        # canvas creation
        self.canvasframe = Frame(parentw, width=300, height=300)
        self.canvasframe.pack(fill=BOTH, expand=True)
        self.canvas = Canvas(self.canvasframe)
        self.canvas.bind("<B1-Motion>", self.motion)

        self.hbar = Scrollbar(self.canvasframe, orient=HORIZONTAL)
        self.hbar.pack(side=BOTTOM, fill=X)
        self.hbar.config(command=self.canvas.xview)

        self.vbar = Scrollbar(self.canvasframe, orient=VERTICAL)
        self.vbar.pack(side=RIGHT, fill=Y)
        self.vbar.config(command=self.canvas.yview)

        self.canvas.config(xscrollcommand=self.hbar.set, yscrollcommand=self.vbar.set)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=True)

        # tileselect creation
        self.selectedTile = StringVar(self.parentw)
        #self.selectedTile.set(TileConfig.tileoptions.keys()[1])
        self.tileOption = apply( OptionMenu, (self.parentw, self.selectedTile) + tuple(TileConfig.tileoptions.keys()) )
        self.tileOption.pack()

        # tilemap creation
        self.new_tilemap(6,8)

    def request_new_size(self):
        d = RequestSizeDialog(self)
        self.master.wait_window(d.top)

    def save_json(self):
        file = tkFileDialog.asksaveasfile()
        json.dump(self.tilemap.tilemap, file)
        file.close()

    def load_json(self):
        file = tkFileDialog.askopenfile()
        self.load_tilemap(json.load(file))
        file.close()

    def load_tilemap(self, tm):
        self.tilemap.tilemap = tm
        self.fit_canvas_to_tilemap()
        self.update_canvas()

    def new_tilemap(self,w,h):
        self.tilemap = Tilemap(w,h)
        self.fit_canvas_to_tilemap()
        self.update_canvas()

    def motion(self, event):
        canvas = event.widget
        x = canvas.canvasx(event.x)
        y = canvas.canvasy(event.y)
        tilesize = TileConfig.tilesize
        tilex = int(x / tilesize)
        tiley = int(y / tilesize)
        self.tilemap.tilemap[tiley][tilex] = TileConfig.tileoptions[self.selectedTile.get()]
        self.update_canvas()

    def fit_canvas_to_tilemap(self):
        canvas_width = self.tilemap.w() * TileConfig.tilesize
        canvas_height = self.tilemap.h() * TileConfig.tilesize
        self.canvas.width = canvas_width
        self.canvas.height = canvas_height
        self.canvas.config(scrollregion=(0,0,canvas_width, canvas_height), xscrollcommand=self.hbar.set, yscrollcommand=self.vbar.set, width = 300, height = 300 )

    def update_canvas_(self, x, y, tile):
        tilesize = TileConfig.tilesize
        x1 = x * tilesize
        y1 = y * tilesize
        x2 = (x + 1) * tilesize
        y2 = (y + 1) * tilesize
        self.canvas.create_rectangle( x1, y1, x2, y2, fill = TileConfig.tilecolor[tile])

    def update_canvas(self):
        self.canvas.delete("all")
        self.tilemap.foreach(self.update_canvas_)

class App:

    def __init__(self):

        # tkinter init
        self.master = Tk()

        self.notebook = Notebook(self.master)
        self.tab1 = Frame(self.notebook)
        self.tab2 = Frame(self.notebook)
        self.notebook.add(self.tab1, text="Room Edition")
        self.notebook.add(self.tab2, text="Set Edition")
        self.notebook.pack(fill=BOTH, expand=True)

        self.tmedit = TilemapEdit(self.master, self.tab1)
        self.genconfig = GenConfigEdit(self.master, self.tab2)

        self.menubar = Menu(self.master)

        self.menu = Menu(self.menubar, tearoff=0)
        self.menu.add_command(label="Exit", command=self.master.quit)
        self.menubar.add_cascade(label="File", menu=self.menu)

        self.menuroom = Menu(self.menubar, tearoff=0)
        self.menuroom.add_command(label="New...", command=self.tmedit.request_new_size)
        self.menuroom.add_command(label="Load...", command=self.tmedit.load_json)
        self.menuroom.add_command(label="Save...", command=self.tmedit.save_json)
        self.menubar.add_cascade(label="Room", menu=self.menuroom)

        self.menugen = Menu(self.menubar, tearoff=0)
        self.menugen.add_command(label="Size", command=self.set_gen_size)
        self.menugen.add_command(label="Generate", command=self.gen_map)
        self.menubar.add_cascade(label="Mapgen", menu=self.menugen)

        self.master.config(menu=self.menubar)
        self.master.minsize(self.master.winfo_width(), self.master.winfo_height())

    def run(self):
        self.master.mainloop()

    def set_gen_size(self):
        pass

    def gen_map(self):

    	# read base code
    	f = open("../asp/sample-gen.lp", "r")
    	generator_asp = f.read()
    	f.close()

    	# generate mapsize code
    	mapsize_asp = asp_map_size(10)

    	# generate
    	roomentry_asp = asp_room_entry(self.tmedit.tilemap, "qwe", 3)
    	
    	# call clingo process
    	print clingo_spawn( mapsize_asp, roomentry_asp, generator_asp )


if __name__ == '__main__':
    app = App()
    app.run()
