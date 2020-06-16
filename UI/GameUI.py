from tkinter import messagebox

import pygame
import Constants

from Classes.Square import Square
from Classes.GameAgainstComp import GameAgainstComp
from Classes.Player import Player
from Classes.User import User
from UI.BoardUI import BoardUI
from UI.TextUI import TextUI


class GameUI:

    logged_in_user = None

    @staticmethod
    def exit_window():
        """displays a warning message before closing the window"""
        return messagebox.askyesno(title="Warning!",
                                   message="Are you sure you want to quit?"
                                   "\nIf the game started, it will \nbe counted as loss.")

    @staticmethod
    def placing_rules(screen):
        """shows the basic rules of the game on the screen"""
        TextUI.write_title(screen,
                           "First of all, place your ships. You can't place a ship on top or next to another ship,",
                           1)
        TextUI.write_title(screen,
                           "and you must place your ships horizontally or vertically. Your board is the left board.", 2)
        TextUI.write_title(screen,
                           "To place a ship, press the square you want it to start and then the square you want it to "
                           "end.",
                           3)
        TextUI.write_title(screen, "To delete a placed ship, right-click the selected ship."
                                   " Now, place the ship that is *5* squares long", 4)

    @staticmethod
    def placing_ships(screen, event, player, start_game, game_over):
        """let's the user place it's ships in order and stores the ship's places"""
        from UI.BoardUI import BoardUI
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:  # check for mouse button click
            """event.button returns 1-left click 2-middle click 3-right click"""
            pos = pygame.mouse.get_pos()  # gets current mouse position
            BoardUI.place_ships(screen, player, pos)
            last_ship = None
            for ship in player.board.ships:
                if ship.square_end is not None and start_game is False and game_over is False:
                    BoardUI.color_ship(screen, ship, BoardUI.color_index["blue"])
                try:  # checks if the ship before the current ship was fully placed
                    if last_ship.square_start is not None and last_ship.square_end is not None:
                        TextUI.clear_title(screen, 4)
                        TextUI.write_title(screen, "To delete a placed ship, right-click the selected ship."
                                                   " Now, place the ship that is *%s* squares long" % ship.size, 4)
                except AttributeError:  # if last_ship wasn't initialized yet
                    TextUI.clear_title(screen, 4)
                    TextUI.write_title(screen, "To delete a placed ship, right-click the selected ship."
                                               " Now, place the ship that is *5* squares long", 4)

                last_ship = ship  # remembers the ship before the current ship

        if event.type == pygame.MOUSEBUTTONUP and event.button == 3 and start_game is False and game_over is not True:
            # deletes a placed ship if the player right-clicks it
            pos = pygame.mouse.get_pos()  # gets current mouse position
            for ship in player.board.ships:
                if BoardUI.get_squares_position(player, pos) in player.board.ship_pos.keys() and start_game is False:
                    if player.board.ship_pos[BoardUI.get_squares_position(player, pos)] == ship.id:
                        TextUI.clear_title(screen, 4)
                        BoardUI.del_ship(screen, ship, player)
                        TextUI.write_title(screen, "To delete a placed ship, right-click the selected ship."
                                                   " Now, replace the ship that is *%s* squares long" % ship.size,
                                           4)
                        break

    @staticmethod
    def player_place_ships(screen, event, player, start_game, game_over):
        """alters the original displayed rules to match the game against another player"""
        TextUI.clear_title(screen, 0)
        TextUI.write_title(screen,
                           "Hello! Here you can play against another player. %s, place your ships. "
                           "The other player- don't pick!" %
                           player.username.upper(), 0)
        GameUI.placing_ships(screen, event, player, start_game, game_over)

        ship_count = 0
        for ship in player.board.ships:
            if ship.square_start is not None and ship.square_end is not None:
                ship_count += 1
        if ship_count == 5:  # checks if all the ships were placed
            for line in range(5):
                TextUI.clear_title(screen, line)
                return "success"

    @staticmethod
    def play_against_comp():
        """running the game against the computer"""

        Square.length = 40
        player = Player(GameUI.logged_in_user.username)
        player.set_board(1)

        opponent = Player("Computer")
        opponent.set_board(2)

        pygame.init()
        done = False
        clock = pygame.time.Clock()
        pygame.display.set_caption("© Battleship by Shani Daniel ©")  # sets window title

        screen = pygame.display.set_mode(
            (opponent.board.end.x + player.board.start.x + Square.length, opponent.board.end.y + 80))
        screen.fill(BoardUI.color_index["light blue"])

        TextUI.write_title(screen, "Hello %s! Welcome to Battleship! You are going to play against the computer."
                           % GameUI.logged_in_user.username, 0)
        GameUI.placing_rules(screen)  # shows the rules on the game screen

        BoardUI.draw_board(screen, player.board)
        BoardUI.draw_board(screen, opponent.board)

        GameAgainstComp.rand_place_ships(opponent)  # the computer randomly places it's ships

        player_turn = True
        start_game = False
        game_over = False
        stat_check = False

        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    if game_over is False:
                        if GameUI.exit_window() is True:
                            done = True
                    else:
                        done = True

                GameUI.placing_ships(screen, event, player, start_game, game_over)  # lets the player place his ships

                ship_count = 0
                for ship in player.board.ships:
                    if ship.square_start is not None and ship.square_end is not None:
                        ship_count += 1
                if ship_count == 5:  # checks if all the ships were placed
                    start_game = True
                    for line in range(5):
                        TextUI.clear_title(screen, line)

                if player.check_if_lost() is True:  # shows result if the game ended with loss
                    TextUI.clear_title(screen, 0, 110)
                    TextUI.write_title(screen, "You Lost!", 1, 48)
                    start_game = False
                    game_over = True
                    for ship in opponent.board.ships:
                        if not ship.is_ship_sunk(opponent):
                            BoardUI.color_ship(screen, ship, BoardUI.color_index["blue"])
                    for square in opponent.board.ship_shot:
                        BoardUI.color_square(screen, square, BoardUI.color_index["red"])
                    break

                if opponent.check_if_lost() is True:
                    # shows result if the game ended with win and adds it to the statistics
                    TextUI.clear_title(screen, 0, 110)
                    TextUI.write_title(screen, "You Won!", 1, 48)
                    if game_over is False:
                        User.add_score(GameUI.logged_in_user.id, won=True)
                        GameUI.logged_in_user.num_of_wins += 1
                    start_game = False
                    game_over = True
                    for ship in player.board.ships:
                        if not ship.is_ship_sunk(player):
                            BoardUI.color_ship(screen, ship, BoardUI.color_index["blue"])
                    for square in player.board.ship_shot:
                        BoardUI.color_square(screen, square, BoardUI.color_index["red"])
                    break

                if start_game is True and game_over is False:
                    if stat_check is False:
                        # if the game started and this action wasn't made yet, add the game to the statistics
                        GameUI.logged_in_user.num_of_games += 1
                        User.add_score(GameUI.logged_in_user.id)
                        stat_check = True

                    if player_turn is True:  # runs the player's turn
                        TextUI.write_title(screen, "Play!", 0.5, 40)
                        TextUI.clear_title(screen, 2, 36)
                        TextUI.write_title(screen, "Your Turn", 2, 36)
                        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                            pos = pygame.mouse.get_pos()
                            if BoardUI.get_squares_position(opponent, pos) is not None:
                                if BoardUI.shoot(screen, opponent, pos) == "success":
                                    player_turn = False  # pass the turn to the computer
                                    TextUI.clear_title(screen, 1, 66)
                                    TextUI.write_title(screen, "%s's Turn" % opponent.username, 2, 36)
                        break

                    if opponent.check_if_lost() is False:
                        pygame.time.delay(1000)  # delays the computer's response to make the game more interactive

                    if player_turn is False and opponent.check_if_lost() is False:
                        rand_pos_square = GameAgainstComp.rand_shoot(player)
                        BoardUI.shoot(screen, player, (rand_pos_square.x, rand_pos_square.y))
                        player_turn = True
                for coord in player.board.empty_shot:
                    BoardUI.draw_x(screen, BoardUI.get_squares_position(player, (coord.x, coord.y)))
                for coord in player.board.ship_shot:
                    BoardUI.color_square(screen, BoardUI.get_squares_position(player, (coord.x, coord.y)),
                                         BoardUI.color_index["red"])

            pygame.display.flip()
            clock.tick(60)
        pygame.quit()

    @staticmethod
    def play_against_player():
        """running the game against another player"""

        Square.length = 40
        player1 = Player(GameUI.logged_in_user.username)
        player1.set_board(1)

        player2 = Player("Guest")
        player2.set_board(2)

        pygame.init()
        done = False
        clock = pygame.time.Clock()
        pygame.display.set_caption("© Battleship by Shani Daniel ©")  # sets window title

        screen = pygame.display.set_mode(
            (player2.board.end.x + player1.board.start.x + Square.length, player2.board.end.y + 80))
        screen.fill(BoardUI.color_index["light blue"])

        BoardUI.draw_board(screen, player1.board)
        BoardUI.draw_board(screen, player2.board)

        player1_turn = True
        start_game = False
        game_over = False
        stat_check = False

        GameUI.placing_rules(screen)  # shows the rules on the game screen

        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    if game_over is False:
                        if GameUI.exit_window() is True:
                            done = True
                    else:
                        done = True

                if player1_turn is True and start_game is False and game_over is False:
                    # lets the first player place his ships
                    if GameUI.player_place_ships(screen, event, player1, start_game, game_over) == "success":
                        player1_turn = False
                        TextUI.clear_title(screen, 4)
                        TextUI.write_title(screen,
                                           "To delete a placed ship, right-click the selected ship. "
                                           "Now, place the ship that is *5* squares long", 4)
                        for ship in player1.board.ships:
                            BoardUI.color_ship(screen, ship, BoardUI.color_index["white"])
                            # after he placed all his ships, they disappear from the screen
                    break

                if player1_turn is False and start_game is False and game_over is False:
                    TextUI.clear_title(screen, 2)
                    TextUI.write_title(screen,
                                       "and you must place your ships horizontally or vertically."
                                       " Your board is the RIGHT board.", 2)

                    if GameUI.player_place_ships(screen, event, player2, start_game, game_over) == "success":
                        # lets the second player place his ships
                        player1_turn = True
                        start_game = True
                        for line in range(5):
                            TextUI.clear_title(screen, line)
                        TextUI.write_title(screen,
                                           "%s's Board                                                                 "
                                           "               Guest's Board"
                                           % player1.username, Constants.BOTTOM_LINE)
                        for ship in player2.board.ships:
                            BoardUI.color_ship(screen, ship, BoardUI.color_index["white"])
                        break

                if player1.check_if_lost() is True:
                    # sets what happens if the first player loses
                    TextUI.clear_title(screen, 0, 110)
                    TextUI.write_title(screen, "%s Won!" % player2.username, 1, 48)
                    start_game = False
                    game_over = True
                    for ship in player2.board.ships:
                        if not ship.is_ship_sunk(player2):
                            BoardUI.color_ship(screen, ship, BoardUI.color_index["blue"])
                    for square in player2.board.ship_shot:
                        BoardUI.color_square(screen, square, BoardUI.color_index["red"])
                    break

                if player2.check_if_lost() is True:
                    # sets what happens if the second player loses
                    TextUI.clear_title(screen, 0, 110)
                    TextUI.write_title(screen, "%s Won!" % player1.username, 1, 48)
                    if game_over is False:
                        User.add_score(GameUI.logged_in_user.id, won=True)
                        GameUI.logged_in_user.num_of_wins += 1
                    start_game = False
                    game_over = True
                    for ship in player1.board.ships:
                        if not ship.is_ship_sunk(player1):
                            BoardUI.color_ship(screen, ship, BoardUI.color_index["blue"])
                    for square in player1.board.ship_shot:
                        BoardUI.color_square(screen, square, BoardUI.color_index["red"])
                    break

                if start_game is True and game_over is False:

                    if stat_check is False:
                        GameUI.logged_in_user.num_of_games += 1
                        User.add_score(GameUI.logged_in_user.id)
                        stat_check = True
                        # when the game begins, adds it to the players statistics

                    if player1_turn is True and player1.check_if_lost() is False:
                        TextUI.clear_title(screen, 0.5, 40)
                        TextUI.write_title(screen, "Play!", 0.5, 40)
                        TextUI.clear_title(screen, 2, 36)
                        TextUI.write_title(screen, "%s's Turn" % player1.username, 2, 36)
                        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                            pos = pygame.mouse.get_pos()
                            if BoardUI.get_squares_position(player2, pos) is not None:
                                if BoardUI.shoot(screen, player2, pos) == "success":
                                    player1_turn = False
                                    TextUI.clear_title(screen, 1, 66)
                                    TextUI.write_title(screen, "%s's Turn" % player2.username, 2, 36)
                        break

                    if player1_turn is False and player2.check_if_lost() is False:
                        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                            pos = pygame.mouse.get_pos()
                            if BoardUI.get_squares_position(player1, pos) is not None:
                                if BoardUI.shoot(screen, player1, pos) == "success":
                                    player1_turn = True
                                    TextUI.clear_title(screen, 1, 66)
                                    TextUI.write_title(screen, "%s's Turn" % player1.username, 2, 36)
                        break
            pygame.display.flip()
            clock.tick(60)
        pygame.quit()
