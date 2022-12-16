class Node:
    """
    Simple class to represent a Node. Every node has a value (e.g. "Node 1")
    """
    def __init__(self, value: str):
        self.value = value
        self.is_visited = False
        self.parent = -1
