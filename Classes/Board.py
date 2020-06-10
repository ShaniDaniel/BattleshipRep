from Classes.Cube import Cube
from Classes.Ship import Ship


class Board:

    def __init__(self, cube_start, cube_end):
        """takes the cubes that specify the start and the end of the board as parameters """
        try:
            assert (cube_start.x - cube_end.x) % Cube.length == 0 and (cube_start.y - cube_end.y) % Cube.length == 0
        except AssertionError:
            print("Invalid board coordinates")
        self.ships = [Ship(5, 5), Ship(4, 4), Ship(3, 3), Ship(2, 3), Ship(1, 2)]
        self.ship_pos = {}  # will contain the ship's cubes as a key and the ship_id it's associated with as a value
        self.cubes_not_shot = []  # a list of all the player's cubes, that will be updated to store the cubes that
        # were not shot
        self.cubes_availability = {}  # will contain the cubes on the board as keys, and 0 or 1 as values.
        # 0- cube's not available to place a ship on (already taken) ; 1- cube is available
        self.ship_shot = []  # a list of the ships cubes that were shot
        self.empty_shot = []  # a list of the cubes that were shot that are empty (not cubes of ships)
        self.start = cube_start
        self.end = cube_end
        self.cubes_list = self.get_board()

    def get_board(self):
        """creates a list of all the board's cubes"""
        board = []
        for x in range(self.start.x, self.end.x + 1, Cube.length):
            for y in range(self.start.y, self.end.y + 1, Cube.length):
                board.append(Cube(x, y))
        return board

    def __repr__(self):
        """prints the board as a list of all the board's cubes converted to string"""
        return str(self.cubes_list)

    @staticmethod
    def available_cubes_dict(player):
        """initializes the dictionary that has the player's board cubes as keys and 1 or 0 as value according to if the
             cube is available of placing ship on (1) or not (0)"""
        start_board = player.board.start
        end_board = player.board.end
        for x in range(start_board.x, end_board.x + 1, Cube.length):
            for y in range(start_board.y, end_board.y + 1, Cube.length):
                player.board.cubes_availability[(x, y)] = 1

    def insert_ship_pos(self, cube, ship_id):
        """Adds an item to the ship_pos dictionary"""
        self.ship_pos[cube] = ship_id

    def cubes_not_shot_list(self):
        """Initiates the cubes_not_shot list"""
        self.cubes_not_shot = list(self.cubes_list)
