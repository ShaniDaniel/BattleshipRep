import tkinter as tk
from ttkthemes import ThemedTk
from tkinter import ttk

from UI.GameUI import GameUI
from Classes.User import User


def register_user():
    try:
        error.destroy()
    except NameError:
        pass

    def error_label(text):
        global error
        error = ttk.Label(reg_screen, text=text, font=("Calibri Bold", 12), foreground='black', background='light blue')
        error.pack()

    if len(first_name.get()) == 0 or len(last_name.get()) == 0 or len(username.get()) == 0 or len(email.get()) == 0 or \
            len(password.get()) == 0 or len(confirm.get()) == 0:
        error_label("missing required info")
    elif first_name.get().isalpha() is False:
        error_label("Invalid first name")
    elif last_name.get().isalpha() is False:
        error_label("Invalid last name")
    elif len(username.get()) > 10:
        error_label("username can't exceed 10 characters")
    elif username.get().isalnum() is False:
        error_label("username must contain only letters and numbers")
    elif len(email.get().split('@')) != 2:
        error_label("Invalid email")
    elif len(password.get()) < 6:
        error_label("password must be at least 6 characters long")
    elif password.get().isalnum() is True and (password.get().isalpha() is True or password.get().isnumeric() is True):
        error_label("password must contain letters and numbers")
    elif password.get() != confirm.get():
        error_label("password's don't match")

    else:
        user_reg = User.create_user(first_name.get(), last_name.get(), username.get(), email.get(), password.get())
        if user_reg != "Registration Completed Successfully":
            error_label(user_reg)
        return user_reg


def register():
    global reg_screen, first_name, last_name, username, email, password, confirm
    reg_screen = tk.Toplevel(screen)
    reg_screen.configure(background='light blue')
    reg_screen.title("© Battleship by Shani Daniel ©")
    reg_screen.geometry("400x350")

    first_name = tk.StringVar()
    last_name = tk.StringVar()
    username = tk.StringVar()
    email = tk.StringVar()
    password = tk.StringVar()
    confirm = tk.StringVar()

    def field(var, text):
        ttk.Label(reg_screen, text=text, font=("Calibri Bold", 12), foreground='black',
                  background='light blue').pack()
        tk.Entry(reg_screen, textvariable=var).pack()

    field(first_name, "First Name: ")
    field(last_name, "Last Name: ")
    field(username, "Username: ")
    field(email, "Email: ")
    field(password, "Password: ")
    field(confirm, "Confirm Password: ")

    ttk.Style().configure('reg2.TButton', font=('Calibri Bold', 12), foreground='black')
    ttk.Button(reg_screen, text="Register", style='reg2.TButton', command=register_user).pack(pady=15)


def menu_screen():
    window = ThemedTk(theme="arc")
    window.title("© Battleship by Shani Daniel ©")
    window.configure(background='light blue')
    ttk.Label(window, text="Welcome to Battleship", font=("Broadway", 50), foreground='black',
              background='light blue').pack(pady=50)
    window.geometry('880x540')

    def play_against_comp():
        window.withdraw()
        GameUI.play_against_comp()
        window.update()
        window.deiconify()

    def play_against_player():
        window.withdraw()
        GameUI.play_against_player()
        window.update()
        window.deiconify()

    tk.Button(window, text="Play Against Computer", font=("Cooper Black", 24),
              background="white", foreground='black', command=play_against_comp).pack(pady=10)
    tk.Button(window, text="Play Against Another Player", font=("Cooper Black", 24),
              background="white", foreground='black', command=play_against_player).pack(pady=10)
    tk.Button(window, text="Statistics", font=("Cooper Black", 24),
              background="white", foreground='black').pack(pady=10)
    tk.Label(window, text="", background='light blue').pack()
    tk.Button(window, text="Change Username", font=("Cooper Black", 12),
              background="white", foreground='black').pack(pady=5)
    tk.Button(window, text="Delete User", font=("Cooper Black", 12),
              background="white", foreground='black').pack(pady=5)

    window.mainloop()


def login_button_click():
    try:
        global incorrect
        incorrect.destroy()
    except NameError:
        pass
    GameUI.logged_in_user = User.verify_login(username_login.get(), password_login.get())
    if GameUI.logged_in_user != "Username or Password Incorrect":
        screen.destroy()
        menu_screen()
    else:
        incorrect = ttk.Label(text="Username or Password Incorrect", font=("Cooper black", 12),
                              foreground='black', background='light blue')
        incorrect.pack(pady=5)


def login_screen():
    global screen, username_login, password_login
    screen = ThemedTk(theme="arc")
    screen.geometry('880x540')
    screen.title("© Battleship by Shani Daniel ©")
    screen.configure(background='light blue')
    style_log = ttk.Style()

    ttk.Label(text='Welcome to Battleship', font=("Broadway", 50), foreground='black', background='light blue').pack(pady=40)
    ttk.Label(text='Login:', font=("Cooper black", 32), foreground='black', background='light blue').pack(pady=20)

    username_login = tk.StringVar()
    password_login = tk.StringVar()
    ttk.Label(screen, text="Username:", font=("Cooper black", 14), foreground='black',
              background='light blue').pack()
    tk.Entry(screen, textvariable=username_login).pack()
    ttk.Label(screen, text="Password:", font=("Cooper black", 14), foreground='black',
              background='light blue').pack()
    tk.Entry(screen, textvariable=password_login).pack()
    style_log.configure('log.TButton', font=('Cooper Black', 16), foreground='black')
    style_log.configure('reg.TButton', font=('Cooper Black', 13), foreground='black')
    ttk.Button(screen, text="Sign in", style='log.TButton', command=login_button_click).pack(pady=15)
    ttk.Button(screen, text="Register", style='reg.TButton', command=register).pack()

    screen.mainloop()


login_screen()
