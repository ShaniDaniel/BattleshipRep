# Shows connection to the database

import pyodbc

conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=vps1.enderpex.com;'
                      'Database=BattleshipProject;'
                      'UID=BattleshipProjectUser;'
                      'PWD=P@ssw0rd;')

cursor = conn.cursor()
cursor.execute('SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES')
# returns a list of all the tables in the DB from this Project, *tables currently empty*.

for row in cursor:
    print(row)
