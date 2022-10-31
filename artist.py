from settings import *

# def connect(path):
#     global connection, cursor

#     connection = sqlite3.connect(path)
#     cursor = connection.cursor()
#     cursor.execute(" PRAGMA foreign_keys=ON; ")
#     connection.commit()
#     return


def getaid(connection, cursor, username):
    # global connection, cursor, username
    cursor.execute(
        """
        SELECT aid
        FROM artists
        WHERE compare(aid, ?)
        """,
        [username],
    )
    aid = cursor.fetchone()[0]
    return aid


def addsongs(connection, cursor, username, title, duration):
    # global connection, cursor, username, title, duration
    aid = getaid(connection, cursor, username)
    cursor.execute(
        """SELECT sid
        FROM songs
        ORDER BY sid DESC"""
    )
    sid = cursor.fetchone()[0]
    uniquesid = sid + 1
    cursor.execute(
        """INSERT INTO songs(sid, title, duration) VALUES
            (?, ?, ?);""",
        (uniquesid, title, duration),
    )
    cursor.execute(
        """INSERT INTO perform (aid, sid) VALUES
                        (?, ?);""",
        (aid, uniquesid),
    )
    os.system("clear")
    otherartist = input(
        "Any additional artists? If dose, input the additional artist's id, otherwise input 'no' to back to the menu\nYour input: "
    )
    while True:
        if otherartist.lower() == "no":
            connection.commit()
            break
        elif otherartist.lower() == aid:
            os.system("clear")
            otherartist = input(
                "This is your id, please input other's id or 'no' to back to the menu\nYour input: "
            )
        else:
            cursor.execute(
                "SELECT COUNT(*) FROM artists WHERE artists.aid = ?", [otherartist]
            )
            check = cursor.fetchone()[0]
            if check == 0:
                os.system("clear")
                otherartist = input(
                    "This artist is not in our database, please input valid id or 'no' to back to the menu\nYour input: "
                )
            else:
                cursor.execute(
                    "INSERT INTO perform (aid, sid) VALUES (?,?);",
                    (otherartist, uniquesid),
                )
                connection.commit()
                break


def rank(connection, cursor, username):
    # global connection, cursor, username, title, duration
    aid = getaid(connection, cursor, username)
    cursor.execute(
        """
        SELECT playlists.pid, playlists.title
        FROM playlists, plinclude, artists, perform, songs
        WHERE artists.aid = ?
        AND artists.aid = perform.aid
        AND perform.sid = songs.sid
        AND songs.sid = plinclude.sid
        AND plinclude.pid = playlists.pid
        GROUP BY playlists.pid ORDER BY COUNT(songs.sid) DESC LIMIT 3;
        """,
        [aid],
    )
    topplaylist = cursor.fetchall()
    cursor.execute(
        """
        SELECT listen.uid, users.name
        FROM listen, artists, perform, songs, users
        WHERE artists.aid = ?
        AND artists.aid = perform.aid
        AND perform.sid = listen.sid
        AND listen.sid = songs.sid
        AND listen.uid = users.uid
        GROUP BY listen.uid
        ORDER BY sum(listen.cnt*songs.duration) DESC LIMIT 3;
        """,
        [aid],
    )
    topplistener = cursor.fetchall()
    print("Top 3 playlists which includes your songs")
    for row in topplaylist:
        print("{}|{}".format(*row))
    # print(topplaylist)
    print("Top 3 users that listen to your songs")
    for row in topplistener:
        print("{}|{}".format(*row))
    input("Press ENTER to continue: ")


def Artists(connection, cursor, username):
    # global connection, cursor, username, title, duration
    aid = getaid(connection, cursor, username)
    while True:
        os.system("clear")
        input1 = input(
            """Artist Operations:
(1) Add a song
(2) Find the top fans and playlists
(3) Logout\n"""
        )
        if input1 == "1":
            os.system("clear")
            title = input("Please input the song title \nTitle: ")
            os.system("clear")
            duration = input("Please input the song duration \nDuration: ")
            cursor.execute(
                """
                SELECT COUNT(*)
                FROM perform, songs
                WHERE perform.aid = ?
                AND perform.sid = songs.sid
                AND compare(songs.title, ?)
                AND songs.duration = ?;""",
                (aid, title, duration),
            )
            count = cursor.fetchone()[0]
            if (
                count == 0
            ):  # check this song is already exist for the current artist or not
                addsongs(connection, cursor, username, title, duration)
            else:
                os.system("clear")
                warning = input(
                    "You already have a song with same tile and duration, input 'c' to continue or any key to back to the menu\nYour input: "
                )
                if warning.lower() == "c":
                    addsongs(connection, cursor, username, title, duration)
                else:
                    pass
        elif input1 == "2":
            os.system("clear")
            rank(connection, cursor, username)
        elif input1 == "3":  # logout. Logging
            return
        else:
            print("Wrong command")


# def main():
#     path = "./a2.db"
#     connect(path)
#     Artists()

# if __name__ == "__main__":
#     main()
