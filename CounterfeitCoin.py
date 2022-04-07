'''
    This is a file that will look to implement an algorithm in finding a 
    counterfeit coin that is lighter than authetic coins from a set of 
    coins with varying amounts in it. This program will also look to 
    show that this algoirthm can be completed in a logarithmic time
    complexity.
'''

import random
import math

# class coin that has weight and a identifier to differentiate the coins
class Coin:

    # initialize the identifier and weight
    def __init__(self, identifier, weight):
        self.identifier = identifier
        self.weight = weight

    # get the identifier of the coin
    def getIdentifier(self):
        return self.identifier

    # get the weight of the coin 
    def getWeight(self):
        return self.weight

# add the weights of set of coins
def totalWeights(listCoins):
    totalWeight = 0
    for coin in listCoins:
        totalWeight += coin.getWeight()

    return totalWeight

# constant variables for number of coins, expected number of balance usage, authentic coin weights, and counterfeit weight
NUMCOINS = random.randint(1000,100000)
EXPECTED_TRIALS = int(math.log(NUMCOINS, 3)) + 1
REALWEIGHT = 1
FAKEWEIGHT = 0.5
listOfCoins = [Coin(x, REALWEIGHT) for x in range(1, NUMCOINS + 1)]

# choose a coin to be a fake and weigh less
randomCoinFake = random.randint(1, NUMCOINS)
listOfCoins[randomCoinFake - 1] = Coin(randomCoinFake, FAKEWEIGHT)

print("\nWe have %d identical-looking coins but one of them is a counterfeit and weighs less than the others." %(NUMCOINS))
print("Using a balance scale, try to find the counterfeit coin by using the balance only %d times.\n" %(EXPECTED_TRIALS))

# important variables to keep track of while weighing the coins
numWeighingCoins = NUMCOINS # number of coins that are in contention for being fake
listWeighingCoins = listOfCoins # list of the coins that are in contention for being fake
WeighNumber = 1 # number of weighs
while not numWeighingCoins == 1:

    # shuffle the list to simulate choosing a random group of a certain number of coins
    random.shuffle(listWeighingCoins)

    # depending on how many coins there are, split into groups such that the groups differentiate in size by at most 1
    if numWeighingCoins % 3 == 0 or numWeighingCoins % 3 == 1:
        group1 = listWeighingCoins[0: int(numWeighingCoins / 3)]
        group2 = listWeighingCoins[int(numWeighingCoins / 3): 2 * int(numWeighingCoins / 3)]
        group3 = listWeighingCoins[int(numWeighingCoins * 2 / 3): ]

    else:
        group1 = listWeighingCoins[0: int((numWeighingCoins + 1) / 3)]
        group2 = listWeighingCoins[int((numWeighingCoins + 1) / 3): 2 * int((numWeighingCoins + 1) / 3)]
        group3 = listWeighingCoins[2 * int((numWeighingCoins + 1) / 3): ]

    # find the total
    alphaTotal = totalWeights(group1)
    betaTotal = totalWeights(group2)

    if alphaTotal == betaTotal:
        listWeighingCoins = group3
    elif alphaTotal > betaTotal:
        listWeighingCoins = group2
    elif betaTotal > alphaTotal:
        listWeighingCoins = group1
    numWeighingCoins = len(listWeighingCoins)

    # print results
    print("--------------------Weight Try #%d--------------------\n" %(WeighNumber))
    outStr = "Left side group will consist of " + str(len(group1)) + " coin(s) with numbers: \n"
    counter = 0
    for coin in group1:
        if counter % 15 == 14:
            outStr += str(coin.getIdentifier()) + "\n"
        else:
            outStr += str(coin.getIdentifier()) + " "
        counter += 1
    print(outStr + "\n")
    outStr = "Right side group will consist of " + str(len(group2)) + " coin(s) with numbers: \n"
    counter = 0
    for coin in group2:
        if counter % 15 == 14:
            outStr += str(coin.getIdentifier()) + "\n"
        else:
            outStr += str(coin.getIdentifier()) + " "
        counter += 1
    print(outStr + "\n")
    
    if alphaTotal == betaTotal:
        print("Both sides were equal in weight so the counterfeit is amongst the unweighed coins.")
    elif alphaTotal > betaTotal:
        print("Left side was heavier so the counterfeit is in the right side.")
    elif betaTotal > alphaTotal:
        print("Right side was heavier so the counterfeit is in the left side.")

    WeighNumber += 1

# see the results of it
print("\n--------------------Final Verdict--------------------")
print("Through our %d weight trials, we have found that %d coin is the counterfeit.\n" %(WeighNumber - 1, listWeighingCoins[0].getIdentifier()))

print("----------------------Analysis-----------------------")
if listWeighingCoins[0].getIdentifier() == randomCoinFake and len(listWeighingCoins) == 1:
    print("SUCCESS! This was the correct coin.")
else:
    print("ERROR! This is the wrong coin. Please check program.")

if WeighNumber - 1 <= EXPECTED_TRIALS:
    print("SUCCESS! We were able to find the counterfeit coin in less than %d expected moves for this algorithm.\n" %(EXPECTED_TRIALS))
else:
    print("ERROR! Algorithm was not able to find the counterfeit in less weighings.\n")


