from settings import *


#
# This function will continuously ask the user for song operations.
# Input: connection, cursor, username
# Output: None
#
def song_action(connection, cursor, username):
    while True:
        song_action_op = song_action_ui(connection, cursor)
        if song_action_op == 1:
            pass
        elif song_action_op == 2:
            pass
        elif song_action_op == 3:
            pass
        elif song_action_op == 4:
            return
        else:
            pass


#
# This function creates a prompt to perform song actions.
# Input: connection, cursor
# Output: a number where
#         1 means to listen to a song
#         2 means to see more information about a song
#         3 means to add a song to playlist
#         4 means to go back
#
def song_action_ui(connection, cursor):
    os.system("cls")
    print(
        """(1) Listen to song
(2) See more information about song
(3) Add song to playlist
(4) Back"""
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
    else:
        print("Invalid input.")
        return -1


#
# This function listens to song according to project specifications.
# Input: connection, cursor, username
# Output: None
#
def listen_to_song(connection, cursor, username):
    pass
