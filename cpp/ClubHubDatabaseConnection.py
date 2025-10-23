import mariadb
from dotenv import load_dotenv
import os
from mariadb._mariadb import cursor


def __main__():
    try:
        load_dotenv()

        print("users:", os.getenv("DB_USER"))
        print("password repr:", repr(os.getenv("DB_PASSWORD")))
        print("host:", os.getenv("DB_HOST"))
        print("port:", os.getenv("DB_PORT"))

        conn = mariadb.connect(
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=int(os.getenv("DB_PORT")),
            database=os.getenv("DB_DATABASE"),
            ssl=True
        )
        cursor = conn.cursor()
        print("Connected to MariaDB")

    except mariadb.Error as e:
        print(f"Error Connecting: {e}")

#I think eventually when we connect to django we will want to use an infinite while loop waiting for data requests.
#   while True:
  #      if #input == 'add user':
            #add_user()


#adding a user to the database // incomplete
def add_user(ufid, name, email, permission = 0):
    #add input validation
    #check to see if unique ufid
    cursor.execute("SELECT ufid FROM users WHERE ufid = ?")
    result = cursor.fetchall()

    if len(result) == 0:
        # inserting user into table
        cursor.execute(
            "INSERT INTO Users(ufid, name, email, permission) VALUES (?, ?, ?, ?)"
        )

#def remove_user(ufid_1, ufid_2, permissions):

#add user to a club by updating the membership table
#def assign_member(ufid, club_name, date_joined, position):
    #1) check to see if touple already exists in the table
    #2) input validation(ufid exists, club_name exists, date joined is current, position is valid)
    #3) insert member into table
    #return 0 for success and 1 for fail

#def remove_member(ufid_1, club_name, ufid_2, permission):

#add clubs to database
#could auto increment permissions with an associated club and whoever holds that number has exec permissions
#def add_club(club_name, exec_ufid, category):
    # 1) input validation (check to see if club exists, match id to users
    # 2) The id associated with the club will be assigned upon validation of position as exec(requires submission of proof)

#make an announcement for clubs only
#def add_announcement(title, content, posted_at, club_name):
    # the key auto-increments in mariadb but idk whether to use an int or not
    # 1) input validation(club exists, figure out datetime data type, message size)
    # 2) add instance to announcement table

#create an event
#def add_event(title, description, event_datetime, club_name):
    # input validation, add to event table



if __name__ == "__main__":
    __main__()
