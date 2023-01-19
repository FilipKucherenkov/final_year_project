import copy
import os

from input_generation.problem_instances.problem_instance import ProblemInstance
from solvers.models.maxflow_cplex_with_reopt import solve_maxflow_cplex_with_reopt
from structures.graph.generate_network import generate_network
from structures.scheduling.schedule import Schedule


def greedy_local_search_with_reopt_v2(instance: ProblemInstance, solver_type: str):
    """
    All time slots are assumed to be open initially. Consider time slots from left to right (i.e in increasing
    order). At a given time slot, close the slot and check if a feasible schedule exists in the open slots. If so,
    leave the slot closed, otherwise, open it again. Continue to the next slot.
    :return:
    """
    # 0. Note: Important to deep copy input to avoid modifying problem instance.
    time_horizon = copy.deepcopy(instance.time_horizon)
    jobs = copy.deepcopy(instance.jobs)

    # 1. Find initial solution.
    network = generate_network(time_horizon.time_slots, jobs)
    total_sum = sum(job.processing_time for job in jobs)
    initial_schedule = solve_maxflow_cplex_with_reopt(network.arcs,
                                                      network.source_node,
                                                      network.sink_node,
                                                      total_sum,
                                                      "")

    if not initial_schedule.is_feasible:
        # If no feasible schedule can be found return.
        return Schedule(False, [])
    closed_timeslots = []
    # 2. Attempt to find a better solution.
    for timeslot in time_horizon.time_slots:
        # 2.1. Close timeslot.
        timeslot.is_open = False
        closed_timeslots.append(f"t_{timeslot.start_time}")
        # 2.2. Check for feasible solution in the other timeslots
        total_sum = sum(job.processing_time for job in jobs)

        # Flow values is used to pass the assigned flow values from previous computations.
        schedule = solve_maxflow_cplex_with_reopt(network.arcs, network.source_node, network.sink_node,
                                                  total_sum, closed_timeslots)
        # initial_bounds = flow_bounds
        # print(schedule.is_feasible)
        if schedule.is_feasible:
            # 2.3. If a better solution is found update the initial schedule.
            initial_schedule = schedule
        else:
            # 2.4. If no better solution is found open the time slot again and continue.
            timeslot.is_open = True
            closed_timeslots.remove(f"t_{timeslot.start_time}")

    return initial_schedule
