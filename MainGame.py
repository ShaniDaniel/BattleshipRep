import pygame

from Classes.GameAgainstComp import GameAgainstComp
from Classes.GameAgainstPlayer import GameAgainstPlayer
from Classes.Player import Player
from Classes.Board import Board
from Classes.Cube import Cube
from UI.BoardUI import BoardUI
from UI.GameUI import GameUI

pygame.init()
done = False

clock = pygame.time.Clock()
pygame.display.set_caption("© Battleship by Shani Daniel ©")  # set window title

Cube.length = 40
player = Player("Shani")
player.board = Board(Cube(20, 100), Cube(380, 460))
player.cubes_not_shot_list()

opponent = Player("Computer")
opponent.board = Board(Cube(460, 100), Cube(820, 460))
opponent.cubes_not_shot_list()


screen = pygame.display.set_mode((opponent.board.end.x + player.board.start.x + Cube.length, opponent.board.end.y + 80))
screen.fill((252, 168, 78))

GameUI.write_title(screen, "Hello! Welcome to Battleship! You are going to play against the computer.", 0)
GameUI.write_title(screen, "First of all, place your ships. You can't place a ship on top or next to another ship,", 1)
GameUI.write_title(screen, "and you must place your ships horizontally or vertically. Your board is the left board.", 2)
GameUI.write_title(screen, "To place a ship, press the cube you want it to start and then the cube you want it to end."
                   , 3)
GameUI.write_title(screen, "To delete a placed ship, right-click the selected ship."
                           " Now, place the ship that is 5 cubes long", 4)

BoardUI.draw_board(screen, player.board)
BoardUI.draw_board(screen, opponent.board)
GameAgainstComp.rand_place_ships(opponent)

for ship in opponent.ships:
    BoardUI.color_ship(screen, ship, BoardUI.color_index["blue"])

start_cube, end_cube = None, None
player.board.available_cubes_dict(player)
player_turn = True
start_game = False
game_over = False

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            done = True
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:  # check for mouse button click
            """event.button returns 1-left click 2-middle click 3-right click"""
            pos = pygame.mouse.get_pos()
            BoardUI.place_ships(screen, player, pos)
            last_ship = None
            for ship in player.ships:
                if ship.cube_end is not None and start_game is False and game_over is False:
                    BoardUI.color_ship(screen, ship, BoardUI.color_index["blue"])
                try:
                    if last_ship.cube_start is not None and last_ship.cube_end is not None:
                        GameUI.clear_title(screen, 4)
                        GameUI.write_title(screen, "To delete a placed ship, right-click the selected ship."
                                                   " Now, place the ship that is %s cubes long" % ship.size, 4)

                except AttributeError:
                    GameUI.clear_title(screen, 4)
                    GameUI.write_title(screen, "To delete a placed ship, right-click the selected ship."
                                               " Now, place the ship that is 5 cubes long", 4)
                last_ship = ship

        if event.type == pygame.MOUSEBUTTONUP and event.button == 3:
            pos = pygame.mouse.get_pos()
            for ship in player.ships:
                if BoardUI.get_cubes_position(player, pos) in player.ship_pos.keys() and start_game is False:
                    if player.ship_pos[BoardUI.get_cubes_position(player, pos)] == ship.id:
                        GameUI.clear_title(screen, 4)
                        GameUI.write_title(screen, "To delete a placed ship, right-click the selected ship."
                                                   " Now, replace the ship that is %s cubes long" % ship.size, 4)
                        BoardUI.del_ship(screen, ship)
                        break

        ship_count = 0
        for ship in player.ships:
            if ship.cube_start is not None and ship.cube_end is not None:
                ship_count += 1
        if ship_count == 5:
            start_game = True
            for line in range(5):
                GameUI.clear_title(screen, line)

        if player.check_if_lost() is True:
            GameUI.clear_title(screen, 0.5, 88)
            GameUI.write_title(screen, "You Lost!", 1, 48)
            start_game = False
            game_over = True
            break
        if opponent.check_if_lost() is True:
            GameUI.clear_title(screen, 0.5, 88)
            GameUI.write_title(screen, "You Won!", 1, 48)
            start_game = False
            game_over = True
            break

        if start_game is True and game_over is False:
            if player_turn is True:
                GameUI.write_title(screen, "Play!", 0.5, 40)
                GameUI.clear_title(screen, 2, 36)
                GameUI.write_title(screen, "your Turn", 2, 36)
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    pos = pygame.mouse.get_pos()
                    if BoardUI.get_cubes_position(opponent, pos) is not None:
                        if BoardUI.shoot(screen, opponent, pos) == "success":
                            player_turn = False
                            GameUI.clear_title(screen, 1, 66)
                            GameUI.write_title(screen, "%s's Turn" % opponent.username, 2, 36)
                break
            if opponent.check_if_lost() is False:
                pygame.time.delay(1000)
            if player_turn is False and opponent.check_if_lost() is False:
                rand_pos_cube = GameAgainstComp.rand_shoot(player)
                BoardUI.shoot(screen, player, (rand_pos_cube.x, rand_pos_cube.y))
                player_turn = True
        for coord in player.board.empty_shot:
            BoardUI.draw_x(screen, BoardUI.get_cubes_position(player, (coord.x, coord.y)))
        for coord in player.board.ship_shot:
            BoardUI.color_cube(screen, BoardUI.get_cubes_position(player, (coord.x, coord.y)),
                               BoardUI.color_index["red"])

    pygame.display.flip()
    clock.tick(60)
pygame.quit()
