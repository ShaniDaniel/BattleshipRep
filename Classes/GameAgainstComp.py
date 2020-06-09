import random
from Classes.GameManager import GameManager
from Classes.Cube import Cube


class GameAgainstComp(GameManager):

    @staticmethod
    def rand_place_ships(player):
        """randomly places the ship on the opponent's board"""
        try_again = True
        while try_again is True:
            player.board.available_cubes_dict(player)
            player.ships_place = {}
            player.ship_pos = {}
            temp = 0
            for ship in player.ships:
                not_done = True  # used to create the loop that searches for a valid and available ship's coordinates
                ship_start = ship_end = Cube(0, 0)  # initializes the ship's start and end cubes that will be randomized
                # inside the loop
                m = ship.m_factor
                # the factor that's used to check if the ship's end will not exceed the board
                available_cubes = []  # all the cubes that are available to place a ship on
                not_available_cubes = []  # all the cubes that are not available to place a ship on
                for key in player.board.cubes_availability:
                    if player.board.cubes_availability[key] == 1:
                        available_cubes.append(Cube(key[0], key[1]))  # adds the relevant cubes to the
                        # available_cubes list
                    elif player.board.cubes_availability[key] == 0:
                        not_available_cubes.append(key)  # adds the relevant cubes to the not_available_cubes list
                while not_done:  # loops to search for an available place to place the ship
                    check = []
                    ship_start = random.choice(available_cubes)  # randomly chooses the ship's start from the
                    # available cubes
                    temp += 1

                    def is_valid(value, axis):
                        return player.board.start.x + m * Cube.length <= value <= player.board.end.x - \
                            m * Cube.length

                    if is_valid(ship_start.x, axis='x'):
                        ship_end.x = random.choice(
                            [ship_start.x - m * Cube.length, ship_start.x, ship_start.x + m * Cube.length])
                    elif player.board.start.x + m * Cube.length <= ship_start.x:
                        ship_end.x = random.choice([ship_start.x - m * Cube.length, ship_start.x])
                    else:
                        ship_end.x = random.choice([ship_start.x, ship_start.x + m * Cube.length])
                    # checks where the ship has enough place to be placed horizontally (if it's too close to the left
                    # or the right of the board) and chooses the ship's end accordingly

                    if ship_start.x != ship_end.x:
                        ship_end.y = ship_start.y
                    else:
                        if player.board.start.y + m * Cube.length <= ship_start.y <= player.board.end.y - m * Cube.length:
                            ship_end.y = random.choice([ship_start.y - m * Cube.length, ship_start.y + m * Cube.length])
                        elif player.board.start.y + m * Cube.length <= ship_start.y:
                            ship_end.y = ship_start.y - m * Cube.length
                        else:
                            ship_end.y = ship_start.y + m * Cube.length
                    # checks where the ship has enough place to be placed vertically (if it's too close to the start
                    # or the bottom of the board) and chooses the ship's end accordingly

                    for x in range(min(ship_start.x, ship_end.x),
                                   max(ship_start.x, ship_end.x) + 1, Cube.length):
                        for y in range(min(ship_start.y, ship_end.y),
                                       max(ship_start.y, ship_end.y) + 1, Cube.length):
                            if (x, y) in not_available_cubes:
                                check.append('no')
                    if len(check) == 0:
                        not_done = False  # stops the loop if all the coordinates are available
                    # checks if the chosen ship coordinate's is available and not placed on or next to another ship
                        try_again = False
                    elif temp > 500:
                        not_done = False
                        try_again = True

                ship.set_position(Cube(min(ship_start.x, ship_end.x), min(ship_start.y, ship_end.y)),
                                  Cube(max(ship_start.x, ship_end.x), max(ship_start.y, ship_end.y)))
                # calls the set_position method to save the ship's coordinates accordingly
                for x in range(min(ship_start.x, ship_end.x) - Cube.length,
                               max(ship_start.x, ship_end.x) + Cube.length + 1, Cube.length):
                    for y in range(min(ship_start.y, ship_end.y) - Cube.length,
                                   max(ship_start.y, ship_end.y) + Cube.length + 1, Cube.length):
                        if (x, y) in player.board.cubes_availability:
                            player.board.cubes_availability[(x, y)] = 0
                            # updates the dictionary that the chosen cubes and the cubes next to them are not available.

    @staticmethod
    def rand_shoot(player):
        """randomly shoots a cube on the player's board"""
        target = 0
        for ship in player.ships:
            temp = []
            if not ship.is_ship_sunk(player):
                for x in player.ship_pos:
                    if player.ship_pos[x] == ship.id:
                        temp.append(x)
            for cube in temp:
                if cube in player.board.ship_shot:
                    for pos in temp:
                        if pos not in player.board.ship_shot:
                            target = pos
                            GameManager.shoot(player, target)  # shoots it with the shoot method
                            break
                    break
        if target == 0:
            target = random.choice(player.cubes_not_shot)  # randomly chooses a cube from the cubes that were not shot
            GameManager.shoot(player, target)  # shoots it with the shoot method

        return target
