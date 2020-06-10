from Classes.Cube import Cube
from Classes.Ship import Ship


class Player:

    def __init__(self, username):
        self.username = username
        self.board = None

    def check_if_lost(self):
        count = 0
        for ship in self.board.ships:
            count += ship.is_ship_sunk(self)
        return count == len(self.board.ships)
