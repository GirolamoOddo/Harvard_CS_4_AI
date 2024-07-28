"""
Tic Tac Toe Player
"""

import math

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
    x_count = sum(row.count(X) for row in board)
    o_count = sum(row.count(O) for row in board)
    return X if x_count <= o_count else O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    return {(i, j) for i in range(3) for j in range(3) if board[i][j] == EMPTY}


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    Raises an exception if the move is invalid.
    """
    i, j = action
    if i < 0 or i >= 3 or j < 0 or j >= 3 or board[i][j] is not EMPTY:
        raise ValueError("Invalid action")

    new_board = [row[:] for row in board]
    new_board[i][j] = player(board)
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] and board[i][0] is not EMPTY:
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] and board[0][i] is not EMPTY:
            return board[0][i]

    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not EMPTY:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not EMPTY:
        return board[0][2]

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    return winner(board) is not None or all(EMPTY not in row for row in board)


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    win = winner(board)
    if win == X:
        return 1
    elif win == O:
        return -1
    else:
        return 0


## this minmax funct implement a fixed depth search and a-b pruning
def minimax(board, max_depth=3):
    """
    Returns the optimal action for the current player on the board.
    Uses alpha-beta pruning and limits the search to a maximum depth.
    """
    if terminal(board):
        return None

    current_player = player(board)

    def max_value(board, alpha, beta, depth):
        if terminal(board) or depth == 0:
            return utility(board), None
        v = -math.inf
        best_action = None
        for action in actions(board):
            min_val, _ = min_value(result(board, action), alpha, beta, depth - 1)
            if min_val > v:
                v = min_val
                best_action = action
            alpha = max(alpha, v)
            if alpha >= beta:
                break
        return v, best_action

    def min_value(board, alpha, beta, depth):
        if terminal(board) or depth == 0:
            return utility(board), None
        v = math.inf
        best_action = None
        for action in actions(board):
            max_val, _ = max_value(result(board, action), alpha, beta, depth - 1)
            if max_val < v:
                v = max_val
                best_action = action
            beta = min(beta, v)
            if alpha >= beta:
                break
        return v, best_action

    if current_player == X:
        _, best_action = max_value(board, -math.inf, math.inf, max_depth)
    else:
        _, best_action = min_value(board, -math.inf, math.inf, max_depth)

    return best_action
