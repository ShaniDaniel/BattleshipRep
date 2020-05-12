from Classes.Cube import Cube


class Player:

    def __init__(self, username):
        self.ships_place = {}  # will contain the ship_id as key and a list of the ship's coordinates as value
        self.ship_pos = {}  # will contain the ship's cubes as a key and the ship_id it's associated with as a value
        self.cubes_not_shot = []  # a list of all the player's cubes, that will be updated to store the cubes that
        # were not shot
        self.username = username
        self.board = None

    """Adds an item to the ship_pos dictionary"""
    def insert_ship_pos(self, cube, ship_id):
        self.ship_pos[cube] = ship_id

    """Initiates the cubes_not_shot list"""
    def cubes_not_shot_list(self, start_board, end_board):
        for x in range(start_board.x, end_board.x+1, Cube.length):
            for y in range(start_board.y, end_board.y+1, Cube.length):
                self.cubes_not_shot.append(Cube(x, y))
