import logging

from solvers.greedy_algorithms.greedy_local_search_with_reopt_v2 import greedy_local_search_with_reopt_v2
from solvers.models.active_time_ip import solve_active_time_ip
from solvers.greedy_algorithms.earliest_released_first import earliest_released_first
from solvers.greedy_algorithms.greedy_local_search import greedy_local_search
from solvers.greedy_algorithms.greedy_local_search_with_cplex import greedy_local_search_with_cplex
from solvers.greedy_algorithms.greedy_local_search_with_cplex_v2 import greedy_local_search_with_cplex_v2
from solvers.greedy_algorithms.greedy_local_search_with_reopt import greedy_local_search_with_reopt
from solvers.models.maxflow_pyomo import solve_max_flow


def solve_instance(instance, algorithm, solver_type):
    """
    Solve a given problem instance for the Active-time-problem
    :param instance: Problem instance object
    :param algorithm: specified algorithm (e.g active-time-ip, max-flow or Greedy-local-search)
    :param solver_type: specified solver (e.g. gurobi or cplex-direct)
    :return:
    """
    logging.info(f"Attempting to solve instance using {algorithm}")

    if algorithm == "Active-time-IP":
        return solve_active_time_ip(instance, solver_type)
    elif algorithm == "Greedy-local-search: Pyomo":
        return greedy_local_search(instance, solver_type)
    elif algorithm == "Greedy-local-search: CPLEX (V1)":
        return greedy_local_search_with_cplex(instance, solver_type)
    elif algorithm == "Greedy-local-search: CPLEX (V2)":
        return greedy_local_search_with_cplex_v2(instance, solver_type)
    elif algorithm == "Greedy-local-search-with-reopt":
        return greedy_local_search_with_reopt(instance, solver_type)
    elif algorithm == "Greedy-local-search-with-reopt-v2":
        return greedy_local_search_with_reopt_v2(instance, solver_type)
    elif algorithm == "Maxflow-LP":
        return solve_max_flow(instance, solver_type)
    elif algorithm == "Earliest-released-first":
        return earliest_released_first(instance)
    else:
        logging.error(f"Aborting due to unsupported solver type: {algorithm}")
        return
