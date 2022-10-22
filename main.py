from settings import *
from login_screen import *


def connect(path):
    global connection, cursor

    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    cursor.execute(" PRAGMA foreign_keys=ON; ")
    connection.commit()
    return


def main():
    global connection, cursor

    dbString = input("Database Name: ")
    path = "./" + dbString
    connect(path)

    while True:
        selection = main_screen(connection, cursor)
        if selection == 1:  # Login
            loginType = login(connection, cursor)
        else:  # Sign up
            sign_up(connection, cursor)


if __name__ == "__main__":
    main()
