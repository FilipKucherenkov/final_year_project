import argparse
import json
import logging
import math
import os

from problem_classes.problem_instances.parsed_instance import ParsedInstance
from solvers.solver_handler import solve_instance
from utils.file_writers import write_results_to_file
from utils.parsing import parse_problem_instance

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s')


def record_objective_deviation():
    """
    Script that records the objective value of a method on a nominal instance
    and then computes the optimal solution on a set ot perturbed instances.
    """
    # Parse script arguments
    parser = argparse.ArgumentParser(description='Script that records performance')

    parser.add_argument("--nominal_id", help="Specify the ID of a nominal instance from the data/nominal_instance "
                                             "directory.")
    parser.add_argument("--method", help="Specify method to be used for solving the perturbed instance")
    args = parser.parse_args()

    file_path = f"data/perturbed_instances/{args.nominal_id}"

    directory = os.fsencode(file_path)

    nominal_instance = parse_problem_instance(f"data/nominal_instances/{args.nominal_id}.json")
    ns = solve_instance(nominal_instance, args.method, "cplex_direct")
    print("Nominal solution")
    print(ns.calculate_active_time())

    pert_stats = {
        "nominal_instance": args.nominal_id,
        "perturbation_results": []
    }
    index = 0
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
            if perturbed_instance.is_feasible():
                ps_opt = solve_instance(perturbed_instance, "Active-time-IP", "cplex_direct")
                ps_m = solve_instance(perturbed_instance, args.method, "cplex_direct")
                new_stats = {
                    "perturbation_id": f"{perturbation_id}",
                    "perturbation_index": f"{index}",
                    "Method": f"{args.method}",
                    "gamma": gamma,
                    "epsilon": epsilon,
                    "perturbed_opt_objective_value": ps_opt.calculate_active_time(),
                    "perturbed_objective_value": ps_m.calculate_active_time(),
                    "nominal_objective_value": ns.calculate_active_time(),
                    "rmse_opt": math.sqrt((ps_opt.calculate_active_time() - ns.calculate_active_time())**2),
                    "rmse_value": math.sqrt((ps_m.calculate_active_time() - ns.calculate_active_time()) ** 2)
                }
                pert_stats["perturbation_results"] = pert_stats["perturbation_results"] + [new_stats]
            # s = recover_from_perturbation("Capacity Search", perturbed_instance, gamma)
            # s.print_schedule_info()
            index  = index + 1
            continue
        else:
            logging.error(f"File is not in JSON format: {filename}")
            continue
    write_results_to_file("perturbation", args.method, args.nominal_id, pert_stats)


record_objective_deviation()
