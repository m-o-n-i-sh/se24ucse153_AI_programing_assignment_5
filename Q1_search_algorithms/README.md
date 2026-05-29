# Search Algorithms Implementation
This repository contains the implementation of four search algorithms applied to the game of Tic-Tac-Toe. 
## Problem statement:
 *"Implement the Minimax search algorithm, Alpha-Beta search, Heuristic alpha-beta search, and Monte-Carlo Tree search. Submit the code, adequate documentation, and testcases to support the working and correctness of your implementation."*

## File Structure

The project is divided into 5 distinct files for clarity and maintainability:

* `minimax.py`: Contains the game environment (board, win detection) and the exhaustive Minimax search algorithm.
* `alpha_beta.py`: Contains the optimized Alpha-Beta Pruning algorithm.
* `heuristic_alpha_beta.py`: Contains depth-limited Alpha-Beta search with custom move ordering and heuristic evaluation.
* `mcts.py`: Contains the Monte Carlo Tree Search (MCTS) implementation with node expansion, simulation, and backpropagation.
* `search_algorithms.py`: The main execution script. Contains the visual demonstration and the automated test suite (17 test cases).

---

## Algorithms Implemented

### 1. Minimax Search
An search algorithm that explores the entire game tree down to the terminal states. It assumes both players play perfectly, maximizing the score for player `X` (+1) and minimizing the score for player `O` (-1).
* **Correctness:** Guarantees an optimal move.

### 2. Alpha-Beta Pruning
An optimized version of Minimax. It keeps track of the best scores guaranteed so far (`alpha` and `beta`) and prunes (ignores) branches of the game tree that the opponent will never allow the agent to reach.
* **Correctness:** Returns the *exact same optimal move* as Minimax but requires exploring significantly fewer nodes.

### 3. Heuristic Alpha-Beta Search
Because exhaustive search is too slow for complex games, this algorithm searches only to a limited depth. Once the depth limit is reached, it relies on a Heuristic Evaluation Function to guess the board's value.
* **Heuristic Used:** Assigns points for controlling the center, having two in a row (threats), and penalizes opponent threats.
* **Move Ordering:** Evaluates highly-scored moves first, drastically increasing the efficiency of alpha-beta pruning.

### 4. Monte Carlo Tree Search (MCTS)
A probabilistic search algorithm that does not rely on hardcoded heuristic rules. Instead, it uses the UCB (Upper Confidence Bound) formula to balance exploration and exploitation. It simulates hundreds of random games to the end and picks the move with the highest empirical win rate.

---

## Test Cases & Correctness

The `search_algorithms.py` script includes automated tests (17 test cases) to mathematically prove the correctness of the implementations. 

### Categories of Tests:
1. **Optimal Play & Blocking (Minimax/Alpha-Beta):** Tests if the algorithms correctly detect terminal wins, terminal losses, and immediate blocks (e.g., stopping the opponent from connecting 3).
2. **Algorithmic Consistency:** Tests Alpha-Beta against Minimax to ensure they return the exact same score. 
3. **Speedup Validation:** Times Alpha-Beta against Minimax to prove that pruning reduces computation time (often showing a 20x+ speedup). It also measures the speedup gained by implementing Move Ordering in the Heuristic search.
4. **MCTS Probabilistic Success:** Validates that MCTS correctly identifies winning moves and blocks opponents.
   * Runs a 50-game simulation of MCTS vs. a completely Random agent to ensure MCTS achieves a near 100% win/draw rate.

---

## How to Run the Code
Open your terminal and clone this repository to your local machine using the following command:
```bash
git clone https://github.com/m-o-n-i-sh/se24ucse153_AI_programing_assignment_5.git
```
Move into the cloned directory:
```bash
cd se24ucse153_AI_programing_assignment_5/Q1_search_algorithms
```
Run the script:
```bash
python search_algorithms.py
```
