import sqlite3
import time
import getpass

from sympy import false, true

connection = None
cursor = None


def connect(path):
    global connection, cursor

    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    cursor.execute(" PRAGMA foreign_keys=ON; ")
    connection.commit()
    return


def login():
    global connection, cursor

    username = input("Username: ")
    password = getpass.getpass("Password: ")

    username = username.lower()
    userLoginBool = false
    artistLoginBool = false

    # Check that credentials are in the users table
    cursor.execute(
        """
        SELECT uid, pwd
        FROM users
        WHERE uid == ?
        AND pwd == ?;""",
        (
            username,
            password,
        ),
    )
    userRows = cursor.fetchall()
    if len(userRows) > 0:
        userLoginBool = true

    # Check that credentials are in the artists table
    cursor.execute(
        """
        SELECT aid, pwd
        FROM artists
        WHERE aid == ?
        AND pwd == ?;""",
        (username, password),
    )
    artistRows = cursor.fetchall()
    if len(artistRows) > 0:
        artistLoginBool = true

    print(userLoginBool)
    print(artistLoginBool)


def main():
    global connection, cursor

    dbString = input("Database Name: ")
    path = "./" + dbString
    connect(path)

    login()


if __name__ == "__main__":
    main()
