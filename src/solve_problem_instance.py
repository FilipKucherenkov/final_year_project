import argparse
import os
import logging

from solvers.solver_handler import solve_instance
from utils.parsing import parse_problem_instance

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s')


# TODO: Can extend this to optionally write the schedule to a file provided a command-line flag.

def solve_problem_instance():
    """
    Solve an problem instance from a json file.
    """
    # Parse script arguments
    parser = argparse.ArgumentParser(description='Script that solves the active-time problem')

    parser.add_argument("--algorithm", help="Specify solver", default="Active-time-IP")
    parser.add_argument("--file", help="Provide the path to a json file containing the problem instance")
    parser.add_argument("--solver_type", help="Choose optimization solver to be utilized", default="cplex_direct")
    args = parser.parse_args()

    logging.info('Validating provided arguments...')
    # Validate that correct file was provided
    if not os.path.exists(args.file) or not os.path.isfile(args.file):
        logging.error(f"Please specify correct path to instance file: {args.file}")
        return

    # Attempt to parse instance
    parsed_instance = parse_problem_instance(args.file)

    if not parsed_instance.is_feasible():
        logging.info(f"Instance is infeasible and cannot be solved.")
        return
    logging.debug(f"Feasibility check passed successfully")

    solution = solve_instance(parsed_instance, args.algorithm, args.solver_type)
    if solution:
        solution.print_schedule_info()


solve_problem_instance()
