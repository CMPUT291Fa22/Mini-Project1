from settings import *

#
# This function gets the login credentials
# Input: connection, cursor
# Output: an integer
#         0 meaning credentials do not exist
#         1 meaning to log in as a user
#         2 meaning to log in as an artist
#
def login(connection, cursor):

    username = input("Username: ")
    password = getpass.getpass("Password: ")

    username = username.lower()
    userLoginBool = False
    artistLoginBool = False

    # Check that credentials are in the users table
    cursor.execute(
        """
        SELECT uid, pwd
        FROM users
        WHERE uid == ?
        AND pwd == ?;""",
        (
            username,
            password,
        ),
    )
    userRows = cursor.fetchall()
    if len(userRows) > 0:
        userLoginBool = True

    # Check that credentials are in the artists table
    cursor.execute(
        """
        SELECT aid, pwd
        FROM artists
        WHERE aid == ?
        AND pwd == ?;""",
        (username, password),
    )
    artistRows = cursor.fetchall()
    if len(artistRows) > 0:
        artistLoginBool = True

    if userLoginBool:
        if artistLoginBool:
            print(
                """
Press 1 to login as a user
Press 2 to login as an artist
"""
            )
            while True:
                selection = input()
                if selection == "1":
                    # Logging in as a user
                    return 1
                elif selection == "2":
                    # Loggin in as an artist
                    return 2
                else:
                    print("You must type either 1 or 2")
        else:
            # Logging in as a user
            return 1
    else:
        if artistLoginBool:
            # Logging in as an artist
            return 2
        else:
            # Log in credentials do not exist in the database
            return 0

    connection.commit()
