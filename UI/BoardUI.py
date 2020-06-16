import pygame
import Constants

from Classes.Square import Square
from Classes.GameAgainstPlayer import GameAgainstPlayer
from Classes.GameManager import GameManager
from UI.TextUI import TextUI


class BoardUI:

    color_index = {"blue": (0, 0, 255), "red": (255, 0, 0), "grey": (210, 210, 210), "orange": (252, 168, 78),
                   "light blue": (173, 216, 230), "white": (255, 255, 255)}
    # a dictionary of different useful colors for the game by their rgb values

    @staticmethod
    def draw_board(screen, board):
        """draws the board"""
        for x in range(board.start.x, board.end.x + Square.length, Square.length):
            for y in range(board.start.y,  board.end.y + Square.length, Square.length):
                pygame.draw.rect(screen, BoardUI.color_index["white"],
                                 pygame.Rect(x, y, Square.length - 1, Square.length - 1))

    @staticmethod
    def get_squares_position(player, position):
        #  gets each squares position to locate if the player pressed a square and which one
        for square in player.board.squares_list:
            if square.x <= position[0] <= square.x + Square.length - 1 and square.y <= position[1] \
                    <= square.y + Square.length - 1:
                return square

    @staticmethod
    def draw_x(screen, square):
        padding_value = Constants.SHAPES_PADDING
        """draws an "X" sign on the square"""
        pygame.draw.line(screen, Constants.BLACK, (square.x + padding_value, square.y + padding_value),
                         (square.x + Square.length - padding_value, square.y + (Square.length - padding_value)),
                         padding_value)
        pygame.draw.line(screen, Constants.BLACK, (square.x + padding_value, square.y + (Square.length-padding_value)),
                         (square.x + (Square.length - padding_value), square.y + padding_value), padding_value)
     
    @staticmethod
    def color_square(screen, square, color):
        """colors a square a certain color"""
        try:
            pygame.draw.rect(screen, color, pygame.Rect(square.x, square.y, Square.length - 1, Square.length - 1))
        except AttributeError:
            pass

    @staticmethod
    def color_ship(screen, ship, color):
        """colors a whole ship a certain color"""
        for x in range(ship.start_x, ship.end_x + 1, Square.length):
            for y in range(ship.start_y, ship.end_y + 1, Square.length):
                BoardUI.color_square(screen, Square(x, y), color)
                
    @staticmethod
    def place_ships(screen, player, pos):
        """places the user's ship py his given squares and colors these ships blue"""
        for ship in player.board.ships:
            if ship.square_end is not None:
                continue
            if ship.square_start is None:
                ship.square_start = BoardUI.get_squares_position(player, pos)
                BoardUI.color_square(screen, ship.square_start, BoardUI.color_index["blue"])
                break
            elif ship.square_end is None and BoardUI.get_squares_position(player, pos) is not None:
                ship.square_end = BoardUI.get_squares_position(player, pos)
                ship_check = GameAgainstPlayer.place_ship(player, ship, ship.square_start, ship.square_end)
                if ship_check != "success":
                    TextUI.clear_title(screen, Constants.BOTTOM_LINE)
                    TextUI.write_title(screen, ship_check, Constants.BOTTOM_LINE)
                    BoardUI.color_square(screen, ship.square_start, BoardUI.color_index["white"])
                    ship.square_start = None
                    ship.square_end = None
                    break
                else:
                    TextUI.clear_title(screen, Constants.BOTTOM_LINE)
                    BoardUI.color_ship(screen, ship, BoardUI.color_index["blue"])
                    return ship
            else:
                BoardUI.color_square(screen, ship.square_start, BoardUI.color_index["white"])
                ship.square_start = None
                ship.square_end = None
                break

    @staticmethod         
    def del_ship(screen, ship, player):
        """deletes a ship from the screen and calls the del_ship function to delete its information"""
        BoardUI.color_ship(screen, ship, BoardUI.color_index["white"])
        ship.del_ship(player)
        
    @staticmethod
    def shoot(screen, player, pos):
        """shoots the given square by calling the "shoot" function and coloring the square red if it contains a ship,
         and draws an X if it doesn't"""
        square_pos = BoardUI.get_squares_position(player, pos)
        game_shoot = GameManager.shoot(player, square_pos)
        if game_shoot == "success":
            if square_pos in player.board.ship_shot:
                BoardUI.color_square(screen, square_pos, BoardUI.color_index["red"])
            elif square_pos in player.board.empty_shot:
                BoardUI.draw_x(screen, square_pos)
        return game_shoot
