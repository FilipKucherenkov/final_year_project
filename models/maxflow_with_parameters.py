import pyomo.environ as pyo
from pyomo.opt import SolverFactory

from structures.graph.network import Network


def solve_max_flow(network: Network, total_sum: int):
    """
    Pyomo model for Linear programming definition derived from Network Models: “Wayne L. Winston (2004) Operations
    Research: Applications and Algorithms, p.414-459”
    :param network: Network object representation of the Active Time problem instance.
    :param total_sum: summation of the processing times of all jobs whose node representation is on the network.
    :return:
    """
    # Create pyomo model
    model = pyo.ConcreteModel()

    # Parameter: Nodes on the network
    model.nodes = pyo.Set(initialize=network.nodes.keys())

    # Parameter: Set of arcs in the form of tuples (Node1, Node2)
    model.arcs = pyo.Set(within=model.nodes * model.nodes,
                         initialize=network.get_arcs_as_tuples())
    # Parameter: Source node
    model.source_node = pyo.Param(within=model.nodes, initialize=network.source_node.value)
    # Parameter: Sink node
    model.sink_node = pyo.Param(within=model.nodes, initialize=network.sink_node.value)

    # Parameter: Arc capacities
    model.arc_capacity = pyo.Param(model.arcs,
                                   initialize=network.get_arc_capacity_map())

    # Decision Variable: flow that goes through an Arc
    model.arc_flow = pyo.Var(model.arcs, within=pyo.NonNegativeReals)
    arc_flow = model.arc_flow

    # Objective function: maximise the flow in the sink node
    def objective_rule(model):
        return sum(arc_flow[i, j] for (i, j) in model.arcs if j == model.sink_node())
    model.objective = pyo.Objective(rule=objective_rule, sense=pyo.maximize)

    # Constraint: Ensure the flow through each arc is less than or equal to the arc's capacity. (Upper bound)
    # (e.g) 0 <= flow through each arc <= arc capacity
    @model.Constraint(model.arcs)
    def feasibility_rule(model, i, j):
        return model.arc_flow[i, j] <= model.arc_capacity[i, j]

    # Constraint: Ensure the inflow of every node equals the outflow of the same node.
    @model.Constraint(model.nodes)
    def conservation_of_flow_rule(model, k):
        if k == model.source_node() or k == model.sink_node():
            return pyo.Constraint.Skip
        inFlow = sum(model.arc_flow[i, j] for (i, j) in model.arcs if j == k)
        outFlow = sum(model.arc_flow[i, j] for (i, j) in model.arcs if i == k)
        return inFlow == outFlow

    solver = SolverFactory('gurobi')
    results = solver.solve(model)

    if results.solver.termination_condition == 'infeasible':
        print("No feasible solution found")
        return 0
    else:
        max_flow = model.objective()
        print(f"Maximum-flow: {max_flow}")
        print(f"Execution time: {results.solver.time}")
        # print(results) An active time instance has a feasible schedule on the set of open time slots iff the

        # maximum flow (integral since capacities are integral) from s to d has value equal to the sum of all job
        # processing times
        if total_sum == max_flow:
            for (i, j) in model.arcs:
                print(f"Node: {i} to Node: {j} with capacity: {model.arc_capacity[i, j]} and flow: {arc_flow[i, j]()}")

        return results.solver.time



