import math
EMPTY, X, O = 0, 1, -1
def make_board():
    return [EMPTY] * 9
def get_winner(board):
    wins = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
    for a,b,c in wins:
        if board[a] == board[b] == board[c] != EMPTY:
            return board[a]
    return None
def ttt_terminal(board):
    return get_winner(board) is not None or EMPTY not in board
def ttt_evaluate(board):
    w = get_winner(board)
    if w == X: return 1
    if w == O: return -1
    return 0
def ttt_heuristic_evaluate(board):
    winner = get_winner(board)
    if winner == X: return 100
    if winner == O: return -100
    score = 0
    wins = [(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)]
    for a,b,c in wins:
        line = [board[a], board[b], board[c]]
        x_count = line.count(X)
        o_count = line.count(O)
        empty_count = line.count(EMPTY)
        if x_count == 2 and empty_count == 1: score += 10
        elif o_count == 2 and empty_count == 1: score -= 10
        elif x_count == 1 and empty_count == 2: score += 1
        elif o_count == 1 and empty_count == 2: score -= 1
    if board[4] == X: score += 3
    elif board[4] == O: score -= 3
    return score
def ttt_children(board, player=X):
    children = []
    turn = X if board.count(X) == board.count(O) else O
    for i in range(9):
        if board[i] == EMPTY:
            new = board[:]
            new[i] = turn
            children.append((i, new))
    return children
def print_board(board):
    sym = {EMPTY: '.', X: 'X', O: 'O'}
    for r in range(3):
        print(' '.join(sym[board[r*3+c]] for c in range(3)))
    print()
def minimax(state, depth, is_maximizing, get_children, evaluate, terminal_test):
    if terminal_test(state) or depth == 0:
        return evaluate(state), None
    best_move = None
    if is_maximizing:
        best_val = -math.inf
        for move, child in get_children(state):
            val, _ = minimax(child, depth - 1, False, get_children, evaluate, terminal_test)
            if val > best_val:
                best_val = val
                best_move = move
        return best_val, best_move
    else:
        best_val = math.inf
        for move, child in get_children(state):
            val, _ = minimax(child, depth - 1, True, get_children, evaluate, terminal_test)
            if val < best_val:
                best_val = val
                best_move = move
        return best_val, best_move