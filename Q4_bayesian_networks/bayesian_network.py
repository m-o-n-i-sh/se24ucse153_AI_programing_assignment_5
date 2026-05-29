from itertools import product
from functools import reduce
class BayesianNetwork:
    def __init__(self, name="BayesianNetwork"):
        self.name = name
        self.nodes = {}
        self._topo_order = None
    def add_node(self, name, parents, cpt):
        self.nodes[name] = {"parents": list(parents), "cpt": cpt}
        self._topo_order = None
        return self
    def _topological_sort(self):
        visited = set()
        order = []
        def dfs(node):
            if node in visited:
                return
            visited.add(node)
            for parent in self.nodes[node]["parents"]:
                dfs(parent)
            order.append(node)
        for node in self.nodes:
            dfs(node)
        self._topo_order = order
        return order
    def get_probability(self, node, value, parent_values):
        cpt = self.nodes[node]["cpt"]
        parents = self.nodes[node]["parents"]
        if not parents:
            return cpt.get(value, cpt.get((value,), 0.0))
        key = tuple(parent_values[p] for p in parents)
        if isinstance(value, bool):
            row = cpt.get(key, {})
            return row.get(value, row.get(True if value else False, 0.0))
        return cpt.get(key, {}).get(value, 0.0)
    def joint_probability(self, assignment):
        if self._topo_order is None:
            self._topological_sort()
        prob = 1.0
        for node in self._topo_order:
            if node not in assignment:
                raise ValueError(f"Missing assignment for node: {node}")
            prob *= self.get_probability(node, assignment[node], assignment)
        return prob
    def enumerate_ask(self, query_var, evidence):
        domain = [True, False]
        results = {}
        for val in domain:
            extended_evidence = dict(evidence)
            extended_evidence[query_var] = val
            results[val] = self._enumerate_all(list(self._topological_sort()), extended_evidence)
        total = sum(results.values())
        if total == 0:
            return {v: 0.0 for v in results}
        return {v: p / total for v, p in results.items()}
    def _enumerate_all(self, variables, evidence):
        if not variables:
            return 1.0
        Y = variables[0]
        rest = variables[1:]
        if Y in evidence:
            return self.get_probability(Y, evidence[Y], evidence) * self._enumerate_all(rest, evidence)
        total = 0.0
        for val in [True, False]:
            extended = dict(evidence)
            extended[Y] = val
            total += self.get_probability(Y, val, extended) * self._enumerate_all(rest, extended)
        return total
    def query(self, query_var, evidence=None):
        evidence = evidence or {}
        if self._topo_order is None:
            self._topological_sort()
        return self.enumerate_ask(query_var, evidence)
    def map_estimate(self, evidence=None):
        evidence = evidence or {}
        if self._topo_order is None:
            self._topological_sort()
        query_vars = [n for n in self.nodes if n not in evidence]
        domains = [[True, False]] * len(query_vars)
        best_prob = -1
        best_assignment = None
        for combo in product(*domains):
            assignment = dict(evidence)
            for var, val in zip(query_vars, combo):
                assignment[var] = val
            try:
                p = self.joint_probability(assignment)
                if p > best_prob:
                    best_prob = p
                    best_assignment = dict(assignment)
            except Exception:
                continue
        return best_assignment, best_prob
    def get_markov_blanket(self, node):
        blanket = set(self.nodes[node]["parents"])
        for other, info in self.nodes.items():
            if node in info["parents"]:
                blanket.add(other)
                blanket.update(info["parents"])
        blanket.discard(node)
        return blanket
    def d_separation(self, x, y, evidence_set):
        def ancestors(node):
            ancs = set()
            queue = list(self.nodes[node]["parents"])
            while queue:
                n = queue.pop()
                ancs.add(n)
                queue.extend(self.nodes[n]["parents"])
            return ancs
        reachable = set()
        via_node = set()
        phase = "up"
        L = [(x, "up")]
        visited = set()
        while L:
            (n, d) = L.pop()
            if (n, d) in visited:
                continue
            visited.add((n, d))
            if n not in evidence_set:
                reachable.add(n)
            if d == "up" and n not in evidence_set:
                for parent in self.nodes[n]["parents"]:
                    L.append((parent, "up"))
                for child, info in self.nodes.items():
                    if n in info["parents"]:
                        L.append((child, "down"))
            elif d == "down":
                if n not in evidence_set:
                    for child, info in self.nodes.items():
                        if n in info["parents"]:
                            L.append((child, "down"))
                if n in evidence_set or any(n in ancestors(ev) for ev in evidence_set):
                    for parent in self.nodes[n]["parents"]:
                        L.append((parent, "up"))
        return y not in reachable
    def stats(self):
        return {
            "nodes": len(self.nodes),
            "edges": sum(len(info["parents"]) for info in self.nodes.values()),
        }
    def __repr__(self):
        s = self.stats()
        return f"BayesianNetwork('{self.name}', nodes={s['nodes']}, edges={s['edges']})"
def build_medical_diagnosis_bn():
    bn = BayesianNetwork("MedicalDiagnosis")
    bn.add_node("Smoking", parents=[], cpt={True: 0.30, False: 0.70})
    bn.add_node("Pollution", parents=[], cpt={True: 0.10, False: 0.90})
    bn.add_node("Genetics", parents=[], cpt={True: 0.20, False: 0.80})
    bn.add_node("LungCancer", parents=["Smoking", "Pollution", "Genetics"], cpt={
        (True,  True,  True):  {True: 0.95, False: 0.05},
        (True,  True,  False): {True: 0.85, False: 0.15},
        (True,  False, True):  {True: 0.75, False: 0.25},
        (True,  False, False): {True: 0.55, False: 0.45},
        (False, True,  True):  {True: 0.60, False: 0.40},
        (False, True,  False): {True: 0.30, False: 0.70},
        (False, False, True):  {True: 0.25, False: 0.75},
        (False, False, False): {True: 0.02, False: 0.98},
    })
    bn.add_node("HeartDisease", parents=["Smoking", "Genetics"], cpt={
        (True,  True):  {True: 0.80, False: 0.20},
        (True,  False): {True: 0.60, False: 0.40},
        (False, True):  {True: 0.40, False: 0.60},
        (False, False): {True: 0.10, False: 0.90},
    })
    bn.add_node("XRayPositive", parents=["LungCancer"], cpt={
        (True,):  {True: 0.90, False: 0.10},
        (False,): {True: 0.05, False: 0.95},
    })
    bn.add_node("Dyspnoea", parents=["LungCancer", "HeartDisease"], cpt={
        (True,  True):  {True: 0.98, False: 0.02},
        (True,  False): {True: 0.80, False: 0.20},
        (False, True):  {True: 0.70, False: 0.30},
        (False, False): {True: 0.10, False: 0.90},
    })
    bn.add_node("Cough", parents=["LungCancer", "Smoking"], cpt={
        (True,  True):  {True: 0.95, False: 0.05},
        (True,  False): {True: 0.85, False: 0.15},
        (False, True):  {True: 0.60, False: 0.40},
        (False, False): {True: 0.10, False: 0.90},
    })
    return bn
def build_weather_bn():
    bn = BayesianNetwork("WeatherPrediction")
    bn.add_node("Season", parents=[], cpt={True: 0.50, False: 0.50})
    bn.add_node("Rain", parents=["Season"], cpt={
        (True,):  {True: 0.70, False: 0.30},
        (False,): {True: 0.20, False: 0.80},
    })
    bn.add_node("Cloudy", parents=["Season"], cpt={
        (True,):  {True: 0.80, False: 0.20},
        (False,): {True: 0.30, False: 0.70},
    })
    bn.add_node("WetGrass", parents=["Rain", "Cloudy"], cpt={
        (True,  True):  {True: 0.99, False: 0.01},
        (True,  False): {True: 0.90, False: 0.10},
        (False, True):  {True: 0.40, False: 0.60},
        (False, False): {True: 0.01, False: 0.99},
    })
    bn.add_node("Flood", parents=["Rain"], cpt={
        (True,):  {True: 0.40, False: 0.60},
        (False,): {True: 0.01, False: 0.99},
    })
    return bn
def demo_medical_bn():
    print("\n" + "=" * 60)
    print("        MEDICAL DIAGNOSIS BAYESIAN NETWORK")
    print("=" * 60)
    bn = build_medical_diagnosis_bn()
    print("\nNetwork Statistics:")
    print(bn.stats())
    print("\nNetwork Representation:")
    print(bn)
    print("\nNodes in the Network:")
    for node in bn.nodes:
        print("-", node)
    print("\nInference Example 1:")
    print("Probability of Lung Cancer given Smoking=True")
    result = bn.query(
        "LungCancer",
        evidence={"Smoking": True}
    )
    print(result)
    print("\nInference Example 2:")
    print("Probability of Lung Cancer given:")
    print("Smoking=True, XRayPositive=True")
    result = bn.query(
        "LungCancer",
        evidence={
            "Smoking": True,
            "XRayPositive": True
        }
    )
    print(result)
    print("\nInference Example 3:")
    print("Probability of Heart Disease given:")
    print("Smoking=True, Dyspnoea=True")
    result = bn.query(
        "HeartDisease",
        evidence={
            "Smoking": True,
            "Dyspnoea": True
        }
    )
    print(result)
    print("\nMAP Estimate:")
    assignment, prob = bn.map_estimate(
        evidence={"Cough": True}
    )
    print("Best Assignment:")
    print(assignment)
    print("Joint Probability:")
    print(prob)
    print("\nMarkov Blanket of LungCancer:")
    print(bn.get_markov_blanket("LungCancer"))
    print("\nd-Separation Test:")
    print("Are Smoking and XRayPositive independent")
    print("given LungCancer?")
    result = bn.d_separation(
        "Smoking",
        "XRayPositive",
        {"LungCancer"}
    )
    print(result)
def demo_weather_bn():
    print("\n" + "=" * 60)
    print("          WEATHER PREDICTION NETWORK")
    print("=" * 60)
    bn = build_weather_bn()
    print("\nNetwork Statistics:")
    print(bn.stats())
    print("\nProbability of Rain given Cloudy=True:")
    result = bn.query(
        "Rain",
        evidence={"Cloudy": True}
    )
    print(result)
    print("\nProbability of Flood given:")
    print("Rain=True")
    result = bn.query(
        "Flood",
        evidence={"Rain": True}
    )
    print(result)
    print("\nProbability of WetGrass given:")
    print("Rain=True, Cloudy=True")
    result = bn.query(
        "WetGrass",
        evidence={
            "Rain": True,
            "Cloudy": True
        }
    )
    print(result)
    print("\nMarkov Blanket of Rain:")
    print(bn.get_markov_blanket("Rain"))
def main():
    print("=" * 60)
    print("      TOOLS USED FOR BAYESIAN NETWORKS")
    print("=" * 60)
    print("""1. pgmpy
   - Python library for probabilistic graphical models
2. Bayes Server
   - Commercial Bayesian network platform
3. GeNIe
   - GUI tool for Bayesian modeling
4. Netica
   - Bayesian network reasoning software
5. bnlearn
   - R package for structure learning
6. PyMC
   - Probabilistic programming framework
7. TensorFlow Probability
   - Deep probabilistic modeling toolkit""")
    demo_medical_bn()
    demo_weather_bn()
if __name__ == "__main__":
    main()