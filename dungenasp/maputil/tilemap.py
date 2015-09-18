

class Tilemap:
    def __init__(self,w,h):
        self.tilemap = []
        for y in range( 0, h ):
            self.tilemap.append( [0] * w )

    def foreach(self, f):
        for y in range(0,len(self.tilemap)):
            for x in range(0,len(self.tilemap[y])):
                f( x, y, self.tilemap[y][x] )

    def w(self):
        return len(self.tilemap[0])

    def h(self):
        return len(self.tilemap)
