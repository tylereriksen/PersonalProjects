'''
    This file is here to test if the Connect 4 board game was implemented
    correctly in the Connect4.py file. It will look to test, from randomly
    generated moves, if certain universal condintions are met when the game
    is finished and while playing the game. Some of the tests will include
    if there does exist a row of 4 nonempty slots of the same token and if
    the difference in the number of tokens between red and yellow is 0 or 1.
'''
import random

# check all possible four in a row combinations
ALLPOSSIBLEWINS = [
    [(5,0), (5,1), (5,2), (5,3)],
    [(5,1), (5,2), (5,3), (5,4)],
    [(5,2), (5,3), (5,4), (5,5)],
    [(5,3), (5,4), (5,5), (5,6)],
    [(4,0), (4,1), (4,2), (4,3)],
    [(4,1), (4,2), (4,3), (4,4)],
    [(4,2), (4,3), (4,4), (4,5)],
    [(4,3), (4,4), (4,5), (4,6)],
    [(3,0), (3,1), (3,2), (3,3)],
    [(3,1), (3,2), (3,3), (3,4)],
    [(3,2), (3,3), (3,4), (3,5)],
    [(3,3), (3,4), (3,5), (3,6)],
    [(2,0), (2,1), (2,2), (2,3)],
    [(2,1), (2,2), (2,3), (2,4)],
    [(2,2), (2,3), (2,4), (2,5)],
    [(2,3), (2,4), (2,5), (2,6)],
    [(1,0), (1,1), (1,2), (1,3)],
    [(1,1), (1,2), (1,3), (1,4)],
    [(1,2), (1,3), (1,4), (1,5)],
    [(1,3), (1,4), (1,5), (1,6)],
    [(0,0), (0,1), (0,2), (0,3)],
    [(0,1), (0,2), (0,3), (0,4)],
    [(0,2), (0,3), (0,4), (0,5)],
    [(0,3), (0,4), (0,5), (0,6)],
    [(5,0), (4,0), (3,0), (2,0)],
    [(4,0), (3,0), (2,0), (1,0)],
    [(3,0), (2,0), (1,0), (0,0)],
    [(5,1), (4,1), (3,1), (2,1)],
    [(4,1), (3,1), (2,1), (1,1)],
    [(3,1), (2,1), (1,1), (0,1)],
    [(5,2), (4,2), (3,2), (2,2)],
    [(4,2), (3,2), (2,2), (1,2)],
    [(3,2), (2,2), (1,2), (0,2)],
    [(5,3), (4,3), (3,3), (2,3)],
    [(4,3), (3,3), (2,3), (1,3)],
    [(3,3), (2,3), (1,3), (0,3)],
    [(5,4), (4,4), (3,4), (2,4)],
    [(4,4), (3,4), (2,4), (1,4)],
    [(3,4), (2,4), (1,4), (0,4)],
    [(5,5), (4,5), (3,5), (2,5)],
    [(4,5), (3,5), (2,5), (1,5)],
    [(3,5), (2,5), (1,5), (0,5)],
    [(5,6), (4,6), (3,6), (2,6)],
    [(4,6), (3,6), (2,6), (1,6)],
    [(3,6), (2,6), (1,6), (0,6)],
    [(5,0), (4,1), (3,2), (2,3)],
    [(5,1), (4,2), (3,3), (2,4)],
    [(5,2), (4,3), (3,4), (2,5)],
    [(5,3), (4,4), (3,5), (2,6)],
    [(4,0), (3,1), (2,2), (1,3)],
    [(4,1), (3,2), (2,3), (1,4)],
    [(4,2), (3,3), (2,4), (1,5)],
    [(4,3), (3,4), (2,5), (1,6)],
    [(3,0), (2,1), (1,2), (0,3)],
    [(3,1), (2,2), (1,3), (0,4)],
    [(3,2), (2,3), (1,4), (0,5)],
    [(3,3), (2,4), (1,5), (0,6)],
    [(2,0), (3,1), (4,2), (5,3)],
    [(2,1), (3,2), (4,3), (5,4)],
    [(2,2), (3,3), (4,4), (5,5)],
    [(2,3), (3,4), (4,5), (5,6)],
    [(1,0), (2,1), (3,2), (4,3)],
    [(1,1), (2,2), (3,3), (4,4)],
    [(1,2), (2,3), (3,4), (4,5)],
    [(1,3), (2,4), (3,5), (4,6)],
    [(0,0), (1,1), (2,2), (3,3)],
    [(0,1), (1,2), (2,3), (3,4)],
    [(0,2), (1,3), (2,4), (3,5)],
    [(0,3), (1,4), (2,5), (3,6)]
]

# class that contains all the methods necessary for the Connect 4 game
class Connect4:
    
    #Some constant variables for the class
    REDWIN = "RED!"
    YELLOWWIN = "YELLOW!"
    TIE = "TIE"
    PLAYERMOVE1 = "R"
    PLAYERMOVE2 = "Y"
    EMPTYBOARDFILLER = "."

    # initialization of the class
    def __init__(self, row, col):
        self.row = row
        self.col = col
        board = []
        for i in range(self.row):
            input_row = []
            for j in range(self.col):
                input_row.append(self.EMPTYBOARDFILLER)
            board.append(input_row)
        self.board = board


    # get the number of rows
    def getRow(self):
        return self.row

    # get the number of columns
    def getCol(self):
        return self.col
    
    # get the board
    def getBoard(self):
        return self.board

    # check if a move, which consists of column input is valid
    def isValidMove(self, move):
        try:
            inputCol = int(move)
        except:
            return False

        return (inputCol - 1 >= 0 and inputCol - 1 < self.getCol())

    # function to see if an column is full or not
    def isColFull(self, inputCol):
        for boardRow in range(self.getRow() - 1, -1, -1):
            if self.getBoard()[boardRow][inputCol - 1] == self.EMPTYBOARDFILLER:
                return False
        return True

    # function to check if the board is full of tokens
    def isBoardFull(self):
        for column in range(self.getCol()):
            if not self.isColFull(column):
                return False
        return True

    # function to update board 
    def updateBoard(self, inputCol, playerColor):
        colNum = inputCol - 1
        
        for row in range(self.getRow() - 1, -1, -1):
            if self.getBoard()[row][colNum] == self.EMPTYBOARDFILLER:
                self.board[row][colNum] = playerColor
                break

    # convert the board into text form
    def toText(self):
        strBoard = ""
        for row in range(self.getRow()):
            for col in range(self.getCol()):
                if not col == self.getCol() - 1:
                    strBoard += self.board[row][col] + " "
                else:
                    strBoard += self.board[row][col]
            strBoard += "\n"
        return strBoard

    # check if there is a horizontal row of 4
    def horizontalWin(self, playerMove):
        for col in range(self.getCol() - 3):
            for row in range(self.getRow()):
                if(self.board[row][col] == playerMove 
                and self.board[row][col + 1] == playerMove 
                and self.board[row][col + 2] == playerMove 
                and self.board[row][col + 3] == playerMove):
                    return True
        return False

    # check if there is a vertical row of 4
    def verticalWin(self, playerMove):
        for row in range(self.getRow() - 3):
            for col in range(self.getCol()):
                if(self.board[row][col] == playerMove
                and self.board[row + 1][col] == playerMove
                and self.board[row + 2][col] == playerMove
                and self.board[row + 3][col] == playerMove):
                    return True
        return False

    # check if there is a diagonal of / shape row of 4
    def rightToTopDiagonalWin(self, playerMove):
        for col in range(3, self.getCol()):
            for row in range(self.getRow() - 3):
                if(self.board[row][col] == playerMove 
                and self.board[row + 1][col - 1] == playerMove 
                and self.board[row + 2][col - 2] == playerMove 
                and self.board[row + 3][col - 3] == playerMove):
                    return True
        return False

    # check if there is a diagonal of \ shape row of 4
    def leftToBottomDiagonalWin(self, playerMove):
        for col in range(self.getCol() - 3):
            for row in range(self.getRow() - 3):
                if(self.board[row][col] == playerMove 
                and self.board[row + 1][col + 1] == playerMove 
                and self.board[row + 2][col + 2] == playerMove 
                and self.board[row + 3][col + 3] == playerMove):
                    return True
        return False

    # check if game is finished by checking if there is a win or full board
    def gameFinished(self):

        if(self.horizontalWin(self.PLAYERMOVE1) 
        or self.verticalWin(self.PLAYERMOVE1) 
        or self.rightToTopDiagonalWin(self.PLAYERMOVE1) 
        or self.leftToBottomDiagonalWin(self.PLAYERMOVE1)):
            return True

        elif(self.horizontalWin(self.PLAYERMOVE2) 
        or self.verticalWin(self.PLAYERMOVE2) 
        or self.rightToTopDiagonalWin(self.PLAYERMOVE2) 
        or self.leftToBottomDiagonalWin(self.PLAYERMOVE2)):
            return True

        elif self.isBoardFull():
            return True

        return False

    # see who won
    def winner(self):

        if(self.horizontalWin(self.PLAYERMOVE1) 
        or self.verticalWin(self.PLAYERMOVE1) 
        or self.rightToTopDiagonalWin(self.PLAYERMOVE1) 
        or self.leftToBottomDiagonalWin(self.PLAYERMOVE1)):
            return self.REDWIN

        elif(self.horizontalWin(self.PLAYERMOVE2) 
        or self.verticalWin(self.PLAYERMOVE2) 
        or self.rightToTopDiagonalWin(self.PLAYERMOVE2) 
        or self.leftToBottomDiagonalWin(self.PLAYERMOVE2)):
            return self.YELLOWWIN

        elif self.isBoardFull():
            print("It's a Tie.")
            return self.TIE

        return "none"


    # Helper Method to count the number of occurances of a certain string in the board
    def PLAYERCOUNT(self, playerMove):
        
        count = 0
        for row in range(self.getRow()):
            for col in range(self.getCol()):
                if self.getBoard()[row][col] == playerMove:
                    count += 1
        return count


for i5 in range(0, 100):
    # numbers to take count of certain tests
    passedTestsTokens = 0
    totalTestsTokens = 0

    passedTestsWins= 0
    totalTestsWins = 0

    passedTestsInvalidMove = 0
    totalTestsInvalidMove = 0

    # counter for red and yellow tokens in the board
    rCount = 0
    yCount = 0

    # make the Connect 4 game
    ROWS = 6
    COLUMNS = 7
    Connect4Game = Connect4(ROWS, COLUMNS)

    # indexToTie = [1,2,1,2,1,2,2,1,2,1,2,1,3,4,3,4,3,4,4,3,4,3,4,3,5,6,5,6,5,6,6,5,6,5,6,5,7,7,7,7,7,7] <-- Indexes to force a tie game

    counterPlayer = 0
    quitInput = "q"

    while not Connect4Game.gameFinished():

        print(Connect4Game.toText())
        
        # this is for determining the which player token will be used
        if counterPlayer % 2 == 0:
            playerMove = "red"
            playerToken = Connect4Game.PLAYERMOVE1

        else:
            playerMove = "yellow"
            playerToken = Connect4Game.PLAYERMOVE2

        print("")
        playerInput = str(random.randint(1, 8)) 
        #playerInput = str(indexToTie[counterPlayer]) <--- this is to force program to have a tie game to test the case

        if playerInput.lower() == quitInput:
            break

        # check if the column entered was valid
        if not Connect4Game.isValidMove(playerInput):
            print("Invalid input...Please try again.")

            totalTestsInvalidMove += 1
            if int(playerInput) == 8:
                passedTestsInvalidMove += 1

            print("\n")
            continue

        elif Connect4Game.isColFull(int(playerInput)):
            print("This column is already full. Please try a different column to put your " + playerMove +  " token.")
            print("\n")
            continue

        Connect4Game.updateBoard(int(playerInput), playerToken)

        if counterPlayer % 2 == 0:
            rCount += 1
        else:
            yCount += 1


        print("\n")

        # TEST FOR NUMBER OF RED AND YELLOW TOKENS
        # When red player's turn, after making a move, there should be one more red token present than yellow
        totalTestsTokens += 1
        if rCount == Connect4Game.PLAYERCOUNT(Connect4Game.PLAYERMOVE1) and yCount == Connect4Game.PLAYERCOUNT(Connect4Game.PLAYERMOVE2):
            if counterPlayer % 2 == 0:
                if rCount - yCount == 1:
                    passedTestsTokens += 1
                else:
                    print("Test Failed - Number of Red Tokens are not one more than the Number of Yellow")

            else:
                if rCount == yCount:
                    passedTestsTokens += 1
                else:
                    print("Test Failed - Number of Red and Yellow Tokens do not match")

        counterPlayer += 1




        # check if there is exactly only one row of 4
        totalTestsWins += 1
        countWin = 0
        locatedWins = []
        for combination in ALLPOSSIBLEWINS:
            if (Connect4Game.getBoard()[combination[0][0]][combination[0][1]]
            == Connect4Game.getBoard()[combination[1][0]][combination[1][1]]
            and Connect4Game.getBoard()[combination[1][0]][combination[1][1]]
            == Connect4Game.getBoard()[combination[2][0]][combination[2][1]]
            and Connect4Game.getBoard()[combination[2][0]][combination[2][1]]
            == Connect4Game.getBoard()[combination[3][0]][combination[3][1]]
            and not Connect4Game.getBoard()[combination[0][0]][combination[0][1]] == Connect4Game.EMPTYBOARDFILLER):
                countWin += 1
                locatedWins.append(combination)

        if countWin == 0:
            passedTestsWins += 1

        else:
            for token in range(6):
                rowInput = token
                if not Connect4Game.getBoard()[token][int(playerInput) - 1] == Connect4Game.EMPTYBOARDFILLER:
                    break

            tupleWin = (rowInput, int(playerInput) - 1)
            countWinCount = 0
            for winCombos in locatedWins:
                if tupleWin in winCombos:
                    countWinCount += 1

            if countWinCount == len(locatedWins):
                passedTestsWins += 1

        
    print("1 2 3 4 5 6 7")
    print("-------------")
    print(Connect4Game.toText() + "\n")

    board = Connect4Game.getBoard()
    print("--------------- END GAME ----------------\n")

    print("-------------- FINAL BOARD --------------")
    print("1 2 3 4 5 6 7")
    print("-------------")
    print(Connect4Game.toText())

    print("\n----------------- WINNER ----------------")
    print(Connect4Game.winner())

    # Test to see if the winner and the number of token make logistic sense
    passedWinCheck = 0
    testWinCheck = 0

    passedWinCheck += 1
    if Connect4Game.PLAYERCOUNT(Connect4Game.PLAYERMOVE1) - Connect4Game.PLAYERCOUNT(Connect4Game.PLAYERMOVE2) == 1:
        if Connect4Game.winner() == Connect4Game.REDWIN:
            testWinCheck += 1
        else:
            print("Test Failed - Number of Red and Yellow Tokens do not match with the winner")
    elif Connect4Game.PLAYERCOUNT(Connect4Game.PLAYERMOVE1) == Connect4Game.PLAYERCOUNT(Connect4Game.PLAYERMOVE2):
        if Connect4Game.winner() == Connect4Game.YELLOWWIN:
            testWinCheck += 1
        elif Connect4Game.winner() == Connect4Game.TIE:
            testWinCheck += 1
        else:
            print("Test Failed - Number of Red and Yellow Tokens do not match with the winner")

    # Test that "gravity exists" in the final - in other words make sure there are no open spaces sandwiched between tokens
    passedTestGravity = 0
    totalTestGravity = 0

    for col in range(Connect4Game.getCol()):
        totalTestGravity += 1
        indexesBlank = []
        for row in range(Connect4Game.getRow()):
            if Connect4Game.getBoard()[row][col] == Connect4Game.EMPTYBOARDFILLER:
                indexesBlank.append(row)

        if len(indexesBlank) == 0:
            passedTestGravity += 1
        elif len(indexesBlank) == (len(range(indexesBlank[0], indexesBlank[-1])) + 1):
            passedTestGravity += 1
        else:
            print("Test Failed - Token did not go down the column to the lowest row")


    # This is where it will show how many tests were run and how many of the tests passsed
    print("\n------------ CHECKS AND TESTS -----------")
    print("      ---------- Run %d ---------      \n" %(i5 + 1))
    print("Program passed %d out of %d tests regarding the number of red and yellow tokens in the board" %(passedTestsTokens, totalTestsTokens))
    print("Program passed %d out of %d tests regarding the continuation of the game and the number of 4 in a rows" %(passedTestsWins, totalTestsWins))
    print("Program passed %d out of %d tests regarding invalid player moves for column inputs" %(passedTestsInvalidMove, totalTestsInvalidMove))
    print("Program passed %d out of %d tests regarding number of red and yellow tokens and the winner" %(passedWinCheck, testWinCheck))
    print("Program passed %d out of %d tests regarding tokens falling down to the lowest blank slot in a column" %(passedTestGravity, totalTestGravity))
    print("\n")
    if(not passedTestsTokens == totalTestsTokens
    and not passedTestsWins == totalTestsWins
    and not passedTestsInvalidMove == totalTestsInvalidMove
    and not passedWinCheck == testWinCheck
    and not passedTestGravity == totalTestGravity):
        print("Program has failed one or more tests...")
        break