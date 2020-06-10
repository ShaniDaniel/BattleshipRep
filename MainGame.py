import tkinter as tk
from tkinter import messagebox
from ttkthemes import ThemedTk
from tkinter import ttk

from UI.GameUI import GameUI
from Classes.User import User


def register_user(reg_screen, first_name, last_name, username, email, password, confirm):
    """takes the values the user entered when signing up, checks for errors and shows them on the screen. 
     if everything is valid the user is registered"""
    try:
        error.destroy()  # if there's already an error on the screen, deletes it first
    except NameError:
        pass

    def error_label(text):  # shows the error on the screen
        global error
        error = ttk.Label(reg_screen, text=text, font=("Calibri Bold", 12), foreground='black', background='light blue')
        error.pack()

    if len(first_name.get()) == 0 or len(last_name.get()) == 0 or len(username.get()) == 0 or len(email.get()) == 0 or \
            len(password.get()) == 0 or len(confirm.get()) == 0:
        error_label("missing required info")
    elif not first_name.get().isalpha():
        error_label("Invalid first name")
    elif not last_name.get().isalpha():
        error_label("Invalid last name")
    elif len(username.get()) > 10:
        error_label("username can't exceed 10 characters")
    elif not username.get().isalnum():
        error_label("username must contain only letters and numbers")
    elif len(email.get().split('@')) != 2:
        error_label("Invalid email")
    elif len(password.get()) < 6:
        error_label("password must be at least 6 characters long")
    elif password.get().isalnum() and (password.get().isalpha() or password.get().isnumeric()):
        error_label("password must contain letters and numbers")
    elif password.get() != confirm.get():
        error_label("password's don't match")

    else:
        user_reg = User.create_user(first_name.get(), last_name.get(), username.get(), email.get(), password.get())
        error_label(user_reg)
        #  creating the user in the database and writing the registration completed successfully


def register():
    reg_screen = tk.Toplevel(screen)  # adds the registration screen on top of the main signing-in screen
    reg_screen.configure(background='light blue')
    reg_screen.title("© Battleship by Shani Daniel ©")
    reg_screen.geometry("400x350")

    first_name = tk.StringVar()
    last_name = tk.StringVar()
    username = tk.StringVar()
    email = tk.StringVar()
    password = tk.StringVar()
    confirm = tk.StringVar()
    # initializing each field the user has to enter as a string variable

    def field(var, text):  # creates the field on the screen and the entry line for the user's input
        ttk.Label(reg_screen, text=text, font=("Calibri Bold", 12), foreground='black',
                  background='light blue').pack()
        if var is password or var is confirm:
            tk.Entry(reg_screen, textvariable=var, show='*').pack()
        else:
            tk.Entry(reg_screen, textvariable=var).pack()

    field(first_name, "First Name: ")
    field(last_name, "Last Name: ")
    field(username, "Username: ")
    field(email, "Email: ")
    field(password, "Password: ")
    field(confirm, "Confirm Password: ")
    # creating each field on the screen

    def register_command():
        register_user(reg_screen, first_name, last_name, username, email, password, confirm)

    ttk.Style().configure('reg2.TButton', font=('Calibri Bold', 12), foreground='black')  # styling the register button
    ttk.Button(reg_screen, text="Register", style='reg2.TButton',
               command=register_command).pack(pady=15)  # creating it


def menu_screen():
    window = ThemedTk(theme="arc")  # creating the menu window with the theme "arc"
    window.title("© Battleship by Shani Daniel ©")
    window.configure(background='light blue')
    ttk.Label(window, text="Welcome to Battleship", font=("Broadway", 50), foreground='black',
              background='light blue').pack(pady=50)
    window.geometry('880x540')

    style = ttk.Style(window)
    style.configure('Option.TButton', font=('Cooper Black', 24), foreground='black')

    def play_against_comp():  # pressing this button on the menu will close the menu window and start this game window
        window.withdraw()
        GameUI.play_against_comp()
        window.update()
        window.deiconify()

    def play_against_player():  # pressing this button on the menu will close the menu window and start this game window
        window.withdraw()
        GameUI.play_against_player()
        window.update()
        window.deiconify()

    def stats():
        stats_screen()

    def del_user():
        delete_user(window)

    def change_user_name():
        change_username(window)

    ttk.Button(window, text="Play Against Computer", style='Option.TButton', command=play_against_comp).pack(pady=10)
    ttk.Button(window, text="Play Against Another Player", style='Option.TButton', command=play_against_player)\
        .pack(pady=10)
    ttk.Button(window, text="Statistics", style='Option.TButton', command=stats).pack(pady=10)
    tk.Label(window, text="", background='light blue').pack()
    tk.Button(window, text="Change Username", font=("Cooper Black", 12),
              background="white", foreground='black', command=change_user_name).pack(pady=5)
    tk.Button(window, text="Delete User", font=("Cooper Black", 12),
              background="white", foreground='black', command=del_user).pack(pady=5)
    # creating the different buttons on the menu screen

    window.mainloop()


def change_username(window):
    """opens up a window where the user can change his username"""
    username_screen = tk.Toplevel(window)
    username_screen.configure(background='light blue')
    username_screen.title("© Battleship by Shani Daniel ©")
    username_screen.geometry("250x180")

    new_username = tk.StringVar()
    ttk.Label(username_screen, text="Enter the new username:", font=("Calibri Bold", 12), foreground='black',
              background='light blue').pack(pady=10)
    tk.Entry(username_screen, textvariable=new_username).pack()

    def replace_username():
        """checks the username the user entered and if it's available changes it in the database"""
        global username_error
        try:
            username_error.destroy()  # if there's already an error on the screen, deletes it first
        except NameError:
            pass
        if User.change_username(GameUI.logged_in_user.id, new_username.get()) != "Username changed":
            username_error = ttk.Label(username_screen, text="Username already exists", font=("Calibri Bold", 12),
                                       foreground='black', background='light blue')
            username_error.pack()
        else:  # changes the username in the database and informs the user
            ttk.Label(username_screen, text="Username changed. To be updated\n   you shall re-enter the program"
                      , font=("Calibri Bold", 12),
                      foreground='black', background='light blue').pack()

    ttk.Style().configure('username.TButton', font=('Calibri Bold', 12), foreground='black')
    ttk.Button(username_screen, text="Change", style='username.TButton', command=replace_username).pack(pady=15)
    #  creating the "change" button


def delete_user(window):
    """allows the user to delete his user from the system (the database)"""
    del_window = messagebox.askyesno(title="Warning!", message="Are you sure you want\nto delete your user?"
                                     "\nThis action can't be undone.")  # asks the user if he is sure
    if del_window is True:  # if he presses "yes" the user is deleted and the game exits
        User.del_user(GameUI.logged_in_user.id)
        messagebox.showinfo(title="Goodbye",
                            message="User deleted.")
        window.destroy()


def login_button_click():
    """after the login button is pressed, verifies the user exists in the database and enters the game menu"""
    try:
        global incorrect
        incorrect.destroy()  # if there's already an error on the screen, deletes it first
    except NameError:
        pass
    GameUI.logged_in_user = User.verify_login(username_login.get(), password_login.get())  # verifies user's login
    if GameUI.logged_in_user != "Username or Password Incorrect":  # if the user's info is correct, enters the game menu
        screen.destroy()
        menu_screen()
    else:  # if not, returns an error message
        incorrect = ttk.Label(text="Username or Password Incorrect", font=("Cooper black", 12),
                              foreground='black', background='light blue')
        incorrect.pack(pady=5)


def login_screen():
    """creates the first screen where the user logs in to the game"""
    global screen, username_login, password_login
    screen = ThemedTk(theme="arc")  # creating a window themed "arc"
    screen.geometry('880x540')
    screen.title("© Battleship by Shani Daniel ©")
    screen.configure(background='light blue')
    style_log = ttk.Style()

    ttk.Label(text='Welcome to Battleship', font=("Broadway", 50), foreground='black', background='light blue').pack(pady=40)
    ttk.Label(text='Login:', font=("Cooper black", 32), foreground='black', background='light blue').pack(pady=20)
    # writes the main game title and the "login" label

    username_login = tk.StringVar()
    password_login = tk.StringVar()
    ttk.Label(screen, text="Username:", font=("Cooper black", 14), foreground='black',
              background='light blue').pack()
    tk.Entry(screen, textvariable=username_login).pack()
    ttk.Label(screen, text="Password:", font=("Cooper black", 14), foreground='black',
              background='light blue').pack()
    tk.Entry(screen, textvariable=password_login, show='*').pack()
    # creates the username and password fields

    style_log.configure('log.TButton', font=('Cooper Black', 16), foreground='black')
    style_log.configure('reg.TButton', font=('Cooper Black', 13), foreground='black')
    ttk.Button(screen, text="Sign in", style='log.TButton', command=login_button_click).pack(pady=15)
    ttk.Button(screen, text="Register", style='reg.TButton', command=register).pack()
    # styles and creates the "sign in" and "register" buttons

    screen.mainloop()


def stats_screen():
    """in this screen the user can see the top 5 players in the game and watch his game statistics """
    cursor = User.db_connect()  # connecting to the database
    cursor.execute("SELECT TOP(5) [Username], [NumberofWinnings] FROM [Users] WHERE [ID]!=0 ORDER BY [NumberofWinnings]"
                   " DESC")  # selects the top 5 players with the highest number of winnings
    rows = cursor.fetchall()  # gets the values that were selected
    stats_win = ThemedTk(theme="Smog")  # created the statistics window themed "smog"
    style = ttk.Style(stats_win)
    style.configure("Treeview.Heading", font=("Calibri Bold", 14))  # styles the tables headings
    style.configure("Treeview", font=("Calibri", 12))  # styles the tables fields

    ttk.Label(stats_win, text='Top Players', font=("Cooper black", 32), foreground='black', background='light blue')\
        .pack(pady=30)
    frame = ttk.Frame(stats_win)  # frames the top players table
    frame.pack(padx=20, pady=20)

    table = ttk.Treeview(frame, columns=(1, 2), show="headings", height='5')  # creates the table

    table.column(1, anchor="c")
    table.column(2, anchor="c")
    table.pack(fill="both", expand=True)
    # centers the table columns and adds the table to the window

    table.heading(1, text="Player")
    table.heading(2, text="Number of Winnings")
    # writes the table headings

    for row in rows:
        table.insert("", "end", values=list(row))  # inserts the values that were given by the database to the table

    stats_win.geometry('540x540')
    stats_win.title("© Battleship by Shani Daniel ©")
    stats_win.configure(background='light blue')

    num_games = GameUI.logged_in_user.num_of_games  # gets the number of games the current user has played from the db
    num_wins = GameUI.logged_in_user.num_of_wins  # gets the number of games the current user has won from the db
    if num_games != 0:
        win_per = int(100 * (num_wins/num_games))  # calculates the winnings percentage
    else:  # if the user's number of games is zero, return 0
        win_per = 0
    ttk.Label(stats_win, text='Your Statistics:', font=("Cooper Black", 20), foreground='black',
              background='light blue').pack(pady=20)
    ttk.Label(stats_win, text='Number of games you played: %s' % num_games, font=("Calibri Bold", 16),
              foreground='black', background='light blue').pack(pady=5)
    ttk.Label(stats_win, text='Number of games you won: %s' % num_wins, font=("Calibri Bold", 16), foreground='black',
              background='light blue').pack(pady=5)
    ttk.Label(stats_win, text='Winning percentage: %s%%' % win_per, font=("Calibri Bold", 16), foreground='black',
              background='light blue').pack(pady=5)
    # creates the labels and adds the statistics we got for the current user

    stats_win.mainloop()


login_screen()  # starts the game by opening the login screen
