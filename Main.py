from Classes.User import User
from Classes.Cube import Cube
from Classes.Board import Board
from Classes.GameAgainstPlayer import GameAgainstPlayer
from Classes.GameAgainstComp import GameAgainstComp
from Classes.Player import Player
from Classes.Ship import Ship

print(User.change_username(1, 'Shani2525'))
print(User.create_user('Shani', 'Daniel', 'Shani25', 'shani.daniel25@gmail.com', 'Shani25'))

Cube.length = 40
cube_start_p_board = Cube(20, 120)
cube_end_p_board = Cube(380, 480)
cube_start_o_board = Cube(480, 120)
cube_end_o_board = Cube(840, 480)

player = Player("me")
player.board = Board(cube_start_p_board, cube_end_p_board)
opponent = Player("opp")
opponent.board = Board(cube_start_o_board, cube_end_o_board)

Board.available_cubes_dict(opponent, opponent.board.start, opponent.board.end)
Board.available_cubes_dict(player, player.board.start, player.board.end)

o_ships = [Ship(opponent, 5, 5), Ship(opponent, 4, 4), Ship(opponent, 3, 3), Ship(opponent, 2, 3), Ship(opponent, 1, 2)]
p_ships = [Ship(player, 1, 2), Ship(player, 2, 3), Ship(player, 3, 3), Ship(player, 4, 4), Ship(player, 5, 5)]


print(player.board)
print(opponent.board)

GameAgainstComp.rand_place_ship(opponent, o_ships[0])
GameAgainstComp.rand_place_ship(opponent, o_ships[1])
GameAgainstComp.rand_place_ship(opponent, o_ships[2])
GameAgainstComp.rand_place_ship(opponent, o_ships[3])
GameAgainstComp.rand_place_ship(opponent, o_ships[4])

print(opponent.ship_pos)


player.cubes_not_shot_list(cube_start_p_board, cube_end_p_board)
opponent.cubes_not_shot_list(cube_start_o_board, cube_end_o_board)


GameAgainstPlayer.place_ship(player, p_ships[0], player.board.get_board()[0], player.board.get_board()[1])
GameAgainstPlayer.place_ship(player, p_ships[1], player.board.get_board()[3], player.board.get_board()[5])
GameAgainstPlayer.place_ship(player, p_ships[2], player.board.get_board()[22], player.board.get_board()[24])
GameAgainstPlayer.place_ship(player, p_ships[3], player.board.get_board()[26], player.board.get_board()[56])
GameAgainstPlayer.place_ship(player, p_ships[4], player.board.get_board()[43], player.board.get_board()[83])

print(player.ship_pos)
print(player.ships_place)


print(GameAgainstPlayer.shoot(opponent, Cube(520, 120)))
print(GameAgainstPlayer.shoot(opponent, Cube(520, 800)))
print(GameAgainstPlayer.shoot(opponent, Cube(520, 120)))
print(GameAgainstPlayer.shoot(opponent, Cube(520, 160)))
print(GameAgainstPlayer.shoot(opponent, Cube(20, 160)))

print(GameAgainstComp.rand_shoot(player))


print(opponent.board.empty_shot)
print(opponent.board.ship_shot)


print(p_ships[0].is_ship_sank(player))
print(p_ships[1].is_ship_sank(player))
