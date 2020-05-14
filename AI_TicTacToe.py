# Global variables

board = [[' ', ' ', ' '],[' ', ' ', ' '],[' ', ' ', ' ']] # Initializing a 3X3 Board
movelist = [-1, -1] # Optimal move for the AI, used later

## Suplementary functions

# Prints the updated board
def printBoard(board):
    print('   1  2  3 ')
    for i in range(3):
        print(i + 1, '|' + board[i][0] + '|' + '|' + board[i][1] + '|' + '|' + board[i][2] + '|')

# To get valid user input
def humanMove(board, piece):
    move = input('Please enter a valid move (Row,Column): ')

    # Checking for valid input
    if ((int(move[0]) in range(1,4) and int(move[1]) in range(1, 4)) and board[int(move[0]) -  1][int(move[1]) - 1] == ' '):
        print('Your move is: ', move[0], move[1])
        board[int(move[0]) -  1][int(move[1]) - 1] = piece
    else:
        print('Invalid Move, try again')
        humanMove(board, piece)

# Used in minimax algorithm
def copyBoard(dupli, original):
    for i in range(3):
        for j in range(3):
            dupli[i][j] = original[i][j]

# To check if there is a winner given the current board state
def winCheck(board):
    x_count = 0
    o_count = 0
    for i in range(3):
        if (board[i][0] == board[i][1] and board[i][1] == board[i][2]):
            if board[i][0] != ' ':
                return board[i][0]
    for j in range(3):
        if (board[0][j] == board[1][j] and board[1][j] == board[2][j]):
            if board[0][j] != ' ':
                return board[0][j]
    if (board[0][0] == board[1][1] and board[1][1] == board[2][2]):
        if board[0][0] != ' ':
            return board[0][0]
    if (board[0][2] == board[1][1] and board[1][1] == board[2][0]):
        if board[1][1] != ' ':
            return board[1][1]
    for i in range(3):
        for j in range(3):
            if (board[i][j] == 'X'):
                x_count += 1
            elif (board[i][j] == 'O'):
                o_count += 1

    if x_count + o_count == 9:
        return 'Tie'
    return 'No winner'

# To alternate the players
def switch(player):
    if player == 'X':
        return 'O'
    else:
        return 'X'

# Uses MiniMax algorithm to create undefeatable TicTacToe Player
def invincible_AI(board, player, movelist):

    # Checking if game is over
    if winCheck(board) == player:
        return 1
    elif winCheck(board) == switch(player):
        return -1
    elif winCheck(board) == 'Tie':
        return 0

    move_x = -1
    move_y = -1
    score = -2

    # Iterating through possible moves
    for i in range(3):
        for j in range(3):
            if board[i][j] == ' ':
                # Creating duplicate board to stimulate moves
                newBoard = [[' ', ' ', ' '],[' ', ' ', ' '],[' ', ' ', ' ']]
                copyBoard(newBoard, board)
                newBoard[i][j] = player

                # Minimax assumes that the opponent makes the best possible move
                moveScore = -invincible_AI(newBoard, switch(player), movelist)
                # Updating max score
                if moveScore > score:
                    move_x = i
                    move_y = j
                    score = moveScore

    if move_x == -1 or move_y == -1:
        return 0

    # Stores best possible move
    movelist[0] = move_x + 1
    movelist[1] = move_y + 1
    return score

## Main Game Code
def tictactoe(hint, mode):

    board = [[' ', ' ', ' '],[' ', ' ', ' '],[' ', ' ', ' ']]
    movelist = [-1, -1]
    x_hint = 0
    o_hint = 0

    if mode == 'ai vs human':
        human = input("Do you want to be 'X' or 'O': ")

        # Checking for valid input
        while (human.lower() != 'x' and human.lower() != 'o'):
            print('Incorrect input, try again')
            human = input("Do you want to be 'X' or 'O': ")

        printBoard(board)
        while(winCheck(board) == 'No winner'):
            if human == 'X':
                AI = 'O'
                humanMove(board, human)
                printBoard(board)
                print('\n')
                temp = invincible_AI(board, AI, movelist)
                print("The AI places", AI, "at",movelist[0], movelist[1])
                board[movelist[0] - 1][movelist[1] - 1] = AI
                printBoard(board)
                print('\n')
            elif human == 'O':
                AI = 'X'
                temp = invincible_AI(board, AI, movelist)
                print("The AI places", AI, "at",movelist[0], movelist[1])
                board[movelist[0] - 1][movelist[1] - 1] = AI
                printBoard(board)
                print('\n')
                humanMove(board, human)
                printBoard(board)
                print('\n')

        if (winCheck(board) == 'Tie'):
            print("It's a tie")
        else:
            print("The winner is", winCheck(board))

    elif mode.lower() == 'human vs human':
        player = 'X'
        printBoard(board)

        while(winCheck(board) == 'No winner'):

            if hint: ## Uses the minimax algorithm to provide hints

                # Provide atmost 2 hints

                if player == 'X' and x_hint < 2:
                    score = invincible_AI(board, player, movelist)
                    print('Hint: Place', player, 'at', movelist[0], movelist[1])
                    x_hint += 1

                elif player == 'O' and o_hint < 2:
                    score = invincible_AI(board, player, movelist)
                    print('Hint: Place', player, 'at', movelist[0], movelist[1])
                    o_hint += 1

            humanMove(board, player)
            printBoard(board)
            print('\n')
            player = switch(player)

        ## Checking for winner
        if (winCheck(board) == 'Tie'):
            print("It's a tie")
        else:
            print("The winner is", winCheck(board))

    else:
        # Checking for valid input
        print('Incorrect mode selected, please try again')
        gameMode  = input('Choose a mode (AI vs Human) or (Human Vs Human): ')
        hint_bool = False

        if gameMode.lower() == 'human vs human':
            hint_bool = input('Do you want hints to be provided (Yes or No)')
            if hint_bool.lower() == 'yes' or hint_bool.lower() == 'y':
                hint_bool = True
            else:
                hint_bool = False

        tictactoe(hint_bool, gameMode)

    ## Reseting the game

    repeat = input("Type 'Yes' to play again: ")

    if repeat.lower() == 'yes' or repeat.lower() == 'y':
        # Recalling the game function
        movelist = [-1, -1]
        tictactoe(hint, mode)
    else:
        pass

gameMode  = input('Choose a mode (AI vs Human) or (Human Vs Human): ')
hint_bool = False

if gameMode.lower() == 'human vs human':
    hint_bool = input('Do you want hints to be provided (Yes or No): ')
    if hint_bool.lower() == 'yes' or hint_bool.lower() == 'y':
        hint_bool = True
    else:
        hint_bool = False

tictactoe(hint_bool, gameMode)
