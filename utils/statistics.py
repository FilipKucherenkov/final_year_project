import json

import pandas as pd


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
        opt_value = row['objective_value']
        opt_stats.append({
            "Instance": row["Instance_index"],
            "OPT": computed_value / opt_value
        })
    total_optimal_solutions = sum(v["OPT"] for v in opt_stats if v["OPT"] == 1)
    total_close_to_opt = sum(1 for v in opt_stats if 1.2 >= v["OPT"] > 1)
    better_than_optimal = sum(1 for v in opt_stats if v["OPT"] < 1)
    total_rest = sum(1 for v in opt_stats if 1.2 <= v["OPT"])
    print(f"===================================================================")
    print(f"Dataset: {dataset_name}")
    print(f"Number of optimal solutions: {int(total_optimal_solutions)}/{len(opt_stats)}")
    print(f"ALG(J) < OPT(J): {better_than_optimal}")
    print(f"OPT(J) < ALG(J) < 1.2: {total_close_to_opt}")
    print(f"ALG(J) > 1.2: {total_rest}")
    print(opt_stats)