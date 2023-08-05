
def dict_to_cypher_prop(dic):
    def to_string(value):
        if isinstance(value, str):
            return f"'{value}'"
        else:
            return value

    msg = ", ".join([f"{k}:{to_string(v)}"for k, v in dic.items()])
    return "{" + msg + "}"


class CypherNode:
    def __init__(self, node):
        self.node = node
        # WISHLIST: Improve the way indentifier is formed
        self.variable_name = f"node_{abs(hash(self.node))}"
        self.properties = dict_to_cypher_prop(node.properties)

    def get_create_statement(self):
        return f"CREATE ({self.variable_name}:{self.node.name} {self.properties})"


class CypherEdge:
    def __init__(self, edge):
        self.edge = edge
        # WISHLIST: Improve the way indentifier is formed
        self.variable_name = f"node_{abs(hash(self.edge))}"
        self.meta = dict_to_cypher_prop(edge.meta)

    def get_create_statement(self, node_l: CypherNode, node_r: CypherNode):
        assert isinstance(node_l, CypherNode) and isinstance(
            node_r, CypherNode)
        return f"({node_l.variable_name})-[:{self.edge.name.upper()} {self.meta}]->({node_r.variable_name})"


class CypherGraph:
    def __init__(self, graph):
        self.graph = graph
        self.cypher_nodes = []
        self.cypher_edges = []

    def get_create_statements(self):
        """CREATE (TheMatrix:Movie {title:'The Matrix', released:1999, tagline:'Welcome to the Real World'})"""
        """
        Identifier
        """
        cypher_nodes = [CypherNode(node) for node in self.graph.nodes]
        self.cypher_nodes = cypher_nodes

        create_cypher_nodes = [cn.get_create_statement()
                               for cn in cypher_nodes]
        node_to_cypher = {
            cypher_node.node: cypher_node for cypher_node in cypher_nodes}

        cypher_edges = [CypherEdge(edge) for edge in self.graph.edges]
        self.cypher_edges = cypher_edges

        create_edges = [cypher_edge.get_create_statement(node_to_cypher[cypher_edge.edge.node_l],
                                                         node_to_cypher[cypher_edge.edge.node_r])
                        for cypher_edge in cypher_edges]

        create_nodes_statement = "\n".join(create_cypher_nodes)
        create_edges_statement = "CREATE\n"+",\n".join(create_edges)
        return create_nodes_statement+"\n"+create_edges_statement
