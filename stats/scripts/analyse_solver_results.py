import json
import logging
import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

from stats.scripts.analysis_helpers.helpers import construct_df_from_files

RESULTS_PATH = os.path.join(os.getcwd(), "stats", "algorithms", "runtime_analysis")

# Set log level
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s')


def compare_runtime_on_dataset_1(filename: str):
    plt.clf()
    files = [
        "data/results/runtime/Greedy-local-search: CPLEX "
        "Re-optimization/results_dataset_1.json",
        "data/results/runtime/Active-time-IP/results_dataset_1.json"
    ]
    df = construct_df_from_files(files, "instance_results")
    sns.lineplot(x="T", y="runtime_in_sec", hue="Algorithm", data=df)
    sns.scatterplot(x="T", y="runtime_in_sec", data=df, hue="Algorithm", legend=False)
    # plt.legend(loc='upper right')
    plt.xlabel("Number of timeslots")
    plt.ylabel("Running time in seconds")
    plt.savefig(os.path.join(os.getcwd(),
                             "stats",
                             "plots",
                             f"{filename}"))


def compare_utilization_perc_on_dataset_1(file_name: str):
    # create plot
    plt.clf()
    files = [
        "data/results/objective/Greedy-local-search: CPLEX "
        "Re-optimization/results_dataset_1.json",
        "data/results/objective/Active-time-IP/results_dataset_1.json"
    ]
    df = construct_df_from_files(files, "instance_results")
    sns.barplot(x='T', y='batch_utilization', hue='Algorithm', data=df, palette='magma')
    df.groupby(['T', 'G']).mean()
    plt.xlabel("Number of timeslots")
    plt.ylabel("Average batch utilization %")
    plt.savefig(os.path.join(os.getcwd(),
                             "stats",
                             "plots",
                             f"{file_name}"))


def compare_runtime_on_dataset_2(file_name: str):
    plt.clf()
    files = [
        "data/results/runtime/Greedy-local-search: CPLEX Re-optimization/results_dataset_2.json",
        "data/results/runtime/Active-time-IP/results_dataset_2.json"
    ]
    df = construct_df_from_files(files, "instance_results")

    sns.lineplot(x="T", y="runtime_in_sec", z="J", hue="Algorithm", data=df)
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
        "Re-optimization/results_dataset_2.json",
        "data/results/objective/Active-time-IP/results_dataset_2.json"
    ]
    df = construct_df_from_files(files, "instance_results")
    sns.barplot(x='T', y='batch_utilization', hue='Algorithm', data=df, palette='magma')
    df.groupby(['T', 'G']).mean()
    plt.xlabel("Number of timeslots")
    plt.ylabel("Average batch utilization %")
    plt.savefig(os.path.join(os.getcwd(),
                             "stats",
                             "plots",
                             f"{file_name}"))


def compare_runtime_on_dataset_4(filename: str):
    plt.clf()
    files = [
        "data/results/runtime/Greedy-local-search: CPLEX "
        "Re-optimization/results_dataset_4.json",
        "data/results/runtime/Active-time-IP/results_dataset_4.json"
    ]
    df = construct_df_from_files(files, "instance_results")
    sns.lineplot(x="J", y="runtime_in_sec", hue="Algorithm", data=df)
    sns.scatterplot(x="J", y="runtime_in_sec", data=df, hue="Algorithm", legend=False)
    # plt.legend(loc='upper right')
    plt.xlabel("Number of jobs")
    plt.ylabel("Running time in seconds")
    plt.savefig(os.path.join(os.getcwd(),
                             "stats",
                             "plots",
                             f"{filename}"))


def compare_utilization_perc_on_dataset_4(file_name: str):
    # create plot
    plt.clf()
    files = [
        "data/results/objective/Greedy-local-search: CPLEX "
        "Re-optimization/results_dataset_4.json",
        "data/results/objective/Active-time-IP/results_dataset_4.json"
    ]
    df = construct_df_from_files(files, "instance_results")
    sns.barplot(x='J', y='batch_utilization', hue='Algorithm', data=df, palette='magma')
    df.groupby(['J', 'G']).mean()
    plt.xlabel("Number of jobs")
    plt.ylabel("Average batch utilization %")
    plt.savefig(os.path.join(os.getcwd(),
                             "stats",
                             "plots",
                             f"{file_name}"))


def compare_runtime_on_dataset_5(filename: str):
    plt.clf()
    files = [
        "data/results/runtime/Greedy-local-search: CPLEX "
        "Re-optimization/results_dataset_5.json",
        "data/results/runtime/Active-time-IP/results_dataset_5.json"
    ]
    df = construct_df_from_files(files, "instance_results")
    sns.lineplot(x="G", y="runtime_in_sec", hue="Algorithm", data=df)
    sns.scatterplot(x="G", y="runtime_in_sec", data=df, hue="Algorithm", legend=False)
    # plt.legend(loc='upper right')
    plt.xlabel("Batch size")
    plt.ylabel("Running time in seconds")
    plt.savefig(os.path.join(os.getcwd(),
                             "stats",
                             "plots",
                             f"{filename}"))


def compare_utilization_perc_on_dataset_5(file_name: str):
    # create plot
    plt.clf()
    files = [
        "data/results/objective/Greedy-local-search: CPLEX "
        "Re-optimization/results_dataset_5.json",
        "data/results/objective/Active-time-IP/results_dataset_5.json"
    ]
    df = construct_df_from_files(files, "instance_results")
    sns.barplot(x='G', y='batch_utilization', hue='Algorithm', data=df, palette='magma')
    df.groupby(['J', 'G']).mean()
    plt.xlabel("Batch size")
    plt.ylabel("Average batch utilization %")
    plt.savefig(os.path.join(os.getcwd(),
                             "stats",
                             "plots",
                             f"{file_name}"))


def compare_runtime_on_dataset_6(filename: str):
    plt.clf()
    files = [
        "data/results/runtime/Greedy-local-search: CPLEX "
        "Re-optimization/results_dataset_6.json",
        "data/results/runtime/Active-time-IP/results_dataset_6.json"
    ]
    df = construct_df_from_files(files, "instance_results")
    sns.lineplot(x="G", y="runtime_in_sec", hue="Algorithm", data=df)
    sns.scatterplot(x="G", y="runtime_in_sec", data=df, hue="Algorithm", legend=False)
    # plt.legend(loc='upper right')
    plt.xlabel("Batch size")
    plt.ylabel("Running time in seconds")
    plt.savefig(os.path.join(os.getcwd(),
                             "stats",
                             "plots",
                             f"{filename}"))


def compare_utilization_perc_on_dataset_6(file_name: str):
    # create plot
    plt.clf()
    files = [
        "data/results/objective/Greedy-local-search: CPLEX "
        "Re-optimization/results_dataset_6.json",
        "data/results/objective/Active-time-IP/results_dataset_6.json"
    ]
    df = construct_df_from_files(files, "instance_results")
    sns.barplot(x='G', y='batch_utilization', hue='Algorithm', data=df, palette='magma')
    df.groupby(['J', 'G']).mean()
    plt.xlabel("Batch size")
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
        "data/results/runtime/Greedy-local-search: Pyomo/results_dataset_3.json",
        "data/results/runtime/Greedy-local-search: CPLEX (V1)/results_dataset_3.json",
        "data/results/runtime/Greedy-local-search: CPLEX (V2)/results_dataset_3.json",
        "data/results/runtime/Greedy-local-search: CPLEX Re-optimization/results_dataset_3.json"
    ]
    plt.clf()
    # Construct dataframe
    df = construct_df_from_files(files, "instance_results")

    sns.lineplot(x="T", y="runtime_in_sec", hue="Algorithm", data=df)
    sns.scatterplot(x="T", y="runtime_in_sec", data=df, hue="Algorithm", legend=False)
    # plt.legend(loc='upper right')
    plt.xlabel("Number of timeslots")
    plt.ylabel("Running time in seconds")
    plt.savefig(os.path.join(os.getcwd(),
                             "stats",
                             "plots",
                             f"{file_name}"))
