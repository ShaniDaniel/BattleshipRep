from Classes.Square import Square
from Classes.GameManager import GameManager


class GameAgainstPlayer(GameManager):

    @staticmethod
    def place_ship(player, ship, ship_start, ship_end):
        """places a ship with square coordinates defined by the player,
         and checks if the ship is placed in a valid place, correct size and inside the board"""
        ship_start_x = min(ship_start.x, ship_end.x)
        ship_end_x = max(ship_start.x, ship_end.x)
        ship_start_y = min(ship_start.y, ship_end.y)
        ship_end_y = max(ship_start.y, ship_end.y)
        not_available_squares = []
        for key in player.board.squares_availability:
            if player.board.squares_availability[key] == 0:
                not_available_squares.append(key)
        try:
            assert player.board.start.x <= ship_start.x <= player.board.end.x and \
                   player.board.start.y <= ship_start.y <= player.board.end.y
        except AssertionError:
            return "Can't place ship outside of board"
        if ship_start.x != ship_end.x and ship_start.y != ship_end.y:
            return "Invalid ship coordinates. Ship must be placed horizontally or vertically."
        elif ship_start.x == ship_end.x or ship_start.y == ship_end.y:
            if (ship_end_y - ship_start_y) / Square.length > ship.size - 1 or \
                    (ship_end_x - ship_start_x) / Square.length > ship.size - 1:
                return "Ship is too long! must be %d squares long." % ship.size
            elif (ship_end_y - ship_start_y) / Square.length < ship.size - 1 and \
                    (ship_end_x - ship_start_x) / Square.length < ship.size - 1:
                return "Ship is too short! must be %d squares long." % ship.size
        for x in range(ship_start_x, ship_end_x + 1, Square.length):
            for y in range(ship_start_y, ship_end_y + 1, Square.length):
                if (x, y) in not_available_squares:
                    return "Can't place ship on top or next to another ship."
        else:
            ship.set_position(player, Square(ship_start_x, ship_start_y),
                              Square(ship_end_x, ship_end_y))
            for x in range(ship_start_x - Square.length,
                           ship_end_x + Square.length + 1, Square.length):
                for y in range(ship_start_y - Square.length,
                               ship_end_y + Square.length + 1, Square.length):
                    if (x, y) in player.board.squares_availability:
                        player.board.squares_availability[(x, y)] = 0
            return "success"
