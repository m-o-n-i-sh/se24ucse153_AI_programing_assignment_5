import math
def alpha_beta(state, depth, alpha, beta, is_maximizing, get_children, evaluate, terminal_test):
    if terminal_test(state) or depth == 0:
        return evaluate(state), None
    best_move = None
    if is_maximizing:
        best_val = -math.inf
        for move, child in get_children(state):
            val, _ = alpha_beta(child, depth - 1, alpha, beta, False, get_children, evaluate, terminal_test)
            if val > best_val:
                best_val = val
                best_move = move
            alpha = max(alpha, best_val)
            if beta <= alpha:
                break
        return best_val, best_move
    else:
        best_val = math.inf
        for move, child in get_children(state):
            val, _ = alpha_beta(child, depth - 1, alpha, beta, True, get_children, evaluate, terminal_test)
            if val < best_val:
                best_val = val
                best_move = move
            beta = min(beta, best_val)
            if beta <= alpha:
                break
        return best_val, best_move
def alpha_beta_root(state, depth, is_maximizing, get_children, evaluate, terminal_test):
    return alpha_beta(state, depth, -math.inf, math.inf, is_maximizing, get_children, evaluate, terminal_test)