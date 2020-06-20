class GameManager:

    @staticmethod
    def is_not_shot(player, target):
        for square in player.board.squares_not_shot:  # checks if the target was not shot yet
            if square.x == target.x and square.y == target.y:
                player.board.squares_not_shot.remove(square)
                return True
        return False

    @staticmethod
    def shoot(player, target):
        """takes the player that it's board is being shot at and the target square as parameters"""
        if player.board.start.x <= target.x <= player.board.end.x and player.board.start.y <= target.y <=\
                player.board.end.y:  # checks if the target is inside the board
            is_not_shot = GameManager.is_not_shot(player, target)
            if is_not_shot:
                for square in player.board.ship_pos:  # checks if a ship was shot
                    if square.x == target.x and square.y == target.y:
                        player.board.ship_shot.append(square)
                        # if a ship was shot, adds the square to the ship_shot list
                        return "success"
                else:
                    player.board.empty_shot.append(target)  # if an empty square was shot,
                    # adds it to the empty_shot list
                    return "success"
            else:  # if the same square was shot already
                return "You already shot that place."
        else:
            return "Outside of board"
