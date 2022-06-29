"""Cho-Han - A simple Japanese dice game of even-odd."""

import random
import sys

JAPANESE_NUMBERS = {1: 'ICHI', 2: 'NI', 3: 'SAN', 4: 'SHI', 5: 'GO', 6: 'ROKU'}

def main():
    print('''Cho-Han : A simple Japanese dice game of even-odd.
    Rules : In this game, two dice are rolled by the dealer. 
    The player must guess if the dice total to an even (cho) or odd (han) number!
    ''')

    money = 10000

    while True:
        print("You currently have ${}. How much would you like to bet? (or QUIT)".format(money))
        while True: #Get a valid bet
            pot = (input("> "))
            if pot.upper() == 'QUIT':
                print("You with with ${}. Thanks for playing - bye!".format(money))
                sys.exit()
            elif not pot.isdecimal():
                print("Please enter a valid number")
            elif int(pot) > money:
                print("You don't have enough money to cover that bet!")
            else: # Valid bet
                pot = int(pot)
                break

        #Roll dice
        dice1 = random.randint(1,6)
        dice2 = random.randint(1,6)

        print("The dealer rolls the dice - what is your bet?")
        print("CHO (even) or HAN (odd)?")
        while True:
            bet = input("> ").upper()
            if bet != 'CHO' and bet != 'HAN':
                print("Please enter either CHO or HAN.")
                continue
            else:
                break
        
        print("The dealer reveals the dice!")
        print("The dice were {} ({}) and {} ({})".format(JAPANESE_NUMBERS[dice1],dice1,JAPANESE_NUMBERS[dice2],dice2))

        #Determine if player wins
        isEven = (dice1+dice2) % 2 == 0
        if isEven:
            correctBet = 'CHO'
        else:
            correctBet = "HAN"
        
        playerWon = bet == correctBet

        #Display Results

        if playerWon:
            print("You won ${}".format(pot))
            money = (money + pot) - (pot // 10)
            print("The house collects a ${} fee".format(pot // 10))

        else:
            print("You lost!")
            money = money - pot

        if money == 0:
            print("You're out of money - thanks for playing!")
            sys.exit()
            
if __name__ == '__main__':
    main()