import logging
import timeit
import json
import pandas as pd

from problem_classes.problem_instances.parsed_instance import ParsedInstance
from solvers.solver_handler import solve_instance


def record_execution_time_on_instance(instance: ParsedInstance, algorithm: str, solver_type: str):
    t = timeit.Timer(lambda: solve_instance(instance, algorithm, solver_type))
    times = t.repeat(3, 3)
    total_time_taken = min(times) / 3
    return total_time_taken


def construct_df_from_files(files: list[str], json_field: str):
    """
    Given a list of paths to json files, construct a DataFrame object with the
    data from the parsed files for further analysis.
    :param json_field: field from json to normalize the data
    :param files: list of strings (file paths to json files).
    :return: DataFrame object containing the parsed data.
    """
    # Parse json
    dataframes = []

    for file in files:
        try:
            with open(file) as json_file:
                data = json.load(json_file)

                dataframes.append(pd.DataFrame.from_dict(pd.json_normalize(data[json_field])))
                logging.info(f"Successfully loaded json file: {file}")
        except:
            logging.error(f"Failed to parse json, please try again: {file}")
            return

    df = pd.concat(dataframes)
    return df


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
    total_rest = sum(1 for v in opt_stats if 1.2 < v["OPT"])
    print(f"Number of optimal solutions: {int(total_optimal_solutions)}/{len(opt_stats)}")
    print(f"OPT(J) < ALG(J) < 1.2: {total_close_to_opt}")
    print(f"ALG(J) > 1.2: {total_rest}")
    print(opt_stats)



