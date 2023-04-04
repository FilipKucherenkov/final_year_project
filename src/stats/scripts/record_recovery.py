import argparse
import json
import logging
import os
import timeit

from problem_classes.problem_instances.parsed_instance import ParsedInstance
from solvers.recovery.ip_recovery_3 import ip_recovery3
from solvers.solver_handler import solve_instance
from utils.file_writers import write_results_to_file
from utils.parsing import parse_problem_instance

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s')


def record_recovery():
    # Parse script arguments
    parser = argparse.ArgumentParser(description='Script that records performance of the recovery model.')
    parser.add_argument("--nominal_id", help="Specify the ID of a nominal instance from the data/nominal_instance "
                                             "directory.")
    parser.add_argument("--method", help="Specify method to be used for solving the nominal instance")
    parser.add_argument("--l1", help="Specify weight for first cost function")
    parser.add_argument("--l2", help="Specify weight for second cost function")
    parser.add_argument("--analysis_type", help="Specify analysis type (e.g. runtime, objective)", default="objective")
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
            print(f"File: {filename}")
            perturbation_id = data["perturbed_id"]
            gamma = data["gamma"]
            epsilon = data["epsilon"]
            perturbed_instance = ParsedInstance(data["instance"])

            if args.analysis_type == "objective":
                optimal_perturbed_solution = solve_instance(perturbed_instance, "Active-time-IP", "cplex_direct")

                recovered_solution = ip_recovery3(perturbed_instance,
                                                  nominal_solution,
                                                  float(args.l1),
                                                  float(args.l2),
                                                  gamma)

                opt_perturbed = optimal_perturbed_solution.calculate_active_time() if optimal_perturbed_solution.calculate_active_time() != 0 else 1
                batch_size = recovered_solution.calculate_batch_size()
                if batch_size > nominal_solution.batch_limit:
                    b_augmentation = batch_size - recovered_solution.batch_limit
                else:
                    b_augmentation = 0
                new_stats = {
                    "perturbation_id": f"{perturbation_id}",
                    "Method": f"{args.method}",
                    "lambda1": float(args.l1),
                    "lambda2": float(args.l2),
                    "gamma": gamma,
                    "epsilon": epsilon,
                    "batch_augmentation": b_augmentation,
                    "variables_changed": recovered_solution.variable_changes,
                    "perturbed_opt_objective_value": optimal_perturbed_solution.calculate_active_time(),
                    "reovered_objective_value": recovered_solution.calculate_active_time(),
                    "opt_ratio": recovered_solution.calculate_active_time() / opt_perturbed
                        # math.sqrt((recovered_solution.calculate_active_time() - optimal_perturbed_solution.calculate_active_time()) ** 2)
                }
                recovery_stats["perturbation_results"] = recovery_stats["perturbation_results"] + [new_stats]

                continue
            else:
                # Record runtime performance
                t = timeit.Timer(lambda: ip_recovery3(perturbed_instance,
                                                      nominal_solution,
                                                      nominal_instance.number_of_parallel_jobs,
                                                      nominal_instance.number_of_parallel_jobs,
                                                      gamma))
                times = t.repeat(3, 3)
                total_time_taken = min(times) / 3
                t2 = timeit.Timer(lambda:  solve_instance(perturbed_instance, "Active-time-IP", "cplex_direct"))
                times2 = t2.repeat(3, 3)
                total_time_taken2 = min(times2) / 3
                new_stats = {
                    "deterministic_model": total_time_taken2,
                    "recovery_model": total_time_taken,
                }
                recovery_stats["perturbation_results"] = recovery_stats["perturbation_results"] + [new_stats]
        else:
            logging.error(f"File is not in JSON format: {filename}")
            continue
    write_results_to_file(f"recovery/{args.analysis_type}/large_instances",
                          f"recovery_method_lambdas({args.l1},{args.l2})",
                          args.nominal_id, recovery_stats)



def record_recovery_runtime():
    moderate_instances = [
        "0e3f7403-5ead-4c0e-8f6c-4dedf931d689",
        "1e07f2e9-1e56-4731-8f8b-cacc425ccbc3",
        "3be5eecc-6b84-4f5c-9534-fee77017e023",
        "04ed6b37-3724-4821-9730-d11a57708ba5",
        "5a979bf6-1670-4fc5-beb4-c2e35ce2363d",
        "93bd11be-79ca-4d81-9749-f9b3a80303d8",
        "27721db8-63df-4e11-beee-892eee7faa27",
        "bab7c328-ed55-4cde-91ca-2f3158771d39",
        "d2f10c62-85f4-4ef3-a063-2f17de8a82c8",
        "e67c7a57-4c94-4511-afd6-7cad90632ff4",
    ]

    large_instances = [
        "0a751308-6ad9-459f-a61c-85aeec3e0a3b",
        "2cf763fa-f99c-4332-90bb-803e13441785",
        "3fe216a8-9d90-4d30-9d30-89a935e39692",
        "4a7006d6-bf42-485f-b491-ed3fdade55f2",
        "62d641e5-4818-427a-b9ed-a660a61b2f74",
        "86aa9d57-d11a-4da6-bd6b-3bce300714e4",
        "586b575a-a882-4512-a5ca-aa59771bff51",
        "3726f6ca-e4fe-4017-8cce-44c3a15c1db9",
        "b1c03081-14b3-43f9-ad53-dd54e9f6216a",
        "f0870c8e-6fbd-43cb-8a91-a33a0724aca0"
    ]
    l_weights = [(1, 1), (0, 1), (1, 0), (0.1, 2)]
    m_weights = [(0, 1), (1, 0), (0.5, 1)]
    for w_p in l_weights:
        l1 = float(w_p[0])
        l2 = float(w_p[1])
        print(l1)
        print(l2)
        for file in large_instances:

            nominal_instance = parse_problem_instance(f"data/nominal_instances/{file}.json")
            nominal_solution = solve_instance(nominal_instance, "Active-time-IP", "cplex_direct")
            file_path = f"data/perturbed_instances/{file}"
            directory = os.fsencode(file_path)
            recovery_stats = {
                "nominal_instance": file,
                "nominal_objective": nominal_solution.calculate_active_time(),
                "perturbation_results": []
            }

            for p_file in os.listdir(directory):
                filename = os.fsdecode(p_file)
                if filename.endswith(".json"):
                    json_file = os.path.join("data", "perturbed_instances", f"{file}", filename)
                    # Open instance file.
                    f = open(json_file)

                    # Parse data.
                    data = json.load(f)
                    f.close()
                    print(f"File: {filename}")
                    perturbation_id = data["perturbed_id"]
                    gamma = data["gamma"]
                    epsilon = data["epsilon"]
                    perturbed_instance = ParsedInstance(data["instance"])

                    # Record runtime performance
                    t = timeit.Timer(lambda: ip_recovery3(perturbed_instance,
                                                          nominal_solution,
                                                          l1,
                                                          l2,
                                                          gamma))
                    times = t.repeat(3, 3)
                    total_time_taken = min(times) / 3
                    t2 = timeit.Timer(lambda: solve_instance(perturbed_instance, "Active-time-IP", "cplex_direct"))
                    times2 = t2.repeat(3, 3)
                    total_time_taken2 = min(times2) / 3
                    new_stats = {
                        "deterministic_model": total_time_taken2,
                        "recovery_model": total_time_taken,
                    }
                    recovery_stats["perturbation_results"] = recovery_stats["perturbation_results"] + [new_stats]

            write_results_to_file(f"recovery/runtime/large_instances",
                                  f"recovery_method_lambdas({l1},{l2})",
                                  file,
                                  recovery_stats)


# record_recovery()