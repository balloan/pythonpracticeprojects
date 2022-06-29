"""Blackjack - the classic card game. 
This is a simple version that doesn't have splitting or insurance."""

from audioop import add
import random
import sys

# Set up constants

HEARTS   = chr(9829) # Character 9829 is '♥'.
DIAMONDS = chr(9830) # Character 9830 is '♦'.
SPADES   = chr(9824) # Character 9824 is '♠'.
CLUBS    = chr(9827) # Character 9827 is '♣'.
BACKSIDE = 'backside'

def main():
    print('''Blackjack - the classic card game
    
    Rules : Try to get as close to 21 as possible, without going over!
    Kings, Queens, and Jacks are worth 10 points.
    Aces are worth 11 or 1 point. 
    All other cards are worth their face value.
    (H)it to draw another card!
    (S)tand to stop taking cards.
    On your first play, you can (D)ouble down to increase your bet, but you have to hit exactly one more time before standing.
    In the case of a tie, the bet is returned to the player.
    The dealer stops hitting at 17.''')

    money = 5000 #Starting cash

    while True: # Game loop
        if money <= 0:
            print("Uh oh - you ran out of money! Thanks for playing!")
            sys.exit()
        
        print("Money:", money)
        bet = getBet(money)

        deck = getDeck()
        dealerHand = [deck.pop(), deck.pop()]
        playerHand = [deck.pop(), deck.pop()]

        #Player actions
        print("Bet:", bet)
        while True: # Run until player stands or busts
            displayHands(playerHand, dealerHand, False)
            print()

            if getHandValue(playerHand) > 21:
                break
                
            move = getMove(playerHand, money - bet)

            if move == 'D': # Double down
                additionalBet = getBet(min(bet, (money - bet)))
                bet += additionalBet
                print("Bet increased to {}.".format(bet))
                print("Bet:", bet)

            if move in ('H', 'D'): # Hit or double down - draw a card
                newCard = deck.pop()
                rank, suit = newCard
                print("You drew a {} of {}.".format(rank,suit))
                playerHand.append(newCard)

                if getHandValue(playerHand) > 21:
                    #Player busted
                    continue
            
            if move in ('S', 'D'): #Stand / double down stops the players turn.
                break
        
        #Dealer actions

        if getHandValue(playerHand) <= 21: #If player didn't bust
            while getHandValue(dealerHand) < 17:
                print("Dealer hits...")
                dealerHand.append(deck.pop())
                displayHands(playerHand, dealerHand, False)

                if getHandValue(dealerHand) > 21:
                    break # Dealer Busted
                
                input("Press enter to continue...")
                print('\n\n') #Formatting

        #Show the final hands
        print("Here are the final hands!")
        displayHands(playerHand, dealerHand, True)

        playerValue = getHandValue(playerHand)
        dealerValue = getHandValue(dealerHand)

        print("Player value : {}".format(playerValue))
        print("Dealer value : {}".format(dealerValue))

        if dealerValue > 21:
            print("The dealer busts! You win ${} !".format(bet))
            money += bet
        elif (playerValue > 21 or playerValue < dealerValue):
            print("You lost! You lose ${} !".format(bet))
            money -= bet
        elif (playerValue > dealerValue):
            print("You won! You won ${} !".format(bet))
            money += bet
        elif playerValue == dealerValue:
            print("It's a tie - we'll return your bet in this version.")

        input("Press Enter to continue...")
        print('\n\n')


def getBet(maxBet):
    """Ask the player how much they want to bet for this round."""
    while True: 
        print('How much do you bet? (1-{}, or QUIT)'.format(maxBet))
        bet = input('> ').upper().strip()
        if bet == 'QUIT':
            print('Thanks for playing!')
            sys.exit()
        
        if not bet.isdecimal():
            continue # if they didn't enter a number, ask again

        bet = int(bet)
        if 1 <= bet <= maxBet:
            return bet # Valid bet


def getDeck():
    """Return a list of (rank, suit) tuples that represent all 52 cards"""
    deck = []
    for suit in (HEARTS,DIAMONDS,SPADES,CLUBS):
        for rank in range(2,11):
            deck.append((str(rank),suit)) # Add numbered cards
        for rank in ('J','Q','K','A'):
            deck.append((rank, suit)) # Add face and ace cards
    random.shuffle(deck)
    return deck

def displayHands(playerHand, dealerHand, showDealerHand):
    """Show the player and dealer's card - hide the dealers first card if set to false """
    print()
    if showDealerHand:
        print("DEALER:", getHandValue(dealerHand))
        displayCards(dealerHand)
    else:
        print("DEALER: ???")
        # Display all dealer cards except the first.
        displayCards([BACKSIDE] + dealerHand[1:])

    # Show the player's cards
    print("PLAYER:", getHandValue(playerHand))
    displayCards(playerHand)

def getHandValue(cards):
    """Returns the value of the cards - face cards = 10, aces are 1 or 11 - this picks the most suitable ace value"""
    value = 0
    numberOfAces = 0

    #Add the values of the non ace cards
    for card in cards:
        rank = card[0] #Cards are tuples (rank, suit)
        if rank == 'A':
            numberOfAces += 1
        elif rank in ('K','Q','J'):
            value += 10
        else:
            value += int(rank)
    
    #Ace logic
    value += numberOfAces # Add 1 per ace
    for i in range(numberOfAces):
        if value + 10 <= 21:
            value += 10

    return value

def displayCards(cards):
    """Display all the cards in the card list"""
    rows = ['', '', '', '', '']  # The text to display on each row.

    for i, card in enumerate(cards):
        rows[0] += ' ___  '  # Print the top line of the card

        if card == BACKSIDE:
            # Print back of card
            rows[1] += '|## | '
            rows[2] += '|###| '
            rows[3] += '|_##| '
        else:
            # Print front of card
            rank, suit = card
            rows[1] += '|{} | '.format(rank.ljust(2))
            rows[2] += '| {} | '.format(suit)
            rows[3] += '|_{}| '.format(rank.rjust(2, '_'))

    for row in rows: # Print all cards
        print(row)

def getMove(playerHand, money):
    """Asks the player for their move, and returns 'H' for hit, 'S' for stand, and 'D' for double down."""

    while True: # Loop until valid move
        moves = ['(H)it', '(S)tand'] # Determine what moves a player can make

        if len(playerHand) == 2 and money > 0:
            moves.append('(D)ouble down')

        #Get the move
        movePrompt = ', '.join(moves) + '> '
        move = input(movePrompt).upper()
        if move in ('H', 'S'):
            return move # valid move
        if move == 'D' and '(D)ouble down' in moves:
            return move # valid


if __name__ == '__main__':
    main()








