import timeit

from problem_classes.problem_instances.parsed_instance import ParsedInstance
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
