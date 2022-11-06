from structures.graph.node import Node


class Arc:
    """
    Simple class used to represent an arc in a network (or a weighted directed edge in a graph).
    An arc contains reference to the source and terminal nodes and its capacity.
    """
    source_node: Node
    terminal_node: Node
    capacity: int

    def __init__(self, source_node: Node, terminal_node: Node, capacity: int):
        self.source_node = source_node
        self.terminal_node = terminal_node
        self.capacity = capacity

