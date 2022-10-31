from settings import *


#
# This function will continuously ask the user for song operations.
# Input: connection, cursor, username
# Output: None
#
def song_action(connection, cursor, username, sid):
    while True:
        song_action_op = song_action_ui(connection, cursor)
        if song_action_op == 1:  # Listen to song
            listen_to_song(connection, cursor, username, sid)
        elif song_action_op == 2:  # See more information about song
            pass
        elif song_action_op == 3:  # Add song to playlist
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
def listen_to_song(connection, cursor, username, sid):
    cursor.execute(
        """
        SELECT COUNT(*)
        FROM sessions
        WHERE compare(uid, ?)
        AND end IS NULL;""",
        (username,),
    )
    num_of_active_sessions = cursor.fetchone()[0]
    active_sno = 0
    if num_of_active_sessions > 0:
        cursor.execute(
            """
            SELECT sno
            FROM sessions
            WHERE compare(uid, ?)
            AND end IS NULL;""",
            (username,),
        )
        active_sno = cursor.fetchone()[0]
    else:
        current_date = time.strftime("%Y-%m-%d %H:%M:%S")
        # Create a unique session number (sno)
        cursor.execute(
            """
            SELECT sno
            FROM sessions
            WHERE compare(uid, ?);""",
            (username,),
        )
        user_sessions = cursor.fetchall()
        user_sessions = [row[0] for row in user_sessions]
        while active_sno in user_sessions:
            active_sno = random.randint(0, 10 ** 9)
        # Add a new session
        cursor.execute(
            """
            INSERT INTO sessions(uid, sno, start, end) VALUES (
                ?, ?, ?, NULL);""",
            (username, active_sno, current_date),
        )
        connection.commit()
    # Check if user already listened to song in the active session
    cursor.execute(
        """
        SELECT sid
        FROM listen
        WHERE compare(uid, ?)
        AND sno = ?
        AND sid = ?;""",
        (username, active_sno, sid),
    )
    listening_to_song_list = cursor.fetchall()
    if len(listening_to_song_list) > 0:
        cursor.execute(
            """
            UPDATE listen SET cnt = cnt + 1
            WHERE compare(uid, ?)
            AND sno = ?
            AND sid = ?;""",
            (username, active_sno, sid),
        )
        connection.commit()
    else:
        cursor.execute(
            """
            INSERT INTO listen
            VALUES (?, ?, ?, 1);""",
            (username, active_sno, sid),
        )
        connection.commit()
