import random
from Classes.GameManager import GameManager
from Classes.Square import Square


class GameAgainstComp(GameManager):

    @staticmethod
    def rand_place_ships(player):
        """randomly places the ship on the opponent's board"""
        try_again = True
        ship_start_x = None
        ship_end_x = None
        ship_start_y = None
        ship_end_y = None
        while try_again is True:
            player.board.available_squares_dict(player)
            player.board.ship_pos = {}
            temp = 0
            for ship in player.board.ships:
                not_done = True  # used to create the loop that searches for a valid and available ship's coordinates
                ship_end = Square(0, 0)
                # initializes the ship's end square that will be randomized inside the loop
                m = ship.m_factor
                # the factor that's used to check if the ship's end will not exceed the board
                available_squares = []  # all the squares that are available to place a ship on
                not_available_squares = []  # all the squares that are not available to place a ship on
                for key in player.board.squares_availability:
                    if player.board.squares_availability[key] == 1:
                        available_squares.append(Square(key[0], key[1]))  # adds the relevant squares to the
                        # available_squares list
                    elif player.board.squares_availability[key] == 0:
                        not_available_squares.append(key)  # adds the relevant squares to the not_available_squares list
                while not_done:  # loops to search for an available place to place the ship
                    check = []
                    ship_start = random.choice(available_squares)  # randomly chooses the ship's start from the
                    # available squares
                    temp += 1

                    def is_valid(value, axis):
                        if axis == 'x':
                            return player.board.start.x + m * Square.length <= value <= player.board.end.x - \
                                m * Square.length
                        elif axis == 'y':
                            return player.board.start.y + m * Square.length <= value <= player.board.end.y - \
                                   m * Square.length

                    if is_valid(ship_start.x, axis='x'):
                        ship_end.x = random.choice(
                            [ship_start.x - m * Square.length, ship_start.x, ship_start.x + m * Square.length])
                    elif player.board.start.x + m * Square.length <= ship_start.x:
                        ship_end.x = random.choice([ship_start.x - m * Square.length, ship_start.x])
                    else:
                        ship_end.x = random.choice([ship_start.x, ship_start.x + m * Square.length])
                    # checks where the ship has enough place to be placed horizontally (if it's too close to the left
                    # or the right of the board) and chooses the ship's end accordingly

                    if ship_start.x != ship_end.x:
                        ship_end.y = ship_start.y
                    else:
                        if is_valid(ship_start.y, axis='y'):
                            ship_end.y = random.choice([ship_start.y - m * Square.length,
                                                        ship_start.y + m * Square.length])
                        elif player.board.start.y + m * Square.length <= ship_start.y:
                            ship_end.y = ship_start.y - m * Square.length
                        else:
                            ship_end.y = ship_start.y + m * Square.length
                    # checks where the ship has enough place to be placed vertically (if it's too close to the start
                    # or the bottom of the board) and chooses the ship's end accordingly

                    ship_start_x = min(ship_start.x, ship_end.x)
                    ship_end_x = max(ship_start.x, ship_end.x)
                    ship_start_y = min(ship_start.y, ship_end.y)
                    ship_end_y = max(ship_start.y, ship_end.y)

                    for x in range(ship_start_x,
                                   ship_end_x + 1, Square.length):
                        for y in range(ship_start_y,
                                       ship_end_y + 1, Square.length):
                            if (x, y) in not_available_squares:
                                check.append('no')
                    if len(check) == 0:
                        not_done = False  # stops the loop if all the coordinates are available
                    # checks if the chosen ship coordinate's is available and not placed on or next to another ship
                        try_again = False
                    elif temp > 500:
                        not_done = False
                        try_again = True

                ship.set_position(player, Square(ship_start_x, ship_start_y),
                                  Square(ship_end_x, ship_end_y))
                # calls the set_position method to save the ship's coordinates accordingly
                for x in range(ship_start_x - Square.length,
                               ship_end_x + Square.length + 1, Square.length):
                    for y in range(ship_start_y - Square.length,
                                   ship_end_y + Square.length + 1, Square.length):
                        if (x, y) in player.board.squares_availability:
                            player.board.squares_availability[(x, y)] = 0
                            # updates the dictionary that the chosen squares and the squares next to them
                            # are not available.

    @staticmethod
    def rand_shoot(player):
        """randomly shoots a square on the player's board"""
        target = 0
        for ship in player.board.ships:
            temp = []
            if not ship.is_ship_sunk(player):
                for x in player.board.ship_pos:
                    if player.board.ship_pos[x] == ship.id:
                        temp.append(x)
            for square in temp:
                if square in player.board.ship_shot:
                    for pos in temp:
                        if pos not in player.board.ship_shot:
                            target = pos
                            GameManager.shoot(player, target)  # shoots it with the shoot method
                            break
                    break
        if target == 0:
            target = random.choice(player.board.squares_not_shot)
            # randomly chooses a square from the squares that were not shot
            GameManager.shoot(player, target)  # shoots it with the shoot method

        return target
