import logging

from recovery.capacity_search import capacity_search
from recovery.ip_recovery import recover_schedule
from solvers.solver_handler import solve_instance


def recover_from_perturbation(recovery_strategy: str,
                              perturbed_instance,
                              nominal_instance,
                              gamma,
                              solver_type,
                              nominal_method: str = "Active-time-IP"):

    logging.info(f"Attempting to recover using {recovery_strategy}")
    if recovery_strategy == "Capacity Search":
        return capacity_search(perturbed_instance, gamma)
    elif recovery_strategy == "IP with fixed variables":
        nominal_solution = solve_instance(nominal_instance, nominal_method, solver_type)
        nominal_solution.print_schedule_info()
        return recover_schedule(perturbed_instance, nominal_solution, nominal_instance, solver_type)
    else:
        logging.error(f"Aborting due to unsupported recovery strategy: {recovery_strategy}")
        return
