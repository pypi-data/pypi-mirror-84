import pandas as pd
from graphpanda.graphpanda import Node, Domain, form_node_domain, form_edges, exact_match


def test_node_uniqueness():
    '''
    Nodes should be unique.
    '''
    n1 = Node("Test",{})
    n2 = Node("Test",{})

    result = set()
    result.add(n1)
    result.add(n2)

    assert result == {n1}

def test_node_formation_partial():
    df = pd.DataFrame(data=[
        {"c1": 1, "c2": 1, "c3": "wow"},
        {"c1": 1, "c2": 2, "c3": "wow"},
        {"c1": 1, "c2": 3, "c3": "wow"},
    ])

    domain = form_node_domain(df, ("TestNode", ["c2"]))
    result = sorted(f"{node}"for node in domain.nodes)

    assert result == ['TestNode c2:1', 'TestNode c2:2', 'TestNode c2:3']


def test_node_formation_complete():
    df = pd.DataFrame(data=[
        {"c1": 1, "c2": 2, "c3": "wow"},
        {"c1": 1, "c2": 2, "c3": "wow"},
        {"c1": 1, "c2": 2, "c3": "wow"},
    ])

    domain = form_node_domain(df, ("TestNode", ["c1", "c2", "c3"]))
    assert f"{domain}" == "TestNode c1:1 c2:2 c3:wow"


def test_edge_formation():
    df1 = pd.DataFrame(data=[
        {"c1": 1},
        {"c1": 2},
        {"c1": 3},
    ])

    df2 = pd.DataFrame(data=[
        {"d1": 1},
        {"d1": 2},
        {"d1": 3},
    ])

    domain1 = form_node_domain(df1, ("Node1", ["c1"]))
    domain2 = form_node_domain(df2, ("Node2", ["d1"]))

    get_selection_func1 = domain1.get_selection_function(["c1"])
    get_selection_func2 = domain2.get_selection_function(["d1"])

    exact_match_one_field = exact_match(
        get_selection_func1, get_selection_func2)

    graph = form_edges(domain1, domain2, exact_match_one_field)

    expected = ("Nodes:\n"
                + "Node1 c1:1\n"
                + "Node1 c1:2\n"
                + "Node1 c1:3\n"
                + "Node2 d1:1\n"
                + "Node2 d1:2\n"
                + "Node2 d1:3\n"
                + "Edges:\n"
                + "exact_match  Node1 c1:1 --- {} --- Node2 d1:1\n"
                + "exact_match  Node1 c1:2 --- {} --- Node2 d1:2\n"
                + "exact_match  Node1 c1:3 --- {} --- Node2 d1:3")

    assert f"{graph}" == expected

