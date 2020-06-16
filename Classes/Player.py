from Classes.Square import Square
from Classes.Board import Board


class Player:

    def __init__(self, username):
        self.username = username
        self.board = None

    def check_if_lost(self):
        count = 0
        for ship in self.board.ships:
            count += ship.is_ship_sunk(self)
        return count == len(self.board.ships)

    def set_board(self, player_num):
        if player_num == 1:
            self.board = Board(Square(20, 100), Square(380, 460))
        elif player_num == 2:
            self.board = Board(Square(460, 100), Square(820, 460))
        self.board.squares_not_shot_list()
        self.board.available_squares_dict(self)

