import argparse
import json
import logging
import os

from problem_classes.problem_instances.parsed_instance import ParsedInstance
from solvers.recovery.two_stage_recovery import two_stage_recovery
from solvers.solver_handler import solve_instance
from utils.file_writers import write_results_to_file
from utils.parsing import parse_problem_instance

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s')


def record_recovery():
    # Parse script arguments
    parser = argparse.ArgumentParser(description='Script that records performance of the recovery method.')
    parser.add_argument("--nominal_id", help="Specify the ID of a nominal instance from the data/nominal_instance "
                                             "directory.")
    parser.add_argument("--method", help="Specify method to be used for solving the nominal instance")
    args = parser.parse_args()

    nominal_instance = parse_problem_instance(f"data/nominal_instances/{args.nominal_id}.json")
    nominal_solution = solve_instance(nominal_instance, args.method, "cplex_direct")

    file_path = f"data/perturbed_instances/{args.nominal_id}"
    directory = os.fsencode(file_path)

    recovery_stats = {
        "nominal_instance": args.nominal_id,
        "nominal_objective": nominal_solution.calculate_active_time(),
        "perturbation_results": []
    }

    for file in os.listdir(directory):
        filename = os.fsdecode(file)

        if filename.endswith(".json"):
            json_file = os.path.join("data", "perturbed_instances", f"{args.nominal_id}", filename)
            # Open instance file.
            f = open(json_file)

            # Parse data.
            data = json.load(f)
            f.close()

            perturbation_id = data["perturbed_id"]
            gamma = data["gamma"]
            epsilon = data["epsilon"]
            perturbed_instance = ParsedInstance(data["instance"])
            optimal_perturbed_solution = solve_instance(perturbed_instance, "Active-time-IP", "cplex_direct")
            recovered_solution = two_stage_recovery(perturbed_instance, nominal_solution, gamma)

            opt_perturbed = optimal_perturbed_solution.calculate_active_time() if optimal_perturbed_solution.calculate_active_time() != 0 else 1
            batch_size = recovered_solution.calculate_batch_size()
            if batch_size > recovered_solution.batch_limit:
                b_augmentation = batch_size - recovered_solution.batch_limit
            else:
                b_augmentation = 0
            new_stats = {
                "perturbation_id": f"{perturbation_id}",
                "Method": f"{args.method}",
                "gamma": gamma,
                "epsilon": epsilon,
                "batch_augmentation": b_augmentation,
                "perturbed_opt_objective_value": optimal_perturbed_solution.calculate_active_time(),
                "reovered_objective_value": recovered_solution.calculate_active_time(),
                "opt_ratio": recovered_solution.calculate_active_time() / opt_perturbed
                    # math.sqrt((recovered_solution.calculate_active_time() - optimal_perturbed_solution.calculate_active_time()) ** 2)
            }
            recovery_stats["perturbation_results"] = recovery_stats["perturbation_results"] + [new_stats]

            continue
        else:
            logging.error(f"File is not in JSON format: {filename}")
            continue
    write_results_to_file("recovery/objective", args.method, args.nominal_id, recovery_stats)

record_recovery()