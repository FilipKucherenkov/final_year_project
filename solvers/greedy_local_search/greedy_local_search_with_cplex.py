import copy

from problem_classes.problem_instances.parsed_instance import ParsedInstance
from solvers.maflow_models.maxflow_cplex import solve_maxflow_cplex
from problem_classes.graph.generate_network import generate_network
from problem_classes.scheduling.schedule_alternative import Schedule


def greedy_local_search_with_cplex(instance: ParsedInstance):
    """
    Greedy local search with Pyomo model for computing Max-flow (V1).
    :param instance: ParsedInstance object for the problem instance
    :return: Schedule object containing the solution
    """

    # 0. Note: Important to deep copy input to avoid modifying problem instance.
    time_horizon = copy.deepcopy(instance.time_horizon)
    jobs = copy.deepcopy(instance.jobs)

    # 1. Build the corresponding flow network and find initial solution
    network = generate_network(time_horizon.time_slots, jobs)
    total_sum = sum(job.processing_time for job in jobs)
    initial_schedule = solve_maxflow_cplex(network.arcs,
                                           network.source_node,
                                           network.sink_node, total_sum,
                                           instance.number_of_parallel_jobs)

    if not initial_schedule.is_feasible:
        return Schedule(False, [], instance.number_of_parallel_jobs)

    # 2. Attempt to find a better solution by closing timeslots.
    for timeslot in time_horizon.time_slots:
        # 2.1. Close current timeslot.
        timeslot.is_open = False

        # 2.2. Re-generate the new corresponding network.
        network = generate_network(time_horizon.time_slots, jobs)
        total_sum = sum(job.processing_time for job in jobs)

        # 2.3. Check whether we can find a solution in the rest of the timeslots.
        schedule = solve_maxflow_cplex(network.arcs,
                                       network.source_node,
                                       network.sink_node,
                                       total_sum,
                                       instance.number_of_parallel_jobs)

        if schedule.is_feasible:
            # 2.3. If a better solution is found update the initial schedule.
            initial_schedule = schedule
        else:
            # 2.4. If no better solution is found open the time slot again and continue searching.
            timeslot.is_open = True

    return initial_schedule
