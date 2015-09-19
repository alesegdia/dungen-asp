import sys

from dungenasp.maputil.tilemap import Tilemap
from dungenasp.parselp import build_data

def raster_chunk(tm, chunk):
	for y in range(0, int(chunk[3])):
		for x in range(0, int(chunk[2])):
			tm.tilemap[int(chunk[1])+y][int(chunk[0])+x] = 1

def build_map(parsestr):
	print(parsestr)
	data = build_data(parsestr)
	sz = (data['size'][0].split(','))
	tm = Tilemap(int(sz[0])+10, int(sz[1])+10)

	for c in data['chunk']:
		chunk = c.split(',')
		raster_chunk(tm, chunk)
	printit(tm)

def printit(tm):
	for y in range(0,len(tm.tilemap)):
		s = ''
		for x in range(0,len(tm.tilemap[y])):
			s = s + str(tm.tilemap[y][x]) + " "

		print(s)


def main():
	build_map(raw_input())


if __name__ == '__main__':
	main()
