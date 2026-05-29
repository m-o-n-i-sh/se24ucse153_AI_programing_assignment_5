import math
import random
import time
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from minimax import (minimax, make_board, ttt_terminal, ttt_evaluate, ttt_heuristic_evaluate,
                     ttt_children, get_winner, print_board, X, O, EMPTY)
from alpha_beta import alpha_beta_root
from heuristic_alpha_beta import heuristic_alpha_beta_root, default_move_ordering
from mcts import MCTSNode, mcts, random_simulate
def demonstrate_algorithms():
    board = [X, EMPTY, O, EMPTY, X, EMPTY, EMPTY, EMPTY, EMPTY]
    print("\nCurrent Board State (O's turn to move):")
    print_board(board)
    print("-" * 60)
    print("1. MINIMAX (Exhaustive Search)")
    t0 = time.time()
    val_mm, move_mm = minimax(board, 9, False, ttt_children, ttt_evaluate, ttt_terminal)
    t_mm = time.time() - t0
    print(f"   => Chose Move: {move_mm} | Score: {val_mm} | Time: {t_mm:.4f}s\n")
    print("2. ALPHA-BETA PRUNING (Optimized Search)")
    t0 = time.time()
    val_ab, move_ab = alpha_beta_root(board, 9, False, ttt_children, ttt_evaluate, ttt_terminal)
    t_ab = time.time() - t0
    print(f"   => Chose Move: {move_ab} | Score: {val_ab} | Time: {t_ab:.4f}s\n")
    print("3. HEURISTIC ALPHA-BETA (Depth-Limited: 4)")
    t0 = time.time()
    val_hab, move_hab = heuristic_alpha_beta_root(
        board, 4, False, ttt_children, ttt_heuristic_evaluate, ttt_terminal,
        order_moves=default_move_ordering, quiescence_depth=0
    )
    t_hab = time.time() - t0
    print(f"   => Chose Move: {move_hab} | Score: {val_hab} | Time: {t_hab:.4f}s\n")
    print("4. MONTE CARLO TREE SEARCH (Probabilistic: 1000 iterations)")
    simulate = make_mcts_simulate(ttt_children, ttt_terminal, ttt_evaluate)
    t0 = time.time()
    move_mcts, conf = mcts(board, 1000, ttt_children, simulate, ttt_terminal, current_player=O)
    t_mcts = time.time() - t0
    print(f"   => Chose Move: {move_mcts} | Win Confidence: {conf:.2%} | Time: {t_mcts:.4f}s\n")
def test_minimax_ttt_optimal():
    board = make_board()
    val, move = minimax(board, 9, True, ttt_children, ttt_evaluate, ttt_terminal)
    assert move is not None
    assert val == 0
    print(f"[PASS] Minimax: empty board score={val}, first move={move}")
def test_minimax_winning_move():
    board = [X, X, EMPTY, O, O, EMPTY, EMPTY, EMPTY, EMPTY]
    val, move = minimax(board, 9, True, ttt_children, ttt_evaluate, ttt_terminal)
    assert move == 2
    print(f"[PASS] Minimax: detects winning move={move}, val={val}")
def test_minimax_blocking_move():
    board = [O, O, EMPTY, X, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY]
    val, move = minimax(board, 9, True, ttt_children, ttt_evaluate, ttt_terminal)
    assert move == 2
    print(f"[PASS] Minimax: blocks opponent at move={move}")
def test_minimax_terminal_win():
    board = [X, X, X, O, O, EMPTY, EMPTY, EMPTY, EMPTY]
    val, move = minimax(board, 9, True, ttt_children, ttt_evaluate, ttt_terminal)
    assert val == 1
    print(f"[PASS] Minimax: terminal win detected val={val}")
def test_minimax_terminal_loss():
    board = [O, O, O, X, X, EMPTY, EMPTY, EMPTY, EMPTY]
    val, move = minimax(board, 9, False, ttt_children, ttt_evaluate, ttt_terminal)
    assert val == -1
    print(f"[PASS] Minimax: terminal loss detected val={val}")
def test_alpha_beta_same_as_minimax():
    board = make_board()
    t0 = time.time()
    val_mm, move_mm = minimax(board, 9, True, ttt_children, ttt_evaluate, ttt_terminal)
    t_mm = time.time() - t0
    t0 = time.time()
    val_ab, move_ab = alpha_beta_root(board, 9, True, ttt_children, ttt_evaluate, ttt_terminal)
    t_ab = time.time() - t0
    assert val_mm == val_ab
    print(f"[PASS] Alpha-Beta: same score as Minimax ({val_mm}), "
          f"MM={t_mm:.3f}s AB={t_ab:.3f}s speedup={t_mm/max(t_ab,0.0001):.1f}x")
def test_alpha_beta_win_detection():
    board = [X, X, EMPTY, O, O, EMPTY, EMPTY, EMPTY, EMPTY]
    val, move = alpha_beta_root(board, 9, True, ttt_children, ttt_evaluate, ttt_terminal)
    assert move == 2 and val == 1
    print(f"[PASS] Alpha-Beta: win detected move={move} val={val}")
def test_alpha_beta_block_detection():
    board = [O, O, EMPTY, X, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY]
    val, move = alpha_beta_root(board, 9, True, ttt_children, ttt_evaluate, ttt_terminal)
    assert move == 2
    print(f"[PASS] Alpha-Beta: blocking move={move}")
def test_alpha_beta_depth_limited():
    board = make_board()
    val, move = alpha_beta_root(board, 3, True, ttt_children, ttt_evaluate, ttt_terminal)
    assert move is not None
    print(f"[PASS] Alpha-Beta depth-limited: move={move} val={val}")
def test_heuristic_ab_consistency():
    board = make_board()
    val_ab, move_ab = alpha_beta_root(board, 6, True, ttt_children, ttt_evaluate, ttt_terminal)
    val_hab, move_hab = heuristic_alpha_beta_root(
        board, 6, True, ttt_children, ttt_evaluate, ttt_terminal,
        order_moves=default_move_ordering, quiescence_depth=0
    )
    assert val_ab == val_hab
    print(f"[PASS] Heuristic AB: consistent with AB val={val_hab} move={move_hab}")
def test_heuristic_ab_move_ordering_speedup():
    board = make_board()
    t0 = time.time()
    val1, m1 = alpha_beta_root(board, 7, True, ttt_children, ttt_evaluate, ttt_terminal)
    t1 = time.time() - t0
    t0 = time.time()
    val2, m2 = heuristic_alpha_beta_root(
        board, 7, True, ttt_children, ttt_evaluate, ttt_terminal,
        order_moves=default_move_ordering, quiescence_depth=0
    )
    t2 = time.time() - t0
    assert val1 == val2
    print(f"[PASS] Heuristic AB ordering: AB={t1:.3f}s HAB={t2:.3f}s "
          f"speedup={t1/max(t2,0.0001):.1f}x")
def test_heuristic_ab_wins():
    board = [X, X, EMPTY, O, O, EMPTY, EMPTY, EMPTY, EMPTY]
    val, move = heuristic_alpha_beta_root(
        board, 9, True, ttt_children, ttt_heuristic_evaluate, ttt_terminal
    )
    assert move == 2 and val == 100
    print(f"[PASS] Heuristic AB: win detected move={move}")
def make_mcts_simulate(get_children, terminal_test, evaluate):
    def sim(state, player):
        return random_simulate(state, player, get_children, terminal_test, evaluate)
    return sim
def test_mcts_returns_move():
    board = make_board()
    simulate = make_mcts_simulate(ttt_children, ttt_terminal, ttt_evaluate)
    move, confidence = mcts(board, 500, ttt_children, simulate, ttt_terminal)
    assert move is not None and 0 <= move <= 8
    print(f"[PASS] MCTS: returns valid move={move} confidence={confidence:.2f}")
def test_mcts_wins_when_possible():
    board = [X, X, EMPTY, O, O, EMPTY, EMPTY, EMPTY, EMPTY]
    simulate = make_mcts_simulate(ttt_children, ttt_terminal, ttt_evaluate)
    move, _ = mcts(board, 1000, ttt_children, simulate, ttt_terminal)
    assert move == 2
    print(f"[PASS] MCTS: selects winning move={move}")
def test_mcts_blocks_opponent():
    simulate = make_mcts_simulate(ttt_children, ttt_terminal, ttt_evaluate)
    board = [X, X, EMPTY, O, O, EMPTY, EMPTY, EMPTY, EMPTY]
    correct_blocks = 0
    for _ in range(10):
        move, _ = mcts(board, 800, ttt_children, simulate, ttt_terminal)
        if move == 2:
            correct_blocks += 1
    assert correct_blocks >= 7, f"MCTS blocked correctly only {correct_blocks}/10 times"
    print(f"[PASS] MCTS: blocks/wins at move=2 in {correct_blocks}/10 trials (both X win and O block)")
def test_mcts_vs_random_winrate():
    simulate = make_mcts_simulate(ttt_children, ttt_terminal, ttt_evaluate)
    wins = draws = losses = 0
    for _ in range(50):
        board = make_board()
        current = X
        while not ttt_terminal(board):
            if current == X:
                move, _ = mcts(board, 200, ttt_children, simulate, ttt_terminal)
            else:
                children = ttt_children(board)
                move, _ = random.choice(children) if children else (None, board)
            if move is not None:
                board = board[:]
                board[move] = current
            current = O if current == X else X
        w = get_winner(board)
        if w == X: wins += 1
        elif w == O: losses += 1
        else: draws += 1
    win_rate = wins / 50
    assert win_rate >= 0.5
    print(f"[PASS] MCTS vs random: wins={wins} draws={draws} losses={losses} "
          f"winrate={win_rate:.0%}")
def test_mcts_terminal_state():
    board = [X, X, X, O, O, EMPTY, EMPTY, EMPTY, EMPTY]
    simulate = make_mcts_simulate(ttt_children, ttt_terminal, ttt_evaluate)
    move, _ = mcts(board, 100, ttt_children, simulate, ttt_terminal)
    assert move is None
    print(f"[PASS] MCTS: returns None on terminal state")
def run_all_tests():
    tests = [
        ("Minimax - Optimal play on empty board",        test_minimax_ttt_optimal),
        ("Minimax - Detects winning move",               test_minimax_winning_move),
        ("Minimax - Blocks opponent",                    test_minimax_blocking_move),
        ("Minimax - Terminal win",                       test_minimax_terminal_win),
        ("Minimax - Terminal loss",                      test_minimax_terminal_loss),
        ("Alpha-Beta - Same result as Minimax",          test_alpha_beta_same_as_minimax),
        ("Alpha-Beta - Win detection",                   test_alpha_beta_win_detection),
        ("Alpha-Beta - Block detection",                 test_alpha_beta_block_detection),
        ("Alpha-Beta - Depth limited",                   test_alpha_beta_depth_limited),
        ("Heuristic AB - Consistent with AB",            test_heuristic_ab_consistency),
        ("Heuristic AB - Move ordering speedup",         test_heuristic_ab_move_ordering_speedup),
        ("Heuristic AB - Win detection",                 test_heuristic_ab_wins),
        ("MCTS - Returns valid move",                    test_mcts_returns_move),
        ("MCTS - Selects winning move",                  test_mcts_wins_when_possible),
        ("MCTS - Blocks opponent",                       test_mcts_blocks_opponent),
        ("MCTS - Win rate vs random",                    test_mcts_vs_random_winrate),
        ("MCTS - Handles terminal state",                test_mcts_terminal_state),
    ]
    passed = failed = 0
    print("=" * 60)
    print("Test Cases")
    print("=" * 60)
    for name, fn in tests:
        print(f"\nTest: {name}")
        try:
            fn()
            passed += 1
        except Exception as e:
            print(f"[FAIL] {e}")
            failed += 1
    print("\n" + "=" * 60)
    print(f"Results: {passed} passed, {failed} failed out of {len(tests)} tests")
    print("=" * 60)
if __name__ == "__main__":
    demonstrate_algorithms()
    run_all_tests()