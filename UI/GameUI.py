import pygame

from Classes.Cube import Cube
from Classes.GameAgainstComp import GameAgainstComp
from Classes.Player import Player
from Classes.Board import Board


class GameUI:

    logged_in_user = None

    @staticmethod
    def write_title(screen, text, line_num, font=24):
        title_font = pygame.font.Font(None, font)
        text_final = title_font.render(text, 1, (0, 0, 0))
        screen.blit(text_final, ((pygame.display.get_surface().get_size()[0] - text_final.get_width()) / 2,
                                 text_final.get_height() * line_num + 5))
        return "success"

    @staticmethod
    def clear_title(screen, line_num, font=24):
        from UI.BoardUI import BoardUI
        title_font = pygame.font.Font(None, font)
        text_final = title_font.render(" ", 1, (0, 0, 0))
        pygame.draw.rect(screen, BoardUI.color_index["light blue"], (0, text_final.get_height() * line_num + 5,
                         pygame.display.get_surface().get_size()[0], text_final.get_height()))
        return "success"

    @staticmethod
    def placing_rules(screen):
        GameUI.write_title(screen,
                           "First of all, place your ships. You can't place a ship on top or next to another ship,",
                           1)
        GameUI.write_title(screen,
                           "and you must place your ships horizontally or vertically. Your board is the left board.", 2)
        GameUI.write_title(screen,
                           "To place a ship, press the cube you want it to start and then the cube you want it to end."
                           , 3)
        GameUI.write_title(screen, "To delete a placed ship, right-click the selected ship."
                                   " Now, place the ship that is 5 cubes long", 4)

    @staticmethod
    def placing_ships(screen, event, player, start_game, game_over):
        from UI.BoardUI import BoardUI
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

        if event.type == pygame.MOUSEBUTTONUP and event.button == 3 and start_game is False and game_over is not True:
            pos = pygame.mouse.get_pos()
            for ship in player.ships:
                if BoardUI.get_cubes_position(player, pos) in player.ship_pos.keys() and start_game is False:
                    if player.ship_pos[BoardUI.get_cubes_position(player, pos)] == ship.id:
                        GameUI.clear_title(screen, 4)
                        BoardUI.del_ship(screen, ship)
                        GameUI.write_title(screen, "To delete a placed ship, right-click the selected ship."
                                                   " Now, replace the ship that is %s cubes long" % ship.size,
                                           4)
                        break

    @staticmethod
    def player_place_ships(screen, event, player, start_game, game_over):
        GameUI.clear_title(screen, 0)
        GameUI.write_title(screen,
                           "Hello! Here you can play against another player. %s, place your ships. "
                           "The other player- don't pick!" %
                           player.username.upper(), 0)
        GameUI.placing_ships(screen, event, player, start_game, game_over)

        ship_count = 0
        for ship in player.ships:
            if ship.cube_start is not None and ship.cube_end is not None:
                ship_count += 1
        if ship_count == 5:
            for line in range(5):
                GameUI.clear_title(screen, line)
                return "success"

    @staticmethod
    def play_against_comp():
        from UI.BoardUI import BoardUI

        Cube.length = 40
        player = Player(GameUI.logged_in_user.username)
        player.board = Board(Cube(20, 100), Cube(380, 460))
        player.cubes_not_shot_list()

        opponent = Player("Computer")
        opponent.board = Board(Cube(460, 100), Cube(820, 460))
        opponent.cubes_not_shot_list()

        pygame.init()
        done = False
        clock = pygame.time.Clock()
        pygame.display.set_caption("© Battleship by Shani Daniel ©")  # set window title

        screen = pygame.display.set_mode(
            (opponent.board.end.x + player.board.start.x + Cube.length, opponent.board.end.y + 80))
        screen.fill(BoardUI.color_index["light blue"])

        GameUI.write_title(screen, "Hello %s! Welcome to Battleship! You are going to play against the computer."
                           % GameUI.logged_in_user.username, 0)
        GameUI.placing_rules(screen)

        BoardUI.draw_board(screen, player.board)
        BoardUI.draw_board(screen, opponent.board)
        GameAgainstComp.rand_place_ships(opponent)

        # for ship in opponent.ships:
        #     BoardUI.color_ship(screen, ship, BoardUI.color_index["blue"])

        player.board.available_cubes_dict(player)
        player_turn = True
        start_game = False
        game_over = False

        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    done = True

                GameUI.placing_ships(screen, event, player, start_game, game_over)

                ship_count = 0
                for ship in player.ships:
                    if ship.cube_start is not None and ship.cube_end is not None:
                        ship_count += 1
                if ship_count == 5:
                    start_game = True
                    for line in range(5):
                        GameUI.clear_title(screen, line)

                if player.check_if_lost() is True:
                    GameUI.clear_title(screen, 0, 110)
                    GameUI.write_title(screen, "You Lost!", 1, 48)
                    start_game = False
                    game_over = True
                    break
                if opponent.check_if_lost() is True:
                    GameUI.clear_title(screen, 0, 110)
                    GameUI.write_title(screen, "You Won!", 1, 48)
                    start_game = False
                    game_over = True
                    break

                if start_game is True and game_over is False:
                    if player_turn is True:
                        GameUI.write_title(screen, "Play!", 0.5, 40)
                        GameUI.clear_title(screen, 2, 36)
                        GameUI.write_title(screen, "Your Turn", 2, 36)
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

    @staticmethod
    def play_against_player():
        from UI.BoardUI import BoardUI

        Cube.length = 40
        player1 = Player(GameUI.logged_in_user.username)
        player1.board = Board(Cube(20, 100), Cube(380, 460))
        player1.cubes_not_shot_list()

        player2 = Player("Guest")
        player2.board = Board(Cube(460, 100), Cube(820, 460))
        player2.cubes_not_shot_list()

        pygame.init()
        done = False
        clock = pygame.time.Clock()
        pygame.display.set_caption("© Battleship by Shani Daniel ©")  # set window title

        screen = pygame.display.set_mode(
            (player2.board.end.x + player1.board.start.x + Cube.length, player2.board.end.y + 80))
        screen.fill(BoardUI.color_index["light blue"])

        BoardUI.draw_board(screen, player1.board)
        BoardUI.draw_board(screen, player2.board)

        player1.board.available_cubes_dict(player1)
        player2.board.available_cubes_dict(player2)

        player1_turn = True
        start_game = False
        game_over = False

        GameUI.placing_rules(screen)

        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    done = True

                if player1_turn is True and start_game is False and game_over is False:
                    if GameUI.player_place_ships(screen, event, player1, start_game, game_over) == "success":
                        player1_turn = False
                        GameUI.clear_title(screen, 4)
                        GameUI.write_title(screen,
                                           "To delete a placed ship, right-click the selected ship. "
                                           "Now, place the ship that is 5 cubes long", 4)
                        for ship in player1.ships:
                            BoardUI.color_ship(screen, ship, BoardUI.color_index["white"])
                    break

                if player1_turn is False and start_game is False and game_over is False:
                    GameUI.clear_title(screen, 2)
                    GameUI.write_title(screen,
                                       "and you must place your ships horizontally or vertically."
                                       " Your board is the RIGHT board.", 2)

                    if GameUI.player_place_ships(screen, event, player2, start_game, game_over) == "success":
                        player1_turn = True
                        start_game = True
                        for line in range(5):
                            GameUI.clear_title(screen, line)
                        GameUI.write_title(screen,
                                           "%s's Board                                                                 "
                                           "               Guest's Board"
                                           % player1.username, 29.5)
                        for ship in player2.ships:
                            BoardUI.color_ship(screen, ship, BoardUI.color_index["white"])
                        break

                if player1.check_if_lost() is True:
                    GameUI.clear_title(screen, 0, 110)
                    GameUI.write_title(screen, "%s Won!" % player2.username, 1, 48)
                    start_game = False
                    game_over = True
                    for ship in player2.ships:
                        if ship.is_ship_sank(player2) is False:
                            BoardUI.color_ship(screen, ship, BoardUI.color_index["blue"])
                    for cube in player2.board.ship_shot:
                        BoardUI.color_cube(screen, cube, BoardUI.color_index["red"])
                    break

                if player2.check_if_lost() is True:
                    GameUI.clear_title(screen, 0, 110)
                    GameUI.write_title(screen, "%s Won!" % player1.username, 1, 48)
                    start_game = False
                    game_over = True
                    for ship in player1.ships:
                        if ship.is_ship_sank(player1) is False:
                            BoardUI.color_ship(screen, ship, BoardUI.color_index["blue"])
                    for cube in player1.board.ship_shot:
                        BoardUI.color_cube(screen, cube, BoardUI.color_index["red"])
                    break

                if start_game is True and game_over is False:
                    if player1_turn is True:
                        GameUI.clear_title(screen, 0.5, 40)
                        GameUI.write_title(screen, "Play!", 0.5, 40)
                        GameUI.clear_title(screen, 2, 36)
                        GameUI.write_title(screen, "%s's Turn" % player1.username, 2, 36)
                        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                            pos = pygame.mouse.get_pos()
                            if BoardUI.get_cubes_position(player2, pos) is not None:
                                if BoardUI.shoot(screen, player2, pos) == "success":
                                    player1_turn = False
                                    GameUI.clear_title(screen, 1, 66)
                                    GameUI.write_title(screen, "%s's Turn" % player2.username, 2, 36)
                        break

                    if player1_turn is False and player2.check_if_lost() is False:
                        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                            pos = pygame.mouse.get_pos()
                            if BoardUI.get_cubes_position(player1, pos) is not None:
                                if BoardUI.shoot(screen, player1, pos) == "success":
                                    player1_turn = True
                                    GameUI.clear_title(screen, 1, 66)
                                    GameUI.write_title(screen, "%s's Turn" % player1.username, 2, 36)
                        break
            pygame.display.flip()
            clock.tick(60)
        pygame.quit()
