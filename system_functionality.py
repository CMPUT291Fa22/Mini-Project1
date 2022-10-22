from settings import *

#
# This function creates a prompt to perform system functionality operations.
# Input: connection, cursor
# Output: a number where
#         1 means to start a session
#         2 means to search for songs and playlists
#         3 means to search for artists
#         4 means to end the session
#         5 means to log out
#
def sys_func_ui(connection, cursor):
    while True:
        print(
            """(1) Start a session
(2) Search for songs and playlists
(3) Search for artists
(4) End the session
(5) Log out
(6) Exit Program"""
        )
        option = input()
        if option == "1":
            return 1
        elif option == "2":
            return 2
        elif option == "3":
            return 3
        elif option == "4":
            return 4
        elif option == "5":
            return 5
        elif option == "6":
            return 6
        else:
            print("Invalid input.")
