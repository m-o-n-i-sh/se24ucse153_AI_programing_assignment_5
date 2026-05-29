# Bayesian Networks Implementation & Tool Exploration
This repository contains an implementation of a Bayesian Network engine from scratch.
## Problem statement:
*"Explore the tools for modelling, problem representing and inferencing using Bayesian Networks. Choose an example of choice to implement."*
## File Structure
The project is contained within a single executable script:
* `bayesian_network.py`: Contains the core `BayesianNetwork` class, inference algorithms, structural analysis methods, and the implementation of two chosen examples (Medical Diagnosis and Weather Prediction domains).
---
## How the Code Works
### 1. Network Construction & Representation
The network is built by adding nodes alongside their parent dependencies and Conditional Probability Tables (CPTs). The system automatically maintains a directed acyclic graph (DAG) representation and uses a Depth-First Search (DFS) to perform a topological sort, ensuring that parent nodes are always evaluated before their children during probability calculations.
### 2. Exact Inference (Enumerate-Ask)
The engine implements the exact inference algorithm `enumerate_ask`. When queried for the probability of a specific variable given a set of evidence, it recursively sums out (marginalizes) the hidden variables over their entire domains (True/False). It calculates the joint probabilities using the chain rule of Bayesian networks and normalizes the final results.

### 3. Maximum A Posteriori (MAP) Estimation
The `map_estimate` function determines the most likely state of the world given partial evidence. It computes the joint probability for every possible combination of the unobserved variables and returns the specific assignment that yields the highest overall probability.

### 4. Structural Graph Analysis
The engine is capable of analyzing the conditional independence properties of the network:
* **Markov Blanket:** Dynamically retrieves the minimal set of nodes (parents, children, and children's parents) that completely shields a target node from the rest of the network.
* **d-Separation:** Implements a reachability algorithm (similar to the Bayes Ball algorithm) with distinct "up" and "down" phases to mathematically prove whether two variables are conditionally independent given a specific set of evidence.

### 5. Tool Exploration & Example Domains
Upon execution, the script lists industry-standard tools used for Bayesian modeling (e.g., pgmpy, GeNIe, Netica, PyMC). It then runs two fully modeled examples:
* **Medical Diagnosis:** Analyzes the probabilistic links between genetics, lifestyle (smoking/pollution), and diseases (lung cancer/heart disease) to infer symptoms.
* **Weather Prediction:** Models the environmental impacts of seasons and weather conditions on environmental states (floods, wet grass).

---
## How to Run the Code
Open your terminal and clone this repository to your local machine using the following command:
```bash
git clone https://github.com/m-o-n-i-sh/se24ucse153_AI_programing_assignment_5.git
```
Move into the cloned directory:
```bash
cd se24ucse153_AI_programing_assignment_5/Q4_bayesian_networks
```
Run the script:
```bash
python bayesian_network.py
```
