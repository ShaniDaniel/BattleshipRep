import pygame
from Classes.Cube import Cube
from Classes.GameAgainstPlayer import GameAgainstPlayer
from Classes.GameManager import GameManager
from UI.GameUI import GameUI


class BoardUI:

    color_index = {"blue": (0, 0, 255), "red": (255, 0, 0), "grey": (210, 210, 210), "orange": (252, 168, 78),
                   "light blue": (173, 216, 230), "white": (255, 255, 255)}

    @staticmethod
    def draw_board(screen, board):
        for x in range(board.start.x, board.end.x + Cube.length, Cube.length):
            for y in range(board.start.y,  board.end.y + Cube.length, Cube.length):
                pygame.draw.rect(screen, BoardUI.color_index["white"],
                                 pygame.Rect(x, y, Cube.length - 1, Cube.length - 1))

    @staticmethod
    def get_cubes_position(player, position):
        for cube in player.board.cubes_list:
            if cube.x <= position[0] <= cube.x + Cube.length - 1 and cube.y <= position[1] <= cube.y + Cube.length - 1:
                return cube

    @staticmethod
    def draw_x(screen, cube):
        try:
            pygame.draw.line(screen, (0, 0, 0), (cube.x + 3, cube.y + 3),
                             (cube.x + Cube.length - 3, cube.y + (Cube.length - 3)), 3)
            pygame.draw.line(screen, (0, 0, 0), (cube.x + 3, cube.y + (Cube.length - 3)),
                             (cube.x + (Cube.length - 3), cube.y + 3), 3)
        except AttributeError:
            pass
     
    @staticmethod
    def color_cube(screen, cube, color):
        try:
            pygame.draw.rect(screen, color, pygame.Rect(cube.x, cube.y, Cube.length - 1, Cube.length - 1))
        except AttributeError:
            pass

    @staticmethod
    def color_ship(screen, ship, color):
        for x in range(min(ship.cube_start.x, ship.cube_end.x), 
                       max(ship.cube_start.x, ship.cube_end.x) + 1, Cube.length):
            for y in range(min(ship.cube_start.y, ship.cube_end.y), 
                           max(ship.cube_start.y, ship.cube_end.y) + 1, Cube.length):
                BoardUI.color_cube(screen, Cube(x, y), color)
                
    @staticmethod
    def place_ships(screen, player, pos):
        for ship in player.ships:
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
                    GameUI.clear_title(screen, 29.5)
                    GameUI.write_title(screen, ship_check, 29.5)
                    BoardUI.color_cube(screen, ship.cube_start, BoardUI.color_index["white"])
                    ship.cube_start = None
                    ship.cube_end = None
                    break
                else:
                    GameUI.clear_title(screen, 29.5)
                    BoardUI.color_ship(screen, ship, BoardUI.color_index["blue"])
                    return ship
            else:
                BoardUI.color_cube(screen, ship.cube_start, BoardUI.color_index["white"])
                ship.cube_start = None
                ship.cube_end = None
                break

    @staticmethod         
    def del_ship(screen, ship):
        BoardUI.color_ship(screen, ship, BoardUI.color_index["white"])
        ship.del_ship()
        
    @staticmethod
    def shoot(screen, player, pos):
        cube_pos = BoardUI.get_cubes_position(player, pos)
        game_shoot = GameManager.shoot(player, cube_pos)
        if game_shoot == "success":
            if cube_pos in player.board.ship_shot:
                BoardUI.color_cube(screen, cube_pos, BoardUI.color_index["red"])
            elif cube_pos in player.board.empty_shot:
                BoardUI.draw_x(screen, cube_pos)
        return game_shoot
