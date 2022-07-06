"""Simple reaction time tester -> Check your reaction time!"""

import random
import sys
import time
import os

print("This is a simple program made to test reaction time! Hit the enter key when you see the word react!")
input("Please press enter to begin!")

reactionList = []

while True:
    os.system('cls||clear') # Clear terminal
    print("\n Get ready....")
    time.sleep(random.randint(20,50) / 10.0) #Sleep for 2-5 seconds before starting
    print("REACT!!!")
    timeStart = time.time() #Get time
    input() #Wait for enter
    reactionTime = time.time() - timeStart

    if reactionTime < 0.01: #If they pressed enter before seeing React
        print("You hit enter before react appeared - it doesn't count!")
    else:
        reactionTime = int((reactionTime * 1000)) # Turn to ms
        reactionList.append(reactionTime) # Add to list of times
        print("You took {} milliseconds to react - try to be even faster next time!".format(reactionTime))

    if len(reactionList) > 1:
        total = 0
        averageTime = 0
        for reaction in reactionList:
            total += reaction
        averageTime = total / len(reactionList)
        print("You've reacted {} times, with an average reaction time of {}ms".format(len(reactionList), averageTime))

    print("Enter QUIT to stop, or press Enter to go again!")
    response = input("> ").upper()
    if response == "QUIT":
        print("Have a great day - bye!")
        sys.exit()




