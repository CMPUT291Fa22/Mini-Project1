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
            end_current_session(connection, cursor, username)
        elif sys_func_op == 5:
            logout(connection, cursor, username)
            return
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
        os.system("cls")
        print(
            """System Functionality Operations:
(1) Start a session
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
# Input: connection, cursor, username
# Output: None
#
def start_new_session(connection, cursor, username):
    # Check that there isn't an active session
    cursor.execute(
        """
        SELECT COUNT(*)
        FROM sessions
        WHERE uid == ?
        AND end IS NULL;""",
        (username,),
    )
    num_of_active_sessions = cursor.fetchone()[0]
    if num_of_active_sessions > 0:
        print(
            "A session is currently active. Please close all active sessions before creating a new session."
        )
        input("Press enter to continue!")
        return

    current_date = time.strftime("%Y-%m-%d %H:%M:%S")

    # Create a unique session number (sno)
    cursor.execute(
        """
        SELECT COUNT(sno)
        FROM sessions
        WHERE uid == ?;""",
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
    input("Session created successfully. Press enter to continue.")
    connection.commit()


#
# This function ends the current active session
# Input: connection, cursor, username
# Output: None
#
def end_current_session(connection, cursor, username):
    current_date = time.strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute(
        """
        UPDATE sessions SET end = ?
        WHERE uid == ?
        AND end IS NULL;""",
        (current_date, username),
    )
    connection.commit()
    input("Session ended successfully. Press enter to continue.")


#
# This function logs out the current user
# Input: connection, cursor, username
# Output: None
#
def logout(connection, cursor, username):
    current_date = time.strftime("%Y-%m-%d %H:%M:%S")

    # Close all active sessions
    cursor.execute(
        """
        UPDATE sessions SET end = ?
        WHERE uid == ?
        AND end IS NULL;""",
        (current_date, username),
    )
    connection.commit()
