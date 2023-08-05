import pytest
from graphpanda.to_cypher import dict_to_cypher_prop, CypherNode, CypherEdge, CypherGraph
from graphpanda.graphpanda import Node, Domain, form_node_domain, form_edges, exact_match, Edge, Graph
import pandas as pd


def test_dict_to_cypher_prop():
    data = {
        'title': 'The Matrix',
        'released': 1999,
        'tagline': 'Welcome to the Real World'
    }

    result = dict_to_cypher_prop(data)
    assert result == "{title:'The Matrix', released:1999, tagline:'Welcome to the Real World'}"


def test_cypher_node_create():
    node = Node("TestNode", {"p": "property", "p_int": 12})

    result = CypherNode(node)
    create_stmt = result.get_create_statement()
    assert "CREATE (node_" in create_stmt
    assert ":TestNode {p:'property', p_int:12})" in create_stmt


def test_cypher_edge_create():
    node1 = Node("TestNode", {"p": "property", "p_int": 12})
    node2 = Node("TestNode", {"p": "property", "p_int": 13})
    edge = Edge("TestEdge", {"test": 1}, node1, node2)

    n1 = CypherNode(node1)
    n2 = CypherNode(node2)

    cypher_edge = CypherEdge(edge)
    result = cypher_edge.get_create_statement(n1, n2)
    assert ")-[:TESTEDGE {test:1}]->(" in result


def test_cypher_graph_create():
    node1 = Node("TestNode", {"p": "property", "p_int": 12})
    node2 = Node("TestNode", {"p": "property", "p_int": 13})
    edge = Edge("TestEdge", {"test": 1}, node1, node2)

    graph = Graph()
    graph.nodes = {node1, node2}
    graph.edges = {edge}

    cypher_graph = CypherGraph(graph)
    out = cypher_graph.get_create_statements()

    assert len(out.split("CREATE")) == 4
    assert len(out.split("TESTEDGE")) == 2
    assert ":TestNode {p:'property', p_int:12})" in out
    assert ")-[:TESTEDGE {test:1}]->(" in out
