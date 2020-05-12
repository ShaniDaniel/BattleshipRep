from Classes.Cube import Cube
from Classes.Player import Player


class GameManager:

    """defines the place of the ship on the board by it's cube's coordinates"""
    @staticmethod
    def place_ship(player, ship, cube_start, cube_end):
        ships_temp = []  # saves current ship's place
        for x in range(cube_start.x, cube_end.x + 1, Cube.length):
            for y in range(cube_start.y, cube_end.y + 1, Cube.length):
                ships_temp.append((x, y))  # saves the current ship's place
        player.ships_place[ship._id] = ships_temp  # adds the ship's ID and place to the ships_place dictionary

    """takes the player that it's board is being shot at and the target cube as parameters"""
    @staticmethod
    def shoot(player, target):
        if player.board.start.x <= target.x <= player.board.end.x and player.board.start.y <= target.y <=\
                player.board.end.y:  # checks if the target is inside the board
            is_not_shot = False
            for cube in player.cubes_not_shot:  # checks if the target was not shot yet
                if cube.x == target.x and cube.y == target.y:
                    is_not_shot = True
                    player.cubes_not_shot.remove(cube)
            if is_not_shot is True:
                for cube in player.ship_pos:  # checks if a ship was shot
                    if cube.x == target.x and cube.y == target.y:
                        player.board.ship_shot.append(cube)  # if a ship was shot, adds the cube to the ship_shot list
                        break
                else:
                    player.board.empty_shot.append([target.x, target.y])  # if an empty cube was shot,
                    # adds it to the empty_shot list
            elif is_not_shot is False:
                return "You already shot that place."
        else:
            return "Outside of board"
