
''' Generates all ASP code needed for a room and the number of instances
	of it for a specific map generation instance '''
def asp_room_entry(tilemap, name, count):
	roomasp = RoomModelASP(tilemap, name).generate()
	sizeasp = asp_room_count(name, count)
	return roomasp + "\n" + sizeasp

class RoomModelASP:
	def __init__(self, tilemap, name):
		self.tilemap = tilemap
		self.name = name

	''' generates ASP code for a room model '''
	def generate(self):
		self.numtiles = 0
		self.tiles = []

		# capture all solid tiles
		self.tilemap.foreach(self.parse_tile)

		self.generate_tiles_asp()
		self.generate_tiles_dim()

		prefix = "{0} {{ figure(F),\n".format(len(self.tiles)+1, self.name)
		postfix = " }} {0} :- {1}(F,X,Y).\n\n".format(len(self.tiles)+1, self.name)

		definition = prefix + \
					 ''.join(self.tileasp) + \
					 ''.join(self.tiledim) + \
					 postfix

		return definition

	def parse_tile(self, x, y, tile):
		if tile != 0:
			self.tiles.append({'x':x, 'y':y})
	
	def generate_tiles_asp(self):
		# generate asp definitions for each tile
		self.tileasp = [ "tile(F,X+{1},Y+{2}),\n" \
				.format(self.name, e["x"], e["y"]) for e in self.tiles ] 
		self.tileasp[-1] = self.tileasp[-1][:-2] + "\n"
	
	def generate_tiles_dim(self):
		# generate dimensions for tiles
		self.tiledim = [ [ \
				": dim(X+{0}) ".format(e["x"]), \
				": dim(Y+{0}) ".format(e["y"])  \
				] for e in self.tiles ]
		self.tiledim = list(set([item for sublist in self.tiledim for item in sublist]))


''' generate ASP code to set a number of rooms for a specific
	room model called roomname'''
def asp_room_count(name, count):
	strr = "exist_{0}(N-1) :- exist_{0}(N), N != 1.\n" + \
		   "1 {{ {0}(N,X,Y) : dim(X) : dim(Y) }} 1 :- exist_{0}(N).\n\n" + \
		   "exist_{0}({1})."
	return strr.format(name, count)

''' generates ASP code to set a generated map size'''
def asp_map_size(mapsize):
	return ("#const width = {0}.\n" + \
		    "dim(1..width).\n").format(mapsize)

