# For sources, see end of file

from math import inf as infinity
from os import system

ROW_COUNT = 6
COLUMN_COUNT = 7

HUMAN = -1
COMP = +1


board = [
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0]
    ]

# This evaluates the score of the various moves. Returns the value of state of board
def evaluate(state):
    score = 0

    if wins(state, COMP):
        score = +infinity
    elif wins(state, HUMAN):
        score = -infinity
    else:
        score = 0
    return score

# Returns True if player wins.
# Marks all the ways someone can win (the "player" whether comp or human, is passed in as argument)
def wins(state, player):
    # Win by vertical four
    for row in range(3):
        for col in range(7):
            if state[row][col] == player and state[row+1][col] == player and state[row+2][col] == player and state[row+3][col] == player:
                return True

    # Win by horizontal
    for row in range(6):
        for col in range(4):
            if state[row][col] == player and state[row][col+1] == player and state[row][col+2] == player and state[row][col+3] == player:
                return True

    # Win by negative slope diagonal
    for row in range(3):
        for col in range(4):
            if state[row][col] == player and state[row+1][col+1] == player and state[row+2][col+2] == player and state[row+3][col+3] == player:
                return True

    # Win by positve slope diagonal
    for row in range(3):
        for col in range(4):
            if state[row][col+3] == player and state[row+1][col-1+3] == player and state[row+2][col-2+3] == player and state[row+3][col-3+3] == player:
                return True

    return False

# The below returns true if there's a win at all
def game_over(state):
    return wins(state, HUMAN) or wins(state, COMP)

# Stores the row,column pairs of empty cells in a list.
def empty_cells(state):
    cells = []

    for x, row in enumerate(state):
        for y, cell in enumerate(row):
            if cell == 0:
                cells.append([x, y])
    return cells

# Checks board to see that the move is valid.
# Returns row where the piece can go to given the column, and -1 if invalid
def valid_move(col):
    for row in range(ROW_COUNT):
        if [5 - row, col] in empty_cells(board):
            return 5 - row
    return -1

# Sets move on the board, as long as the move is valid.
def set_move(col, player):
    row = valid_move(col)
    if row != -1:
        board[row][col] = player
        return True
    else:
        return False

# Creates list for minimax to iterate over.
def possible_moves(state):
    cells = []
    for row in range(ROW_COUNT):
        for col in range(COLUMN_COUNT):
            if (row == 5 and state[row][col] == 0) or (state[row][col] == 0 and state[row+1][col] != 0):
                cells.append([row, col])
    return cells


# Determins best move, returning the column number and score
# AI tries to maximize, human to minimize.
def minimax(state, depth, player):

    # Initializing score, to be changed and then returned.
    # Negative of what the respective players are trying to minimized is put as value here, since there will be a comparison later.
    if player == COMP:
        best = [-1, -infinity]
    else: # player is HUMAN
        best = [-1, +infinity]

    # case where board is full or game over--outcome  determined
    if depth == 0 or game_over(state):
        score = evaluate(state)
        return [-1, score]

    # Juicy part with lots of recurisivity--tree lives here.
    # iterating over each empty cell (row,column), x is row, y is column
    for cell in possible_moves(state):
        row, col = cell[0], cell[1]
        state[row][col] = player
        # Minimax called for the next turn...
        score = minimax(state, depth - 1, -player)
        # here is where for-loop runs for ALL the empty cells of the OTHER player, returning scores of win/lose/draw.
        state[row][col] = 0
        
        # Once all the moves have been analyzed the algorithm will give spit out the best option
        # The best move is preventing yourself from losing--making the winning move. 
        score[0] = col

        # How the computer maximizes
        if player == COMP:
            if score[1] > best[1]:
                best = score
        else: # For human, we want smaller value.
            if score[1] < best[1]:
                best = score
    return best

# Prints board on terminal
def render(state, c_choice, h_choice):
    # Chars is dictionary for key-value pair, since board is initialized to all 0s,
    # and human is -1, comp is +1, and later it is printed as X or O depending on choice.
    chars = {
        -1: h_choice,
        +1: c_choice,
        0: ' '
    }
    str_line = '-----------------------------------'

    print('\n' + str_line)
    for row in state:
        for cell in row:
            symbol = chars[cell]
            print(f'| {symbol} |', end='')
        print('\n' + str_line)


def ai_turn(c_choice, h_choice):

    depth = 5
    if depth == 0 or game_over(board):
        return

    render(board, c_choice, h_choice)
    print(f'Computer turn [{c_choice}]')

    # if AI starts, starts in the middle
    if len(empty_cells(board)) == 42:
        y = 3

    # Figure out best move, using minimax algorithm.
    else:
        move = minimax(board, depth, COMP)
        y = move[0]
        print(f"Computer's move: {move[0]+1}")

    set_move(y, COMP)


def human_turn(c_choice, h_choice):

    # Determine if game over
    cells_empty = len(empty_cells(board))
    if cells_empty == 0 or game_over(board):
        return

    render(board, c_choice, h_choice)
    print(f'Human turn [{h_choice}]')

    # Obtain valid move
    move = -1
    while move < 0 or move > 7:
        try:
            # For valid moves
            move = int(input('Your turn (columns 1-7): ')) - 1
             # Getting value using key in dict.
            can_move = set_move(move, HUMAN) # Note that set_move calls is_valid function

            # For invalid moves/quitting game--
            if not can_move:
                print('You cannot place it there-choose again')
                move = -1
        except (EOFError, KeyboardInterrupt):
            print('Bye')
            exit()
        except (KeyError, ValueError):
            print('Please choose a valid key')

# For the below, I give credit to the source identified below.
def main():
    h_choice = ''  # X or O
    c_choice = ''  # X or O
    first = ''  # if human is the first

    # Human chooses X or O to play
    while h_choice != 'O' and h_choice != 'X':
        try:
            print('')
            h_choice = input('Choose X or O\nChosen: ').upper()
        # Quitting
        except (EOFError, KeyboardInterrupt):
            print('Bye')
            exit()
        # Invalid move
        except (KeyError, ValueError):
            print('Please choose correctly >:|')

    # Setting computer's choice
    if h_choice == 'X':
        c_choice = 'O'
    else:
        c_choice = 'X'

    # Human may starts first
    while first != 'Y' and first != 'N':
        try:
            first = input('First to start?[y/n]: ').upper()
        # Quitting
        except (EOFError, KeyboardInterrupt):
            print('Bye')
            exit()
        # Invalid input
        except (KeyError, ValueError):
            print('Input not valid XD')

    #------------------------ above is configuration for game, which I have taken from

    # Main loop of this game--so smart
    while len(empty_cells(board)) > 0 and not game_over(board):
        if first == 'N':
            ai_turn(c_choice, h_choice)
            first = ''

        human_turn(c_choice, h_choice)

        ai_turn(c_choice, h_choice)

    # Game over message
    if wins(board, HUMAN):
        print(f'Your\'s victory move [{h_choice}]')
        render(board, c_choice, h_choice)
        print('YOU WIN!')
    elif wins(board, COMP):
        print(f'Computer\'s victory move [{c_choice}]')
        render(board, c_choice, h_choice)
        print('YOU LOSE, No!')
    else:
        render(board, c_choice, h_choice)
        print('DRAW!')

    exit()

if __name__ == '__main__':
    main()

# For tic-tac-toe implementation, I've looked at https://github.com/Cledersonbc/tic-tac-toe-minimax
# for implementation of connect 4, I've referenced https://github.com/KeithGalli/Connect4-Python/blob/master/connect4.py

