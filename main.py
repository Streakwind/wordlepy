# meaningpedia api

# import sqlite3

from time import sleep

import sys
import os

from account import Accounts
from game import Wordle
import constants

curUser = "Guest"
curPasw = "123"
hidword = "NO"
back_up = hidword
userExist = False

# connection = sqlite3.connect("accountsdb")
# connection.execute("""CREATE TABLE AccountList(username STRING,password STRING,wins INT,losses INT);""")
# connection.close()

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
    
userAcc = input("Do you have an account? (yes/no): ")

if userAcc.lower() == "yes":
    attempts = 0
    logres = False
    while not logres and attempts < 5:
        obj = Accounts(input("Username? "), input(f"Password? {constants.Invisible}"))
        
        logres = obj.login()
        
        attempts += 1
    if attempts >= 5:
        print(f"{constants.White}You have reached your maximum attempt limit.")
        sys.exit()
    if logres:
        curUser = obj.user
        curPasw = obj.pasW
        userExist = True
else:
    signup = input('''Do you want to sign up? 
A guest account works too, except your stats will not be saved. yes/no: ''')

    if signup.lower() == "yes":
        obj = Accounts(curUser, curPasw)
        obj.signup()
        
        curUser = obj.user
        curPasw = obj.pasW
        userExist = True
    else:
        curUser = "Guest"
    
conClear()
obj = Wordle(curUser, curPasw, userExist)
obj.reOpt()