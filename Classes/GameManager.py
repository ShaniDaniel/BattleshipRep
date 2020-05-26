from Classes.Cube import Cube


class GameManager:

    @staticmethod
    def shoot(player, target):
        """takes the player that it's board is being shot at and the target cube as parameters"""
        if player.board.start.x <= target.x <= player.board.end.x and player.board.start.y <= target.y <=\
                player.board.end.y:  # checks if the target is inside the board
            is_not_shot = False
            for cube in player.cubes_not_shot:  # checks if the target was not shot yet
                if cube.x == target.x and cube.y == target.y:
                    is_not_shot = True
                    player.cubes_not_shot.remove(cube)
                    break
            if is_not_shot is True:
                for cube in player.ship_pos:  # checks if a ship was shot
                    if cube.x == target.x and cube.y == target.y:
                        player.board.ship_shot.append(cube)  # if a ship was shot, adds the cube to the ship_shot list
                        return "success"
                else:
                    player.board.empty_shot.append(target)  # if an empty cube was shot,
                    # adds it to the empty_shot list
                    return "success"
            elif is_not_shot is False:
                return "You already shot that place."
        else:
            return "Outside of board"

