
# colors:
color_yellow="\x1b[6;30;43m"
color_undo="\x1b[0m"

# importing required modules:
import random 
import math
import time
import copy

random.seed(time.time()) # this will make sure the sequence of random numbers is different each time.

#######################################################

# we start with creating the board which contains the current state of the game.
currBoard =[[' ' for x in range(3)] for y in range(3)] # list of list with each entry empty space, total 3 rows and 3 cols.

#######################################################

# The following functions are to print relevant stuff:

# @ param: character c, integer r
# @output: prints a horizontal rule of size r, made from char c
def printVisualSep(c, r):
        print()
        for i in range(r): print(c, end=''); 
        print()

# @output: prints the Board array in classic tic-tac-toe game style.
def printBoard(board):
    # printing the content
    for x in range (3):
        for y in range (3):
            # print each element separated by | and appropriate amount of spaces, with newline at the end.
            print(" ",board[x][y],' |' if y!=2 else '\n', sep="", end="") 
        print("-----------" if x!=2 else "") # each line is separated by horizontal dashes

# @output: prints some text to be displayed while playing the game
def printInGameText():
    print()
    print(color_yellow+"[*]"+color_undo+"  Your Move: Enter 1-9 position of the cell")
    print(color_yellow+"[*]"+color_undo+"  Press M to return to main menu")
    print()
    
# @output: prints text to be displayed on main menu
def printMainMenu():
    print(color_yellow+"\n Tic Tac Toe Game!\n Main Menu"+color_undo)
    print()
    print(color_yellow+"[*]"+ color_undo +"  Press S to start a new game")
    print(color_yellow+"[*]"+ color_undo +"  Press Q to quit the game")
    print()

# @output: prints text to be displayed on the difficulty selection menu
def printDiffSelectMenu():
    print(color_yellow+"\n Select Difficulty:"+ color_undo)
    print()
    print(color_yellow+"[*]"+ color_undo +"  Press E for Easy mode")
    print(color_yellow+"[*]"+ color_undo +"  Press I for Impossible mode")
    print()
    print(color_yellow+"[*]"+ color_undo +"  Press M to return to main menu")
    print()

# @output: prints dialogue to be displayed when user wins
def win_msg():
    printVisualSep("/", 27)
    print("///  Congrats! You won! ///", end="")
    printVisualSep("/", 27)
    printBoard(currBoard)
    input("Press Enter to continue ") # allows user to clearly see the board condition, before moving on

# @output: prints dialogue to be displayed when user loses
def lost_msg():
    printVisualSep("/", 36)
    print("// AI won, better luck next time! //", end="")
    printVisualSep("/", 36)
    printBoard(currBoard)
    input("Press Enter to continue ")# allows user to clearly see the board condition, before moving on

# @output: prints dialogue to be displayed when draw happens
def draw_msg():
    printVisualSep("/", 30)
    print()
    print("Draw!")
    print()
    printBoard(currBoard)
    input("Press Enter to continue ")# allows user to clearly see the board condition, before moving on

#########################################################

# Now we implement the functions which will check if user or ai won.
# Note: this program treats O as the user's symbol, and X for ai.

# checks if any col is filled
# @ param: player char ( O or X ) -- for who we check
# @ return: true is at least one col is filled with the player char, false otherwise
def check_col(board, player):
    for y in range(3):
        winner=True
        # if atleast at one location we get a different char, 
        # it means the col isn't fully occupied by the player we're checking for
        for x in range(3):
            if board[x][y]!=player: winner=False
        if winner==True: return True 
    return False 

# checks if any row is filled
# @ param: player char ( O or X ) -- for who we check
# @ return: true is at least one row is filled with the player char, false otherwise
def check_row(board, player):
    for x in range(3):
        winner=True
        # if atleast at one location we get a different char, 
        # it means the row isn't fully occupied by the player we're checking for
        for y in range(3):
            if board[x][y]!=player: winner=False
        if winner: return True 
    return False 


# checks for the diagnols
# @ param: player char ( O or X ) -- for who we check
# @ return: true if at least one of the two col is filled, false otherwise
def check_diag(board,player):
    # there are only two cols to check, so we directly use their postions in Board array:
    if board[0][0]==player and board[1][1]==player and board[2][2]==player: return True 
    elif board[0][2]==player and board[1][1]==player and board[2][0]==player: return True 
    else:
        return False

# this function calls the above 3 function to get if anyone won.
# @return: 0 is nobody won, 1 if user won, 2 if ai won.
def anyoneWon(board):
    # someone wins if either (1) a row, (2) a column or (3) a diagnol is filled.
    if check_col(board,'O') or check_row(board,'O') or check_diag(board,'O'): return 1
    elif check_col(board,'X') or check_row(board,'X') or check_diag(board,'X'): return 2
    else: return 0


# this function takes a board, and checks if all cells are filled.
# if nobody wins and all cells are filled, we'll know its a draw.
# @return: true is draw, false otherwise
def checkDraw(board):
    filled_boxes=0
    for i in range(3):
        for j in range(3): 
            if board[i][j]!=' ': filled_boxes+=1 # iterate thru all cells, count number of filled cells
    if filled_boxes==9: return True 
    else: return False

#############################################################

# asks user to select difficulty level
# @return: 1 if easy mode selected, 2 for impossible mode, 0 for returning to main menu
def get_difficulty():
    printVisualSep("-", 40)
    printDiffSelectMenu() # first prints the menu
    usr_in=input("Input: ") # then asks for user response
    # then the function processes it:
    usr_in=usr_in.replace(" ", "") # removing extra spaces

    if usr_in== 'E' or usr_in== 'e':
        return 1
    elif usr_in== 'I' or usr_in == 'i':
        return 2
    elif usr_in== 'M' or usr_in == 'm':
        return 0 # return to main menu
    else: # error handling:
        print()
        print("Error: Invalid input")
        input("Press Enter to continue ")
        return -1 

# this function fills cells of a board
# @param: the board to be filled, index(1-9) of cell to fill, and a char "user" to fill it with
# @return: -1 if cell is already filled, 1 otherwise
def fill_a_cell(board, index, user):
    row=(index-1)// 3
    col=(index-1) % 3
    if board[row][col]==' ': # check if its empty
        board[row][col]=user
        return 1
    else: return -1

# check if a string s represents an integer
# @return: true is s is integer, false otherwise 
def isInteger(s):
    try: 
        int(s)
        return True
    except ValueError: # if trying int(s) returns an error, its not int.
        return False

# finds all cells that are empty yet
# @return: a list containing position of empty cells
def getEmptyCells(board):
    available_moves=[]
    for i in range(3): 
        for j in range(3):
            if board[i][j]==' ': available_moves.append((i*3+j+1)) #if empty, add it to the list
    return available_moves 

# this is the func which prints the board, asks for user's move and then fills the corresponding cell in the board.
# @return: 0 if user asked to return to main Menu
#          -1 if the input is invalid
#          1 if the user-move is made successfully 
def user_move():
    printVisualSep("-", 40)
    printInGameText() # first print relevant text
    printBoard(currBoard) # show the board
    usr_in=input("Input: ") # ask for input
    usr_in=usr_in.replace(" ", "") # remove extra spaces

    if usr_in == 'M' or usr_in == 'm': # return-to-MainMenu 
        print("\nReturning to main menu...")
        return 0 
    if len(usr_in) != 1 or not isInteger(usr_in): # invalid input
        print()
        print("Error: Invalid input")
        input("Press enter to continue ")
        return -1
    elif int(usr_in)>9 or int(usr_in)<1: # invalid input
        print()
        print("Error: Invalid input")
        input("Press enter to continue ")
        return -1

    fill_res=fill_a_cell(currBoard, int(usr_in), 'O') # call the fill_a_cell function, and
    if fill_res==-1:                                  # if the function returns -1, print error msg
        print()
        print("Error: Given cell already filled! ")
        input("Press enter to continue ")
        return -1
    else : return 1 

################################################################
    
# Implementing the minimax algorithm:

# @param:  
#        position, refers to the board we're operation on.
#        depth, number of moves left till the board is filled 
#        alpha-beta, for pruning optimization, reducing the number of states to check
#        isMaxiPlayer: true if its AI for which we want to maximize score, false for user.
# @return: a dictionary containing 2 entries: 
#           first for "index", the position of cell to be filled 
#           second for "score", resulting score from the move specified in "index"
#          
def minimax(position, depth, alpha, beta, isMaxiPlayer):
    # for depth 0 (no move possible) or someone won, we have the base case:
    whoWon=anyoneWon(position)
    if depth==0 or whoWon!=0:
        if whoWon==2:
            return {'index':None, 'score':10-depth}
        elif whoWon==1: 
            return {'index':None, 'score': depth-10}
        else : return {'index' :None, 'score': 0} 

    if isMaxiPlayer: # the maximizing player's turn: 
        childs=getEmptyCells(position)  # the list of empty cells       
        bestScore={'index':None, 'score':-math.inf}
        for child_index in childs: # among every possible child of the current position we check:
            child_position= copy.deepcopy(position)
            fill_a_cell(child_position, child_index, 'X')                 # fill the cell and 
            filled_eval=minimax(child_position, depth-1,alpha,beta,False) # get the score resulting from this move
            if filled_eval['score']>bestScore["score"]:                   # if the score is better, we change the bestscore accordingly
                bestScore["score"]=filled_eval['score']
                bestScore["index"]=child_index
            alpha=max(alpha, filled_eval['score']) # pruning the solution
            if beta <= alpha:
                break
        return bestScore

    else: # minimizating player's turn:
        childs=getEmptyCells(position)   # the list of empty cells
        bestScore={'index':None, 'score':math.inf}
        for child_index in childs: # among every possible child of the current position we check:
            child_position= copy.deepcopy(position)
            fill_a_cell(child_position, child_index, 'O')                # fill the cell and
            filled_eval=minimax(child_position, depth-1,alpha,beta,True) # get the score resulting from this move
            if filled_eval['score']<bestScore["score"]:                  # if the score is lower, we change best score accordingly
                bestScore["score"]=filled_eval['score']
                bestScore["index"]=child_index
            beta=min(beta,filled_eval['score']) # pruning the solution
            if beta <= alpha:
                break
        return bestScore

# ai making its move, based on the difficulty level provided in parameters
def ai_move(difficulty):

    theMove=0 # this variable contains the move ai will make.

    # Easy mode: random moves
    if difficulty==1:
        # we first get the list of available moves:
        available_moves=getEmptyCells(currBoard)
        # now we'll select a random move from the generated list.
        theMove=random.choice(available_moves)

    # Impossible mode: minimax algo
    elif difficulty==2:
        # First we create a copy of current Board, which is the current postion
        position=copy.deepcopy(currBoard) # deepcopy allows to make a full copy of the board
        # find the list of possible moves:
        available=getEmptyCells(position)
        # minimax func requires depth, which is here, the number of moves possible
        depth=len(available)
        # calling the minimax function:
        theMove=minimax(position, depth, -math.inf, math.inf, True)['index']
        # we grab the index from the return object of the function, stored in theMove variable

    # got the move, now printing the board state for user to see the the move: 
    printVisualSep("/", 40)
    print()
    print(color_yellow+" AI's move: "+color_undo, theMove) # showing in text AI's move
    fill_a_cell(currBoard,theMove, 'X') # filling the board with the move
        
#################################################################
#################################################################

# this function initiates and runs the game:

def game_on():

    #first we reset the Board array to all empty spaces.
    for x in range(3):
        for y in range(3):
            currBoard[x][y]=' ' 

   # get difficulty 
    difficulty = get_difficulty()
    if difficulty==-1: # if some error occurs, keep asking for user input till it gets right
        while difficulty == -1 :
            difficulty = get_difficulty()
    if difficulty == 0: # exit call 
        printVisualSep("-", 40)
        return

    # game starts, and will end when someone wins or all cells get filled

    # for the first move, we randomly decides if user goes first or ai. 
    if random.random() > 0.5: 
        ai_move(difficulty) # if the random value is greater than 0.5, we allow ai to make the first move.
    # no need to check if someone won, since this is the first move.

    while True :
        # FIRST USER MAKES THEIR MOVE:

        # collecting user input:
        user_res= user_move()
        if user_res == -1 : # if error occurs, we ask input again till we get a valid response:
            while(user_res==-1): user_res=user_move()
        if user_res == 0: 
            break # exit call, break out of the infinte game loop

        # checking if user won or draw happened:
        if anyoneWon(currBoard) !=0: 
            win_msg() #printing winning dialogue
            break # break out of the infinite game loop
        if checkDraw(currBoard):
            draw_msg() #printing draw msg
            break # break out of the infinite game loop
        
        # THEN AI MAKES ITS MOVE:
        ai_move(difficulty)

        # checking if ai won or draw:
        if anyoneWon(currBoard)!=0: # if someone won it has to be ai
            lost_msg() # so we print user lost msg
            break # break out of the infinite game loop
        if checkDraw(currBoard):
            draw_msg() #printing draw msg
            break # break out of the infinite game loop

    # after finishing the game we print a line
    printVisualSep("/",40) 
# function ends................

###############################################
###############################################

# this loop will run when program starts:
while True:
    # This loop runs the game.
    # First we print the main menu:
    printMainMenu()
    # then ask for user response
    usr_in=input("Input: ")
    # then process it 
    usr_in=usr_in.replace(" ", "") # removing extra spaces, if any

    if usr_in=="s" or usr_in=="S": game_on() # game_on function starts the game
    elif usr_in=="q" or usr_in=="Q":# exit call 
        print("\nExiting the game!")
        break
    else: # error handling 
        print()
        print("Error: Unknown option! ")
        input("Press enter to continue ")

