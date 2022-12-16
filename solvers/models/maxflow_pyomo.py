import pyomo.environ as pyo
from pyomo.opt import SolverFactory

from structures.graph.generate_network import generate_network
from structures.graph.network import Network
from structures.scheduling.schedule import Schedule

import logging

logging.getLogger('pyomo.core').setLevel(logging.ERROR)  # Disable logging for performance


def solve_max_flow(instance, solver_type):
    network = generate_network(instance.time_horizon.time_slots, instance.jobs)
    total_sum = sum(job.processing_time for job in instance.jobs)
    return solve_max_flow_model(network, total_sum, solver_type)


def solve_max_flow_model(network: Network, total_sum: int, solver_type: str):
    """
    Pyomo model for Linear Programming formulation derived from Network Models: “Wayne L. Winston (2004) Operations
    Research: Applications and Algorithms, p.414-459”
    :param network: Network object representation of the Active Time problem instance.
    :param total_sum: summation of the processing times of all jobs whose node representation is on the network.
    :param solver_type: specified solver (e.g. gurobi or cplex-direct)
    :return: Schedule object containing Job to timeslot mapping
    """
    # Create pyomo model
    model = pyo.AbstractModel()

    # Parameter: Set of nodes on the network
    model.nodes = pyo.Set(initialize=network.get_nodes_values_lst())
    # Parameter: Set of arcs in the form of tuples (Node1, Node2)
    model.arcs = pyo.Set(within=model.nodes * model.nodes, initialize=network.get_arcs_as_tuples())
    # Parameter: Source node
    model.source_node = pyo.Param(within=model.nodes, initialize="source")
    # Parameter: Sink node
    model.sink_node = pyo.Param(within=model.nodes, initialize="sink")
    # Parameter: Arc capacities
    model.arc_capacity = pyo.Param(model.arcs,
                                   initialize=network.get_arc_capacity_map())

    # Decision Variable: flow that goes through an Arc
    model.arc_flow = pyo.Var(model.arcs, within=pyo.NonNegativeReals)

    # Objective function: maximise the inflow to the sink node
    def objective_rule(model):
        return sum(model.arc_flow[i, j] for (i, j) in model.arcs if j == model.sink_node())
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

    solver = SolverFactory(solver_type)
    instance = model.create_instance()

    results = solver.solve(instance, warmstart=True)  # Add warmstart=True in future for optimization

    if results.solver.termination_condition == 'infeasible':
        # No feasible solution found
        return Schedule(False, [])
    else:
        max_flow = instance.objective()
        # instance.display()
        # An active time instance has a feasible schedule on the set of open time slots iff the
        # maximum flow (integral since capacities are integral) from s to d has value equal to the sum of all job
        # processing times
        if total_sum == max_flow:
            job_to_timeslot_mapping = []
            for (i, j) in instance.arcs:
                source_node_info: list = i.split("_")  # As we care only about job and timeslot nodes
                dest_node_info: list = j.split("_")  # [0] - node type (job or timeslot), [1] (node number)
                if source_node_info[0] == "j" and dest_node_info[0] == "t":
                    if instance.arc_flow[i, j]() == 1:  # we care only where the arc flow is 1
                        # Schedule job j at timeslot t
                        job_to_timeslot_mapping.append((f"Job_{source_node_info[1]}", f"Slot_{dest_node_info[1]}"))

            schedule = Schedule(True, job_to_timeslot_mapping)
            return schedule

        # No feasible solution found
        return Schedule(False, [])
