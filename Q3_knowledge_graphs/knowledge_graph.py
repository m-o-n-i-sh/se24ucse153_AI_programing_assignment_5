from collections import defaultdict, deque
class KnowledgeGraph:
    def __init__(self, name="KnowledgeGraph"):
        self.name = name
        self._triples = set()
        self._entity_attrs = defaultdict(dict)
        self._index_subj = defaultdict(set)
        self._index_pred = defaultdict(set)
        self._index_obj = defaultdict(set)
    def add_triple(self, subject, predicate, obj):
        triple = (subject, predicate, obj)
        self._triples.add(triple)
        self._index_subj[subject].add(triple)
        self._index_pred[predicate].add(triple)
        self._index_obj[obj].add(triple)
        return self
    def add_entity(self, entity, **attrs):
        self._entity_attrs[entity].update(attrs)
        return self
    def get_attributes(self, entity):
        return dict(self._entity_attrs.get(entity, {}))
    def get_entities(self):
        entities = set()
        for s, p, o in self._triples:
            entities.add(s)
            entities.add(o)
        entities.update(self._entity_attrs.keys())
        return entities
    def get_predicates(self):
        return set(self._index_pred.keys())
    def query(self, subject=None, predicate=None, obj=None):
        if subject and predicate and obj:
            return (
                {(subject, predicate, obj)}
                if (subject, predicate, obj) in self._triples
                else set()
            )
        if subject and predicate:
            return {
                t for t in self._index_subj[subject]
                if t[1] == predicate
            }
        if subject and obj:
            return {
                t for t in self._index_subj[subject]
                if t[2] == obj
            }
        if predicate and obj:
            return {
                t for t in self._index_pred[predicate]
                if t[2] == obj
            }
        if subject:
            return set(self._index_subj[subject])
        if predicate:
            return set(self._index_pred[predicate])
        if obj:
            return set(self._index_obj[obj])
        return set(self._triples)
    def get_neighbors(self, entity):
        neighbors = set()
        for s, p, o in self._index_subj[entity]:
            neighbors.add(o)
        for s, p, o in self._index_obj[entity]:
            neighbors.add(s)
        return neighbors
    def bfs(self, start, end, max_depth=6):
        if start == end:
            return [[start]]
        queue = deque([[start]])
        all_paths = []
        while queue:
            path = queue.popleft()
            if len(path) > max_depth:
                continue
            node = path[-1]
            for neighbor in self.get_neighbors(node):
                if neighbor in path:
                    continue
                new_path = path + [neighbor]
                if neighbor == end:
                    all_paths.append(new_path)
                else:
                    queue.append(new_path)
        return all_paths
    def infer_transitive(self, predicate):
        inferred = set()
        direct = {
            (s, o)
            for s, p, o in self._index_pred[predicate]
        }
        changed = True
        while changed:
            changed = False
            new_inferred = set()
            for s1, o1 in direct | inferred:
                for s2, o2 in direct | inferred:
                    if (
                        o1 == s2
                        and (s1, o2) not in direct
                        and (s1, o2) not in inferred
                    ):
                        new_inferred.add((s1, o2))
                        changed = True
            inferred |= new_inferred
        return inferred
    def infer_inverse(self, predicate, inverse_predicate):
        new_triples = []
        for s, p, o in self._index_pred[predicate]:
            if (o, inverse_predicate, s) not in self._triples:
                new_triples.append((o, inverse_predicate, s))
        for s, p, o in new_triples:
            self.add_triple(s, p, o)
        return new_triples
    def sparql_like_query(self, patterns):
        bindings = [{}]
        for pattern in patterns:
            s_pat, p_pat, o_pat = pattern
            new_bindings = []
            for binding in bindings:
                s = (
                    binding.get(s_pat, s_pat)
                    if s_pat.startswith("?")
                    else s_pat
                )
                p = (
                    binding.get(p_pat, p_pat)
                    if p_pat.startswith("?")
                    else p_pat
                )
                o = (
                    binding.get(o_pat, o_pat)
                    if o_pat.startswith("?")
                    else o_pat
                )
                s_var = s_pat if s_pat.startswith("?") else None
                p_var = p_pat if p_pat.startswith("?") else None
                o_var = o_pat if o_pat.startswith("?") else None
                s_val = None if s_var and s_var not in binding else s
                p_val = None if p_var and p_var not in binding else p
                o_val = None if o_var and o_var not in binding else o
                results = self.query(
                    subject=s_val if not s_var or s_var in binding else None,
                    predicate=p_val if not p_var or p_var in binding else None,
                    obj=o_val if not o_var or o_var in binding else None,
                )
                for rs, rp, ro in results:
                    new_b = dict(binding)
                    if s_var and s_var not in binding:
                        new_b[s_var] = rs
                    if p_var and p_var not in binding:
                        new_b[p_var] = rp
                    if o_var and o_var not in binding:
                        new_b[o_var] = ro
                    if s_var and s_var in binding and binding[s_var] != rs:
                        continue
                    if p_var and p_var in binding and binding[p_var] != rp:
                        continue
                    if o_var and o_var in binding and binding[o_var] != ro:
                        continue
                    new_bindings.append(new_b)
            bindings = new_bindings
        return bindings
    def stats(self):
        return {
            "entities": len(self.get_entities()),
            "triples": len(self._triples),
            "predicates": len(self.get_predicates()),
            "entity_attributes": len(self._entity_attrs),
        }
    def export_turtle(self):
        lines = [f"Knowledge Graph: {self.name}\n"]
        for s, p, o in sorted(self._triples):
            lines.append(f"<{s}> <{p}> <{o}> .")
        return "\n".join(lines)
    def __repr__(self):
        s = self.stats()
        return (
            f"KnowledgeGraph('{self.name}', "
            f"entities={s['entities']}, "
            f"triples={s['triples']}, "
            f"predicates={s['predicates']})"
        )
def build_movie_kg():
    kg = KnowledgeGraph("MovieKG")
    kg.add_entity(
        "Christopher_Nolan",
        type="Person",
        nationality="British-American",
        born=1970
    )
    kg.add_entity(
        "Inception",
        type="Movie",
        year=2010,
        genre="Sci-Fi"
    )
    kg.add_entity(
        "Interstellar",
        type="Movie",
        year=2014,
        genre="Sci-Fi"
    )
    kg.add_entity(
        "Leonardo_DiCaprio",
        type="Person",
        nationality="American",
        born=1974
    )
    kg.add_entity(
        "Matthew_McConaughey",
        type="Person",
        nationality="American",
        born=1969
    )
    kg.add_entity(
        "Hans_Zimmer",
        type="Person",
        nationality="German",
        born=1957
    )
    kg.add_triple(
        "Christopher_Nolan",
        "directed",
        "Inception"
    )
    kg.add_triple(
        "Christopher_Nolan",
        "directed",
        "Interstellar"
    )
    kg.add_triple(
        "Leonardo_DiCaprio",
        "starred_in",
        "Inception"
    )
    kg.add_triple(
        "Matthew_McConaughey",
        "starred_in",
        "Interstellar"
    )
    kg.add_triple(
        "Hans_Zimmer",
        "composed_for",
        "Inception"
    )
    kg.add_triple(
        "Hans_Zimmer",
        "composed_for",
        "Interstellar"
    )
    kg.add_triple(
        "Inception",
        "genre",
        "Science_Fiction"
    )
    kg.add_triple(
        "Interstellar",
        "genre",
        "Science_Fiction"
    )
    kg.add_triple(
        "Christopher_Nolan",
        "is_a",
        "Director"
    )
    kg.add_triple(
        "Leonardo_DiCaprio",
        "is_a",
        "Actor"
    )
    kg.add_triple(
        "Hans_Zimmer",
        "is_a",
        "Composer"
    )
    return kg
def build_geography_kg():
    kg = KnowledgeGraph("GeographyKG")
    countries = {
        "India": "Asia",
        "France": "Europe",
        "Brazil": "South_America",
        "USA": "North_America",
        "Japan": "Asia"
    }
    cities = {
        "Mumbai": "India",
        "Delhi": "India",
        "Paris": "France",
        "Tokyo": "Japan",
        "New_York": "USA"
    }
    for country, continent in countries.items():
        kg.add_triple(country, "part_of", continent)
        kg.add_entity(country, type="Country")
    for city, country in cities.items():
        kg.add_triple(city, "located_in", country)
        kg.add_entity(city, type="City")
    kg.add_triple("India", "borders", "China")
    kg.add_triple("France", "borders", "Germany")
    kg.add_triple("USA", "borders", "Canada")
    return kg
def demo_movie_kg():
    print("\n" + "=" * 60)
    print("MOVIE KNOWLEDGE GRAPH DEMO")
    print("=" * 60)
    kg = build_movie_kg()
    print("\nKnowledge Graph Statistics:")
    print(kg.stats())
    print("\nGraph Representation:")
    print(kg)
    print("\nAll Entities:")
    print(kg.get_entities())
    print("\nAll Predicates:")
    print(kg.get_predicates())
    print("\nMovies Directed by Christopher Nolan:")
    results = kg.query(
        subject="Christopher_Nolan",
        predicate="directed"
    )
    for triple in results:
        print(triple)
    print("\nAttributes of Inception:")
    print(kg.get_attributes("Inception"))
    print("\nNeighbors of Inception:")
    print(kg.get_neighbors("Inception"))
    print("\nSPARQL-like Query:")
    patterns = [
        ("?person", "directed", "?movie"),
        ("?movie", "genre", "Science_Fiction")
    ]
    results = kg.sparql_like_query(patterns)
    for r in results:
        print(r)
    print("\nInverse Relation Inference:")
    inferred = kg.infer_inverse(
        "directed",
        "directed_by"
    )
    for t in inferred:
        print(t)
    print("\nExporting Turtle Format:")
    print(kg.export_turtle())
def demo_geography_kg():
    print("\n" + "=" * 60)
    print("GEOGRAPHY KNOWLEDGE GRAPH DEMO")
    print("=" * 60)
    kg = build_geography_kg()
    print("\nKnowledge Graph Statistics:")
    print(kg.stats())
    print("\nCities Located in India:")
    results = kg.query(
        predicate="located_in",
        obj="India"
    )
    for triple in results:
        print(triple)
    print("\nCountries Bordering France:")
    results = kg.query(
        subject="France",
        predicate="borders"
    )
    for triple in results:
        print(triple)
    print("\nPath Search (Mumbai -> Asia):")
    paths = kg.bfs("Mumbai", "Asia")
    for path in paths:
        print(" -> ".join(path))
def main():
    print("\n" + "=" * 60)
    print("TOOLS USED TO BUILD KNOWLEDGE GRAPHS")
    print("=" * 60)
    print("""
1. Neo4j
- Graph database platform
- Uses Cypher query language
2. RDFLib
- Python library for RDF graphs
3. Apache Jena
- Java framework for semantic web applications
4. Protégé
- Ontology editor for OWL/RDF
5. GraphDB
- Semantic graph database
6. spaCy
- NLP library for entity extraction
7. NetworkX
- Graph analysis library in Python
""")
    choice = input("Enter 1 for Movie KG Demo, 2 for Geography KG Demo, or 3 for Both: ").strip()
    if choice == '1':
        demo_movie_kg()
    elif choice == '2':
        demo_geography_kg()
    elif choice == '3':
        demo_movie_kg()
        demo_geography_kg()
    else:
        print("Invalid selection.")
if __name__ == "__main__":
    main()