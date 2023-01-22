import json
import logging
import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


RESULTS_PATH = os.path.join(os.getcwd(), "stats", "algorithms", "runtime_analysis")

# Set log level
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s')


def compare_running_times_from_json_file():
    # Parse json
    dataframes = []
    dataset_name = ""
    files = [
        "data/results/runtime/Greedy-local-search: CPLEX "
        "Re-optimization/Greedy-local-search: CPLEX "
        "Re-optimization-on-changes_in_number_of_timeslots_comparison_set.json",
        "data/results/runtime/Active-time-IP/Active-time-IP-on-changes_in_number_of_timeslots_comparison_set.json"
    ]
    for file in files:
        try:
            with open(file) as json_file:
                data = json.load(json_file)

                dataset_name = data["data_set_name"]
                dataframes.append(pd.DataFrame.from_dict(pd.json_normalize(data["instance_results"])))
                print("hello")
                logging.info(f"Successfully loaded json file: {file}")
        except:
            logging.error(f"Failed to parse json, please try again: {file}")
            return

    df = pd.concat(dataframes)
    print(df)
    # hue = "Algorithm"
    sns.lineplot(x="T", y="runtime_in_sec", hue="Algorithm", data=df)
    sns.scatterplot(x="T", y="runtime_in_sec", data=df, hue="Algorithm", legend=False)
    # plt.legend(loc='upper right')
    plt.xlabel("Number of timeslots")
    plt.ylabel("Running time in seconds")
    plt.savefig(os.path.join(os.getcwd(),
                             "stats",
                             "algorithms",
                             "execution_times",
                             "plots",
                             f"{dataset_name}"))
    print(df, "")


def compare_running_times_for_greedy_local_search():
    # Parse json
    dataframes = []
    dataset_name = ""
    files = [
        "data/results/runtime/Greedy-local-search: Pyomo/Greedy-local-search: "
        "Pyomo-on-data_set_with_changes_in_T_used_for_maxflow comparisson.json",
        "data/results/runtime/Greedy-local-search: CPLEX (V2)/Greedy-local-search: CPLEX ("
        "V2)-on-data_set_with_changes_in_T_used_for_maxflow comparisson.json", 
        "data/results/runtime/Greedy-local-search: CPLEX Re-optimization/Greedy-local-search: CPLEX "
        "Re-optimization-on-data_set_with_changes_in_T_used_for_maxflow comparisson.json"
    ]
    for file in files:
        try:
            with open(file) as json_file:
                data = json.load(json_file)

                dataset_name = data["data_set_name"]
                dataframes.append(pd.DataFrame.from_dict(pd.json_normalize(data["instance_results"])))
                print("hello")
                logging.info(f"Successfully loaded json file: {file}")
        except:
            logging.error(f"Failed to parse json, please try again: {file}")
            return

    df = pd.concat(dataframes)
    print(df)
    # hue = "Algorithm"
    sns.lineplot(x="T", y="runtime_in_sec", hue="Algorithm", data=df)
    sns.scatterplot(x="T", y="runtime_in_sec", data=df, hue="Algorithm", legend=False)
    # plt.legend(loc='upper right')
    plt.xlabel("Number of timeslots")
    plt.ylabel("Running time in seconds")
    plt.savefig(os.path.join(os.getcwd(),
                             "stats",
                             "algorithms",
                             "execution_times",
                             "plots",
                             f"{dataset_name}"))
    print(df, "")