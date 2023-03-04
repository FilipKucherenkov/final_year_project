import json
import os

import pandas as pd

moderate_instances = [
    "results_0e3f7403-5ead-4c0e-8f6c-4dedf931d689.json",
    "results_1e07f2e9-1e56-4731-8f8b-cacc425ccbc3.json",
    "results_3be5eecc-6b84-4f5c-9534-fee77017e023.json",
    "results_04ed6b37-3724-4821-9730-d11a57708ba5.json",
    "results_5a979bf6-1670-4fc5-beb4-c2e35ce2363d.json",
    "results_93bd11be-79ca-4d81-9749-f9b3a80303d8.json",
    "results_27721db8-63df-4e11-beee-892eee7faa27.json",
    "results_bab7c328-ed55-4cde-91ca-2f3158771d39.json",
    "results_d2f10c62-85f4-4ef3-a063-2f17de8a82c8.json",
    "results_e67c7a57-4c94-4511-afd6-7cad90632ff4.json",
]

large_instances = [
    "results_0a751308-6ad9-459f-a61c-85aeec3e0a3b.json",
    "results_2cf763fa-f99c-4332-90bb-803e13441785.json",
    "results_3fe216a8-9d90-4d30-9d30-89a935e39692.json",
    "results_4a7006d6-bf42-485f-b491-ed3fdade55f2.json",
    "results_62d641e5-4818-427a-b9ed-a660a61b2f74.json",
    "results_86aa9d57-d11a-4da6-bd6b-3bce300714e4.json",
    "results_586b575a-a882-4512-a5ca-aa59771bff51.json",
    "results_3726f6ca-e4fe-4017-8cce-44c3a15c1db9.json",
    "results_b1c03081-14b3-43f9-ad53-dd54e9f6216a.json",
    "results_f0870c8e-6fbd-43cb-8a91-a33a0724aca0.json"
]

def print_rmse_stats_for_methods():
    # Calculate Root Mean Square Error (RMSE) value for results
    calculate_total_rmse("Active-time-IP", "moderate")
    calculate_total_rmse("Greedy-local-search: CPLEX Re-optimization", "moderate")
    calculate_total_rmse("Active-time-IP", "large")
    calculate_total_rmse("Greedy-local-search: CPLEX Re-optimization", "large")
    # Calculate Root Mean Square Error (RMSE) with respect to Gamma
    calculate_rmse_for_different_gamma("Active-time-IP", "moderate")
    calculate_rmse_for_different_gamma("Greedy-local-search: CPLEX Re-optimization", "moderate")
    calculate_rmse_for_different_gamma("Active-time-IP", "large")
    calculate_rmse_for_different_gamma("Greedy-local-search: CPLEX Re-optimization", "large")
    # Calculate Root Mean Square Error (RMSE) with respect to epsilon
    calculate_rmse_for_different_epsilon("Active-time-IP", "moderate")
    calculate_rmse_for_different_epsilon("Greedy-local-search: CPLEX Re-optimization", "moderate")
    calculate_rmse_for_different_epsilon("Active-time-IP", "large")
    calculate_rmse_for_different_epsilon("Greedy-local-search: CPLEX Re-optimization", "large")
def calculate_total_rmse(method, instance_type):
    """
    Calculate Root-Mean-Square-Error for a method to measure how close is
    the objective value of a nominal instance to the optimal objective value on all perturbed
    instances.
    :param method: str specifying the method for analysis.
    """
    dir_path = f"data/results/perturbation/{method}/"
    directory = os.fsencode(dir_path)
    total_opt_rmse = 0
    total_rmse = 0
    number_of_results = 0
    instances = []
    if instance_type == "moderate":
        instances = moderate_instances
    else:
        instances = large_instances

    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        file_path = f"data/results/perturbation/{method}/{filename}"
        if filename.endswith(".json") and filename in instances:
            with open(file_path) as json_file:
                data = json.load(json_file)
                for result in data["perturbation_results"]:
                    total_rmse = total_rmse + result["rmse_value"] # Used for Sensitivity
                    total_opt_rmse = total_opt_rmse + result["rmse_opt"] # Used for RR
                    number_of_results = number_of_results + 1

    print(f"Total RMSE on {instance_type} instances for: {method}")
    print("=============================================")
    print(f"Sensitivity: {total_rmse / number_of_results}")
    print(f"RR: {total_opt_rmse / number_of_results}")
    print("=============================================")


def calculate_rmse_for_different_gamma(method, instance_type):
    dir_path = f"data/results/perturbation/{method}/"
    directory = os.fsencode(dir_path)
    gamma_count = {}
    total_opt_rmse_sum = {} # RR
    total_rmse_sum = {}
    rmse_results = []
    opt_rmse_results = [] # RR

    instances = []
    if instance_type == "moderate":
        instances = moderate_instances
    else:
        instances = large_instances

    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        file_path = f"data/results/perturbation/{method}/{filename}"
        if filename.endswith(".json") and filename in instances:
            with open(file_path) as json_file:
                data = json.load(json_file)
                for result in data["perturbation_results"]:
                    gamma = result["gamma"]
                    rmse = result["rmse_value"]
                    opt_rmse = result["rmse_opt"]
                    if gamma in gamma_count:
                        gamma_count[gamma] = gamma_count[gamma] + 1
                        total_rmse_sum[gamma] = total_rmse_sum[gamma] + rmse
                        total_opt_rmse_sum[gamma] = total_opt_rmse_sum[gamma] + opt_rmse
                    else:
                        gamma_count[gamma] = 1
                        total_rmse_sum[gamma] = rmse
                        total_opt_rmse_sum[gamma] = opt_rmse

    for gamma, rmse_value in total_rmse_sum.items():
        rmse_results.append({
            "Gamma": gamma,
            "rmse": (rmse_value / gamma_count[gamma])
        })
    for gamma, opt_rmse_value in total_opt_rmse_sum.items():
        opt_rmse_results.append({
            "Gamma": gamma,
            "opt_rmse": (opt_rmse_value / gamma_count[gamma])
        })
    print(f"RMSE Results on {instance_type} instances for: {method}")
    print(rmse_results) # Sensitivity
    print(opt_rmse_results) # RR
    print("=============================================")


def calculate_rmse_for_different_epsilon(method, instance_type):
    dir_path = f"data/results/perturbation/{method}/"
    directory = os.fsencode(dir_path)
    eps_count = {}
    total_opt_rmse_sum = {}  # RR
    total_rmse_sum = {}
    rmse_results = []
    opt_rmse_results = []  # RR

    instances = []
    if instance_type == "moderate":
        instances = moderate_instances
    else:
        instances = large_instances
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        file_path = f"data/results/perturbation/{method}/{filename}"
        if filename.endswith(".json") and filename in instances:
            with open(file_path) as json_file:
                data = json.load(json_file)
                for result in data["perturbation_results"]:
                    epsilon = result["epsilon"]
                    rmse = result["rmse_value"]
                    opt_rmse = result["rmse_opt"]
                    if epsilon in eps_count:
                        eps_count[epsilon] = eps_count[epsilon] + 1
                        total_rmse_sum[epsilon] = total_rmse_sum[epsilon] + rmse
                        total_opt_rmse_sum[epsilon] = total_opt_rmse_sum[epsilon] + opt_rmse
                    else:
                        eps_count[epsilon] = 1
                        total_rmse_sum[epsilon] = rmse
                        total_opt_rmse_sum[epsilon] = opt_rmse

    for epsilon, rmse_value in total_rmse_sum.items():
        rmse_results.append({
            "epsilon": epsilon,
            "rmse": (rmse_value / eps_count[epsilon])
        })
    for epsilon, opt_rmse_value in total_opt_rmse_sum.items():
        opt_rmse_results.append({
            "epsilon": epsilon,
            "opt_rmse": (opt_rmse_value / eps_count[epsilon])
        })
    print(f"RMSE Results on {instance_type} instances for: {method}")
    print(rmse_results)
    print(opt_rmse_results)
    print("=============================================")


def calculate_runtime_stats(dataset_name: str, method):
    file = f"data/results/runtime/{method}/results_{dataset_name}.json"
    data = None
    with open(file) as json_file:
        data = json.load(json_file)

    average_runtime_on_set = 0
    max_runtime_on_set = -1
    for instance in data["instance_results"]:
        runtime = instance["runtime_in_sec"]
        average_runtime_on_set = average_runtime_on_set + runtime
        if runtime >= max_runtime_on_set:
            max_runtime_on_set = runtime

    average_runtime_on_set = average_runtime_on_set / len(data["instance_results"])
    print(f"===================================================================")
    print(f"Dataset: {dataset_name}")
    print(f"Method: {method}")

    print(f"Average time taken in seconds: {average_runtime_on_set}")
    print(f"Maximum time taken in seconds: {max_runtime_on_set}")


def count_optimal_objectives(dataset_name: str, method: str):
    files = [
        f"data/results/objective/Active-time-IP/results_{dataset_name}.json",
        f"data/results/objective/{method}/results_{dataset_name}.json"
    ]
    opt_df = pd.DataFrame()
    with open(files[0]) as json_file:
        data = json.load(json_file)
        opt_df = pd.DataFrame.from_dict(pd.json_normalize(data["instance_results"]))

    df = pd.DataFrame()
    with open(files[1]) as json_file:
        data = json.load(json_file)
        df = pd.DataFrame.from_dict(pd.json_normalize(data["instance_results"]))

    opt_stats = []
    for index, row in opt_df.iterrows():
        computed_value = df.loc[df['Instance_index'].eq(row['Instance_index']), 'objective_value'].iat[0]
        batch_util = df.loc[df['Instance_index'].eq(row['Instance_index']), 'batch_utilization'].iat[0]
        opt_value = row['objective_value']

        opt_stats.append({
            "Instance": row["Instance_index"],
            "OPT": computed_value / opt_value,
            "UTIL": batch_util
        })
    total_optimal_solutions = sum(v["OPT"] for v in opt_stats if v["OPT"] == 1)
    # total_rest = sum(1 for v in opt_stats if 1.2 <= v["OPT"])
    # total_close_to_opt = sum(1 for v in opt_stats if 1.2 >= v["OPT"] > 1)
    better_than_optimal = sum(1 for v in opt_stats if v["OPT"] < 1)
    mean_opt_ratio = sum(v["OPT"] for v in opt_stats) / len(opt_stats)
    max_opt_ratio = -1
    for v in opt_stats:
        if v["OPT"] >= max_opt_ratio:
            max_opt_ratio = v["OPT"]
    mean_batch_util = sum(v["UTIL"] for v in opt_stats) / len(opt_stats)
    max_batch_util = -1
    for v in opt_stats:
        if v["UTIL"] >= max_batch_util:
            max_batch_util = v["UTIL"]

    print(f"===================================================================")
    print(f"Dataset: {dataset_name}")
    print(f"Method: {method}")
    print(f"Number of optimal solutions: {int(total_optimal_solutions)}/{len(opt_stats)}")
    print(f"Number of solutions below optimal: {better_than_optimal}/{len(opt_stats)}")
    print(f"MEAN ALG(J) / OPT(J): {mean_opt_ratio}")
    print(f"MAX ALG(J) / OPT(J): {max_opt_ratio}")
    print(f"MEAN UTIL: {mean_batch_util}")
    print(f"MAX UTIL: {max_batch_util}")
    #
    # print(f"ALG(J) < OPT(J): {better_than_optimal}")
    # print(f"OPT(J) < ALG(J) < 1.2: {total_close_to_opt}")
    # print(opt_stats)
