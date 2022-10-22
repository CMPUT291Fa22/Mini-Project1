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


def main():
    global connection, cursor

    dbString = input("Database Name: ")
    path = "./" + dbString
    connect(path)


if __name__ == "__main__":
    main()
