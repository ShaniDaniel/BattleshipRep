from Classes.Cube import Cube
from Classes.GameManager import GameManager


class GameAgainstPlayer(GameManager):
    """places a ship with cube coordinates defined by the player, and checks if the ship is placed in a valid place,
    correct size and inside the board"""
    @staticmethod
    def place_ship(player, ship, ship_start, ship_end):
        not_available_cubes = []
        for key in player.board.cubes_availability:
            if player.board.cubes_availability[key] == 0:
                not_available_cubes.append(key)
        try:
            assert player.board.start.x <= ship_start.x <= player.board.end.x and \
                   player.board.start.y <= ship_start.y <= player.board.end.y
        except AssertionError:
            return "Can't place ship outside of board"
        if ship_start.x != ship_end.x and ship_start.y != ship_end.y:
            return "Invalid ship coordinates. Ship must be placed horizontally or vertically."
        elif ship_start.x == ship_end.x or ship_start.y == ship_end.y:
            if (max(ship_start.y, ship_end.y) - min(ship_start.y, ship_end.y)) / Cube.length > ship.size - 1 or \
                    (max(ship_start.x, ship_end.x) - min(ship_start.x, ship_end.x)) / Cube.length > ship.size - 1:
                return "Ship is too long! must be %d cubes long." % ship.size
            elif (max(ship_start.y, ship_end.y) - min(ship_start.y, ship_end.y)) / Cube.length < ship.size - 1 and \
                    (max(ship_start.x, ship_end.x) - min(ship_start.x, ship_end.x)) / Cube.length < ship.size - 1:
                return "Ship is too short! must be %d cubes long." % ship.size
        for x in range(min(ship_start.x, ship_end.x), max(ship_start.x, ship_end.x) + 1, Cube.length):
            for y in range(min(ship_start.y, ship_end.y), max(ship_start.y, ship_end.y) + 1, Cube.length):
                if (x, y) in not_available_cubes:
                    return "Can't place ship on top or next to another ship."
        else:
            GameManager.place_ship(player, ship, Cube(min(ship_start.x, ship_end.x), min(ship_start.y, ship_end.y)),
                                   Cube(max(ship_start.x, ship_end.x), max(ship_start.y, ship_end.y)))
            ship.set_position(Cube(min(ship_start.x, ship_end.x), min(ship_start.y, ship_end.y)),
                              Cube(max(ship_start.x, ship_end.x), max(ship_start.y, ship_end.y)))
            for x in range(min(ship_start.x, ship_end.x) - Cube.length,
                           max(ship_start.x, ship_end.x) + Cube.length + 1, Cube.length):
                for y in range(min(ship_start.y, ship_end.y) - Cube.length,
                               max(ship_start.y, ship_end.y) + Cube.length + 1, Cube.length):
                    if (x, y) in player.board.cubes_availability:
                        player.board.cubes_availability[(x, y)] = 0
