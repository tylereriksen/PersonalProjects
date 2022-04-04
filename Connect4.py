'''
    This file's purpose is to try to to program the popular Connect 4 board game.
    It will contain a class for the Connect 4 board game that will implement many
    functions to recreate the real life rules and moves of the game.

'''

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


ROWS = 6
COLUMNS = 7
Connect4Game = Connect4(ROWS, COLUMNS)

print("Let's play CONNECT4!")
print("")
print("Player 1 will go first and be red while Player 2 will go second and be yellow.")
print("If you want to quit in the middle of the game, enter 'q' when asked for your move.")
print("Enter a valid column for your move. The columns are listed as follows: ")
print("")

counterPlayer = 0
quitInput = "q"

while not Connect4Game.gameFinished():

    print("1 2 3 4 5 6 7")
    print("-------------")
    print(Connect4Game.toText())
    
    # this is for determining the which player token will be used
    if counterPlayer % 2 == 0:
        playerMove = "red"
        playerToken = Connect4Game.PLAYERMOVE1

    else:
        playerMove = "yellow"
        playerToken = Connect4Game.PLAYERMOVE2

    print("")
    playerInput = input("Enter a column to put your " + playerMove + " token: ")

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
    counterPlayer += 1

    print("\n")

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