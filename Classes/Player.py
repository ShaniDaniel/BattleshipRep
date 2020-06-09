from Classes.Cube import Cube
from Classes.Ship import Ship


class Player:

    def __init__(self, username):
        self.ship_pos = {}  # will contain the ship's cubes as a key and the ship_id it's associated with as a value
        self.cubes_not_shot = []  # a list of all the player's cubes, that will be updated to store the cubes that
        # were not shot
        self.username = username
        self.board = None
        self.ships = [Ship(self, 5, 5), Ship(self, 4, 4), Ship(self, 3, 3), Ship(self, 2, 3), Ship(self, 1, 2)]

    def insert_ship_pos(self, cube, ship_id):
        """Adds an item to the ship_pos dictionary"""
        self.ship_pos[cube] = ship_id

    def cubes_not_shot_list(self):
        """Initiates the cubes_not_shot list"""
        self.cubes_not_shot = list(self.board.cubes_list)

    def check_if_lost(self):
        count = 0
        for ship in self.ships:
            count += ship.is_ship_sunk(self)
        return count == len(self.ships)

