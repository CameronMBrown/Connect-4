import sys
from termcolor import cprint

gameState = [["_","_","_","_","_","_",], ["_","_","_","_","_","_",], ["_","_","_","_","_","_",], ["_","_","_","_","_","_",], ["_","_","_","_","_","_",], ["_","_","_","_","_","_",]]

def drawBoard(winner = False):
  print(" ___________")
  for i in range(6): #rows loop
    for j in range(6): #columns loop
      if j == 0:
        print("|" , end="")
        drawPiece(i, j)
        print("|", end="")
      elif j == 5:
        drawPiece(i, j)
        print("|")
      else:
        drawPiece(i, j)
        print("|", end="")
  print(" //       \\\\") # game board "feet"
  if winner != False:
    # if a winner is passed in, display congratulations and reset the game
    print("Congratulations " + winner + " is the winner!")
    playAgain = ""
    while playAgain != "y" and playAgain != "n":
      playAgain = input("would you like to play again? (y/n)")
      if playAgain == "y":
        clearGameState()
        drawBoard()
      elif playAgain == "n":
        return

def turn(player):
  row = None
  column = input("enter a column between 1 - 6")
  if not column.isdigit(): #check for valid input
    print("please enter a number") 
    turn(player)
  column = int(column)-1 #convert to int, and 0 based index
  if column > 5 or column < 0: #check for valid index
    print("looks like you didn't enter a number between 1 and 6, try again.") 
    turn(player)
  if gameState[0][column] != "_": #player chose a full column
    print("that column is full, try again") 
    turn(player)
  for i in range(5, -1, -1):
    # "drop" the piece, find the min row that is unoccupied
    if gameState[i][column] == "_":
      gameState[i][column] = player # store move in gameState
      row = i
      break
  checkForWinner(row, column, player)
  drawBoard() # draw board after each move
  turn(not player) # successful turn, next player's turn

def checkForWinner(row, column, player):
  # checks for 4 in a row in all directions after each turn
  vertical = filterBlanks([gameState[0][column], gameState[1][column], gameState[2][column], gameState[3][column], gameState[4][column], gameState[5][column]])
  horizontal = filterBlanks(gameState[row])
  diagonal_A = filterBlanks(getDiagonal_A(row, column))
  diagonal_B = filterBlanks(getDiagonal_B(row, column))
  if find4InARow(vertical, player) or find4InARow(horizontal, player) or find4InARow(diagonal_A, player) or find4InARow(diagonal_B, player):
    # for in a row in any direction satisfies win condition (or)
    # winner found!
    if player:
      drawBoard("Red")
    else:
      drawBoard("Blue")

def getDiagonal_A(row, column): #\
  # returns an array of adjacent elements to row & column in a diagonal direction ( \ )
  count = 0 
  diag = [gameState[row][column]]
  temp_row = row - 1
  temp_column = column - 1
  while temp_row > -1 and temp_column > -1 and count < 3: # move up, left
    diag = [gameState[temp_row][temp_column]] + diag # prepend to preserve order
    temp_row -= 1
    temp_column -= 1
    count += 1
  count = 0
  temp_row = row + 1
  temp_column = column + 1
  while temp_row < 6 and temp_column < 6 and count < 3: # move down, right
    diag = diag + [gameState[temp_row][temp_column]]
    temp_row += 1
    temp_column += 1
    count += 1
  return diag

def getDiagonal_B(row, column): #/
  # returns an array of adjacent elements to row & column in a diagonal direction ( / )
  count = 0 
  diag = [gameState[row][column]]
  temp_row = row + 1
  temp_column = column - 1
  while temp_row < 6 and temp_column > -1 and count < 3: # move down, left
    diag = [gameState[temp_row][temp_column]] + diag # prepend to preserve order
    temp_row += 1
    temp_column -= 1
    count += 1
  count = 0
  temp_row = row - 1
  temp_column = column + 1
  while temp_row > -1 and temp_column < 6 and count < 3:# move up, right
    diag = diag + [gameState[temp_row][temp_column]]
    temp_row -= 1
    temp_column += 1
    count += 1
  return diag

def find4InARow(arr, player):
  count = 0
  index = 0
  while index < len(arr) and count < 4:
    if arr[index] == player:
      count += 1
      index += 1
    else:
      count = 0 # reset count, needs to be consecutive
      index += 1
  if count == 4: # 4 in a row!
    return True

def drawPiece(row, column):
  # use unicode to draw circle in given row and column
  # cprint used here to give circles the colour for the right player, red or blue
  if gameState[row][column] == True:
    cprint(u'\u25CF', 'red', end="")
  elif gameState[row][column] == False:
    cprint(u'\u25CF', 'blue', end="")
  else: 
    print("_", end="")

def filterBlanks(arr):
  # get just the spaces that are filled, eliminate any "_"
  new_arr = []
  for i in arr:
    if i != "_":
      new_arr = new_arr + [i]
  return new_arr

def clearGameState():
  # reset the gamestate when players want to play again
  global gameState
  gameState = [["_","_","_","_","_","_",],["_","_","_","_","_","_",],["_","_","_","_","_","_",],["_","_","_","_","_","_",],["_","_","_","_","_","_",],["_","_","_","_","_","_",]]

drawBoard()
turn(True) # True = red, False = blue