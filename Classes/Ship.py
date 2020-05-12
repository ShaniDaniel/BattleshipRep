from Classes.Cube import Cube


class Ship:

    def __init__(self, player, _id, size):
        self._id = _id
        self.size = size
        self.player = player
        self.cube_start = None
        self.cube_end = None

    """Defines the position of the specific ship and adds it to the relevant dictionary accordingly"""
    def set_position(self, start, end):
        self.cube_start = start
        self.cube_end = end

        for x in range(start.x, end.x+1, Cube.length):
            for y in range(start.y, end.y+1, Cube.length):
                self.player.insert_ship_pos(Cube(x, y), self._id)  # adds the ship to the dictionary

    """m is a factor that is used to calculate the ship's needed space so it can be placed on the board and is used 
    by the place_ship functions later on"""
    def position_m(self):
        m = self.size - 1
        return m

    """checks if the ship has completely sank"""
    def is_ship_sank(self, player):
        count = 0
        for cube in player.board.ship_shot:
            if (cube.x, cube.y) in player.ships_place[self._id]:
                count += 1
        if count == self.size:
            return True
        else:
            return False
