import sqlite3
import os
connection = None
cursor = None
username = 'Lady Gaga'
title = ''
duration =''

def connect(path):
    global connection, cursor

    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    cursor.execute(' PRAGMA foreign_keys=ON; ')
    connection.commit()
    return

def getaid():
    global connection, cursor, username
    cursor.execute("SELECT aid FROM artists WHERE name = ?", [username])
    aid = cursor.fetchone()[0]
    return aid

def addsongs():
    global connection, cursor, username, title, duration
    aid = getaid()
    cursor.execute("SELECT sid FROM songs ORDER BY sid DESC")
    sid = cursor.fetchone()[0]
    uniquesid = sid + 1
    cursor.execute("INSERT INTO songs(sid, title, duration) VALUES (?, ?, ?)",(uniquesid, title, duration))
    cursor.execute('INSERT INTO perform (aid, sid) VALUES (?,?);', (aid,uniquesid))
    os.system("cls")
    otherartist = input("Any additional artists? If dose, input the additional artist's id, otherwise input 'no' to back to the menu\nYour input: ")
    while True:
        if otherartist.lower() == 'no':
            connection.commit()
            break
        elif otherartist.lower() == aid:
            os.system("cls")
            otherartist = input("This is your id, please input other's id or 'no' to back to the menu\nYour input: ")
        else:
            cursor.execute("SELECT COUNT(*) FROM artists WHERE ? = artists.aid" ,[otherartist])
            check = cursor.fetchone()[0]
            if check == 0:
                os.system("cls")
                otherartist = input("This artist is not in our database, please input valid id or 'no' to back to the menu\nYour input: ")
            else:
                cursor.execute('INSERT INTO perform (aid, sid) VALUES (?,?);', (otherartist,uniquesid))
                connection.commit()
                break

def rank():
    global connection, cursor, username, title, duration
    aid = getaid()
    cursor.execute("SELECT playlists.pid FROM playlists, plinclude, artists, perform, songs WHERE ? = artists.aid and artists.aid = perform.aid and perform.sid = songs.sid and songs.sid = plinclude.sid and plinclude.pid = playlists.pid GROUP BY playlists.pid ORDER BY COUNT(songs.sid) DESC LIMIT 3",[aid])
    topplaylist = cursor.fetchall()
    cursor.execute("SELECT listen.uid, sum(listen.cnt*songs.duration) FROM listen, artists, perform, songs WHERE ? = artists.aid and artists.aid = perform.aid and perform.sid = listen.sid and perform.sid = songs.sid and songs.sid = listen.sid GROUP BY listen.uid ORDER BY sum(listen.cnt*songs.duration) DESC LIMIT 3", [aid])
    topplistener = cursor.fetchall()
    print("Top 3 playlists which includes your songs")
    print(topplaylist)
    print("Top 3 users that listen to your songs")
    print(topplistener)

def Artists():
    global connection, cursor, username, title, duration
    aid = getaid()
    while True:
        os.system("cls")
        input1 = input("Please input command 'add' for adding a song or 'rank' to find the top fans and playlists or 'logout'\nYour input: ")
        if input1.lower() == 'add':
            os.system("cls")
            title = input("Please input the song tilte \nTitle: ")
            os.system("cls")
            duration = input("Please input the song duration \nDuration: ")
            cursor.execute("SELECT COUNT(*) FROM perform, songs WHERE ? = perform.aid and perform.sid = songs.sid and songs.title = ? and songs.duration = ?" ,(aid, title, duration))
            count = cursor.fetchone()[0]
            if count == 0:#check this song is already exist for the current artist or not
               addsongs()
            else:
                os.system("cls")
                warning = input("You already have a song with same tile and duration, input 'c' to continue or any key to back to the menu\nYour input: ")
                if warning.lower() == 'c':
                    addsongs()
                else:
                    None
        elif input1.lower() == 'rank':
            os.system("cls")
            rank()
        elif input1.lower() ==  'logout':#logout. Logging
            exit()
        else:
            print("Wrong command")


def main():
    path = "./a2.db"
    connect(path)
    Artists()

if __name__ == "__main__":
    main()