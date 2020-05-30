import pyodbc


class User:

    def __init__(self, _id, first_name, last_name, username, email, reg_date, num_of_games, num_of_wins):
        """Can create a new user in the database, delete one or change one's username"""
        self.id = _id
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.email = email
        self.reg_date = reg_date
        self.num_of_games = num_of_games
        self.num_of_wins = num_of_wins

    def __repr__(self):
        return str((self.id, self.first_name, self.last_name, self.username, self.email, self.reg_date,
                    self.num_of_games, self.num_of_wins))

    @staticmethod
    def db_connect():
        conn = pyodbc.connect('Driver={SQL Server};'
                              'Server=vps1.enderpex.com;'
                              'Database=BattleshipProject;'
                              'UID=BattleshipProjectUser;'
                              'PWD=P@ssw0rd;')
        return conn.cursor()

    @staticmethod
    def create_user(first_name, last_name, username, email, password):
        cursor = User.db_connect()

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
        return "Registration Completed Successfully"

    @staticmethod
    def del_user(_id):
        if _id == 0:
            return "ID cannot be 0"
        cursor = User.db_connect()

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
        cursor = User.db_connect()
        cursor.execute("UPDATE [Users] SET [Username]=? WHERE [ID]=?", new_username, _id)  # changes username in the db
        cursor.commit()  # executes SQL command
        return "Success"
    
    @staticmethod
    def add_score(_id, won=False):
        cursor = User.db_connect()
        if won:
            cursor.execute("""UPDATE [Users] SET
                    [NumberOfWinnings]=(select [NumberOfWinnings]+1 from [Users] WHERE [ID]=?) AND
                    [NumberOfGames]=(select [NumberOfGames]+1 from [Users] WHERE [ID]=?)
                    "WHERE [ID]=?""", _id, _id, _id)
        else:
            cursor.execute("""UPDATE [Users] SET
                            [NumberOfGames]=(select [NumberOfGames]+1 from [Users] WHERE [ID]=?)
                            WHERE [ID]=?""", _id, _id)
        cursor.commit()  # executes SQL command
        return "Success"

    @staticmethod
    def verify_login(username, password):
        cursor = User.db_connect()
        cursor.execute("SELECT * FROM [Users] WHERE [Username]=? AND [Password]=?", username, password)
        rows = cursor.fetchall()
        if len(rows) < 1:
            return "Username or Password Incorrect"
        else:
            return User(rows[0].ID, rows[0].FirstName, rows[0].LastName, rows[0].Username, rows[0].Email,
                        rows[0].RegistrationDate, rows[0].NumberOfGames, rows[0].NumberOfWinnings)
