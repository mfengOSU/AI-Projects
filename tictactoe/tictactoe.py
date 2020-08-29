"""
Tic Tac Toe Player
"""

import math
from copy import deepcopy
import random

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    
    if board == initial_state():
        return X
    if sum(row.count(X) for row in board) > sum(row.count(O) for row in board):
        return O
    else:
        return X
    
def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_moves = set()
    for row in range(len(board)):
        for col in range(len(board)):
            if board[row][col] == EMPTY:
                possible_moves.add((row, col))
    return possible_moves


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    result_board = deepcopy(board)
    player_turn = player(board=board)
    # Check if action is valid and return resulting board. Otherwise raise an exception
    if action < (3,3) and action >= (0,0) and board[action[0]][action[1]] == EMPTY:
        result_board[action[0]][action[1]] = player_turn
    else:
        raise Exception("Invalid action for board")
    return result_board

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Check for horizontal wins
    for row in board:
        if row.count(row[0]) == len(board) and row[0] != EMPTY:
            return row[0]
    # Check for vertical wins
    list_transpose = [list(x) for x in zip(*board)]
    for col in list_transpose:
        if col.count(col[0]) == len(board) and col[0] != EMPTY:
            return col[0]
    # Check for both diagonal wins
    [row, col] = [0, 0]
    if board[row][col] == board[row+1][col+1] == board[row+2][col+2] and board[row][col] != EMPTY:
        return board[row][col]
    [row, col] = [0, len(board)-1]
    if board[row][col] == board[row+1][col-1] == board[row+2][col-2] and board[row][col] != EMPTY:
        return board[row][col]
    return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if (sum(row.count(EMPTY) for row in board) == 0) or winner(board=board) != None:
        return True
    return False

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board=board) == X:
        return 1
    if winner(board=board) == O:
        return -1
    return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # no moves possible if game is over
    if terminal(board=board):
        return None
    # Computer plays random move when board is initial state
    if board == initial_state():
        return random.sample(actions(board=board), 1)[0]
    player_turn = player(board=board)
    # Player X maximizes his score/Player O minimizes his score
    if player_turn == X:
        score = -math.inf
        action_list = [] # List of possible non-losing actions 
        for action in actions(board=board):
            # Get the max value of all the minimum values of the opponent
            score = max(score, min_value(board=result(board=board, action=action)))
            # Immediately return action if it is a winning move (score is 1)
            if score == 1:
                return action
            # Only add non-losing moves to the action_list
            if score > -1:
                action_list.append((score, action))
        # Return any action since they are all neutral
        return action_list[0][1]

    else:
        score = math.inf
        action_list = []
        for action in actions(board=board):
            # Get the min value of all the maximum values of the opponent
            score = min(score, max_value(board=result(board=board, action=action)))
            # Immediately return action if it is a winning move (score is -1)
            if score == -1:
                return action
            # Only add non-losing moves to the action_list
            if score < 1:
                action_list.append((score, action))
        # Return any action since they are all neutral
        return action_list[0][1]

def max_value(board):
    """
    Returns max value for maximizing player from the given board state
    """
    if terminal(board=board):
        return utility(board=board)
    score = -math.inf
    for action in actions(board=board):
        score = max(score, min_value(board=result(board=board, action=action)))
        
    return score

def min_value(board):
    """
    Returns min value for minimizing player from the given board state
    """
    if terminal(board=board):
        return utility(board=board)
    score = math.inf
    for action in actions(board=board):
        score = min(score, max_value(board=result(board=board, action=action)))
        
    return score


