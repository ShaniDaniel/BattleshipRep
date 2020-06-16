import unittest

from Classes.GameManager import GameManager
from Classes.Square import Square
from Classes.Player import Player
from Classes.GameAgainstComp import GameAgainstComp
from Classes.User import User


class Test(unittest.TestCase):

    test_player = None

    @classmethod
    def setUpClass(cls):
        Square.length = 40
        Test.test_player = Player("test")
        Test.test_player.set_board(1)
        Test.test_player.board.available_squares_dict(Test.test_player)

    def test_db_connection(self):
        """testing the connection to the database"""
        cursor = User.db_connect()  # connects to db
        cursor.execute("SELECT * FROM [Users] WHERE [ID]=0")  # selects the first row in the db (test row)
        rows = cursor.fetchall()
        self.assertEqual(rows[0].FirstName, 'testFirstName')
        self.assertEqual(rows[0].LastName, 'testLastName')
        self.assertEqual(rows[0].Username, 'testUsername')

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
        num_squares_not_shot = len(Test.test_player.board.squares_not_shot)
        GameManager.shoot(Test.test_player, Test.test_player.board.squares_list[0])
        self.assertGreater(num_squares_not_shot, len(Test.test_player.board.squares_not_shot))


if __name__ == '__main__':
    unittest.main()
