import math
import random
from minimax import get_winner
class MCTSNode:
    def __init__(self, state, parent=None, move=None):
        self.state = state
        self.parent = parent
        self.move = move
        self.children = []
        self.visits = 0
        self.wins = 0.0
        self._untried_moves = None
    def is_fully_expanded(self, get_children):
        if self._untried_moves is None:
            self._untried_moves = list(get_children(self.state))
        return len(self._untried_moves) == 0
    def best_child(self, c=1.414):
        return max(self.children, key=lambda n: (n.wins / n.visits) + c * math.sqrt(math.log(self.visits) / n.visits))
    def expand(self, get_children):
        if self._untried_moves is None:
            self._untried_moves = list(get_children(self.state))
        move, state = self._untried_moves.pop()
        child = MCTSNode(state, parent=self, move=move)
        self.children.append(child)
        return child
    def update(self, result):
        self.visits += 1
        self.wins += result
def mcts(root_state, iterations, get_children, simulate, terminal_test, current_player=1):
    root = MCTSNode(root_state)
    for _ in range(iterations):
        node = root
        while not terminal_test(node.state) and node.is_fully_expanded(get_children):
            node = node.best_child()
        if not terminal_test(node.state):
            node = node.expand(get_children)
        result = simulate(node.state, current_player)
        while node is not None:
            node.update(result)
            node = node.parent
    if not root.children: return None, 0
    best = max(root.children, key=lambda n: n.visits)
    return best.move, best.visits / root.visits
def random_simulate(state, current_player, get_children, terminal_test, evaluate):
    while not terminal_test(state):
        children = list(get_children(state))
        if not children:
            break
        _, state = random.choice(children)
    winner = get_winner(state)
    if winner == current_player:
        return 1.0
    if winner == -current_player:
        return 0.0
    return 0.5