from Classes.Cube import Cube


class Ship:

    def __init__(self, player, _id, size):
        self.id = _id
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
                for cube in self.player.board.cubes_list:
                    if cube.x == x and cube.y == y:
                        self.player.insert_ship_pos(cube, self.id)  # adds the ship to the dictionary

    def del_ship(self):
        temp = []
        for cube in self.player.ship_pos:
            if self.player.ship_pos[cube] == self.id:
                temp.append(cube)
        for item in temp:
            del self.player.ship_pos[item]
        for x in range(min(self.cube_start.x, self.cube_end.x) - Cube.length,
                       max(self.cube_start.x, self.cube_end.x) + Cube.length + 1, Cube.length):
            for y in range(min(self.cube_start.y, self.cube_end.y) - Cube.length,
                           max(self.cube_start.y, self.cube_end.y) + Cube.length + 1, Cube.length):
                if (x, y) in self.player.board.cubes_availability:
                    self.player.board.cubes_availability[(x, y)] = 1
        self.cube_start = None
        self.cube_end = None

    """m is a factor that is used to calculate the ship's needed space so it can be placed on the board and is used 
    by the place_ship functions later on"""
    def position_m(self):
        m = self.size - 1
        return m

    def is_ship_sank(self, player):
        """checks if the ship has completely sank"""
        count = 0
        temp = []
        for cube in player.ship_pos:
            if player.ship_pos[cube] == self.id:
                temp.append((cube.x, cube.y))
        for shot_cube in player.board.ship_shot:
            if (shot_cube.x, shot_cube.y) in temp:
                count += 1
        if count == self.size:
            return True
        else:
            return False
