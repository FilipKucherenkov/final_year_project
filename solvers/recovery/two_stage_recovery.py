import logging

from solvers.recovery.capacity_search import capacity_search
from solvers.recovery.ip_recovery import recover_schedule


def two_stage_recovery(perturbed_instance, nominal_solution, gamma):
    """
    2-Stage-Recovery method
    :param perturbed_instance: ParsedInstance object representing the True Scenario
    (Scenario after uncertainty realisation)
    :param nominal_solution: Schedule object representing the solution to the Nominal Scenario
    (Scenario before uncertainty realisation)
    :param gamma: int denoting the number of jobs with deviation in processing time
    :return: Schedule object representing recovered solution.
    """
    batch_limit = perturbed_instance.number_of_parallel_jobs
    if not perturbed_instance.is_feasible():
        # Type 2 Perturbation occurred - augment capacity.
        batch_limit = capacity_search(perturbed_instance, gamma)

        if batch_limit == -1:
            logging.error("Instance is infeasible and can't be solved.")
            return

    logging.info(f"Attempting to recover schedule using IP model with binded decisions. ")
    # Recover using IP model with Binded Decisions
    return recover_schedule(perturbed_instance,
                            nominal_solution,
                            perturbed_instance.number_of_parallel_jobs,
                            batch_limit)
