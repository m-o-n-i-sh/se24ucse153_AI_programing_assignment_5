# AI Programming Assignment 5
## Repository Structure
The repository is organized into four main modules. Each folder contains its own dedicated source code and a detailed `README.md` explaining the specific logic and test cases for that assignment.
### [Q1_search_algorithms](./Q1_search_algorithms)
**Adversarial Search & Decision Making**
Implementation of fundamental search algorithms applied to the game of Tic-Tac-Toe to evaluate decision making efficiency and optimality.
* **Algorithms Included:** Minimax, Alpha-Beta Pruning, Depth-Limited Heuristic Alpha-Beta, and Monte-Carlo Tree Search (MCTS).
* **Highlights:** Includes an automated test suite demonstrating algorithmic consistency, win/block detection, and significant computation speedups.

### [Q2_travel_planner](./Q2_travel_planner)
**Knowledge-Based Expert Systems**
A personalized AI travel planner that utilizes a structured domain knowledge base to generate highly customized vacation itineraries.
* **Features:** Intelligent destination scoring, 1.5x budget threshold pruning, dynamic cost estimation, and dish-level dietary restriction filtering based on a custom ontology.

### [Q3_knowledge_graphs](./Q3_knowledge_graphs)
**Semantic Networks & Logical Inference**
A custom Knowledge Graph engine demonstrating data structuring and semantic relationships across Movie and Geography domains.
* **Features:** Semantic triple (Subject-Predicate-Object) indexing, SPARQL-like pattern matching queries, Breadth-First Search (BFS) pathfinding, and automated transitive/inverse relationship inference.

### [Q4_bayesian_networks](./Q4_bayesian_networks)
**Probabilistic Modeling & Reasoning**
A Bayesian Network framework built from scratch to model uncertainty, perform exact inference, and analyze structural graph properties.
* **Features:** Topological sorting, exact inference via Enumerate-Ask, Maximum A Posteriori (MAP) estimation, and conditional independence testing (Markov Blanket and d-separation).

---

## Prerequisites

All projects in this repository are built using standard Python. There are no external dependencies or third-party libraries (such as NumPy, Pandas, or external AI frameworks) required to run the core algorithms. 
* **Requirement:** Python 3.x

## How to Clone and Run

**1. Clone the repository to your local machine:**
```bash
git clone https://github.com/m-o-n-i-sh/se24ucse153_AI_programing_assignment_5.git

```

**2. Navigate into the cloned directory:**

```bash
cd se24ucse153_AI_programing_assignment_5

```

**3. Run specific assignments:**
Navigate into any of the sub-directories and execute the main python script. For example, to run the Search Algorithms:

```bash
cd Q1_search_algorithms
python search_algorithms.py

```

*(Note: If you are on macOS or Linux and `python` defaults to Python 2, use `python3` instead).*

---

