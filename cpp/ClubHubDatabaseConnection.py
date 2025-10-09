import mariadb
import os
from mariadb._mariadb import cursor


def __main__():
    try:
        conn = mariadb.connect(
            user="clubhub_user",
            password="GatorClubHub2025!",
            host="localhost",
            port=3306,
            database="ClubHub"
        )
        cursor = conn.cursor()
        print("Connected to MariaDB")

    except mariadb.Error as e:
        print(f"Error Connecting: {e}")


#adding a user to the database // incomplete
def add_user(ufid, name, email, permission = 0):
    #check to see if unique ufid
    cursor.execute("SELECT ufid FROM users WHERE ufid = ?")
    result = cursor.fetchall()

    if len(result) == 0:
        # inserting user into table
        cursor.execute(
            "INSERT INTO Users(ufid, name, email, permission) VALUES (?, ?, ?, ?)"
        )

if __name__ == "__main__":
    __main__()
