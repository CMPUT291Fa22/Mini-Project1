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
            view_song_info(connection, cursor, username, sid)
        elif song_action_op == 3:  # Add song to playlist
            choice = add_to_playlist_ui()
            if choice == 1:  # Add to existing playlist
                add_to_existing_playlist(connection, cursor, username, sid)
            else:  # Create a new playlist
                create_new_playlist(connection, cursor, username, sid)
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
    os.system("clear")
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


#
# This function displays more information about a song according to the project specifications.
# Input: connection, cursor, username, sid
# Output: None
#
def view_song_info(connection, cursor, username, sid):
    # Get all performing artists
    cursor.execute(
        """
        SELECT artists.name
        FROM perform, artists
        WHERE perform.sid = ?
        AND perform.aid = artists.aid;""",
        (sid,),
    )
    performing_artists_list = cursor.fetchall()
    performing_artists_list = [row[0] for row in performing_artists_list]
    performing_artists_list = ", ".join(performing_artists_list)

    # Get all playlists the song is in
    cursor.execute(
        """
        SELECT playlists.title
        FROM plinclude, playlists
        WHERE plinclude.sid = ?
        AND plinclude.pid = playlists.pid;""",
        (sid,),
    )
    playlists_list = cursor.fetchall()
    playlists_list = [row[0] for row in playlists_list]
    playlists_list = ", ".join(playlists_list)

    # Get the rest of the song info
    cursor.execute(
        """
        SELECT *
        FROM songs
        WHERE sid = ?;""",
        (sid,),
    )
    song_info = cursor.fetchone()

    print("Performing Artists: {}".format(performing_artists_list))
    print("ID: {}".format(song_info[0]))
    print("Title: {}".format(song_info[1]))
    print("Duration: {}".format(song_info[2]))
    print("Playlists: {}".format(playlists_list))
    input("Press ENTER to continue!")


#
# This function continuously asks the user whether to add to existing playlist or create a new playlist
# Input: None
# Output: an integer
#         1 = Add to existing playlist
#         2 = Create new playlist
#
def add_to_playlist_ui():
    while True:
        os.system("clear")
        print(
            """(1) Add to existing playlist
(2) Create new playlist"""
        )
        choice = input()
        if choice == "1":
            return 1
        elif choice == "2":
            return 2
        else:
            input("Invalid input. Press ENTER to try again.")


#
# This function adds a song to an existing playlist
# Input: connection, cursor, username, sid
# Output: None
#
def add_to_existing_playlist(connection, cursor, username, sid):
    cursor.execute(
        """
        SELECT *
        FROM playlists
        WHERE uid = ?
        AND NOT EXISTS (
            SELECT *
            FROM plinclude
            WHERE playlists.pid = plinclude.pid
            AND plinclude.sid = ?
        );""",
        (username, sid),
    )
    playlist_list = cursor.fetchall()
    pivot = 0  # This is the starting index to display
    numEntities = len(playlist_list)
    while True:
        os.system("clear")
        pivot = 0 if pivot >= numEntities else pivot
        if not pivot >= numEntities:
            print("{}: {}|{}|{}".format(pivot, *playlist_list[pivot]))
        if not pivot + 1 >= numEntities:
            print("{}: {}|{}|{}".format(pivot + 1, *playlist_list[pivot + 1]))
        if not pivot + 2 >= numEntities:
            print("{}: {}|{}|{}".format(pivot + 2, *playlist_list[pivot + 2]))
        if not pivot + 3 >= numEntities:
            print("{}: {}|{}|{}".format(pivot + 3, *playlist_list[pivot + 3]))
        if not pivot + 4 >= numEntities:
            print("{}: {}|{}|{}".format(pivot + 4, *playlist_list[pivot + 4]))
        print("###########################################################")
        print("Type ENTER to exit.")
        print("Type in the index position + ENTER to view song.")
        print("Type space + ENTER to view next 5 entries.")
        print("###########################################################")
        cmd = input()
        if cmd == "":
            break
        elif cmd == " ":
            pivot += 5
        else:
            try:
                index = int(cmd)
                if index >= pivot and index < pivot + 5 and index < numEntities:
                    # Playlist selection is valid
                    pid = playlist_list[index][0]
                    cursor.execute(
                        """
                        SELECT MAX(sorder)
                        FROM plinclude
                        WHERE pid = ?;""",
                        (pid,),
                    )
                    sorder = cursor.fetchone()[0]
                    sorder = 0 if sorder is None else sorder
                    print(sorder)
                    cursor.execute(
                        """
                        INSERT INTO plinclude VALUES (
                            ?, ?, ?);""",
                        (pid, sid, sorder),
                    )
                    connection.commit()
                    input(
                        "Successfully added song to playlist. Press ENTER to continue."
                    )
                else:
                    # Song selection is invalid
                    print("Invalid index. Press ENTER to continue.")
                    input()
            except Exception as e:
                print("Exception Occurred. Press ENTER to continue.")
                print(e)
                input()


#
# This function adds a song to a new playlist
# Input: connection, cursor, username, sid
# Output: None
#
def create_new_playlist(connection, cursor, username, sid):
    title = input("New Playlist Title: ")
    # Get all the pids
    cursor.execute(
        """
        SELECT pid
        FROM playlists"""
    )
    pid_list = [row[0] for row in cursor.fetchall()]
    pid = 0
    while pid in pid_list:
        pid = random.randint(0, 10 ** 9)
    # Create a new playlist
    cursor.execute(
        """
        INSERT INTO playlists VALUES (
            ?, ?, ?);""",
        (pid, title, username),
    )
    # Insert song into new playlist
    cursor.execute(
        """
        INSERT INTO plinclude VALUES (
            ?, ?, 0);""",
        (pid, sid),
    )
    connection.commit()
    input("Successfully created playlist and added song. Press ENTER to continue.")
