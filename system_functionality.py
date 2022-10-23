from settings import *

keywords = []


#
# This function counts the number of keywords that match the title
# Input: The title is a string. The keyList parameter is a list of strings.
# Output: an integer
#
def countMatch(row):
    global keywords
    i = 0
    for key in keywords:
        if row[2].lower() == key.lower():
            i += 1
    return i


#
# This function is called when a user selects to view a playlist.
# Input: connection, cursor
# Output: None
#
def viewPlaylist(connection, cursor, pid):
    os.system("cls")
    cursor.execute(
        """
        SELECT songs.sid, songs.title, songs.duration
        FROM playlists, plinclude, songs
        WHERE playlists.pid = plinclude.pid
        AND plinclude.sid = songs.sid
        AND playlists.pid = ?""",
        (pid,),
    )
    plRows = cursor.fetchall()
    for row in plRows:
        print("{}|{}|{}".format(row[0], row[1], row[2]))
    input("Press ENTER to continue.")


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
            search_for_song_and_playlist(connection, cursor)
        elif sys_func_op == 3:
            pass
        elif sys_func_op == 4:
            end_current_session(connection, cursor, username)
        elif sys_func_op == 5:
            logout(connection, cursor, username)
            return
        elif sys_func_op == 6:
            exit_program(connection, cursor, username)
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
        WHERE compare(uid, ?)
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
        WHERE compare(uid, ?);""",
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
# This function searches among songs and playlists
# Input: connection, cursor
# Output: None
#
def search_for_song_and_playlist(connection, cursor):
    global keywords  # This list needs to be global because the countMatch function needs to use this list to
    # sort songs and playlists by number of matches

    print("Retrieve songs and playlists by keywords. Separate keywords using space.")
    keywords = input().split()

    # Get all the songs that match list of keywords
    cursor.execute(
        """
        SELECT "song", sid, title, duration
        FROM songs
        WHERE {};""".format(
            " OR ".join(["match(title, '{}')".format(kw) for kw in keywords])
        )
    )
    song_rows = cursor.fetchall()
    # for row in song_rows:
    #     print("{}|{}|{}|{}".format(row[0], row[1], row[2], row[3]))

    # Get all playlists that match list of keywords
    cursor.execute(
        """
        SELECT "playlist", playlists.pid, playlists.title, SUM(songs.duration)
        FROM playlists, plinclude, songs
        WHERE playlists.pid = plinclude.pid
        AND plinclude.sid = songs.sid
        AND ({})
        GROUP BY playlists.pid""".format(
            " OR ".join(["match(playlists.title, '{}')".format(kw) for kw in keywords])
        )
    )
    playlist_rows = cursor.fetchall()
    # for row in playlist_rows:
    #     print("{}|{}|{}|{}".format(row[0], row[1], row[2], row[3]))

    # Combine the songs and playlists
    songs_and_playlists_rows = []
    for song in song_rows:
        songs_and_playlists_rows.append(song)
    for playlist in playlist_rows:
        songs_and_playlists_rows.append(playlist)
    songs_and_playlists_rows.sort(reverse=True, key=countMatch)

    # Display query in paginated downward format
    pivot = 0  # This is the starting index to display
    numEntities = len(songs_and_playlists_rows)
    while True:
        os.system("cls")
        pivot = 0 if pivot >= numEntities else pivot
        if not pivot >= numEntities:
            print("{}: {}|{}|{}|{}".format(pivot, *songs_and_playlists_rows[pivot]))
        if not pivot + 1 >= numEntities:
            print(
                "{}: {}|{}|{}|{}".format(
                    pivot + 1, *songs_and_playlists_rows[pivot + 1]
                )
            )
        if not pivot + 2 >= numEntities:
            print(
                "{}: {}|{}|{}|{}".format(
                    pivot + 2, *songs_and_playlists_rows[pivot + 2]
                )
            )
        if not pivot + 3 >= numEntities:
            print(
                "{}: {}|{}|{}|{}".format(
                    pivot + 3, *songs_and_playlists_rows[pivot + 3]
                )
            )
        if not pivot + 4 >= numEntities:
            print(
                "{}: {}|{}|{}|{}".format(
                    pivot + 4, *songs_and_playlists_rows[pivot + 4]
                )
            )
        print("Press ENTER to exit.")
        print("Type in the index position + ENTER to view song/playlist.")
        print("Press space to view next 5.")
        cmd = input()
        if cmd == "":
            break
        elif cmd == " ":
            pivot += 5
        else:
            try:
                index = int(cmd)
                if index >= pivot and index < pivot + 5 and index < numEntities:
                    # Song/Playlist selection is valid
                    if songs_and_playlists_rows[index][0] == "song":
                        # Perform a song action
                        pass
                    else:
                        viewPlaylist(
                            connection, cursor, songs_and_playlists_rows[index][1]
                        )
                else:
                    # Song/Playlist selection is invalid
                    print("Invalid index. Press ENTER to continue.")
                    input()
            except:
                print("Invalid input. Press ENTER to continue.")
                input()


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
        WHERE compare(uid, ?)
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
        WHERE compare(uid, ?)
        AND end IS NULL;""",
        (current_date, username),
    )
    connection.commit()


#
# This function directly quits the program
# Input: connection, cursor, username
# Output: None
#
def exit_program(connection, cursor, username):
    current_date = time.strftime("%Y-%m-%d %H:%M:%S")

    # Close all active sessions
    cursor.execute(
        """
        UPDATE sessions SET end = ?
        WHERE compare(uid, ?)
        AND end IS NULL;""",
        (current_date, username),
    )
    connection.commit()
    connection.close()

    os.system("cls")
    quit()
