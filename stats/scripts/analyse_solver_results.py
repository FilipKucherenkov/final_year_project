import json
import logging
import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

RESULTS_PATH = os.path.join(os.getcwd(), "stats", "algorithms", "runtime_analysis")

# Set log level
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s')


def compare_runtime_on_dataset_1(filename: str):
    """
    Produces a line plot to compare the runtime of the IP model and
    the Greedy local search algorithm on a data set with changes in the length
    of time horizon (25, 50, 75, 100) where the batch size G=20 and the number of jobs J=100 (fixed).
    """
    plt.clf()
    files = [
        "data/results/runtime/Greedy-local-search: CPLEX "
        "Re-optimization/Greedy-local-search: CPLEX "
        "Re-optimization-on-changes_in_number_of_timeslots_comparison_set.json",
        "data/results/runtime/Active-time-IP/Active-time-IP-on-changes_in_number_of_timeslots_comparison_set.json"
    ]
    df = construct_df_from_files(files)

    sns.lineplot(x="T", y="runtime_in_sec", hue="Algorithm", data=df)
    sns.scatterplot(x="T", y="runtime_in_sec", data=df, hue="Algorithm", legend=False)
    # plt.legend(loc='upper right')
    plt.xlabel("Number of timeslots")
    plt.ylabel("Running time in seconds")
    plt.savefig(os.path.join(os.getcwd(),
                             "stats",
                             "plots",
                             f"{filename}"))


def compare_runtime_on_dataset_2(file_name: str):
    """
    Produces a line plot which compares the runtime of the IP model and
    the Greedy local search algorithm on a data set with changes in the length
    of time horizon (25, 50, 75, 100) where the batch size G=20 and the number of jobs J=100.
    :param file_name: string to provide a name for the file.
    """

    plt.clf()
    files = [
        "data/results/runtime/Greedy-local-search: CPLEX "
        "Re-optimization/Greedy-local-search: CPLEX "
        "Re-optimization-on-Proportional changes in params Small.json",
        "data/results/runtime/Active-time-IP/Active-time-IP-on-Proportional changes in params Small.json"
    ]
    df = construct_df_from_files(files)

    sns.lineplot(x="T", y="runtime_in_sec", hue="Algorithm", data=df)
    sns.scatterplot(x="T", y="runtime_in_sec", data=df, hue="Algorithm", legend=False)
    # plt.legend(loc='upper right')
    plt.xlabel("Number of timeslots")
    plt.ylabel("Running time in seconds")
    plt.savefig(os.path.join(os.getcwd(),
                             "stats",
                             "plots",
                             f"{file_name}"))


def compare_utilization_perc_on_dataset_2(file_name: str):
    """
    Produces a bar plot which compares the average batch utilization produced by the IP model and
    the Greedy local search algorithm on a data set with changes in the length
    of time horizon (25, 50, 75, 100) where the batch size G=20 and the number of jobs J=100.
    :param file_name: string to provide a name for the file.
    """
    # create plot
    plt.clf()
    files = [
        "data/results/objective/Greedy-local-search: CPLEX "
        "Re-optimization/Greedy-local-search: CPLEX "
        "Re-optimization-on-Proportional changes in params Small.json",
        "data/results/objective/Active-time-IP/Active-time-IP-on-Proportional changes in params Small.json"
    ]
    df = construct_df_from_files(files)
    sns.barplot(x='T', y='batch_utilization', hue='Algorithm', data=df, palette='magma')
    df.groupby(['T', 'G']).mean()
    plt.xlabel("Number of timeslots")
    plt.ylabel("Average batch utilization %")
    plt.savefig(os.path.join(os.getcwd(),
                             "stats",
                             "plots",
                             f"{file_name}"))


def compare_running_times_for_greedy_local_search(file_name: str):
    """
    Function produces a plot which compares the runtime of the 4 implementations of
    the Greedy local search algorithm on a data set with changes in the length
    of time horizon (25, 50, 75, 100) where the batch size G=20 and the number of jobs J=100.
    """
    files = [
        "data/results/runtime/Greedy-local-search: Pyomo/Greedy-local-search: "
        "Pyomo-on-data_set_with_changes_in_T_used_for_maxflow comparisson.json",
        "data/results/runtime/Greedy-local-search: CPLEX (V2)/Greedy-local-search: CPLEX ("
        "V2)-on-data_set_with_changes_in_T_used_for_maxflow comparisson.json",
        "data/results/runtime/Greedy-local-search: CPLEX Re-optimization/Greedy-local-search: CPLEX "
        "Re-optimization-on-data_set_with_changes_in_T_used_for_maxflow comparisson.json"
    ]
    plt.clf()
    # Construct dataframe
    df = construct_df_from_files(files)

    sns.lineplot(x="T", y="runtime_in_sec", hue="Algorithm", data=df)
    sns.scatterplot(x="T", y="runtime_in_sec", data=df, hue="Algorithm", legend=False)
    # plt.legend(loc='upper right')
    plt.xlabel("Number of timeslots")
    plt.ylabel("Running time in seconds")
    plt.savefig(os.path.join(os.getcwd(),
                             "stats",
                             "plots",
                             f"{file_name}"))


def construct_df_from_files(files: list[str]):
    """
    Given a list of paths to json files, construct a DataFrame object with the
    data from the parsed files for further analysis.
    :param files: list of strings (file paths to json files).
    :return: DataFrame object containing the parsed data.
    """
    # Parse json
    dataframes = []
    dataset_name = ""

    for file in files:
        try:
            with open(file) as json_file:
                data = json.load(json_file)

                dataset_name = data["data_set_name"]
                dataframes.append(pd.DataFrame.from_dict(pd.json_normalize(data["instance_results"])))
                logging.info(f"Successfully loaded json file: {file}")
        except:
            logging.error(f"Failed to parse json, please try again: {file}")
            return

    df = pd.concat(dataframes)
    return df
