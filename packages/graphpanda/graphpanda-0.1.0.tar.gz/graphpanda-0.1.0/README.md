# Graphpanda 🛠

`Graphpanda` is a python package that allows you to convert pandas dataframe into `Cypher` insert queries. It gives you a way to specify your record linking algorithms for determining edges and setting attributes.

## Who should use it?
Anyone who is analyzing data in python using pandas and wants to have a way to analyze it with cypher in a graph database.

## Installation
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install graphpanda.

```bash
pip install -e path_to_graphpanda
```

## Usage

```python
df = pd.DataFrame(data=[
    {"c1": 1, "c2": 2, "c3": "wow"},
    {"c1": 1, "c2": 2, "c3": "wow"},
    {"c1": 1, "c2": 2, "c3": "wow"},
])

df2 = pd.DataFrame(data=[
    {"d1": 1},
    {"d1": 2},
    {"d1": 3},
])

domain1 = form_node_domain(df, ("TestNode", ["c2"]))
domain2 = form_node_domain(df2, ("Node2", ["d1"]))

get_selection_func1 = domain1.get_selection_function(["c2"])
get_selection_func2 = domain2.get_selection_function(["d1"])

exact_match_one_field = exact_match(
    get_selection_func1, get_selection_func2)

graph = form_edges(domain1, domain2, exact_match_one_field)

cypher_graph = CypherGraph(graph)
out = cypher_graph.get_create_statements()
print(out)

CREATE (node_339606590492800375:Node2 {d1:2})
CREATE (node_4387139851793128730:Node2 {d1:1})
CREATE (node_4180099955292202157:Node2 {d1:3})
CREATE (node_5208008065052232978:TestNode {c2:2})
CREATE
(node_5208008065052232978)-[:EXACT_MATCH {}]->(node_339606590492800375)
```

## Contributing 💓
Pull requests are welcome. For significant changes, please open an issue first to discuss what you would like to change. Please make sure to update the tests as appropriate. It would be nice to ask @Bobrinik before to make sure that we follow the same guidelines and vision.

## Future work
- Add more record linking functions:
    - https://en.wikipedia.org/wiki/Record_linkage

## License
[MIT](https://choosealicense.com/licenses/mit/)
