# Knowledge Graph Implementation & Tools Exploration
This repository contains the implementation of a Knowledge Graph (KG).
## Problem statement:
*"Describe Knowledge Graphs and explore the tools to build KG."*
## File Structure
The project is contained within a single executable script:
* `knowledge_graph.py`: Contains the core `KnowledgeGraph` class, inference engines, SPARQL-like querying logic, and the interactive command-line demonstrations for both Movie and Geography domains.
---
## How the Code Works
### 1. Data Structuring and Indexing
The graph stores relationships as semantic triples (Subject, Predicate, Object). To ensure fast retrieval, the class maintains multiple inverted indexes (`_index_subj`, `_index_pred`, `_index_obj`) using Python's `defaultdict`. It also allows mapping specific metadata directly to entities via the `_entity_attrs` dictionary.

### 2. Querying Engine (`query` & `sparql_like_query`)
* **Direct Queries:** Users can fetch specific triples by providing any combination of subject, predicate, or object.
* **SPARQL-like Pattern Matching:** The system supports complex queries using variables (e.g., `?person`, `?movie`). It evaluates an array of patterns, resolving variable bindings iteratively to find sub-graphs that match the exact semantic criteria requested.

### 3. Logical Inference (`infer_transitive` & `infer_inverse`)
The engine is capable of deducing new knowledge from existing facts without human intervention:
* **Inverse Inference:** Automatically generates reverse relationships (e.g., if A `directed` B, it infers B is `directed_by` A).
* **Transitive Inference:** Chases paths through the graph to establish new direct links based on transitive logic.

### 4. Graph Algorithms (`bfs`)
Implements a Breadth First Search (BFS) to find the shortest path between two entities in the graph. For example, it can successfully navigate the Geography KG to find the path from "Mumbai" to "Asia".

### 5. Tool Exploration & Serialization
Upon execution, the script automatically details a curated list of standard tools used to build Knowledge Graphs (e.g., Neo4j, RDFLib, Apache Jena, Protégé). Furthermore, the custom KG can serialize its internal memory into standard Turtle (.ttl) format for interoperability with these exact tools.

---
## How to Run the Code
Open your terminal and clone this repository to your local machine using the following command:
```bash
git clone https://github.com/m-o-n-i-sh/se24ucse153_AI_programing_assignment_5.git
```
Move into the cloned directory:
```bash
cd se24ucse153_AI_programing_assignment_5/Q3_knowledge_graphs
```
Run the script:
```bash
python knowledge_graph.py
```
