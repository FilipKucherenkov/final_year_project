import logging

from solvers.heuristic.erf_with_back_filling import erf_with_back_filling
from solvers.models.active_time_ip import solve_active_time_ip
from solvers.heuristic.earliest_released_first import earliest_released_first
from solvers.greedy_algorithms.greedy_local_search import greedy_local_search
from solvers.greedy_algorithms.greedy_local_search_with_cplex import greedy_local_search_with_cplex
from solvers.greedy_algorithms.greedy_local_search_with_cplex_v2 import greedy_local_search_with_cplex_v2
from solvers.models.maxflow_cplex_with_reopt import solve_maxflow_cplex_with_reopt
from solvers.models.maxflow_pyomo import solve_max_flow


def solve_instance(instance, algorithm, solver_type):
    """
    Solve a given problem instance of the Active-time-problem
    :param instance: ParsedInstance object
    :param algorithm: specified algorithm (e.g active-time-ip, max-flow or Greedy-local-search)
    :param solver_type: specified solver (e.g. gurobi or cplex-direct)
    :return: Schedule object containing the solution.
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
    elif algorithm == "Maxflow-LP":
        return solve_max_flow(instance, solver_type)
    elif algorithm == "Greedy-local-search: CPLEX Re-optimization":
        return solve_maxflow_cplex_with_reopt(instance)
    elif algorithm == "Earliest-released-first":
        return earliest_released_first(instance)
    elif algorithm == "Earliest-released-first-with-back-filling":
        return erf_with_back_filling(instance)
    else:
        logging.error(f"Aborting due to unsupported algorithm: {algorithm}")
        return
