import copy

from problem_classes.problem_instances.parsed_instance import ParsedInstance
from solvers.maflow_models.maxflow_pyomo import solve_max_flow_model
from problem_classes.graph.generate_network import generate_network
from problem_classes.scheduling.schedule_alternative import Schedule


def greedy_local_search(instance: ParsedInstance, solver_type: str):
    """
    Greedy local search with Pyomo model for computing Max-flow.
    :param instance: ParsedInstance object for the problem instance
    :param solver_type: str to specify which solver to use (e.g. gurobi or cplex_direct)
    :return: Schedule object containing the solution
    """

    # 0. Note: Important to deep copy input to avoid modifying problem instance.
    time_horizon = copy.deepcopy(instance.time_horizon)
    jobs = copy.deepcopy(instance.jobs)

    # 1. Build the corresponding flow network and find initial solution.
    network = generate_network(time_horizon.time_slots, jobs)
    total_sum = sum(job.processing_time for job in jobs)
    initial_schedule = solve_max_flow_model(network, total_sum, solver_type, instance.number_of_parallel_jobs)

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
        schedule = solve_max_flow_model(network, total_sum, solver_type, instance.number_of_parallel_jobs)

        if schedule.is_feasible:
            # 2.3. If a better solution is found update the initial schedule.
            initial_schedule = schedule
        else:
            # 2.4. If no better solution is found open the time slot again and continue searching.
            timeslot.is_open = True

    return initial_schedule
