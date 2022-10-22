import sqlite3
import time

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
    password = input("Password: ")

    username = username.lower()

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
    rows = cursor.fetchall()
    print(len(rows))

    # Check that credentials are in the artists table
    cursor.execute(
        """
        SELECT aid, pwd
        FROM artists
        WHERE aid == ?
        AND pwd == ?;""",
        (username, password),
    )
    rows = cursor.fetchall()
    print(len(rows))


def main():
    global connection, cursor

    dbString = input("Database Name: ")
    path = "./" + dbString
    connect(path)

    login()


if __name__ == "__main__":
    main()
