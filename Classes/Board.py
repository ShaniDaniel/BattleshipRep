from Classes.Square import Square
from Classes.Ship import Ship


class Board:

    def __init__(self, square_start, square_end):
        """takes the squares that specify the start and the end of the board as parameters """
        try:
            assert (square_start.x - square_end.x) % Square.length == 0 and (square_start.y - square_end.y)\
                   % Square.length == 0
        except AssertionError:
            print("Invalid board coordinates")
        self.ships = [Ship(5, 5), Ship(4, 4), Ship(3, 3), Ship(2, 3), Ship(1, 2)]
        self.ship_pos = {}  # will contain the ship's squares as a key and the ship_id it's associated with as a value
        self.squares_not_shot = []  # a list of all the player's squares, that will be updated to store the squares that
        # were not shot
        self.squares_availability = {}  # will contain the squares on the board as keys, and 0 or 1 as values.
        # 0- square's not available to place a ship on (already taken) ; 1- square is available
        self.ship_shot = []  # a list of the ships squares that were shot
        self.empty_shot = []  # a list of the squares that were shot that are empty (not squares of ships)
        self.start = square_start
        self.end = square_end
        self.squares_list = self.get_board()

    def get_board(self):
        """creates a list of all the board's squares"""
        board = []
        for x in range(self.start.x, self.end.x + 1, Square.length):
            for y in range(self.start.y, self.end.y + 1, Square.length):
                board.append(Square(x, y))
        return board

    def __repr__(self):
        """prints the board as a list of all the board's squares converted to string"""
        return str(self.squares_list)

    @staticmethod
    def available_squares_dict(player):
        """initializes the dictionary that has the player's board squares as keys and 1 or 0 as value according to if
         the square is available of placing ship on (1) or not (0)"""
        start_board = player.board.start
        end_board = player.board.end
        for x in range(start_board.x, end_board.x + 1, Square.length):
            for y in range(start_board.y, end_board.y + 1, Square.length):
                player.board.squares_availability[(x, y)] = 1

    def insert_ship_pos(self, square, ship_id):
        """Adds an item to the ship_pos dictionary"""
        self.ship_pos[square] = ship_id

    def squares_not_shot_list(self):
        """Initiates the squares_not_shot list"""
        self.squares_not_shot = list(self.squares_list)
