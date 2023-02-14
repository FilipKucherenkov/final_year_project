import json

import pandas as pd


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
