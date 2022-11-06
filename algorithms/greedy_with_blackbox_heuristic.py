from models.maxflow_with_parameters import solve_max_flow
from structures.graph.arc import Arc
from structures.graph.network import Network
from structures.graph.node import Node
from structures.job import Job
from structures.problem_instance import ProblemInstance
from structures.time_horizon import TimeHorizon


def generate_network(time_horizon: TimeHorizon, jobs: list[Job]) -> Network:
    """
    Helper method to generate a flow network from a given time horizon and list of jobs.
    :param time_horizon: TimeHorizon object
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

    for timeslot in time_horizon.time_slots:
        if timeslot.is_active:
            # Add a node for each open timeslot t
            new_node: Node = Node(f"t_{timeslot.start_time}")
            network.add_node(new_node)

            # Add arcs from each open time slot node t to sink with capacity G
            network.add_arc(Arc(new_node, sink, timeslot.capacity))

    # For each job j, for each timeslot t in its window, add an edge from job node j to timeslot node t with unit
    # capacity.
    for job in jobs:
        for timeslot in time_horizon.time_slots:
            if timeslot.is_timeslot_within_job_window(job):
                job_node: Node = network.nodes[f"j_{job.number}"]
                timeslot_node: Node = network.nodes[f"t_{timeslot.start_time}"]
                network.add_arc(Arc(job_node, timeslot_node, 1))

    return network


def greedy_with_blackbox_heuristic(instance: ProblemInstance):
    """
    All time slots are assumed to be open initially. Consider time slots from left to right (i.e in increasing
    order). At a given time slot, close the slot and check if a feasible schedule exists in the open slots. If so,
    leave the slot closed, otherwise, open it again. Continue to the next slot.
    :return:
    """
    # time_horizon = instance.time_horizon
    # for timeslot in time_horizon.time_slots:
    #     timeslot.is_open = False
    #     network = generate_network(time_horizon, ProblemInstance.jobs)
    #     time = solve_max_flow(network)
    #     print(time)


def test_network():
    time_horizon: TimeHorizon = TimeHorizon(6, 2)
    jobs: list[Job] = []
    job1 = Job(1)
    job1.release_time = 0
    job1.deadline = 2
    job1.processing_time = 2
    jobs.append(job1)

    job2 = Job(2)
    job2.release_time = 0
    job2.deadline = 4
    job2.processing_time = 2
    jobs.append(job2)

    job3 = Job(3)
    job3.release_time = 1
    job3.deadline = 6
    job3.processing_time = 1
    jobs.append(job3)

    job4 = Job(4)
    job4.release_time = 0
    job4.deadline = 4
    job4.processing_time = 4
    jobs.append(job4)

    network = generate_network(time_horizon, jobs)
    network.print_network_info()
    total_sum = sum(job.processing_time for job in jobs)
    time = solve_max_flow(network, total_sum)
    print(time)


def test():
    # Create nodes
    source: Node = Node("1")
    sink: Node = Node("5")

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
    network.add_arc(Arc(node_3, sink, 1))
    network.add_arc(Arc(node_2, sink, 2))

    network.print_network_info()
