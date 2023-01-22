import timeit

from input_generation.problem_instances.parsed_instance import ParsedInstance
from solvers.solver_handler import solve_instance


def record_execution_time_on_instance(instance: ParsedInstance, algorithm: str, solver_type: str):
    t = timeit.Timer(lambda: solve_instance(instance, algorithm, solver_type))
    times = t.repeat(3, 3)
    total_time_taken = min(times) / 3
    return total_time_taken
