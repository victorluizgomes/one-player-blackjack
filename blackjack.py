'''
Project: BlackJack

MISC NOTES:
- BlackJack rules used: https://www.pagat.com/banking/blackjack.html
- Online free blackjack game: https://www.arkadium.com/games/blackjack/

- Start with the input for the pots.
    (minimum bet should be calcualted as 1/20 of the initial pot)

- Card suit characters: ♠ ♥ ♦ ♣
    or can use S, H, D and C
    or omitted.

BASIC RULES:
- Players are dealt 2 cards and are shown one of the dealer's cards
    1. Then players can choose to stand or hit (unless they have Blackjack).
        stand means the hand you have is the final hand.
        hit means to get dealt another card.
    2. players are dealt cards until they bust or choose to stand.
        bust means the sum of the hand's card values is greater than 21.
    3. Then the other dealer's card is shown. (See dealer's actions below)

- The game should end when the player pot goes to $0.
    or Player chooses to "Cash out" thus printing summary and quitting game.

PAYOUT:
- The payout after a round is 1:1 what the player put down if the player won.
    If the player and dealer have equal hands, player gets the bet back.
    Otherwise player loses his bet to the house (including a player's bust).
    If the player gets a 'Blackjack' he should be paid a 3:2.

CARD VALUES:
- Card values are the normal numeral on the cards 2 to 10.
    Jack, Queen, King are also worth 10.
    Ace is worth 11, unless the hand goes over 21, then is worth 1.

- A hand of a 10 valued card and an Ace is a 'BlackJack', it beats all hands
    other than another BlackJack (In that case bets are returned).

DEALER BEHAVIOR:
- After both of dealer's cards show, the dealer will continue to take cards
    until they have a value of 17 or higher. If the dealer has 17 or higher
    with the first 2 cards, then that is his final hand.

'''

import random
import time

def main():
    print("~*~*~ BLACKJACK ~*~*~")

    # The 52 cards in a deck
    deck = ['A♠', 'A♥', 'A♦', 'A♣', '2♠', '2♥', '2♦', '2♣',
            '3♠', '3♥', '3♦', '3♣', '4♠', '4♥', '4♦', '4♣',
            '5♠', '5♥', '5♦', '5♣', '6♠', '6♥', '6♦', '6♣',
            '7♠', '7♥', '7♦', '7♣', '8♠', '8♥', '8♦', '8♣',
            '9♠', '9♥', '9♦', '9♣', 'T♠', 'T♥', 'T♦', 'T♣',
            'J♠', 'J♥', 'J♦', 'J♣', 'Q♠', 'Q♥', 'Q♦', 'Q♣',
            'K♠', 'K♥', 'K♦', 'K♣']


    # The value of each card in Blackjack
    card_value = {'A♠':11, 'A♥':11, 'A♦':11, 'A♣':11,
                  '2♠':2, '2♥':2, '2♦':2, '2♣':2,
                  '3♠':3, '3♥':3, '3♦':3, '3♣':3,
                  '4♠':4, '4♥':4, '4♦':4, '4♣':4,
                  '5♠':5, '5♥':5, '5♦':5, '5♣':5,
                  '6♠':6, '6♥':6, '6♦':6, '6♣':6,
                  '7♠':7, '7♥':7, '7♦':7, '7♣':7,
                  '8♠':8, '8♥':8, '8♦':8, '8♣':8,
                  '9♠':9, '9♥':9, '9♦':9, '9♣':9,
                  'T♠':10, 'T♥':10, 'T♦':10, 'T♣':10,
                  'J♠':10, 'J♥':10, 'J♦':10, 'J♣':10,
                  'Q♠':10, 'Q♥':10, 'Q♦':10, 'Q♣':10,
                  'K♠':10, 'K♥':10, 'K♦':10, 'K♣':10}

    pot = 1000
    cash_out = False
    print("Player's balance: $" + str(pot))

    while cash_out == False and pot > 0:
        
        bet = input("$ Bet: ")
        while not bet.isnumeric() or int(bet) <= 20 or int(bet) > pot:
            print("ERROR: bet needs to be an amount between 20 and the pot.")
            bet = input("$ Bet: ")

        # reset lists
        p_blackjack = False
        d_blackjack = False
        picked_cards = []
        p_hand = []
        d_hand = []
    
        # get the cards dealt
        deal_cards(p_hand, 2, deck, picked_cards)
        deal_cards(d_hand, 2, deck, picked_cards)

        # print player and dealer's hand/value
        print_hand(p_hand, "Player", card_value, False)
        time.sleep(1.0) # time for style
        print_hand(d_hand, "Dealer", card_value, True)

        # run through player decision to hit or stand or print blackjack
        if cards_value(p_hand, card_value) != 21:
            hit_or_stand(p_hand, deck, picked_cards, card_value)
        else:
            print("Player got a Blackjack")
            p_blackjack = True

        time.sleep(1.0) # time for style

        # finish getting dealer's hand if still needs or print blackjack 
        if cards_value(d_hand, card_value) != 21:
            dealer_behavior(d_hand, card_value, deck, picked_cards)
        else:
            print_hand(d_hand, "Dealer", card_value, False)
            print("Dealer got a Blackjack")
            d_blackjack = True

        time.sleep(1.0) # time for style

        print()
        # calculate player's payout
        pot += payout(p_hand, d_hand, card_value, bet,
                      p_blackjack, d_blackjack)

        print("Player's balance: $" + str(pot))
        if pot != 0:
            cash_out = input("Cash out?(yes or no) ")
            if cash_out.lower() == 'yes':
                cash_out = True
            else:
                cash_out = False

        print()

    # after cashing out, show summary
    summary(pot)

'''
deal_cards will randomly pick cards from deck that have not been picked yet
    modifies the hand with the cards picked.
- hand: list with the hand
- num_cards: number of cards to be picked
- deck: deck with 52 cards to pick from
- picked_cards: list of the index of the cards that have been picked already
'''
def deal_cards(hand, num_cards, deck, picked_cards):

    # loop through the number of cards we need to pick
    for i in range(num_cards):
        card_index = random.randint(0, 51)
        # get another card index if that one was picked before
        while card_index in picked_cards:
            card_index = random.randint(0, 51)

        # add the card to the hand and add to picked cards
        hand.append(deck[card_index])
        picked_cards.append(card_index)

'''
print_hand prints the hand passed in and the value of it's cards. Has the
    option to hide the second card of the hand.
- hand: list with the hand
- who: the string of who's hand it is
- card_value: dictionary of all the card values
- hide_second: hides the second card in the hand if True
'''
def print_hand(hand, who, card_value, hide_second):
    print()
    if hide_second:
        hand_value = card_value[hand[0]]
        print(who + "'s hand: " + hand[0] + "|XX")
        print("Hand value: " + str(hand_value))
        
    else:
        hand_value = cards_value(hand, card_value)
        print(who + "'s hand: " + hand[0], end='')
        for i in range(1, len(hand)):
            print("|" + hand[i], end='')
        print()
        print("Hand value: " + str(hand_value))

'''
cards_value will return the sum value of the hand
- hand: list with the hand
- card_value: dictionary of all the card values
'''
def cards_value(hand, card_value):

    value = 0
    ace = 0
    for card in hand:
        value += card_value[card]

        # check if the card is an ace
        if card[0] == 'A':
            ace += 1

    # if the deck has aces and the value is greater than 21 make aces 1
    while value > 21 and ace > 0:
        value -= 10
        ace -= 1

    return value
'''
hit_or_stand will loop through the player choosing to hit or stand
    their current hand. It modifies the player's hand passed in.
- hand: list with the hand
- deck: a list with all the 52 cards
- picked_cards: list of the index of the cards that have been picked already
- card_value: dictionary of all the card values
'''
def hit_or_stand(hand, deck, picked_cards, card_value):
    hit_or_stand = input("Hit or stand(h or s): ")
    bust = False

    while hit_or_stand.lower() == 'h':
                
        deal_cards(hand, 1, deck, picked_cards)
        print_hand(hand, "Player", card_value, False)

        # check if the player busted or has a 21
        value = cards_value(hand, card_value)
        if value > 21:
            print("Player's hand busted")
            break
        elif value == 21:
            break
                
        hit_or_stand = input("Hit or stand(h or s): ")

'''
dealer_behavior will execute the dealer behavior after the player's turn.
    It will pick a new card until the hand value is 17+.
- hand: list with the hand
- deck: a list with all the 52 cards
- picked_cards: list of the index of the cards that have been picked already
- card_value: dictionary of all the card values
'''
def dealer_behavior(hand, card_value, deck, picked_cards):

    value = cards_value(hand, card_value)
    while value < 17:
        deal_cards(hand, 1, deck, picked_cards)
        value = cards_value(hand, card_value)

    # print updated dealer's hand
    print_hand(hand, "Dealer", card_value, False)
        
    if value > 21:
        print("Dealer's hand busted")
    
'''
payout returns the payout amount for the player (positive or negative).
- p_hand: players hand list
- d_hand: dealers hand list
- card_value: dictionary of all the card values
- bet: the bet amount
- p_blackjack: boolean True wheater player has a blackjack
- d_blackjack: boolean True wheater dealer has a blackjack
'''
def payout(p_hand, d_hand, card_value, bet, p_blackjack, d_blackjack):
    p_value = cards_value(p_hand, card_value)
    d_value = cards_value(d_hand, card_value)
    bet = int(bet)

    if p_value > 21: # player bust
        print("Player lost $" + str(bet))
        return -bet
    
    elif p_blackjack and not d_blackjack: # player blackjack
        print("Player won $" + str(bet * 1.5) + " (Blackjack)")
        return 1.5 * bet

    elif d_blackjack and not p_blackjack: # dealer blackjack
        print("Player lost $" + str(bet))
        return -bet
    
    elif d_value > 21 or p_value > d_value: # player > value
        print("Player won $" + str(bet))
        return bet

    elif d_value > p_value: # dealer > value
        print("Player lost $" + str(bet))
        return -bet

    elif p_value == d_value: # tie
        print("Tie")
        return 0

'''
summary of final cash_out
- pot: amount of money at the end
'''
def summary(pot):

    print("Player's balance: $" + str(pot))
    if pot > 1000:
        print("Good Job! You started with $1000")
        print("and made $" + str(pot - 1000))
        
    elif pot == 1000:
        print("You didn't make any money")
            
    else:
        print("You started with $1000")
        print("You lost $" + str(1000 - pot))
        
main()


