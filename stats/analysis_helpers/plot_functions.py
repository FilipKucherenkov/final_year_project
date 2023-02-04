import logging
import os
import matplotlib.pyplot as plt
import seaborn as sns

from stats.analysis_helpers.helpers import construct_df_from_files, count_optimal_objectives
from stats.analysis_helpers.plot_producer import PlotProducer

RESULTS_PATH = os.path.join(os.getcwd(), "stats", "algorithms", "runtime_analysis")

# Set log level
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s')


def print_objective_stats_for_all_methods():
    # Print objective stats for an algorithm on dataset compared to the optimal
    count_optimal_objectives("dataset_1", "Earliest-released-first-with-density-heuristic")
    count_optimal_objectives("dataset_2", "Earliest-released-first-with-density-heuristic")
    count_optimal_objectives("dataset_3", "Earliest-released-first-with-density-heuristic")
    count_optimal_objectives("dataset_4", "Earliest-released-first-with-density-heuristic")
    count_optimal_objectives("dataset_5", "Earliest-released-first-with-density-heuristic")
    count_optimal_objectives("dataset_6", "Earliest-released-first-with-density-heuristic")
    count_optimal_objectives("dataset_7", "Earliest-released-first-with-density-heuristic")

    count_optimal_objectives("dataset_1", "Greedy-local-search: CPLEX Re-optimization")
    count_optimal_objectives("dataset_2", "Greedy-local-search: CPLEX Re-optimization")
    count_optimal_objectives("dataset_3", "Greedy-local-search: CPLEX Re-optimization")
    count_optimal_objectives("dataset_4", "Greedy-local-search: CPLEX Re-optimization")
    count_optimal_objectives("dataset_5", "Greedy-local-search: CPLEX Re-optimization")
    count_optimal_objectives("dataset_6", "Greedy-local-search: CPLEX Re-optimization")
    count_optimal_objectives("dataset_7", "Greedy-local-search: CPLEX Re-optimization")


def generate_all_plots():
    # ------ Dataset 1 plots --------
    runtime_plot_1("runtime_on_dataset_1", "dataset_1")
    util_plot_1("Batch-util-dataset_1", "dataset_1")
    # LCS vs IP model
    objective_plot_1("LCS_vs_IP_dataset_1", "Greedy-local-search: CPLEX Re-optimization",
                     "dataset_1")
    # Maxflow model vs IP model
    objective_plot_1("Maxflow_vs_IP_dataset_1", "Maxflow-LP", "dataset_1")
    # Greedy vs IP model
    objective_plot_1("Greedy_vs_IP_dataset_1", "Earliest-released-first-with-density-heuristic",
                     "dataset_1")

    # ------ Dataset 2 plots --------
    runtime_plot_2("Runtime_on_dataset_2", "dataset_2")
    util_plot_2("Batch-util-dataset_2", "dataset_2")
    # LCS vs IP model
    objective_plot_2("LCS_vs_IP_dataset_2", "Greedy-local-search: CPLEX Re-optimization",
                     "dataset_2")
    # Greedy vs IP model
    objective_plot_2("Greedy_vs_IP_dataset_2", "Earliest-released-first-with-density-heuristic",
                     "dataset_2")

    # ------ Dataset 4 plots --------
    runtime_plot_4("Runtime-on-dataset-4", "dataset_4")
    util_plot_4("Batch-util-dataset-4", "dataset_4")

    # ------ Dataset 5 plots --------
    runtime_plot_5("Runtime-on-dataset-5", "dataset_5")
    util_plot_5("Batch-util-dataset-5", "dataset_5")

    # ------ Dataset 6 plots --------
    runtime_plot_6("Runtime-on-dataset-6", "dataset_6")
    util_plot_6("Batch-util-dataset-6", "dataset_6")

    # Batch-utilization plots

    # Local search optimizations and analysis on datasets 3 & 7
    runtime_gls_plot("Runtime-dataset-3-local-search", "dataset_3")
    runtime_gls_2_plot("Change-in-objective-dataset-3", "dataset_3")
    runtime_gls_3_plot("Change-in-objective-dataset-7", "dataset_7")


# ======== Dataset 1 plots ============
def runtime_plot_1(file_name: str, dataset_name: str):
    files = [
        "data/results/runtime/Greedy-local-search: CPLEX "
        "Re-optimization/results_dataset_1.json",
        "data/results/runtime/Active-time-IP/results_dataset_1.json"
    ]
    plot_producer = PlotProducer(files, file_name, dataset_name)
    plot_producer.generate_line_plot("T", "runtime_in_sec", "Number of timeslots", "Running time in seconds")


def util_plot_1(file_name: str, dataset_name: str):
    files = [
        "data/results/objective/Greedy-local-search: CPLEX "
        "Re-optimization/results_dataset_1.json",
        "data/results/objective/Active-time-IP/results_dataset_1.json",
        "data/results/objective/Earliest-released-first-with-density-heuristic/results_dataset_1.json"
    ]

    plot_producer = PlotProducer(files, file_name, dataset_name)
    plot_producer.generate_bar_plot("T", "batch_utilization", "Number of timeslots", "Average batch utilization %")


def objective_plot_1(file_name: str, method: str, dataset_name: str):
    files = [
        f"data/results/objective/{method}/results_{dataset_name}.json",
        f"data/results/objective/Active-time-IP/results_{dataset_name}.json"
    ]
    plot_producer = PlotProducer(files, file_name, dataset_name)
    plot_producer.generate_line_plot("T", "objective_value", "Number of time slots", "Objective value")


# ======== Dataset 2 plots ============
def runtime_plot_2(file_name: str, dataset_name: str):
    plt.clf()
    files = [
        "data/results/runtime/Greedy-local-search: CPLEX Re-optimization/results_dataset_2.json",
        "data/results/runtime/Active-time-IP/results_dataset_2.json"
    ]
    plot_producer = PlotProducer(files, file_name, dataset_name)
    plot_producer.generate_line_plot("T", "runtime_in_sec", "Number of timeslots", "Running time in seconds")


def util_plot_2(file_name: str, dataset_name: str):
    files = [
        "data/results/objective/Greedy-local-search: CPLEX "
        "Re-optimization/results_dataset_2.json",
        "data/results/objective/Active-time-IP/results_dataset_2.json",
        "data/results/objective/Earliest-released-first-with-density-heuristic/results_dataset_2.json"
    ]
    plot_producer = PlotProducer(files, file_name, dataset_name)
    plot_producer.generate_bar_plot("T", "batch_utilization", "Number of timeslots", "Average batch utilization %")


def objective_plot_2(file_name: str, method: str, dataset_name: str):
    files = [
        f"data/results/objective/{method}/results_{dataset_name}.json",
        f"data/results/objective/Active-time-IP/results_{dataset_name}.json"
    ]
    plot_producer = PlotProducer(files, file_name, dataset_name)
    plot_producer.generate_line_plot("T", "objective_value", "Number of time slots", "Objective value")


# ======== Dataset43 plots ============
def runtime_plot_4(file_name: str, dataset_name: str):
    files = [
        "data/results/runtime/Greedy-local-search: CPLEX "
        "Re-optimization/results_dataset_4.json",
        "data/results/runtime/Active-time-IP/results_dataset_4.json"
    ]

    plot_producer = PlotProducer(files, file_name, dataset_name)
    plot_producer.generate_line_plot("J", "runtime_in_sec", "Number of jobs", "Running time in seconds")


def util_plot_4(file_name: str, dataset_name: str):
    files = [
        "data/results/objective/Greedy-local-search: CPLEX "
        "Re-optimization/results_dataset_4.json",
        "data/results/objective/Active-time-IP/results_dataset_4.json"
    ]
    plot_producer = PlotProducer(files, file_name, dataset_name)
    plot_producer.generate_bar_plot("J", "batch_utilization", "Number of jobs", "Average batch utilization %")


def runtime_plot_5(file_name: str, dataset_name: str):
    plt.clf()
    files = [
        "data/results/runtime/Greedy-local-search: CPLEX "
        "Re-optimization/results_dataset_5.json",
        "data/results/runtime/Active-time-IP/results_dataset_5.json"
    ]
    plot_producer = PlotProducer(files, file_name, dataset_name)
    plot_producer.generate_line_plot("G", "runtime_in_sec", "Batch size", "Running time in seconds")


def util_plot_5(file_name: str, dataset_name: str):
    files = [
        "data/results/objective/Greedy-local-search: CPLEX "
        "Re-optimization/results_dataset_5.json",
        "data/results/objective/Active-time-IP/results_dataset_5.json"
    ]
    plot_producer = PlotProducer(files, file_name, dataset_name)
    plot_producer.generate_bar_plot("G", "batch_utilization", "Batch size", "Average batch utilization %")


def runtime_plot_6(file_name: str, dataset_name: str):
    files = [
        "data/results/runtime/Greedy-local-search: CPLEX "
        "Re-optimization/results_dataset_6.json",
        "data/results/runtime/Active-time-IP/results_dataset_6.json"
    ]
    plot_producer = PlotProducer(files, file_name, dataset_name)
    plot_producer.generate_line_plot("G", "runtime_in_sec", "Batch size", "Running time in seconds")


def util_plot_6(file_name: str, dataset_name: str):
    # create plot
    plt.clf()
    files = [
        "data/results/objective/Greedy-local-search: CPLEX "
        "Re-optimization/results_dataset_6.json",
        "data/results/objective/Active-time-IP/results_dataset_6.json"
    ]
    plot_producer = PlotProducer(files, file_name, dataset_name)
    plot_producer.generate_bar_plot("G", "batch_utilization", "Batch size", "Average batch utilization %")


def runtime_gls_plot(file_name: str, dataset_name: str):
    files = [
        "data/results/runtime/Greedy-local-search: Pyomo/results_dataset_3.json",
        "data/results/runtime/Greedy-local-search: CPLEX (V1)/results_dataset_3.json",
        "data/results/runtime/Greedy-local-search: CPLEX (V2)/results_dataset_3.json",
        "data/results/runtime/Greedy-local-search: CPLEX Re-optimization/results_dataset_3.json"
    ]
    plot_producer = PlotProducer(files, file_name, dataset_name)
    plot_producer.generate_line_plot("T", "runtime_in_sec", "Number of timeslots", "Running time in seconds")


def runtime_gls_2_plot(file_name: str, dataset_name: str):
    files = [
        "data/results/runtime/Greedy-local-search: CPLEX (V1)/results_dataset_3.json",
        "data/results/runtime/Greedy-local-search: CPLEX (V2)/results_dataset_3.json",
    ]

    plot_producer = PlotProducer(files, file_name, dataset_name)
    plot_producer.generate_line_plot("T", "runtime_in_sec", "Number of timeslots", "Running time in seconds")


def runtime_gls_3_plot(file_name: str, dataset_name: str):
    files = [
        "data/results/runtime/Greedy-local-search: CPLEX (V1)/results_dataset_7.json",
        "data/results/runtime/Greedy-local-search: CPLEX (V2)/results_dataset_7.json",
    ]
    plot_producer = PlotProducer(files, file_name, dataset_name)
    plot_producer.generate_line_plot("J", "runtime_in_sec", "Number of jobs", "Running time in seconds")
