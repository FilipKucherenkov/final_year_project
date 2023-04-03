import argparse
import os
import logging

from solvers.recovery.ip_recovery_3 import ip_recovery3
from solvers.solver_handler import solve_instance
from utils.parsing import parse_problem_instance
from utils.performance_monitors import record_execution_time_of_recovery_on_instance

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s')


def recover_schedule():
    # Parse script arguments
    parser = argparse.ArgumentParser(description="Script recovers a schedule from disturbances.")

    parser.add_argument("--nominal_instance", help="Specify the path to a json file containing the nominal instance")
    parser.add_argument("--perturbed_instance",
                        help="Specify the path to a json file containing the perturbed instance")
    parser.add_argument("--v1",
                        help="Specify coefficient for first cost function. (Min proximity to nominal solution)")
    parser.add_argument("--v2",
                        help="Specify coefficient for second cost function. (Min active time)")
    parser.add_argument("--gamma",
                        help="Specify an upper bound on the number of perturbed jobs.")
    parser.add_argument("--planning_method", help="Specify method for stage 1.", default="Active-time-IP")
    parser.add_argument("--solver_type", help="Choose optimization solver to be utilized", default="cplex_direct")
    parser.add_argument("--runtime_monitor", help="Specify whether to track performance", default=False)
    args = parser.parse_args()

    logging.info('Validating provided arguments...')
    # Validate that correct file was provided
    if not os.path.exists(args.nominal_instance) or not os.path.isfile(args.nominal_instance):
        logging.error(f"Please specify correct path to a nominal instance file: {args.nominal_instance}")
        return

    if not os.path.exists(args.perturbed_instance) or not os.path.isfile(args.perturbed_instance):
        logging.error(f"Please specify correct path to a nominal instance file: {args.perturbed_instance}")
        return


    # Attempt to parse nominal instance
    nominal_instance = parse_problem_instance(args.nominal_instance)

    if not nominal_instance.is_feasible():
        logging.info(f"Instance is infeasible and cannot be solved.")
        return
    logging.debug(f"Feasibility check passed successfully")

    nominal_solution = solve_instance(nominal_instance, args.planning_method, args.solver_type)
    if nominal_solution:
        logging.debug(f"Nominal active time: {nominal_solution.calculate_active_time()}")
        # solution.print_schedule_info()

    perturbed_instance = parse_problem_instance(args.perturbed_instance)
    logging.debug(f"Specified weights v1={args.v1} and v2={args.v2}")
    logging.debug(f"Specified Gamma: {args.gamma}")
    logging.debug("Recovering schedule...")
    recovered_solution = ip_recovery3(perturbed_instance,
                                      nominal_solution,
                                      float(args.v1),
                                      float(args.v2),
                                      int(args.gamma))

    recovered_solution.print_schedule_info()

    if bool(args.runtime_monitor):
        record_execution_time_of_recovery_on_instance(nominal_instance,
                                                      perturbed_instance,
                                                      args.planning_method,
                                                      "cplex_direct",
                                                      float(args.v1),
                                                      float(args.v2),
                                                      int(args.gamma))
        logging.info(f"Expected active time: {nominal_solution.calculate_active_time()}")
        logging.info(f"Recovered active time: {recovered_solution.calculate_active_time()}")
        logging.info(f"Number of changes: {recovered_solution.variable_changes}")


recover_schedule()
