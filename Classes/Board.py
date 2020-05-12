from Classes.Cube import Cube


class Board:

    """takes the cubes that specify the start and the end of the board as parameters """
    def __init__(self, cube_start, cube_end):
        self.cubes_availability = {}  # will contain the cubes on the board as keys, and 0 or 1 as values.
        # 0- cube's not available to place a ship on (already taken) ; 1- cube is available
        self.ship_shot = []  # a list of the ships cubes that were shot
        self.empty_shot = []  # a list of the cubes that were shot that are empty (not cubes of ships)
        self.start = cube_start
        self.end = cube_end

    """prints the board as a list of all the board's cubes converted to string"""
    def __repr__(self):
        board = []
        for x in range(self.start.x, self.end.x+1, Cube.length):
            for y in range(self.start.y, self.end.y+1, Cube.length):
                board.append([x, y])
        return str(board)

    """creates a list of all the board's cubes"""
    def get_board(self):
        board = []
        for x in range(self.start.x, self.end.x + 1, Cube.length):
            for y in range(self.start.y, self.end.y + 1, Cube.length):
                board.append(Cube(x, y))
        return board

    """initializes the dictionary that has the player's board cubes as keys and 1 or 0 as value according to if the
     cube is available of placing ship on (1) or not (0)"""
    @staticmethod
    def available_cubes_dict(player, start_board, end_board):
        for x in range(start_board.x, end_board.x, Cube.length):
            for y in range(start_board.y, end_board.y, Cube.length):
                player.board.cubes_availability[(x, y)] = 1
