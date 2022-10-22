from settings import *

#
# This function will continuously ask the user for system functionality operations.
# Input: connection, cursor, username
# Output: None
#
def sys_func(connection, cursor, username):
    while True:
        sys_func_op = sys_func_ui(connection, cursor)
        if sys_func_op == 1:
            start_new_session(connection, cursor, username)
        elif sys_func_op == 2:
            pass
        elif sys_func_op == 3:
            pass
        elif sys_func_op == 4:
            pass
        elif sys_func_op == 5:
            pass
        elif sys_func_op == 6:
            pass
        else:
            pass


#
# This function creates a prompt to perform system functionality operations.
# Input: connection, cursor
# Output: a number where
#         1 means to start a session
#         2 means to search for songs and playlists
#         3 means to search for artists
#         4 means to end the session
#         5 means to log out
#         6 means to exit the program directly
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


#
# This function starts a new session
# Input: connection, cursor
# Output: None
#
def start_new_session(connection, cursor, username):
    current_date = time.strftime("%Y-%m-%d %H:%M:%S")

    # Create a unique session number (sno)
    cursor.execute(
        """
        SELECT COUNT(sno)
        FROM sessions
        WHERE uid == ?""",
        (username,),
    )
    sno = cursor.fetchone()[0]  # The sno will just be the current number of sessions

    # Add a new session
    cursor.execute(
        """
        INSERT INTO sessions(uid, sno, start, end) VALUES (
            ?, ?, ?, NULL);""",
        (username, sno, current_date),
    )
    connection.commit()
