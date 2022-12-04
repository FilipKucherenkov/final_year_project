from solvers.models.active_time_ip import solve_active_time_ip
from solvers.models.greedy_with_blackbox_heuristic import greedy_with_blackbox_heuristic
from solvers.models.maxflow_with_parameters import solve_max_flow


def solve_instance(instance, algorithm, solver_type):
    """
    Solve a given problem instance for the Active-time-problem
    :param instance: Problem instance object
    :param algorithm: specified algorithm (e.g active-time-ip, max-flow or greedy-maxflow)
    :param solver_type: specified solver (e.g. gurobi or cplex-direct)
    :return:
    """

    if algorithm == "active-time-ip":
        return solve_active_time_ip(instance, solver_type)
    elif algorithm == "greedy-maxflow":
        return greedy_with_blackbox_heuristic(instance, solver_type)
