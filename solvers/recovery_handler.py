import logging

from solvers.recovery.ip_recovery_3 import ip_recovery3
from solvers.solver_handler import solve_instance


def recover_schedule(nominal_instance, perturbed_instance, v1, v2, gamma):
    """
    Recovery Handler
    :param nominal_instance: ParsedInstance object representing the nominal scenario.
    :param perturbed_instance: ParsedInstance object representing the true scenario.
    :param v1: float value for Cost coefficient 1
    :param v2: float value for Cost coefficient 2
    :param gamma: int value for upper bound on the number of perturbed jobs.
    :return: Schedule object representing the recovered schedule.
    """
    nominal_solution = solve_instance(nominal_instance, "Active-time-IP", "cplex_direct")
    logging.info(f"Expected Active Time: {nominal_solution.calculate_active_time()}")
    logging.info(f"Attempting to recover schedule...")

    recovered_schedule = ip_recovery3(perturbed_instance, nominal_solution, v1, v2, gamma)

    logging.info(f"Recovery completed")
    logging.info(f"Active time: {recovered_schedule.calculate_active_time()}")
    logging.info(f"Variables changed: {recovered_schedule.variable_changes}")
    batch_size = recovered_schedule.calculate_batch_size()
    if batch_size > recovered_schedule.batch_limit:
        capacity_augmentation = batch_size - recovered_schedule.batch_limit
    else:
        capacity_augmentation = 0
    logging.info(f"Capacity Augmentation {capacity_augmentation}")

    return recovered_schedule
