#Poker Odds/Equity Calculator
import copy
import functools
import itertools
class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
    def getSuit(self):
        return self.suit
    def getRank(self):
        return self.rank
    def __repr__(self):
        return str(self.rank) + " of " + str(self.suit)
    def __str__(self):
        return str(self.rank) + " of " + str(self.suit)
    def __eq__(self, other):
        return self.suit == other.suit and self.rank == other.rank
    def __ne__(self, other):
        return self.suit != other.suit or self.rank != other.rank
    def __lt__(self, other):
        return self.rank < other.rank
    def __le__(self, other):
        return self.rank <= other.rank
    def __gt__(self, other):
        return self.rank > other.rank
    def __ge__(self, other):
        return self.rank >= other.rank
    def __hash__(self):
        return hash((self.suit, self.rank))
deck = ([0]*13)*4
for i in range(4):
    for j in range(13):
        deck[i*13+j] = Card(i,j+1)
#print(deck)
def dealDeck(hands, communityCards):
    d = copy.deepcopy(deck)
    for hand in hands:
        for card in hand:
            d.remove(card)
    for card in communityCards:
        d.remove(card)
    return d

def compareHands(tup1, tup2):
    return 1 if tup1 > tup2 else -1 if tup1 < tup2 else 0
            


def findHand(hand):
        highHand = (0,0,0)
        numSuit = [0]*4
        numRank = [0]*13
        highCard = 0
        flush = False
        straight = False
        for card in hand:
            if card.getRank() == 1:
                highCard = 14
            elif card.getRank() > highCard:
                highCard = card.getRank()
            numSuit[card.getSuit()] += 1
            numRank[card.getRank() - 1] += 1
        #print("numRank: " + str(numRank))
        #print("numSuit: " + str(numSuit))
        #Check for flush
        flush = False
        straight = False
        highStraight = False
        for i in range(4):
            if numSuit[i] == 5:
                flush = True
                break
        for i in range(13):
             #Check for straight
            if ((i < 9 and (numRank[i] == 1 and numRank[i+1] == 1 and numRank[i+2] == 1 and numRank[i+3] == 1 and numRank[i+4] == 1))) or numRank == [1,0,0,0,0,0,0,0,0,1,1,1,1]:
                straight = True
                if numRank == [1,0,0,0,0,0,0,0,0,1,1,1,1]:
                    highStraight = True
                #check for straight flush or royal flush
                if flush:
                    if highStraight:
                        highHand = (9, 14) if compareHands(highHand ,(9, 14)) == -1 else highHand
                        continue
                    else:
                        highHand = (8, highCard) if compareHands(highHand, (8, highCard)) == -1 else highHand  
                        continue             
            #Check for four of a kind
            if numRank[i] == 4:
                for card in hand:
                    if card.getRank() != i+1:
                        highHand = (7, i if i != 0 else 14, card.getRank()) if compareHands(highHand, (7,  i if i != 0 else 14, card.getRank())) == -1 else highHand
                        continue
            #Check for full house
            if numRank[i] == 3:
                for j in range(13):
                    if numRank[j] == 2:
                        highHand = (6, i if i != 0 else 14, j  if j != 0 else 14) if compareHands(highHand, (6, i if i != 0 else 14, j  if j != 0 else 14)) == -1 else highHand
                        continue
            #Check for flush
            if flush:
                highHand = (5, highCard) if compareHands(highHand, (5, highCard)) == -1 else highHand
                continue
            #Check for straight
            if straight:
                highHand = (4, 14 if highStraight else highCard) if compareHands(highHand, (4, 14 if highStraight else i+4 )) == -1 else highHand
                continue
            #Check for three of a kind
            if numRank[i] == 3:
                three = (3, i if i != 0 else 14)
                if numRank[0] == 1:
                    three = three + (14,)
                for j in reversed(range(13)):
                    if numRank[j] == 1 and j != i and j != 0:
                        three = three + (14 if j == 0 else j,)
                highHand = three if compareHands(highHand, three) == -1 else highHand        
                continue
            #Check for two pair
            if numRank[i] == 2:
                    if(highHand[0] == 1):
                        prev = highHand[1]
                        kicker = 0
                        for j in range(13):
                            if numRank[j] == 1:
                                kicker = 14 if j == 0 else j
                        highHand = (2, prev if prev > i else i, prev if prev < i else i, kicker) if compareHands(highHand, (2, highHand[1] if highHand[1] > i else i, prev if prev < i else i, kicker)) == -1 else highHand
                        continue
                    else:
                #Check for pair
                        pair = (1, 14 if i == 0 else i)
                        if numRank[0] == 1:
                            pair = pair + (14,)
                        for j in reversed(range(13)):
                            if numRank[j] == 1 and j != i and j != 0:
                                 pair = pair + (14 if j == 0 else j,)
                        highHand = pair if compareHands(highHand, pair) == -1 else highHand
                        continue
            #Check for high card
            hCard =  (0, highCard)
            if numRank[0] == 1:
                hCard = hCard + (14,)
            for j in reversed(range(13)):
                if numRank[j] == 1 and j != highCard and j != 0:
                    hCard = hCard + (j,)
            highHand = hCard if compareHands(highHand, hCard) == -1 else highHand
        return highHand
def getTopHand(fullHand):
    possibleHands = list(itertools.combinations(fullHand, 5))
    #print(possibleHands)
    maxHand = (0,0,0)
    for hand in possibleHands:
        #print("Hand: " + str(hand))
        current = findHand(hand)
        #print("findHand output" + str(current))
        maxHand = current if compareHands(current, maxHand) == 1 else maxHand
    return maxHand

def getEquity(hands, communityCards):
    numCommunityCards = len(communityCards)
    numPlayers = len(hands)
    dealedDeck = dealDeck(hands, communityCards)
    typeOfHands = ([0]*10)*numPlayers
    #print(dealedDeck)
    possibleCommunityCards = list(itertools.combinations(dealedDeck, 5 - numCommunityCards))
    for i in range(len(possibleCommunityCards)):
        possibleCommunityCards[i] = communityCards + list(possibleCommunityCards[i])
    #print(possibleCommunityCards)
    winningHands = [0]*(numPlayers)
    tiedHands = [0]*(numPlayers)
    for i in range(len(possibleCommunityCards)):
        bestHands = [0]*numPlayers
        for j in range(numPlayers): 
            bestHands[j] = getTopHand(hands[j] + possibleCommunityCards[i])
            #print("Player " + str(j) + ": " + str(bestHands[j]) + " " + str(hands[j] + possibleCommunityCards[i]))
            typeOfHands[j*10 + bestHands[j][0]] += 1 
        #sort bestHands in reverse order using compareHands
        bH = copy.deepcopy(bestHands)
        bH.sort(reverse = True, key=functools.cmp_to_key(compareHands))
        #print(bH)
        if(bH[0] == bH[1]):
            for j in range(numPlayers):
                if bestHands[j] == bH[0]:
                    tiedHands[j] += 1
                    #print("Player " + str(j) + " tied")
        else:
            for j in range(numPlayers):
                if bestHands[j] == bH[0]:
                    winningHands[j] += 1
    equity = [(0,0,0)]*(numPlayers)
    for i in range(numPlayers):
        equity[i] = (winningHands[i]/len(possibleCommunityCards), tiedHands[i]/len(possibleCommunityCards), 1 - ((winningHands[i] + tiedHands[i])/len(possibleCommunityCards)))
    #     for j in range(10):
    #         typeOfHands[i*10 + j] = typeOfHands[i*10 + j]/len(possibleCommunityCards)
    # print(typeOfHands)
    return equity


       
#print(getTopHand([Card(1, 4), Card(3,9), Card(2,7), Card (0, 6), Card(1, 6), Card(3, 8), Card(3, 12)]))

print(getEquity([[Card(3,12), Card(3,11)], [Card(1,9), Card(2,6)], [Card(2,2), Card(2,11)], [Card(0,9), Card(1,4)]], [Card(3,5), Card(1, 1), Card(2, 8)]))
                        
                    
                    

                

