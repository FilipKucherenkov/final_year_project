import logging
import timeit

from problem_classes.problem_instances.parsed_instance import ParsedInstance
from solvers.recovery.ip_recovery import ip_recovery
from solvers.solver_handler import solve_instance


def record_execution_time_on_instance(instance: ParsedInstance, method: str, solver_type: str):
    """
    Record a method's runtime performance on a parsed instance.
    :param instance: ParsedInstance object
    :param method: Method to be used for solving the instance
    :param solver_type: type of solver (e.g. gurobi or cplex-direct)
    :return:the total time taken to obtain a result.
    """
    t = timeit.Timer(lambda: solve_instance(instance, method, solver_type))
    times = t.repeat(3, 3)
    total_time_taken = min(times) / 3
    return total_time_taken


def record_execution_time_of_recovery_on_instance(nominal_instance: ParsedInstance,
                                                  perturbed_instance: ParsedInstance,
                                                  deterministic_method: str,
                                                  solver_type: str,
                                                  v1: float,
                                                  v2: float,
                                                  gamma: int):
    """
    Record recovery method's runtime performance.
    :param nominal_instance: ParsedInstance object corresponding to the nominal scenario
    :param deterministic_method: Method to be used for solving the nominal instance
    :param solver_type: type of solver (e.g. gurobi or cplex-direct)
    :param v1: float value for weight for cost function 1.
    :param v2: float value for weight for cost function 2.
    :param gamma: int value for upper bound on the number of perturbed jobs.
    :return:the total time taken to obtain a result.
    """
    nominal_solution = solve_instance(nominal_instance, deterministic_method, solver_type)
    t2 = timeit.Timer(lambda: ip_recovery(perturbed_instance, nominal_solution, v1, v2, gamma))
    times2 = t2.repeat(3, 3)
    total_time_taken2 = min(times2) / 3

    t = timeit.Timer(lambda: solve_instance(perturbed_instance, deterministic_method, solver_type))
    times = t.repeat(3, 3)
    total_time_taken = min(times) / 3
    logging.info(f"Deterministic model: {total_time_taken} secs")
    logging.info(f"Recovery model: {total_time_taken2} secs")

