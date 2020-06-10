from Classes.Cube import Cube


class Ship:

    def __init__(self, _id, size):
        self.id = _id
        self.size = size
        self.m_factor = self.size - 1
        # m is a factor that is used to calculate the ship's needed space so it can be placed on the board and is used
        # by the place_ship functions later on
        self.cube_start = None
        self.cube_end = None
        self.start_x = None
        self.end_x = None
        self.start_y = None
        self.end_y = None

    """Defines the position of the specific ship and adds it to the relevant dictionary accordingly"""
    def set_position(self, player, start, end):
        self.cube_start = start
        self.cube_end = end
        self.start_x = min(start.x, end.x)
        self.end_x = max(start.x, end.x)
        self.start_y = min(start.y, end.y)
        self.end_y = max(start.y, end.y)

        for x in range(start.x, end.x+1, Cube.length):
            for y in range(start.y, end.y+1, Cube.length):
                for cube in player.board.cubes_list:
                    if cube.x == x and cube.y == y:
                        player.board.insert_ship_pos(cube, self.id)  # adds the ship to the dictionary

    def del_ship(self, player):
        temp = []
        for cube in player.board.ship_pos:
            if player.board.ship_pos[cube] == self.id:
                temp.append(cube)
        for item in temp:
            del player.board.ship_pos[item]
        for x in range(self.start_x - Cube.length, self.end_x + Cube.length + 1, Cube.length):
            for y in range(self.start_y - Cube.length, self.end_y + Cube.length + 1, Cube.length):
                if (x, y) in player.board.cubes_availability:
                    player.board.cubes_availability[(x, y)] = 1
        self.cube_start = None
        self.cube_end = None

    def is_ship_sunk(self, player):
        """checks if the ship has completely sank"""
        count = 0
        temp = []
        for cube in player.board.ship_pos:
            if player.board.ship_pos[cube] == self.id:
                temp.append((cube.x, cube.y))
        for shot_cube in player.board.ship_shot:
            if (shot_cube.x, shot_cube.y) in temp:
                count += 1
        if count == self.size:
            return True
        else:
            return False
