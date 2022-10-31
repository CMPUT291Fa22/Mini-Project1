from settings import *
from song_actions import *

keywords = []


#
# This function counts the number of keywords that match the title of a song or playlist
# Input: Row is a tuple representing song or playlist information
# Output: an integer representing number of matches
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
def viewPlaylist(connection, cursor, pid, username):
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
    # Display query in paginated downward format
    pivot = 0  # This is the starting index to display
    numEntities = len(plRows)
    while True:
        os.system("cls")
        pivot = 0 if pivot >= numEntities else pivot
        if not pivot >= numEntities:
            print("{}: {}|{}|{}".format(pivot, *plRows[pivot]))
        if not pivot + 1 >= numEntities:
            print("{}: {}|{}|{}".format(pivot + 1, *plRows[pivot + 1]))
        if not pivot + 2 >= numEntities:
            print("{}: {}|{}|{}".format(pivot + 2, *plRows[pivot + 2]))
        if not pivot + 3 >= numEntities:
            print("{}: {}|{}|{}".format(pivot + 3, *plRows[pivot + 3]))
        if not pivot + 4 >= numEntities:
            print("{}: {}|{}|{}".format(pivot + 4, *plRows[pivot + 4]))
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
                    # Song selection is valid
                    song_action(connection, cursor, username)
                else:
                    # Song selection is invalid
                    print("Invalid index. Press ENTER to continue.")
                    input()
            except Exception as e:
                print("Exception Occurred. Press ENTER to continue.")
                print(e)
                input()


#
# This function is called when the user selects to view the artist
# Input: connection, cursor, name is a string, nationality is a string
# Output: None
#
def view_artist(connection, cursor, name, nationality, username):
    os.system("cls")
    cursor.execute(
        """
        SELECT artists.aid, songs.title, songs.duration
        FROM artists, perform, songs
        WHERE artists.aid = perform.aid
        AND perform.sid = songs.sid
        AND artists.name = ?
        AND artists.nationality = ?;""",
        (
            name,
            nationality,
        ),
    )
    a_rows = cursor.fetchall()

    pivot = 0  # This is the starting index to display
    numEntities = len(a_rows)
    while True:
        os.system("cls")
        pivot = 0 if pivot >= numEntities else pivot
        if not pivot >= numEntities:
            print("{}: {}|{}|{}".format(pivot, *a_rows[pivot]))
        if not pivot + 1 >= numEntities:
            print("{}: {}|{}|{}".format(pivot + 1, *a_rows[pivot + 1]))
        if not pivot + 2 >= numEntities:
            print("{}: {}|{}|{}".format(pivot + 2, *a_rows[pivot + 2]))
        if not pivot + 3 >= numEntities:
            print("{}: {}|{}|{}".format(pivot + 3, *a_rows[pivot + 3]))
        if not pivot + 4 >= numEntities:
            print("{}: {}|{}|{}".format(pivot + 4, *a_rows[pivot + 4]))
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
                    # Song selection is valid
                    song_action(connection, cursor, username)
                else:
                    # Song selection is invalid
                    print("Invalid index. Press ENTER to continue.")
                    input()
            except Exception as e:
                print("Exception Occurred. Press ENTER to continue.")
                print(e)
                input()


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
            search_for_song_and_playlist(connection, cursor, username)
        elif sys_func_op == 3:
            search_for_artists(connection, cursor, username)
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
            return -1


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
        SELECT sno
        FROM sessions
        WHERE compare(uid, ?);""",
        (username,),
    )
    user_sessions = cursor.fetchall()
    user_sessions = [row[0] for row in user_sessions]
    sno = 0
    while sno in user_sessions:
        sno = random.randint(0, 10 ** 9)

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
# This function searches for songs and playlists
# Input: connection, cursor
# Output: None
#
def search_for_song_and_playlist(connection, cursor, username):
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
        print("###########################################################")
        print("Type ENTER to exit.")
        print("Type in the index position + ENTER to view song/playlist.")
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
                    # Song/Playlist selection is valid
                    if songs_and_playlists_rows[index][0] == "song":
                        # Perform a song action
                        song_action(connection, cursor, username)
                    else:
                        viewPlaylist(
                            connection,
                            cursor,
                            songs_and_playlists_rows[index][1],
                            username,
                        )
                else:
                    # Song/Playlist selection is invalid
                    print("Invalid index. Press ENTER to continue.")
                    input()
            except Exception as e:
                print("Exception Occurred. Press ENTER to continue.")
                print(e)
                input()


#
# This function searches for artists
# Input: connection, cursor
# Output: None
#
def search_for_artists(connection, cursor, username):
    global keywords

    print(
        "Retrieve artists from their name or song titles by keywords. Separate keywords using space."
    )
    keywords = input().split()

    # Get all the artists that match list of keywords
    cursor.execute(
        """
        SELECT artists.name, artists.nationality, COUNT(songs.sid)
        FROM artists, perform, songs
        WHERE artists.aid = perform.aid
        AND perform.sid = songs.sid
        AND artists.aid IN (
            SELECT artists.aid
            FROM artists, perform, songs
            WHERE artists.aid = perform.aid
            AND perform.sid = songs.sid
            AND ({} OR {})
        )
        AND artists.name IS NOT NULL
        AND songs.title IS NOT NULL
        GROUP BY artists.name, artists.nationality
        ORDER BY count_artist_match(artists.name, songs.title, '{}') DESC""".format(
            " OR ".join(["match(artists.name, '{}')".format(kw) for kw in keywords]),
            " OR ".join(["match(songs.title, '{}')".format(kw) for kw in keywords]),
            " ".join(keywords),
        )
    )
    artist_rows = cursor.fetchall()
    pivot = 0  # This is the starting index to display
    numEntities = len(artist_rows)
    while True:
        os.system("cls")
        pivot = 0 if pivot >= numEntities else pivot
        if not pivot >= numEntities:
            print("{}: {}|{}|{}".format(pivot, *artist_rows[pivot]))
        if not pivot + 1 >= numEntities:
            print("{}: {}|{}|{}".format(pivot + 1, *artist_rows[pivot + 1]))
        if not pivot + 2 >= numEntities:
            print("{}: {}|{}|{}".format(pivot + 2, *artist_rows[pivot + 2]))
        if not pivot + 3 >= numEntities:
            print("{}: {}|{}|{}".format(pivot + 3, *artist_rows[pivot + 3]))
        if not pivot + 4 >= numEntities:
            print("{}: {}|{}|{}".format(pivot + 4, *artist_rows[pivot + 4]))
        print("###########################################################")
        print("Type ENTER to exit.")
        print("Type in the index position + ENTER to view artist.")
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
                    # Artist selection is valid
                    view_artist(
                        connection, cursor, artist_rows[index][0], artist_rows[index][1]
                    )
                else:
                    # Song/Playlist selection is invalid
                    print("Invalid index. Press ENTER to continue.")
                    input()
            except Exception as e:
                print("Exception Occurred. Press ENTER to continue.")
                print(e)
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
