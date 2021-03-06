from Tkinter import *
from ttk import *
import json

from dungenasp.maputil.tilemap import Tilemap
from dungenasp.asp.clingo import clingo_spawn
from dungenasp.asp.generator import asp_room_entry, asp_map_size

from dungenasp.widget.roomedit import TilemapEdit
from dungenasp.widget.genconfigedit import GenConfigEdit
from dungenasp.widget.genprocess import GenProcess


class App:

    def __init__(self):

        # tkinter init
        self.master = Tk()

        self.notebook = Notebook(self.master, width=1, height=1)
        self.tab1 = Frame(self.notebook)
        self.tab3 = Frame(self.notebook)
        self.notebook.add(self.tab1, text="Room Edition")
        self.notebook.add(self.tab3, text="Map generation")
        self.notebook.pack(fill=BOTH, expand=True)

        self.tmedit = TilemapEdit(self.master, self.tab1)
        self.genprocess = GenProcess(self.master, self.tab3)

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
        self.master.update()
        self.master.minsize(400,400)

    def run(self):
        self.master.mainloop()

    def set_gen_size(self):
        pass

    def gen_map(self):

        # read base code
            f = open("asp/sample-gen.lp", "r")
            generator_asp = f.read()
            f.close()

            # generate mapsize code
            mapsize_asp = asp_map_size(10)

            # generate
            roomentry_asp = asp_room_entry(self.tmedit.tilemapwidget.tilemap, "qwe", 3)

            # call clingo process
            print clingo_spawn( mapsize_asp, roomentry_asp, generator_asp )


def main():
    app = App()
    app.run()

