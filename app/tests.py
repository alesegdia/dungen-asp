
from tilemap import Tilemap
from aspgen import RoomModelASP, asp_room_entry

tm = Tilemap(10,10)
tm.tilemap[0][2] = 1
tm.tilemap[2][4] = 1
tm.tilemap[2][5] = 1
tm.tilemap[4][6] = 1
tm.tilemap[5][6] = 1

print(asp_room_entry(tm, "qweqwe", 10))
