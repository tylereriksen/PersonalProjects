import time

class Board:

    # constructor
    def __init__(self, board):

        self.board = board
        self.redWinOutput = "RED!"
        self.yellowWinOutput = "YELLOW!"
        self.tieOutput = "TIE"
        if self.validBoard():
            self.row = self.getRow()
            self.column = self.getCol()
        else:
            self.row = -1
            self.column = -1

    # check to see if board is a valid board
    def validBoard(self):

        # check if the board is a list
        if type(self.board) != type([]):
            return False
            quit()

        # check if the first element int he board is a list
        elif type(self.board[0]) != type([]) or len(self.board) == 0:
            return False
            quit()

        elif type(self.board[0][0]) != type("") or len(self.board[0]) == 0:
            return False
            quit()

        totalSame = 0
        for i in range(0, self.getRow() - 1):
            if len(self.board[i]) == len(self.board[i + 1]):
                totalSame += 1

        return (totalSame == self.getRow() - 1)

    def getRow(self):
        return len(self.board)

    def getCol(self):
        return len(self.board[0])

    def validColInput(self, inputCol):

        try:
            inputCol = int(inputCol)

        except:
            return False

        return (inputCol - 1 >= 0 and inputCol - 1 < self.getCol())

    def columnFilled(self, inputCol):

        filledRow = 0
        for row in range(0, self.getRow()):
            if self.board[row][inputCol - 1] != ".":
                filledRow += 1

        if filledRow == self.getRow():
            return True
        else:
            return False

    def boardFilled(self):

        for row in range(self.getRow()):
            for column in range(self.getCol()):
                if self.board[row][column] == ".":
                    return False

        return True

    def changeBoard(self, inputCol, playerMove):

        if self.columnFilled(inputCol) == True:
            return "Sorry. That column is already filled"

        rowNum = self.getRow() - 1

        newBoard = self.board

        while rowNum >= 0:
            if newBoard[rowNum][inputCol - 1] == ".":
                newBoard[rowNum][inputCol - 1] = playerMove
                break
            rowNum -= 1

        return newBoard

    def toText(self):
        returnString = ""

        counter = 0

        for set in self.board:
            for element in set:
                returnString += str(element)
                returnString += " "

            counter += 1

            # check if this was the last element of the set to see if there should be a new line
            if(counter < self.getRow()):
                returnString += "\n"

        return returnString

    def horizontalWin(self, playerMove):
        
        for j in range(self.getCol() - 3):
            for i in range(self.getRow()):
                if self.board[i][j] == playerMove and self.board[i][j + 1] == playerMove and self.board[i][j + 2] == playerMove and self.board[i][j + 3] == playerMove:
                    return True

        return False

    def verticalWin(self, playerMove):
        for i in range(self.getRow() - 3):
            for j in range(self.getCol()):
                if self.board[i][j] == playerMove and self.board[i + 1][j] == playerMove and self.board[i + 2][j] == playerMove and self.board[i + 3][j] == playerMove:
                    return True

        return False

    def rightToTopDiagonalWin(self, playerMove):
        for i in range(3, self.getCol()):
            for j in range(self.getRow() - 3):
                if self.board[j][i] == playerMove and self.board[j + 1][i - 1] == playerMove and self.board[j + 2][i - 2] == playerMove and self.board[j + 3][i - 3] == playerMove:
                    return True

        return False

    def leftToBottomDiagonalWin(self, playerMove):
        for i in range(self.getCol() - 3):
            for j in range(self.getRow() - 3):
                if self.board[j][i] == playerMove and self.board[j + 1][i + 1] == playerMove and self.board[j + 2][i + 2] == playerMove and self.board[j + 3][i + 3] == playerMove:
                    return True

        return False

    def gameFinished(self):

        if self.horizontalWin("R") or self.verticalWin("R") or self.rightToTopDiagonalWin("R") or self.leftToBottomDiagonalWin("R"):
            return True

        elif self.horizontalWin("Y") or self.verticalWin("Y") or self.rightToTopDiagonalWin("Y") or self.leftToBottomDiagonalWin("Y"):
            return True

        elif self.boardFilled():
            return True

        return False

    def winner(self):

        if self.horizontalWin("R") or self.verticalWin("R") or self.rightToTopDiagonalWin("R") or self.leftToBottomDiagonalWin("R"):
            return self.redWinOutput

        elif self.horizontalWin("Y") or self.verticalWin("Y") or self.rightToTopDiagonalWin("Y") or self.leftToBottomDiagonalWin("Y"):
            return self.yellowWinOutput

        elif self.boardFilled():
            return self.tieOutput

        return "none"



def generateEmptyBoard(r, c):
    emptyBoard = []
    inputRow = []
    for i in range(r):
        for j in range(c):
            inputRow.append(".")
        emptyBoard.append(inputRow)
        inputRow = []
    return emptyBoard
   
# static dimensions of the board
NUM_ROWS = 6
NUM_COLUMNS = 7

Connect4Board = generateEmptyBoard(NUM_ROWS, NUM_COLUMNS)

Board4 = Board(Connect4Board)
if not Board4.validBoard():
    print("Sorry, Invalid Board...")
    quit()


print("Let's play CONNECT4!")
print("")
print("Player 1 will go first and be red while Player 2 will go second and be yellow.")
print("If you want to quit in the middle of the game, enter 'q' when asked for your move.")
print("Enter a valid column for your move. The columns are listed as follows: ")
print("")

counterPlayer = 0
quitInput = ""

while not Board4.gameFinished():

    print("1 2 3 4 5 6 7")
    print("-------------")
    print(Board4.toText())
    
    if counterPlayer % 2 == 0:
        playerMove = "red"
        playerToken = "R"

    else:
        playerMove = "yellow"
        playerToken = "Y"

    print("")
    playerInput = input("Enter a column to put your " + playerMove + " token: ")

    if playerInput.lower() == "q":
        quitInput = "q"
        break

    # check if the column entered was valid
    if not Board4.validColInput(playerInput):
        print("Invalid input...Please try again.")
        print("\n")
        continue

    elif Board4.columnFilled(int(playerInput)):
        print("This column is already full. Please try a different column to put your " + playerMove +  " token.")
        print("\n")
        continue

    Board4 = Board(Board4.changeBoard(int(playerInput), playerToken))
    counterPlayer += 1

    print("\n")

    if Board4.gameFinished():
        break

print("-------------- FINAL BOARD --------------")
print(Board4.toText())

print("--------------- END GAME ----------------")
time.sleep(2)
print("Processing results...")
print("")
time.sleep(3)
winner = Board4.winner()
if quitInput == "q":
    print("Unfinished game. There is no winner.")

elif winner == Board4.tieOutput:
    print("It's a %s" % winner)

elif winner == Board4.redWinOutput:
    print("...and the winner is...")
    time.sleep(3)
    print("----------------- %s ------------------" % winner)

elif winner == Board4.yellowWinOutput:
    print("...and the winner is...")
    time.sleep(3)
    print("---------------- %s ----------------" % winner)
