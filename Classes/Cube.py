class Cube:
    length = None

    def __init__(self, x_coordinate, y_coordinate):
        self.x = x_coordinate
        self.y = y_coordinate

    def __repr__(self):
        return str((self.x, self.y))
