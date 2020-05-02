import pyodbc
import random
player_board_x = []  # list of the cube's x values in the player's board
board_y = []  # list of the cube's y values in the board
player_board_by_ships = {}
player_ships_place = {}
player_all_ships = []  # list of all the ship's coordinates on the player's board
player_ship_pos_dict = {}  # dictionary of the coordinates of the ships and the ship ID as value
opponent_board_x = []  # list of the cube's x values in the opponent's board
opponent_board_by_ships = {}
opponent_ships_place = {}  # dictionary of the ship's ID and it's place on the board accordingly
opponent_all_ships = []  # list of all the ship's coordinates on the player's board
opponent_ship_pos_dict = {}  # dictionary of the coordinates of the ships and the ship ID as value


class User:
    def __init__(self, _id, first_name, last_name, username, email, reg_date, num_of_games, num_of_wins):
        self.id = _id
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.email = email
        self.reg_date = reg_date
        self.num_of_games = num_of_games
        self.num_of_wins = num_of_wins

    @staticmethod
    def create_user(first_name, last_name, username, email, password):

        conn = pyodbc.connect('Driver={SQL Server};'
                              'Server=vps1.enderpex.com;'
                              'Database=BattleshipProject;'
                              'UID=BattleshipProjectUser;'
                              'PWD=P@ssw0rd;')

        cursor = conn.cursor()

        cursor.execute("SELECT * FROM [Users] WHERE [Username]=?", username)
        # selects all users with the same username in the db table and returns a list if exists.
        rows = cursor.fetchall()  # executes SQL command and puts the result into rows
        if len(rows) > 0:  # checks that there are no existing users with this username
            return "Username already exists"
        cursor.execute("SELECT * FROM [Users] WHERE [Email]=?", email)
        # selects all users with the same email in the db table and returns a list if exists.
        rows = cursor.fetchall()  # executes SQL command and puts the result into rows
        if len(rows) > 0:  # checks that there are no existing users with this email
            return "Email already exists"
        cursor.execute("""
        INSERT INTO [Users]
        (ID, FirstName, LastName, Username, Email, Password, RegistrationDate, NumberOfGames, NumberOfWinnings) 
        VALUES((SELECT MAX(ID) + 1 FROM [Users]), ?, ?, ?, ?, ?, (SELECT CONVERT(DATE, GETDATE())), 0, 0)
        """, first_name, last_name, username, email, password)  # inserts the values to the db table
        cursor.commit()  # executes SQL command
        return "Success"

    @staticmethod
    def del_user(_id):
        if _id == 0:
            return "ID cannot be 0"
        conn = pyodbc.connect('Driver={SQL Server};'
                              'Server=vps1.enderpex.com;'
                              'Database=BattleshipProject;'
                              'UID=BattleshipProjectUser;'
                              'PWD=P@ssw0rd;')
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM [Users] WHERE [ID]=?", _id)  # selects the row with this ID value
        rows = cursor.fetchall()
        if len(rows) > 0:  # checks if a row with this ID exists
            cursor.execute("DELETE FROM [Users] Where ID=?", _id)  # deletes the row
            cursor.commit()  # executes SQL command
            return "Success"
        else:
            return "ID doesn't exists"

    @staticmethod
    def change_username(_id, new_username):
        conn = pyodbc.connect('Driver={SQL Server};'
                              'Server=vps1.enderpex.com;'
                              'Database=BattleshipProject;'
                              'UID=BattleshipProjectUser;'
                              'PWD=P@ssw0rd;')
        cursor = conn.cursor()
        cursor.execute("UPDATE [Users] SET [Username]=? WHERE [ID]=?", new_username, _id)  # changes username in the db
        cursor.commit()  # executes SQL command
        return "Success"


class Ship:
    ship_sank = False

    def __init__(self, _id, size):
        self._id = _id
        self.size = size
        self.x_start = None
        self.y_start = None
        self.x_end = None
        self.y_end = None

    def set_position(self, x_start, y_start, x_end, y_end, cube_and_space):
        self.x_start = x_start
        self.y_start = y_start
        self.x_end = x_end
        self.y_end = y_end
        if min(player_board_x) <= x_start <= max(player_board_x):
            for x in range(x_start, x_end+1, cube_and_space):
                for y in range(y_start, y_end+1, cube_and_space):
                    player_ship_pos_dict[x, y] = self._id
        elif min(opponent_board_x) <= x_start <= max(opponent_board_x):
            for x in range(x_start, x_end+1, cube_and_space):
                for y in range(y_start, y_end+1, cube_and_space):
                    opponent_ship_pos_dict[x, y] = self._id

    def position_m(self):
        m = self.size - 1
        return m

    def is_ship_sank(self):
        count = 0
        for cube in opponent_ships_place[self._id]:
            if cube in Game.ship_shot:
                count += 1
        if count == self.size:
            return True
        else:
            return False


class Board:

    def __init__(self):
        self.place_y_end = None
        self.place_x_end = None
        self.place_y_start = None
        self.ship_id = None
        self.place_x_start = None

    @staticmethod
    def player_board(x_start_board, x_end_board, y_start_board, y_end_board):
        cube_and_space = int((x_end_board - x_start_board) / 10)
        for x in range(x_start_board, x_end_board, cube_and_space):
            for y in range(y_start_board, y_end_board, cube_and_space):
                if x not in player_board_x:
                    player_board_x.append(x)
                if y not in board_y:
                    board_y.append(y)
                player_board_by_ships[(x, y)] = 0

    @staticmethod
    def opponent_board(x_start_board, x_end_board, y_start_board, y_end_board):
        cube_and_space = int((x_end_board - x_start_board) / 10)
        for x in range(x_start_board, x_end_board, cube_and_space):
            for y in range(y_start_board, y_end_board, cube_and_space):
                if x not in opponent_board_x:
                    opponent_board_x.append(x)
                if y not in board_y:
                    board_y.append(y)
                opponent_board_by_ships[(x, y)] = 0


class Game:
    empty_cubes_shot = []
    ship_shot = []

    def __init__(self, my_board, opponent_board):
        self.my_board = my_board
        self.opponent_board = opponent_board

    @staticmethod
    # defines the place of the ship on the board by it's cube's coordinates
    def place_ship(ship_id, place_x_start, place_y_start, place_x_end, place_y_end):
        cube_and_space = player_board_x[1] - player_board_x[0]
        ships_temp = []  # saves current ship's place
        if min(player_board_x) <= place_x_start <= max(player_board_x):
            for x in range(place_x_start, place_x_end + 1, cube_and_space):
                for y in range(place_y_start, place_y_end + 1, cube_and_space):
                    ships_temp.append([x, y])  # saves the current ship's place
                    player_all_ships.append([x, y])  # adds the ship's place to the all_ships list
            player_ships_place[ship_id] = ships_temp  # adds the ship's ID and place to the ships_place dictionary
        elif min(opponent_board_x) <= place_x_start <= max(opponent_board_x):
            for x in range(place_x_start, place_x_end + 1, cube_and_space):
                for y in range(place_y_start, place_y_end + 1, cube_and_space):
                    ships_temp.append([x, y])  # saves the current ship's place
                    opponent_all_ships.append([x, y])  # adds the ship's place to the all_ships list
            opponent_ships_place[ship_id] = ships_temp  # adds the ship's ID and place to the ships_place dictionary

    @staticmethod
    def shoot(cube_x, cube_y):
        for ship in opponent_all_ships:
            if ship[0] == cube_x and ship[1] == cube_y:
                Game.ship_shot.append([cube_x, cube_y])
                break
        else:
            Game.empty_cubes_shot.append([cube_x, cube_y])


class GameAgainstComp(Game):

    @staticmethod
    def rand_place_ship(ship):
        not_done = True
        x_start_board = min(opponent_board_x)
        x_end_board = max(opponent_board_x)
        y_start_board = min(board_y)
        y_end_board = max(board_y)
        cube_and_space = opponent_board_x[1] - opponent_board_x[0]
        m = ship.position_m()
        available_cubes = []
        not_available_cubes = []
        for key in opponent_board_by_ships:
            if opponent_board_by_ships[key] == 0:
                available_cubes.append(key)
            if opponent_board_by_ships[key] == 1:
                not_available_cubes.append(key)

        while not_done:
            check = []
            cube_start = random.choice(available_cubes)
            rand_x_start = cube_start[0]
            rand_y_start = cube_start[1]

            if x_start_board + m * cube_and_space <= rand_x_start < x_end_board - m * cube_and_space:
                rand_x_end = random.choice(
                    [rand_x_start - m * cube_and_space, rand_x_start, rand_x_start + m * cube_and_space])
            elif x_start_board + m * cube_and_space <= rand_x_start:
                rand_x_end = random.choice([rand_x_start - m * cube_and_space, rand_x_start])
            else:
                rand_x_end = random.choice([rand_x_start, rand_x_start + m * cube_and_space])

            if rand_x_start != rand_x_end:
                rand_y_end = rand_y_start
            else:
                if y_start_board + m * cube_and_space <= rand_y_start < y_end_board - m * cube_and_space:
                    rand_y_end = random.choice([rand_y_start - m * cube_and_space, rand_y_start + m * cube_and_space])
                elif y_start_board + m * cube_and_space <= rand_y_start:
                    rand_y_end = rand_y_start - m * cube_and_space
                else:
                    rand_y_end = rand_y_start + m * cube_and_space

            for x in range(min(rand_x_start, rand_x_end) - cube_and_space,
                           max(rand_x_start, rand_x_end) + cube_and_space + 1, cube_and_space):
                for y in range(min(rand_y_start, rand_y_end) - cube_and_space,
                               max(rand_y_start, rand_y_end) + cube_and_space + 1, cube_and_space):
                    if (x, y) in not_available_cubes:
                        check.append('no')
            if len(check) == 0:
                not_done = False

        Game.place_ship(ship._id, min(rand_x_start, rand_x_end), min(rand_y_start, rand_y_end),
                        max(rand_x_start, rand_x_end), max(rand_y_start, rand_y_end))
        Ship.set_position(ship, min(rand_x_start, rand_x_end), min(rand_y_start, rand_y_end),
                          max(rand_x_start, rand_x_end), max(rand_y_start, rand_y_end), cube_and_space)
        for x in range(min(rand_x_start, rand_x_end) - cube_and_space,
                       max(rand_x_start, rand_x_end) + cube_and_space + 1, cube_and_space):
            for y in range(min(rand_y_start, rand_y_end) - cube_and_space,
                           max(rand_y_start, rand_y_end) + cube_and_space + 1, cube_and_space):
                if (x, y) in opponent_board_by_ships:
                    opponent_board_by_ships[(x, y)] = 1
                    ship.set_position(min(rand_x_start, rand_x_end), min(rand_y_start, rand_y_end),
                                      max(rand_x_start, rand_x_end), max(rand_y_start, rand_y_end), cube_and_space)
                    not_done = False


class GameAgainstPlayer():
    @staticmethod
    def place_ship(ship, cube_place_start, cube_place_end):
        place_x_start = cube_place_start[0]
        place_y_start = cube_place_start[1]
        place_x_end = cube_place_end[0]
        place_y_end = cube_place_end[1]
        x_start_board = min(player_board_x)
        x_end_board = max(player_board_x)
        y_start_board = min(board_y)
        y_end_board = max(board_y)
        cube_and_space = player_board_x[1] - player_board_x[0]
        not_available_cubes = []
        for key in player_board_by_ships:
            if player_board_by_ships[key] == 1:
                not_available_cubes.append(key)
        try:
            assert x_start_board <= place_x_start < x_end_board and y_start_board <= place_y_start < y_end_board
        except AssertionError:
            return "Can't place ship outside of board"
        for x in range(min(place_x_start, place_x_end) - cube_and_space,
                       max(place_x_start, place_x_end) + cube_and_space + 1, cube_and_space):
            for y in range(min(place_y_start, place_y_end) - cube_and_space,
                           max(place_y_start, place_y_end) + cube_and_space + 1, cube_and_space):
                if (x, y) in not_available_cubes:
                    return "Can't place ship on top or next to another ship."
        if place_x_start != place_x_end and place_y_start != place_y_end:
            return "Invalid ship coordinates. Ship must be placed horizontally or vertically."
        if place_x_start == place_x_end:
            if (max(place_y_start, place_y_end) - min(place_y_start, place_y_end))/cube_and_space > ship.size:
                return "Ship is too long! must be %d cubes long." % ship.size
            elif (max(place_y_start, place_y_end) - min(place_y_start, place_y_end))/cube_and_space < ship.size:
                return "Ship is too short! must be %d cubes long." % ship.size
            else:
                Game.place_ship(ship._id, min(place_x_start, place_x_end), min(place_y_start, place_y_end),
                                max(place_x_start, place_x_end), max(place_y_start, place_y_end))
                Ship.set_position(ship, min(place_x_start, place_x_end), min(place_y_start, place_y_end),
                                  max(place_x_start, place_x_end), max(place_y_start, place_y_end), cube_and_space)
                for x in range(min(place_x_start, place_x_end) - cube_and_space,
                               max(place_x_start, place_x_end) + cube_and_space + 1, cube_and_space):
                    for y in range(min(place_y_start, place_y_end) - cube_and_space,
                                   max(place_y_start, place_y_end) + cube_and_space + 1, cube_and_space):
                        if (x, y) in player_board_by_ships:
                            player_board_by_ships[(x, y)] = 1


class Statistics:
    def update_stats(self, user_id):
        self.user_id = user_id
        conn = pyodbc.connect('Driver={SQL Server};'
                              'Server=vps1.enderpex.com;'
                              'Database=BattleshipProject;'
                              'UID=BattleshipProjectUser;'
                              'PWD=P@ssw0rd;')

        cursor = conn.cursor()

        cursor.execute()





# print(User.change_username(1, 'Shani2525'))
# print(User.create_user('Shani', 'Daniel', 'Shani25', 'shani.daniel25@gmail.com', 'Shani25'))

ship1 = Ship(1, 2)
ship2 = Ship(2, 3)
ship3 = Ship(3, 3)
ship4 = Ship(4, 4)
ship5 = Ship(5, 5)

Board.player_board(20, 420, 120, 520)
Board.opponent_board(480, 880, 120, 520)
#print(board_x)
#print(board_y)

#print(board_by_ships)
GameAgainstComp.rand_place_ship(ship5)
GameAgainstComp.rand_place_ship(ship4)
GameAgainstComp.rand_place_ship(ship3)
GameAgainstComp.rand_place_ship(ship2)
GameAgainstComp.rand_place_ship(ship1)

print(opponent_ship_pos_dict)


#print(ships_place)
#print(board_by_ships)

# Game.place_ship(4, 20, 120, 100, 120, 40)
#print(all_ships)
#print(opponent_ships_place)
#print(ship_pos_dict)

Game.shoot(20, 120)
Game.shoot(60, 120)
Game.shoot(340, 120)
Game.shoot(300, 400)
Game.shoot(100, 120)
#print(Game.empty_cubes_shot)
#print(Game.ship_shot)


#print(ship1.is_ship_sank())
#print(ship2.is_ship_sank())





