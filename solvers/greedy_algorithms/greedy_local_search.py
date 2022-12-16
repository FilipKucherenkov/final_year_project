import copy

from input_generation.problem_instances.custom_instance import CustomInstance
from input_generation.problem_instances.problem_instance import ProblemInstance
from solvers.models.active_time_ip import solve_active_time_ip
from solvers.models.maxflow_pyomo import solve_max_flow_model
from structures.graph.generate_network import generate_network
from structures.scheduling.schedule import Schedule


def greedy_local_search(instance: ProblemInstance, solver_type: str):
    """
    All time slots are assumed to be open initially. Consider time slots from left to right (i.e in increasing
    order). At a given time slot, close the slot and check if a feasible schedule exists in the open slots. If so,
    leave the slot closed, otherwise, open it again. Continue to the next slot.

    Note: Algorithm uses a Pyomo model for solving Maximum flow problem.
    :return: Schedule object containing the job to timeslot mapping.
    """
    # 0. Note: Important to deep copy input to avoid modifying problem instance.
    time_horizon = copy.deepcopy(instance.time_horizon)
    jobs = copy.deepcopy(instance.jobs)

    # 1. Find initial solution.
    network = generate_network(time_horizon.time_slots, jobs)
    total_sum = sum(job.processing_time for job in jobs)
    initial_schedule = solve_max_flow_model(network, total_sum, solver_type)

    if not initial_schedule.is_feasible:
        # If no feasible schedule can be found return.
        return Schedule(False, [])

    # 2. Attempt to find a better solution.
    for timeslot in time_horizon.time_slots:
        # 2.1. Close timeslot.
        timeslot.is_open = False

        # 2.2. Check for feasible solution in the other timeslots
        network = generate_network(time_horizon.time_slots, jobs)
        total_sum = sum(job.processing_time for job in jobs)

        # Flow values is used to pass the assigned flow values from previous computations.
        schedule = solve_max_flow_model(network, total_sum, solver_type)

        if schedule.is_feasible:
            # 2.3. If a better solution is found update the initial schedule.
            initial_schedule = schedule
        else:
            # 2.4. If no better solution is found open the time slot again and continue.
            timeslot.is_open = True

    return initial_schedule


def test_network():
    # TODO: Add this as a test for the algorithms
    instance = CustomInstance(6, 12, 2)
    instance.add_job(0, 0, 2, 2)
    instance.add_job(1, 0, 4, 2)
    instance.add_job(2, 1, 6, 1)
    instance.add_job(3, 0, 4, 4)

    # 1 Answer for Maxflow computation (Should be 5)
    network = generate_network(instance.time_horizon.time_slots, instance.jobs)
    network.print_network_info()
    total_sum = sum(job.processing_time for job in instance.jobs)
    answer, f = solve_max_flow_model(network, total_sum, "gurobi", {})
    print(answer.is_feasible)
    print(answer.print_schedule_info())

    # 2 Answer for IP model (Should be 5)
    answer2 = solve_active_time_ip(instance, "gurobi")
    print(answer2.is_feasible)
    print(answer2.print_schedule_info())

    # 3 Answer for Greedy local search (Should be 5)
    answer3 = greedy_local_search(instance, "gurobi")
    print(answer3.is_feasible)
    print(answer3.print_schedule_info())
