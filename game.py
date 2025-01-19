# import re
# import requests

import random
import os
from time import sleep

import sqlite3

from account import Accounts
import constants

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

# def checkBad (num):
#     if num == 4043:
#         return False
#     elif num == 566:
#         return False
#     else:
#         return True
    
class Wordle ():
    def __init__ (self, username, password, exist):
        self.curUser = username
        self.curPasw = password
        self.userExist = exist
        
    def fetch_word (letters):
        # the website went down :(
        # meaningpedia_resp = requests.get(
        #     f"https://meaningpedia.com/5-letter-words?show=all")
        # pattern = re.compile(r'<span itemprop="name">(\w+)</span>')
        # word_list = pattern.findall(meaningpedia_resp.text)
        # 4043 is bad word, 566: 6363 total
        file = open('words.txt', mode='r')
        word_list = []
        
        for i in range(5755):
            word_list.append(file.readline())
            
        finalIn = random.randint(0, 5754)
        # ohno = False

        # if not checkBad(finalIn):
        #     ohno = True
        
        # while ohno:
        #     finalIn = random.randint(0, 6364)

        #     if checkBad(finalIn):
        #         return word_list[finalIn]
        
        hidword = word_list[finalIn]
        back_up = hidword
        return hidword

    def guess (guess, back_up):
        greens = [""]
        yellows = [""]
        none = [""]
        print(f"{back_up}{constants.Reset}")

        # following code from stackoverflow: https://stackoverflow.com/questions/45263205/python-how-to-print-on-same-line-clearing-previous-text
        # for t in ['long line', '%']:
        #   sys.stdout.write('\033[K' + t.expandtabs(2) + '\r')
        # sys.stdout.write('\n')
        for i in range(len(back_up)-1):
            if guess[i] == back_up[i]:
                print(f"{constants.Green}{guess[i]}{constants.White}", end="")
                continue
            elif back_up.find(guess[i]) != -1:
                print(f"{constants.Yellow}{guess[i]}{constants.White}", end="")
                continue
            print(f"{constants.Red}{guess[i]}{constants.White}", end="")

    def checkValid (guess, guess_list):
        # meaningpedia_resp = requests.get(
        #     f"https://meaningpedia.com/5-letter-words?show=all")
        # pattern = re.compile(r'<span itemprop="name">(\w+)</span>')
        # word_list = pattern.findall(meaningpedia_resp.text)

        if len(guess) != 5:
            print(f"{constants.Bold}Your guess must be 5 letters long!{constants.Reset}\n")
            return False
        if guess in guess_list:
            print(f"{constants.Bold}You have already guessed this!{constants.Reset}")
            return False
        # if guess not in word_list:
        #   print("Your guess must be a valid English word!")
        #   return False

        return True

    # games begin
    def wordle (self):
        connection = sqlite3.connect("accountsdb")
        guess_list = [""]
        hidword = Wordle.fetch_word(5)
        back_up = hidword

        guess = input(
            f"{constants.Bold}Game has begun! Insert your first guess\nNote: Yellow means it is in the string.\nGreen means it is at the correct place.\n{constants.Reset}")

        # print(guess, back_up)
        
        if guess == back_up:
            print(f"{constants.Blue}Good job! You got the word!{constants.White}")
            if self.userExist:
                connection.execute("UPDATE AccountList SET wins = wins + 1 WHERE username=?", (str(self.curUser),))
                connection.commit()
                connection.close()
            return

        while not Wordle.checkValid(guess, guess_list):
            print(f"{constants.Reset}")
            guess = input(f"{constants.Bold}Please enter another guess{constants.Reset}\n")

        guess_list.append(guess)
        Wordle.guess(guess, back_up)

        for i in range(5):
            print("\n")
            guess = input(f"{constants.Bold}{constants.White}Next guess?{constants.Reset}\n")
            while not Wordle.checkValid(guess, guess_list):
                guess = input(f"{constants.Bold}Please enter another guess{constants.Reset}\n")

            guess_list.append(guess)
            Wordle.guess(guess, hidword)
            
            count = 0
            for m in range(len(back_up)-1):
                if guess[i] == back_up[i]:
                    count += 1
                    
            if count == 5:
                print(f"{constants.Bold}{constants.Blue}\nGood job! You got the word!{constants.White}{constants.Reset}")
                sleep(1)
                if self.userExist:
                    connection.execute("UPDATE AccountList SET wins = wins + 1 WHERE username=?", (str(self.curUser),))
                    connection.commit()
                    connection.close()
                break
            if i == 4:
                print(f"{constants.Bold}{constants.Blue}\nUh-oh! You ran out of guesses!{constants.White}{constants.Reset}")
                sleep(1)
                if self.userExist:
                  connection.execute("UPDATE AccountList SET losses = losses + 1 WHERE username=?", (str(self.curUser),))
                  connection.commit()
                  connection.close()
                break
            
        connection.close()
        # for i in len(back_upup):
        # 	if guess[i] == back_up[i]:
        # 		print("placeholder")

    def insOption ():
        option = input(f'''{constants.Bright_Blue}What would you like to do?
    {constants.Blue}1. Start a new game
    {constants.Red}2. Delete acccount
    {constants.Cyan}3. Change password
    {constants.Green}4. Log out
    {constants.Orange}5. View profile\n{constants.White}''')  # keep #3 like that, there's an issue

        return option

    def reOpt (self):
        option = Wordle.insOption()
        if option == "1":
            Wordle.wordle(self)
            conClear()

            Wordle.reOpt(self)
        elif option == "2" and self.curUser != "Guest":
            obj = Accounts(self.curUser, self.curPasw)
            if obj.delete():
                raise SystemExit
            else:
                sleep(0.1)
                conClear()
                Wordle.reOpt(self)
        elif option == "4":
            raise SystemExit
        elif option == "5":
            connection = sqlite3.connect("accountsdb")
            win = connection.execute("SELECT wins FROM AccountList WHERE username=?", (str(self.curUser),))
            loss = connection.execute("SELECT losses FROM AccountList WHERE username=?", (str(self.curUser),))
            
            curWin = str(win.fetchone())
            curLoss = str(loss.fetchone())
            
            connection.close()
            
            winNum = ""
            lossNum = ""
            
            #remove (,)
            for i in range(len(curWin)):
                if curWin[i] != "(" and curWin[i] != "," and curWin[i] != ")":
                    winNum += curWin[i]
                    
            for i in range(len(curWin)):
                if curLoss[i] != "(" and curLoss[i] != "," and curLoss[i] != ")":
                    lossNum += curLoss[i]
                
            print(f'''{constants.White}Stats for user {self.curUser}:
  Wins: {winNum}
  Losses: {lossNum}''')
            sleep(1)
            conClear()
            Wordle.reOpt(self)
        elif option == "3" and self.curUser != "Guest":
            obj = Accounts(self.curUser, self.curPasw)
            obj.change_password()
            conClear()
            Wordle.reOpt(self)
        else:
            print(f"{constants.White}Not a valid option. Try again.")
            sleep(0.5)
            conClear()
            Wordle.reOpt(self)