import logging

from solvers.heuristic.erf_with_density_heuristic import erf_with_density_heuristic

from solvers.heuristic.earliest_released_first import earliest_released_first
from solvers.greedy_local_search.greedy_local_search import greedy_local_search
from solvers.greedy_local_search.greedy_local_search_with_cplex import greedy_local_search_with_cplex
from solvers.greedy_local_search.greedy_local_search_with_cplex_v2 import greedy_local_search_with_cplex_v2
from solvers.greedy_local_search.greedy_local_search_cplex_with_reopt import greedy_local_search_with_reopt
from solvers.ip_models.active_time_ip import solve_active_time_ip
from solvers.maflow_models.maxflow_cplex import solve_max_flow


def solve_instance(instance, method, solver_type):
    """
    Solve a ATSP problem instance.
    :param instance: ParsedInstance object for the problem instance
    :param method: specified method (e.g active-time-ip, max-flow or Greedy-local-search)
    :param solver_type: specified solver (e.g. cplex-direct)
    :return: Schedule object containing the solution.
    """
    logging.info(f"Attempting to solve instance using {method}")

    if method == "Active-time-IP":
        return solve_active_time_ip(instance, solver_type)
    elif method == "Greedy-local-search: Pyomo":
        return greedy_local_search(instance, solver_type)
    elif method == "Greedy-local-search: CPLEX (V1)":
        return greedy_local_search_with_cplex(instance)
    elif method == "Greedy-local-search: CPLEX (V2)":
        return greedy_local_search_with_cplex_v2(instance)
    elif method == "Maxflow-LP":
        return solve_max_flow(instance)
    elif method == "Greedy-local-search: CPLEX Re-optimization":
        return greedy_local_search_with_reopt(instance)
    elif method == "Earliest-released-first":
        return earliest_released_first(instance)
    elif method == "Earliest-released-first-with-density-heuristic":
        return erf_with_density_heuristic(instance)
    else:
        logging.error(f"Aborting due to unsupported method: {method}")
        return
