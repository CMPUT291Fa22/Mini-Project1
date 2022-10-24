from settings import *
from login_screen import *
from system_functionality import *

#
# This is a user-defined function that compares two strings non case-sensitively
# Input: two strings a and b
# Output: a boolean
#
def compare(a, b):
    return a.lower() == b.lower()


#
# This is a user-defined function that checks for keyword matches
# Inputs: a and b are strings
# Outputs: a boolean
#
def match(a, b):
    if a is None:
        return False
    if b is None:
        return False
    if b.lower() in a.lower():
        return True
    return False


#
# This function returns the number of matching keywords that match artist name or song title
# Input: a is a string, b is a string representing space-separated keywords
# Output: an integer representing number of matches
#
def count_artist_match(name, title, b):
    keywords = b.split()
    i = 0
    for key in keywords:
        if key.lower() in name.lower():
            i += 1
            continue
        if key.lower() in title.lower():
            i += 1
            continue
    return i


def connect(path):
    global connection, cursor

    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    cursor.execute(" PRAGMA foreign_keys=ON; ")
    connection.commit()

    connection.create_function("compare", 2, compare)
    connection.create_function("match", 2, match)
    connection.create_function("count_artist_match", 3, count_artist_match)
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
                input("Press ENTER to continue: ")
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
