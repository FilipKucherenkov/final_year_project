from models.active_time_ip import solve_active_time_ip
from structures.problem_instance import ProblemInstance


def main():
    instance1: ProblemInstance = ProblemInstance(12, 4, 3)

    solve_active_time_ip(instance1)

main()
