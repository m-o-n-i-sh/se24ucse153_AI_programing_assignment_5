import math
def heuristic_alpha_beta(state, depth, alpha, beta, is_maximizing, get_children, evaluate, terminal_test, order_moves=None, quiescence_depth=0):
    if terminal_test(state):
        return evaluate(state), None
    if depth == 0:
        if quiescence_depth > 0:
            return quiescence_search(state, quiescence_depth, alpha, beta, is_maximizing, get_children, evaluate, terminal_test)
        return evaluate(state), None
    children = get_children(state)
    if order_moves:
        children = order_moves(children, state, is_maximizing, evaluate)
    best_move = None
    if is_maximizing:
        best_val = -math.inf
        for move, child in children:
            val, _ = heuristic_alpha_beta(child, depth - 1, alpha, beta, False, get_children, evaluate, terminal_test, order_moves, quiescence_depth)
            if val > best_val:
                best_val = val
                best_move = move
            alpha = max(alpha, best_val)
            if beta <= alpha: break
        return best_val, best_move
    else:
        best_val = math.inf
        for move, child in children:
            val, _ = heuristic_alpha_beta(child, depth - 1, alpha, beta, True, get_children, evaluate, terminal_test, order_moves, quiescence_depth)
            if val < best_val:
                best_val = val
                best_move = move
            beta = min(beta, best_val)
            if beta <= alpha: break
        return best_val, best_move
def quiescence_search(state, depth, alpha, beta, is_maximizing, get_children, evaluate, terminal_test):
    stand_pat = evaluate(state)
    if depth == 0 or terminal_test(state):
        return stand_pat, None
    if is_maximizing:
        if stand_pat >= beta: return stand_pat, None
        alpha = max(alpha, stand_pat)
        best_val = stand_pat
        best_move = None
        for move, child in get_children(state):
            val, _ = quiescence_search(child, depth - 1, alpha, beta, False, get_children, evaluate, terminal_test)
            if val > best_val:
                best_val = val
                best_move = move
            alpha = max(alpha, best_val)
            if beta <= alpha: break
        return best_val, best_move
    else:
        if stand_pat <= alpha: return stand_pat, None
        beta = min(beta, stand_pat)
        best_val = stand_pat
        best_move = None
        for move, child in get_children(state):
            val, _ = quiescence_search(child, depth - 1, alpha, beta, True, get_children, evaluate, terminal_test)
            if val < best_val:
                best_val = val
                best_move = move
            beta = min(beta, best_val)
            if beta <= alpha: break
        return best_val, best_move
def default_move_ordering(children, state, is_maximizing, evaluate):
    scored = []
    for move, child in children:
        score = evaluate(child)
        scored.append((score, move, child))
    scored.sort(key=lambda x: x[0], reverse=is_maximizing)
    return [(move, child) for score, move, child in scored]
def heuristic_alpha_beta_root(state, depth, is_maximizing, get_children, evaluate, terminal_test, order_moves=default_move_ordering, quiescence_depth=2):
    return heuristic_alpha_beta(state, depth, -math.inf, math.inf, is_maximizing, get_children, evaluate, terminal_test, order_moves, quiescence_depth)