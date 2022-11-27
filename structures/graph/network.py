from structures.graph.arc import Arc
from structures.graph.node import Node


class Network:
    """
    Simple class to represent a network. A Network holds information about the
    nodes that are part of it, the arcs between nodes and the source and sink nodes of the
    Network.

    Note: getter methods are used assist with feeding input to the maxflow optimisation model.
    """

    def __init__(self, source_node: Node, sink_node: Node):
        self.source_node = source_node
        self.sink_node = sink_node
        self.nodes: dict[str, Node] = {"source": source_node, "sink": sink_node}
        self.arcs: list[Arc] = []

    def add_node(self, node: Node):
        self.nodes[node.value] = node

    def add_arc(self, arc: Arc):
        self.arcs.append(arc)

    def get_nodes_values_lst(self):
        nodes_lst = []
        for node in self.nodes:
            nodes_lst.append(node)
        return nodes_lst

    def get_arcs_as_tuples(self):
        arcs_lst = []
        for arc in self.arcs:
            arcs_lst.append((arc.source_node.value, arc.terminal_node.value))
        return arcs_lst

    def get_arc_capacity_map(self):
        arc_capacity_map = {}
        for arc in self.arcs:
            arc_capacity_map[(arc.source_node.value, arc.terminal_node.value)] = arc.capacity
        return arc_capacity_map

    def print_network_info(self):
        print(f"Source node: {self.source_node.value}")
        print(f"Sink node: {self.sink_node.value}")
        print(f"All nodes in the network:")
        for value in self.nodes.keys():
            print(f"Node: {value}")
        print(f"All arcs in the network:")
        for arc in self.arcs:
            print(f"Source: {arc.source_node.value} Destination: {arc.terminal_node.value} Capacity: {arc.capacity}")