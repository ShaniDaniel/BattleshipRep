import unittest

from Classes.GameAgainstPlayer import GameAgainstPlayer
from Classes.GameManager import GameManager
from Classes.Square import Square
from Classes.Player import Player
from Classes.GameAgainstComp import GameAgainstComp
from Classes.User import User


class Test(unittest.TestCase):

    test_player = None

    @classmethod
    def setUpClass(cls):
        """creating a test player"""
        Square.length = 40
        Test.test_player = Player("test")
        Test.test_player.set_board(1)
        Test.test_player.board.available_squares_dict(Test.test_player)

    @classmethod
    def tearDownClass(cls):
        """resets the database changes"""
        cursor = User.db_connect()  # connects to db
        cursor.execute("""UPDATE [Users] SET [NumberOfWinnings]=0 WHERE [ID]=0""")
        cursor.execute("""UPDATE [Users] SET [NumberOfGames]=0 WHERE [ID]=0""")
        cursor.commit()  # executes SQL command

    def test_db_connection(self):
        """testing the connection to the database"""
        cursor = User.db_connect()  # connects to db
        cursor.execute("SELECT * FROM [Users] WHERE [ID]=0")  # selects the first row in the db (test row)
        rows = cursor.fetchall()
        self.assertEqual(rows[0].FirstName, 'testFirstName')
        self.assertEqual(rows[0].LastName, 'testLastName')
        self.assertEqual(rows[0].Username, 'testUsername')

    def test_board(self):
        """testing the board was generated correctly"""
        board_x_start = Test.test_player.board.start.x
        board_x_end = Test.test_player.board.end.x
        board_y_start = Test.test_player.board.start.y
        board_y_end = Test.test_player.board.end.y

        number_of_squares_x_axis = (board_x_end - board_x_start + Square.length) / Square.length
        number_of_squares_y_axis = (board_y_end - board_y_start + Square.length) / Square.length

        self.assertEqual(len(Test.test_player.board.get_board()), number_of_squares_x_axis * number_of_squares_y_axis)
        # the number of squares on the board should match the number of squares calculated by the board list

    def test_rand_place_ships(self):
        """testing the rand_place_ships method in GameAgainstComp"""
        num_of_ship_squares = 0
        for ship in Test.test_player.board.ships:
            num_of_ship_squares += ship.size
        # number of squares that contain ships and needs to be added to the ship_pos dictionary
        for test in range(20):
            GameAgainstComp.rand_place_ships(Test.test_player)
            self.assertEqual(len(Test.test_player.board.ship_pos), num_of_ship_squares)

    def test_square_is_shot(self):
        """testing that the squares_not_shot list is updated when a square is shot"""
        num_of_squares_not_shot = len(Test.test_player.board.squares_not_shot)
        GameManager.shoot(Test.test_player, Test.test_player.board.squares_list[0])  # shooting a square
        self.assertGreater(num_of_squares_not_shot, len(Test.test_player.board.squares_not_shot))
        # checking the list was updated correctly

    def test_statistics_won(self):
        """testing that the statistics are updated accordingly if the user won"""

        cursor = User.db_connect()
        cursor.execute("SELECT * FROM [Users] WHERE [ID]=0")  # selects the first row in the db (test row)
        rows = cursor.fetchall()

        User.add_score(0, won=True)

        cursor = User.db_connect()
        cursor.execute("SELECT * FROM [Users] WHERE [ID]=0")  # selects the updated first row in the db (test row)
        updated_rows = cursor.fetchall()

        self.assertEqual(updated_rows[0].NumberOfWinnings, rows[0].NumberOfWinnings+1)
        # the number of winnings should grow by 1

    def test_statistics_lost(self):
        """testing that the statistics are updated accordingly if the user lost"""

        cursor = User.db_connect()
        cursor.execute("SELECT * FROM [Users] WHERE [ID]=0")  # selects the first row in the db (test row)
        rows = cursor.fetchall()

        User.add_score(0, won=False)

        cursor = User.db_connect()
        cursor.execute("SELECT * FROM [Users] WHERE [ID]=0")   # selects the updated first row in the db (test row)
        updated_rows = cursor.fetchall()

        self.assertEqual(updated_rows[0].NumberOfGames, rows[0].NumberOfGames+1)  # the number of games should grow by 1
        self.assertEqual(updated_rows[0].NumberOfWinnings, rows[0].NumberOfWinnings)
        # the number of winnings should not change

    def test_player_place_ships(self):
        """testing the place_ship method works correctly and returns errors if ship placing is invalid"""

        player = Test.test_player

        def check_ship(ship_index, start_square, end_square):
            # calls the place_ship method with different ships and coordinates
            return GameAgainstPlayer.place_ship(player, ship=player.board.ships[ship_index],
                                                ship_start=player.board.squares_list[start_square],
                                                ship_end=player.board.squares_list[end_square])

        self.assertEqual(check_ship(0, 0, 3), "Ship is too short! must be 5 squares long.")
        # in the ships list, ship index 0 is the ship 5 squares long. In the squares list, indexes 0-3 are only 4
        # squares total, so the function should return too short error.

        self.assertEqual(check_ship(1, 0, 4), "Ship is too long! must be 4 squares long.")
        # ship index 1 is the ship 4 squares long. In the squares list, indexes 0-4 are 5 squares total,
        # so the function should return too long error.

        self.assertEqual(check_ship(2, 0, 21), "Invalid ship coordinates. Ship must be placed horizontally or "
                                               "vertically.")
        # In the squares list, indexes 0-21 are diagonal, so the function should return invalid coordinates error.

        self.assertEqual(check_ship(0, 0, 40), "success")
        # ship index 0 is the ship 5 squares long. This ship is placed vertically on 5 squares, so this ship is valid.


if __name__ == '__main__':
    unittest.main()
