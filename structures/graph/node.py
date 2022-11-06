class Node:
    """
    Simple class to represent a Node. Every node has a value (e.g. "Node 1")
    """
    value: str

    def __init__(self, value: str):
        self.value = value
