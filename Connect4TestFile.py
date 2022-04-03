'''
    This file is here to test if the Connect 4 board game was implemented
    correctly in the Connect4.py file. It will look to test, from randomly
    generated moves, if certain universal condintions are met when the game
    is finished and while playing the game. Some of the tests will include
    if there does exist a row of 4 nonempty slots of the same token and if
    the difference in the number of tokens between red and yellow is 0 or 1.
'''

import random

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

for i5 in range(0, 100000):
    ROWS = 6
    COLUMNS = 7
    Connect4Game = Connect4(ROWS, COLUMNS)
    print (Connect4Game.getBoard())

    print("Let's play CONNECT4!")
    print("")
    print("Player 1 will go first and be red while Player 2 will go second and be yellow.")
    print("If you want to quit in the middle of the game, enter 'q' when asked for your move.")
    print("Enter a valid column for your move. The columns are listed as follows: ")
    print("")

    counterPlayer = 0
    quitInput = "q"

    RedCount = 0
    YellowCount = 0

    while not Connect4Game.gameFinished():

        print("1 2 3 4 5 6 7")
        print("-------------")
        print(Connect4Game.toText())
        
        # this is for determining the which player token will be used
        if counterPlayer % 2 == 0:
            playerMove = "red"
            playerToken = "R"

        else:
            playerMove = "yellow"
            playerToken = "Y"

        print("")
        playerInput = str(random.randint(1, 8))  #<--- this was for tests to see if program had no bugs
        # ^^ other inputs that been inputted in the Connect4.py such as strings

        if playerInput.lower() == quitInput:
            break

        # check if the column entered was valid
        if not Connect4Game.isValidMove(playerInput):
            print("Invalid input...Please try again.")
            print("\n")
            continue

        elif Connect4Game.isColFull(int(playerInput)):
            print("This column is already full. Please try a different column to put your " + playerMove +  " token.")
            print("\n")
            continue
        Connect4Game.updateBoard(int(playerInput), playerToken)
        if counterPlayer % 2 == 0:
            RedCount += 1
        else:
            YellowCount += 1

        counterPlayer += 1
        print("\n")

        if not RedCount - YellowCount == 1 and not RedCount == YellowCount:
            break



    print(Connect4Game.toText() + "\n")

    board = Connect4Game.getBoard()
    print("--------------- END GAME ----------------\n")

    print("-------------- FINAL BOARD --------------")
    print("1 2 3 4 5 6 7")
    print("-------------")
    print(Connect4Game.toText())

    print("\n----------------- WINNER ----------------")
    print(Connect4Game.winner())

    print("\n----------------- CHECK -----------------\n")

    numTests = 0
    totTests = 0

    print("----------Test Token Count----------")
    # make sure the the difference in Red and Yellow tokens is at most 1
    # and that the last move was a win
    totTests += 1
    if RedCount - YellowCount == 1 and Connect4Game.winner() == Connect4Game.REDWIN:
        print(True)
        numTests += 1
    elif RedCount == YellowCount and Connect4Game.winner() == Connect4Game.TIE:
        print(True)
        numTests += 1
    elif RedCount == YellowCount and Connect4Game.winner() == Connect4Game.YELLOWWIN:
        print(True)
        numTests += 1
    else:
        print(False)

    print("\n")

    print("-----Test Special 4 Row Matches-----")
    # check if there is exactly only one row of 4
    countWin = 0
    locatedWins = []
    for combination in ALLPOSSIBLEWINS:
        if (board[combination[0][0]][combination[0][1]]
        == board[combination[1][0]][combination[1][1]]
        and board[combination[1][0]][combination[1][1]]
        == board[combination[2][0]][combination[2][1]]
        and board[combination[2][0]][combination[2][1]]
        == board[combination[3][0]][combination[3][1]]
        and not board[combination[0][0]][combination[0][1]] == Connect4Game.EMPTYBOARDFILLER):
            countWin += 1
            locatedWins.append(combination)

    speical = False
    # for the cases where the last move happened to complete a 4+ in a row
    if len(locatedWins) >= 2:
        prev = [x[0] for x in locatedWins]
        for i in range(0, len(prev) - 1):
            if(prev[i + 1][0] - prev[i][0] == 1 
            or prev[i + 1][1] - prev[i][1] == 1
            or (prev[i][0] - prev[i + 1][0] == 1 and prev[i + 1][1] - prev[i][1] == 1)
            or (prev[i][0] - prev[i + 1][0] == 1 and prev[i][1] - prev[i + 1][1] == 1)):
                print(True)  
                numTests += 1
                totTests += 1

            else:
                print("\nExamine This Case") # There be at least one common tuple in all the sets in the set
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
                    numTests += 1
                    print(True)
                else:
                    print(False)

                totTests += 1
                special = True



    if(totTests == 1):
        print("None")
    print("\n")

    print("---------Test 4 Row Matches---------")

    totTests += 1
    if((not (len(locatedWins) >= 2) or not special) 
    and not countWin == 1  # <---- this will erroneously say False if the last token complated two different types of 4 in a rows
    and not Connect4Game.winner() == Connect4Game.TIE): # <---- for example, if the last token completes a diagonal and a horizontal
        # these cases will be checked manually
        print(False)
    else:
        print(True)
        numTests += 1

    print("\nThis game passed %d out of %d tests." %(numTests, totTests))

'''
    Bug in the check is that this will throw a test as false if the last token/move 
    completed two different orientations of 4 in a row. Since these are typically 
    rarer these can be checked manually. The logic of the program will still be 
    completed so in theory there should be no bugs for this special scenario.
'''