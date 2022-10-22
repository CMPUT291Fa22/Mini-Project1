from settings import *
from login_screen import *
from system_functionality import *


def connect(path):
    global connection, cursor

    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    cursor.execute(" PRAGMA foreign_keys=ON; ")
    connection.commit()
    return


def main():
    global connection, cursor

    os.system("cls")
    dbString = input("Database Name: ")
    path = "./" + dbString
    connect(path)

    while True:
        selection = main_screen(connection, cursor)
        if selection == 1:  # Login
            loginType, username = login(connection, cursor)
            if loginType == 0:
                print("Cannot find account matching these credentials.")
            elif loginType == 1:
                # Invoke the system functionalities UI
                sys_func(connection, cursor, username)
            else:  # loginType == 2:
                # Invoke the artist actions UI
                pass
        elif selection == 2:  # Sign up
            username = sign_up(connection, cursor)
            sys_func(connection, cursor, username)
        else:
            os.system("cls")
            break

    connection.commit()
    connection.close()


if __name__ == "__main__":
    main()
