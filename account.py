import constants
import os
import sqlite3
from time import sleep

def conClear ():
    print(f"{constants.White}{constants.Reset}Clearing.", end="")
    print("\r", end="")
    sleep(0.3)
    print("Clearing..", end="")
    print("\r", end="")
    sleep(0.3)
    print("Clearing...", end="")
    print("\r", end="")
    sleep(0.3)
    os.system('cls' if os.name == 'nt' else 'clear')
    
class Accounts ():
    def __init__(self, username, password):
        self.user = username
        self.pasW = password

    def login (self):
        print(constants.White)
        connection = sqlite3.connect("accountsdb")
        cursor_object = connection.execute("SELECT password FROM AccountList WHERE username=?",(str(self.user),))

        data = cursor_object.fetchone()
        
        connection.close()
        
        if data is None:
            print(f"That is not a valid username")
            return False

        if (data is not None) and (str(data) == f"({self.pasW},)"):
            print(f"Login successful.")
            global curUser
            curUser = self.user
            global userExist
            userExist = True
            
            return True
        else:
            print("I'm sorry, that is incorrect")
            return False

    def signup (self):
        while True:
            connection = sqlite3.connect("accountsdb")

            user = input("What is your new username?: ")
            
            cursor_object = connection.execute("SELECT password FROM AccountList WHERE username=?", (str(user),))
            
            data = cursor_object.fetchall()
            
            while user.lower() == "guest" or len(data) != 0:
              cursor_object = connection.execute("SELECT password FROM AccountList WHERE username=?", (str(user),))

              data = cursor_object.fetchall()
              
              if len(data) == 0 or user.lower() == "guest":
                  print("That is not a valid username! Please try again.\n")
                  user = input("What is your new username?")

            passW = input("Okay! What is the password?")
            print("Sure. Registering the account... this might take a while.")
            data = [user, passW, 0, 0]
            connection.execute("INSERT INTO AccountList VALUES (?, ?, ?, ?)", data)
            connection.commit()
            connection.close()
            #print(
            #    f'''Done. Your account is registered. \nUsername: {user}, Password: {passW}, Wins: {db[user][1]}, Loses: {db[user][2]}	\nDon't forget! Please don't make multiple accounts.''')
            print("Done. Your account has been registered!")
            sleep(1)
            global curUser
            curUser = user
            conClear()
            global userExist
            userExist = True
            return

    def delete (self):
        connection = sqlite3.connect("accountsdb")
        confirm = input("\nAre you sure you want to delete your account? All your data will be wiped. (yes/no): ")
        if confirm.lower() == "yes":
            connection.execute("DELETE FROM AccountList WHERE username=?", (str(self.user),))
            connection.commit()
        connection.close()

    def change_password (self):
        connection = sqlite3.connect("accountsdb")

        newPass = input("What is the new password?")
        connection.execute("UPDATE AccountList SET password=? WHERE username=?", (str(newPass), str(self.user)))
        connection.commit()
        connection.close()
        print("Success!", end="")
        print("\r", end="")