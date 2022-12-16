from solvers.models.maxflow_cplex import solve_maxflow_cplex
from solvers.models.maxflow_cplex_v2 import solve_maxflow_cplex_v2
from solvers.models.maxflow_cplex_with_opt import solve_maxflow_cplex_with_opt
from structures.graph.arc import Arc
from structures.graph.network import Network
from structures.graph.node import Node
from structures.scheduling.job import Job
from structures.scheduling.timeslot import Timeslot


def generate_network(time_slots: list[Timeslot], jobs: list[Job]) -> Network:
    """
    Helper method to generate a flow network from a given time horizon and list of jobs.
    :param time_slots: list of timeslots part of our time horizon
    :param jobs: list of given jobs.
    :return: network representation of the jobs and the time_horizon.
    """

    # Create initial nodes
    source: Node = Node("source")
    sink: Node = Node("sink")

    # Create network and add nodes
    network: Network = Network(source, sink)

    for job in jobs:
        # Add a node for each job j
        new_node: Node = Node(f"j_{job.number}")
        network.add_node(new_node)

        # Add arcs from source to each job node j with capacity pj
        network.add_arc(Arc(source, new_node, job.processing_time))

    for timeslot in time_slots:
        if timeslot.is_open:
            # Add a node for each open timeslot t
            new_node: Node = Node(f"t_{timeslot.start_time}")
            network.add_node(new_node)
            # Add arcs from each open time slot node t to sink with capacity G
            network.add_arc(Arc(new_node, sink, timeslot.capacity))

    # For each job j, for each timeslot t in its window, add an edge from job node j to timeslot node t with unit
    # capacity.
    for job in jobs:
        for timeslot in time_slots:
            if timeslot.is_open and timeslot.is_timeslot_within_job_window(job):
                job_node: Node = network.nodes[f"j_{job.number}"]
                timeslot_node: Node = network.nodes[f"t_{timeslot.start_time}"]
                network.add_arc(Arc(job_node, timeslot_node, 1))

    return network


def test():
    # Create nodes
    source: Node = Node("s")
    sink: Node = Node("t")

    node_1: Node = Node("2")
    node_2: Node = Node("3")
    node_3: Node = Node("4")

    # Create network and add nodes
    network: Network = Network(source, sink)
    network.add_node(node_1)
    network.add_node(node_2)
    network.add_node(node_3)

    # Add arcs
    network.add_arc(Arc(source, node_1, 2))
    network.add_arc(Arc(source, node_2, 3))
    network.add_arc(Arc(node_1, node_2, 3))
    network.add_arc(Arc(node_1, node_3, 4))
    network.add_arc(Arc(node_2, node_3, 4))
    network.add_arc(Arc(node_3, sink, 1))
    network.add_arc(Arc(node_2, sink, 2))

    schedule = solve_maxflow_cplex(network.arcs, network.source_node, network.sink_node, 3)
    schedule = solve_maxflow_cplex_v2(network.arcs, network.source_node, network.sink_node, 3)
    # Create network and add nodes
    schedule.print_schedule_info()
    schedule.print_schedule_info()
    # network.print_network_info()
