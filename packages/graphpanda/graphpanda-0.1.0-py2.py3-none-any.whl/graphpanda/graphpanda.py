import pandas as pd
from typing import Dict, List, Tuple


class Node:
    '''
    interpret. Node represents a collection of columns based
               on the DataFrame.
    DataFrame:
        1,13, Rectangle, red -> Node("GeometricFigure", {"hight":1, "width": 13, "name": "Rectangle", "color": "red"})
    '''

    def __init__(self, name, properties):
        assert isinstance(properties, dict)
        self.name = name
        self.properties = properties
        self.edges = set()

    def get_property(self, prop_name):
        return self.properties[prop_name]

    def __get_hash(self, obj):
        properties = tuple(
            sorted([(k, v) for k, v in obj.properties.items()], key=lambda x: x[0]))
        return hash((properties, self.name))

    def __hash__(self):
        return self.__get_hash(self)

    def __eq__(self, other):
        return self.__get_hash(self) == self.__get_hash(other)

    def __repr__(self):
        return f"{self.name} " + " ".join([f"{k}:{v}" for k, v in self.properties.items()])


class Domain:
    def __init__(self):
        self.nodes = set()

    def add_node(self, node: Node):
        if node not in self.nodes:
            self.nodes.add(node)

    def get_selection_function(self, fields):
        '''
        NOTE: Order of the fields that are passed in here is important
              because the way equivalence checking is done depends on it.
        '''
        def selection(node):
            return [node.get_property(prop) for prop in fields]
        return selection

    def __repr__(self):
        return "\n".join(repr(node) for node in self.nodes)


def form_node_domain(df: pd.DataFrame, node_spec: Tuple[str, List[str]]) -> Domain:
    assert(df, pd.DataFrame)
    node_name, node_properties = node_spec
    assert set(node_properties) == set(df.columns).intersection(
        set(node_properties)), f"Not all {node_properties} are present in {df.columns}"

    domain = Domain()

    def form_node(row):
        properties = {p: row[p] for p in node_properties}
        node = Node(node_name, properties)
        domain.add_node(node)

    df.apply(form_node, axis=1)

    return domain


class Graph:
    '''
    interpret: It's an intermediare representation that can be used
               to output graphs into different graph processing formats.
    '''

    def __init__(self):
        self.nodes = set()
        self.edges = set()

    def add(self, graph):
        """
        WISHLIST: Test a case when adding duplicated nodes and duplicate edges.
        """
        self.nodes += graph.nodes
        self.edges += graph.edges

    def __repr__(self):
        """
        WISHLIST: Add option for printing edges on nodes as well.
        """
        nodes = sorted(f"{node}" for node in self.nodes)
        edges = sorted(f"{edge}" for edge in self.edges)
        nodes = "\n".join(nodes)
        edges = "\n".join(edges)
        return "Nodes:\n"+nodes+"\nEdges:\n"+edges


class Edge:
    '''
    interpret: It represents a link between two nodes with
               a meta telling who and how
               formed the link.
    '''

    def __init__(self, name: str, meta: Dict, node_l: Node, node_r: Node):
        assert isinstance(node_l, Node) and isinstance(node_r, Node)
        assert isinstance(meta, dict)
        self.name = name
        self.meta = meta
        self.node_l = node_l
        self.node_r = node_r

    def __repr__(self):
        return f"{self.name}  {self.node_l} --- {self.meta} --- {self.node_r}"


def exact_match(selection_f1, selection_f2, name="exact_match"):
    '''
    WISHLIST: Add a case for Directed Edges.
    '''
    def exact_match_func(n1, n2):
        if all(x == y for x, y in zip(selection_f1(n1), selection_f2(n2))):
            edge = Edge(name, {}, n1, n2)
            n1.edges.add(edge)
            n2.edges.add(edge)
            return edge
        else:
            return None

    return exact_match_func


def form_edges(d1: Domain, d2: Domain, edge_func) -> Graph:
    graph = Graph()

    for node_l in d1.nodes:
        for node_r in d2.nodes:
            graph.nodes.add(node_l)
            graph.nodes.add(node_r)

            edge = edge_func(node_l, node_r)
            if edge is not None:
                graph.edges.add(edge)

    return graph
