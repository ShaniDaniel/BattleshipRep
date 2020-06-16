from Classes.Square import Square


class Ship:

    def __init__(self, _id, size):
        self.id = _id
        self.size = size
        self.m_factor = self.size - 1
        # m is a factor that is used to calculate the ship's needed space so it can be placed on the board and is used
        # by the place_ship functions later on
        self.square_start = None
        self.square_end = None
        self.start_x = None
        self.end_x = None
        self.start_y = None
        self.end_y = None

    """Defines the position of the specific ship and adds it to the relevant dictionary accordingly"""
    def set_position(self, player, start, end):
        self.square_start = start
        self.square_end = end
        self.start_x = min(start.x, end.x)
        self.end_x = max(start.x, end.x)
        self.start_y = min(start.y, end.y)
        self.end_y = max(start.y, end.y)

        for x in range(start.x, end.x+1, Square.length):
            for y in range(start.y, end.y+1, Square.length):
                for square in player.board.squares_list:
                    if square.x == x and square.y == y:
                        player.board.insert_ship_pos(square, self.id)  # adds the ship to the dictionary

    def del_ship(self, player):
        temp = []
        for square in player.board.ship_pos:
            if player.board.ship_pos[square] == self.id:
                temp.append(square)
        for item in temp:
            del player.board.ship_pos[item]
        for x in range(self.start_x - Square.length, self.end_x + Square.length + 1, Square.length):
            for y in range(self.start_y - Square.length, self.end_y + Square.length + 1, Square.length):
                if (x, y) in player.board.squares_availability:
                    player.board.squares_availability[(x, y)] = 1
        self.square_start = None
        self.square_end = None

    def is_ship_sunk(self, player):
        """checks if the ship has completely sank"""
        count = 0
        temp = []
        for square in player.board.ship_pos:
            if player.board.ship_pos[square] == self.id:
                temp.append((square.x, square.y))
        for shot_square in player.board.ship_shot:
            if (shot_square.x, shot_square.y) in temp:
                count += 1
        if count == self.size:
            return True
        else:
            return False
