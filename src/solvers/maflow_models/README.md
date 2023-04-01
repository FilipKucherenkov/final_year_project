## Optimization models for computing the Maximum-flow of a network.
#### **Textbook:** *Operations Research: Applications and Algorithms, (2004), p.414-459*
#### **Author:** *Wayne L. Winston*

Folder contains several optimization models that are used by the Greedy Local search algorithm and for checking instance feasibility when generating input sets for analysis. Those include:
- `maxflow_pyomo.py`: Method for generating and solving a Pyomo Optimization model for computing Maximum flow of a network. 
- `maxflow_cplex.py`: Method for generating and solving an Optimization model implemented using IBM CPLEX Python API. Objective function maximises the outflow from the source node.
- `maxflow_cplex_v2.py`: Method for generating and solving an Optimization model implemented using IBM CPLEX Python API. Objective function maximises the inflow to the sink node.

In addition, our models utilize several problem classes which can be found at `problem_classes/graph` for assisting with the graph representation. Those include:
- `network.py`: Python class to represent a flow network.
- `arc.py`: Python class to represent arcs in the flow network.
- `node.py`: Python class to represent the nodes in the network.
- `generate_network.py`: Algorithm for generating a flow network instance that corresponds to problem instance of the Active time problem
