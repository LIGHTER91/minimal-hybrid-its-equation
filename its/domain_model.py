import json
import networkx as nx


class DomainModel:
    def __init__(self, graph_path: str):
        with open(graph_path, "r") as f:
            data = json.load(f)

        self.concepts = data["concepts"]
        self.graph = nx.DiGraph()

        for cid, cdata in self.concepts.items():
            self.graph.add_node(cid)
            for prereq in cdata["prerequisites"]:
                self.graph.add_edge(prereq, cid)

    def get_available_concepts(self, mastery: dict):
        available = []
        for concept in self.graph.nodes:
            prereqs = list(self.graph.predecessors(concept))
            if all(mastery.get(p, 0.0) >= 0.6 for p in prereqs):
                available.append(concept)
        return available

    def get_concept_name(self, concept_id: str) -> str:
        return self.concepts[concept_id]["name"]

    def get_common_errors(self, concept_id: str):
        return self.concepts[concept_id]["common_errors"]
