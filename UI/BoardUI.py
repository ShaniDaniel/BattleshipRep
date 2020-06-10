import pygame
from Classes.Cube import Cube
from Classes.GameAgainstPlayer import GameAgainstPlayer
from Classes.GameManager import GameManager
from UI.TextUI import TextUI


class BoardUI:

    color_index = {"blue": (0, 0, 255), "red": (255, 0, 0), "grey": (210, 210, 210), "orange": (252, 168, 78),
                   "light blue": (173, 216, 230), "white": (255, 255, 255)}
    # a dictionary of different useful colors for the game by their rgb values
    padding_value = 3  # padding for creating more suitable shapes
    bottom_line = 29.5  # the line number underneath the board

    @staticmethod
    def draw_board(screen, board):
        """draws the board"""
        for x in range(board.start.x, board.end.x + Cube.length, Cube.length):
            for y in range(board.start.y,  board.end.y + Cube.length, Cube.length):
                pygame.draw.rect(screen, BoardUI.color_index["white"],
                                 pygame.Rect(x, y, Cube.length - 1, Cube.length - 1))

    @staticmethod
    def get_cubes_position(player, position):
        #  gets each cubes position to locate if the player pressed a cube and which one
        for cube in player.board.cubes_list:
            if cube.x <= position[0] <= cube.x + Cube.length - 1 and cube.y <= position[1] <= cube.y + Cube.length - 1:
                return cube

    @staticmethod
    def draw_x(screen, cube):
        padding_value = BoardUI.padding_value
        """draws an "X" sign on the cube"""
        pygame.draw.line(screen, (0, 0, 0), (cube.x + padding_value, cube.y + padding_value),
                         (cube.x + Cube.length - padding_value, cube.y + (Cube.length - padding_value)), padding_value)
        pygame.draw.line(screen, (0, 0, 0), (cube.x + padding_value, cube.y + (Cube.length - padding_value)),
                         (cube.x + (Cube.length - padding_value), cube.y + padding_value), padding_value)
     
    @staticmethod
    def color_cube(screen, cube, color):
        """colors a cube a certain color"""
        try:
            pygame.draw.rect(screen, color, pygame.Rect(cube.x, cube.y, Cube.length - 1, Cube.length - 1))
        except AttributeError:
            pass

    @staticmethod
    def color_ship(screen, ship, color):
        """colors a whole ship a certain color"""
        for x in range(ship.start_x, ship.end_x + 1, Cube.length):
            for y in range(ship.start_y, ship.end_y + 1, Cube.length):
                BoardUI.color_cube(screen, Cube(x, y), color)
                
    @staticmethod
    def place_ships(screen, player, pos):
        """places the user's ship py his given cubes and colors these ships blue"""
        bottom_line = BoardUI.bottom_line
        for ship in player.board.ships:
            if ship.cube_end is not None:
                continue
            if ship.cube_start is None:
                ship.cube_start = BoardUI.get_cubes_position(player, pos)
                BoardUI.color_cube(screen, ship.cube_start, BoardUI.color_index["blue"])
                break
            elif ship.cube_end is None and BoardUI.get_cubes_position(player, pos) is not None:
                ship.cube_end = BoardUI.get_cubes_position(player, pos)
                ship_check = GameAgainstPlayer.place_ship(player, ship, ship.cube_start, ship.cube_end)
                if ship_check != "success":
                    TextUI.clear_title(screen, bottom_line)
                    TextUI.write_title(screen, ship_check, bottom_line)
                    BoardUI.color_cube(screen, ship.cube_start, BoardUI.color_index["white"])
                    ship.cube_start = None
                    ship.cube_end = None
                    break
                else:
                    TextUI.clear_title(screen, bottom_line)
                    BoardUI.color_ship(screen, ship, BoardUI.color_index["blue"])
                    return ship
            else:
                BoardUI.color_cube(screen, ship.cube_start, BoardUI.color_index["white"])
                ship.cube_start = None
                ship.cube_end = None
                break

    @staticmethod         
    def del_ship(screen, ship, player):
        """deletes a ship from the screen and calls the del_ship function to delete its information"""
        BoardUI.color_ship(screen, ship, BoardUI.color_index["white"])
        ship.del_ship(player)
        
    @staticmethod
    def shoot(screen, player, pos):
        """shoots the given cube by calling the "shoot" function and coloring the cube red if it contains a ship, and
        draws an X if it doesn't"""
        cube_pos = BoardUI.get_cubes_position(player, pos)
        game_shoot = GameManager.shoot(player, cube_pos)
        if game_shoot == "success":
            if cube_pos in player.board.ship_shot:
                BoardUI.color_cube(screen, cube_pos, BoardUI.color_index["red"])
            elif cube_pos in player.board.empty_shot:
                BoardUI.draw_x(screen, cube_pos)
        return game_shoot
