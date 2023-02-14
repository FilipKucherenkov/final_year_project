import logging
import os
import matplotlib.pyplot as plt

from utils.plot_producer import PlotProducer
from utils.statistics import count_optimal_objectives, calculate_runtime_stats

RESULTS_PATH = os.path.join(os.getcwd(), "stats", "algorithms", "runtime_analysis")

# Set log level
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s')


def print_objective_performance_on_all_datasets(method: str):
    # Available methods:
    # 1. Earliest-released-first
    # 2. Earliest-released-first-with-density-heuristic
    # 3. Maxflow-LP
    # 4. Greedy-local-search: CPLEX Re-optimization

    count_optimal_objectives("dataset_1", method)
    calculate_runtime_stats("dataset_1", method)
    count_optimal_objectives("dataset_2", method)
    calculate_runtime_stats("dataset_2", method)
    count_optimal_objectives("dataset_3", method)
    calculate_runtime_stats("dataset_3", method)
    count_optimal_objectives("dataset_4", method)
    calculate_runtime_stats("dataset_4", method)
    count_optimal_objectives("dataset_5", method)
    calculate_runtime_stats("dataset_5", method)
    count_optimal_objectives("dataset_6", method)
    calculate_runtime_stats("dataset_6", method)
    count_optimal_objectives("dataset_7", method)
    calculate_runtime_stats("dataset_7", method)


def generate_all_plots():
    # ------ Dataset 1 plots --------
    runtime_plot_1("runtime_on_dataset_1", "dataset_1")
    util_plot_1("Batch-util-dataset_1", "dataset_1")
    objective_plot_1("LCS_vs_IP_dataset_1", "Greedy-local-search: CPLEX Re-optimization",
                     "dataset_1")  # LCS vs IP model
    objective_plot_1("Maxflow_vs_IP_dataset_1", "Maxflow-LP", "dataset_1")  # Maxflow model vs IP model
    objective_plot_1("Density_vs_IP_dataset_1", "Earliest-released-first-with-density-heuristic",
                     "dataset_1")
    objective_plot_1("Greedy_vs_IP_dataset_1", "Earliest-released-first",
                     "dataset_1")

    # ------ Dataset 2 plots --------
    runtime_plot_2("Runtime_on_dataset_2", "dataset_2")
    util_plot_2("Batch-util-dataset_2", "dataset_2")
    objective_plot_2("LCS_vs_IP_dataset_2", "Greedy-local-search: CPLEX Re-optimization",
                     "dataset_2")  # LCS vs IP model
    objective_plot_2("Greedy_vs_IP_dataset_2", "Earliest-released-first",
                     "dataset_2")
    objective_plot_2("Density_vs_IP_dataset_2", "Earliest-released-first-with-density-heuristic",
                     "dataset_2")

    # ------ Dataset 4 plots --------
    runtime_plot_3("Runtime_on_dataset_3", "dataset_3")
    util_plot_3("Batch-util-dataset_3", "dataset_3")
    objective_plot_3("LCS_vs_IP_dataset_3", "Greedy-local-search: CPLEX Re-optimization",
                     "dataset_3")  # LCS vs IP model
    objective_plot_3("Greedy_vs_IP_dataset_3", "Earliest-released-first",
                     "dataset_3")
    objective_plot_3("Density_vs_IP_dataset_3", "Earliest-released-first-with-density-heuristic",
                     "dataset_3")

    # ------ Dataset 4 plots --------
    runtime_plot_4("Runtime-on-dataset-4", "dataset_4")
    util_plot_4("Batch-util-dataset-4", "dataset_4")
    objective_plot_4("LCS_vs_IP_dataset_4", "Greedy-local-search: CPLEX Re-optimization",
                     "dataset_4")  # LCS vs IP model
    objective_plot_4("Maxflow_vs_IP_dataset_4", "Maxflow-LP", "dataset_4")  # Maxflow model vs IP model
    objective_plot_4("Density_vs_IP_dataset_4", "Earliest-released-first-with-density-heuristic",
                     "dataset_4")  # Greedy vs IP model
    objective_plot_4("Greedy_vs_IP_dataset_4", "Earliest-released-first",
                     "dataset_4")

    # ------ Dataset 5 plots --------
    runtime_plot_5("Runtime-on-dataset-5", "dataset_5")
    util_plot_5("Batch-util-dataset-5", "dataset_5")
    objective_plot_5("LCS_vs_IP_dataset_5", "Greedy-local-search: CPLEX Re-optimization",
                     "dataset_5")  # LCS vs IP model
    objective_plot_5("Maxflow_vs_IP_dataset_5", "Maxflow-LP", "dataset_5")  # Maxflow model vs IP model
    objective_plot_5("Density_vs_IP_dataset_5", "Earliest-released-first-with-density-heuristic",
                     "dataset_5")  # Greedy vs IP model
    objective_plot_5("Greedy_vs_IP_dataset_5", "Earliest-released-first",
                     "dataset_5")

    # ------ Dataset 6 plots --------
    runtime_plot_6("Runtime-on-dataset-6", "dataset_6")
    util_plot_6("Batch-util-dataset-6", "dataset_6")
    objective_plot_6("LCS_vs_IP_dataset_6", "Greedy-local-search: CPLEX Re-optimization",
                     "dataset_6")  # LCS vs IP model
    objective_plot_6("Maxflow_vs_IP_dataset_6", "Maxflow-LP", "dataset_6")  # Maxflow model vs IP model
    objective_plot_6("Density_vs_IP_dataset_6", "Earliest-released-first-with-density-heuristic",
                     "dataset_6")  # Greedy vs IP model
    objective_plot_6("Greedy_vs_IP_dataset_6", "Earliest-released-first",
                     "dataset_6")

    # ------ Dataset 7 plots --------
    runtime_plot_7("Runtime-on-dataset-7", "dataset_7")
    objective_plot_7("LCS_vs_IP_dataset_7", "Greedy-local-search: CPLEX Re-optimization",
                     "dataset_7")  # LCS vs IP model
    objective_plot_7("Maxflow_vs_IP_dataset_7", "Maxflow-LP", "dataset_7")  # Maxflow model vs IP model
    objective_plot_7("Density_vs_IP_dataset_7", "Earliest-released-first-with-density-heuristic",
                     "dataset_7")  # Greedy vs IP model
    objective_plot_7("Greedy_vs_IP_dataset_7", "Earliest-released-first",
                     "dataset_7")

    # Local search optimizations and analysis on datasets 3 & 7
    runtime_gls_plot("Runtime-dataset-3-local-search", "dataset_3")
    runtime_gls_2_plot("Change-in-objective-dataset-3", "dataset_3")
    runtime_gls_3_plot("Change-in-objective-dataset-7", "dataset_7")


# ======== Dataset 1 plots ============
def runtime_plot_1(file_name: str, dataset_name: str):
    files = [
        "data/results/runtime/Greedy-local-search: CPLEX "
        "Re-optimization/results_dataset_1.json",
        "data/results/runtime/Active-time-IP/results_dataset_1.json",
        # "data/results/runtime/Earliest-released-first-with-density-heuristic/results_dataset_1.json",
        # "data/results/runtime/Earliest-released-first/results_dataset_1.json",
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
        "data/results/runtime/Active-time-IP/results_dataset_2.json",
        # "data/results/runtime/Earliest-released-first-with-density-heuristic/results_dataset_2.json",
        # "data/results/runtime/Earliest-released-first/results_dataset_2.json",
    ]
    plot_producer = PlotProducer(files, file_name, dataset_name)
    plot_producer.generate_line_plot("T", "runtime_in_sec", "Number of jobs and time slots", "Running time in seconds",
                                     ["Greedy Local Search: CPLEX re-optimization", "Integer Programming Model"])


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


# ======== Dataset 3 plots ============
def runtime_plot_3(file_name: str, dataset_name: str):
    files = [
        "data/results/runtime/Greedy-local-search: CPLEX "
        "Re-optimization/results_dataset_3.json",
        "data/results/runtime/Active-time-IP/results_dataset_3.json",
        "data/results/runtime/Earliest-released-first-with-density-heuristic/results_dataset_3.json",
        "data/results/runtime/Earliest-released-first/results_dataset_3.json",
    ]
    plot_producer = PlotProducer(files, file_name, dataset_name)
    plot_producer.generate_line_plot("T", "runtime_in_sec", "Number of timeslots", "Running time in seconds")


def objective_plot_3(file_name: str, method: str, dataset_name: str):
    files = [
        f"data/results/objective/{method}/results_{dataset_name}.json",
        f"data/results/objective/Active-time-IP/results_{dataset_name}.json"
    ]
    plot_producer = PlotProducer(files, file_name, dataset_name)
    plot_producer.generate_line_plot("T", "objective_value", "Number of timeslots", "Objective value")


def util_plot_3(file_name: str, dataset_name: str):
    files = [
        "data/results/objective/Greedy-local-search: CPLEX "
        "Re-optimization/results_dataset_3.json",
        "data/results/objective/Active-time-IP/results_dataset_3.json",
        "data/results/objective/Earliest-released-first-with-density-heuristic/results_dataset_3.json",
        "data/results/objective/Earliest-released-first/results_dataset_3.json",
    ]
    plot_producer = PlotProducer(files, file_name, dataset_name)
    plot_producer.generate_bar_plot("T", "batch_utilization", "Number of timeslots", "Average batch utilization %")


# ======== Dataset 4 plots ============
def runtime_plot_4(file_name: str, dataset_name: str):
    files = [
        "data/results/runtime/Greedy-local-search: CPLEX "
        "Re-optimization/results_dataset_4.json",
        "data/results/runtime/Active-time-IP/results_dataset_4.json",
        "data/results/runtime/Earliest-released-first-with-density-heuristic/results_dataset_4.json",
        "data/results/runtime/Earliest-released-first/results_dataset_4.json",
    ]

    plot_producer = PlotProducer(files, file_name, dataset_name)
    plot_producer.generate_line_plot("J", "runtime_in_sec", "Number of jobs", "Running time in seconds")


def objective_plot_4(file_name: str, method: str, dataset_name: str):
    files = [
        f"data/results/objective/{method}/results_{dataset_name}.json",
        f"data/results/objective/Active-time-IP/results_{dataset_name}.json"
    ]
    plot_producer = PlotProducer(files, file_name, dataset_name)
    plot_producer.generate_line_plot("J", "objective_value", "Number of jobs", "Objective value")


def util_plot_4(file_name: str, dataset_name: str):
    files = [
        "data/results/objective/Greedy-local-search: CPLEX "
        "Re-optimization/results_dataset_4.json",
        "data/results/objective/Active-time-IP/results_dataset_4.json",
        "data/results/objective/Earliest-released-first-with-density-heuristic/results_dataset_4.json",
        "data/results/objective/Earliest-released-first/results_dataset_4.json",
    ]
    plot_producer = PlotProducer(files, file_name, dataset_name)
    plot_producer.generate_bar_plot("J", "batch_utilization", "Number of jobs", "Average batch utilization %")


# ======== Dataset 5 plots ============
def runtime_plot_5(file_name: str, dataset_name: str):
    plt.clf()
    files = [
        "data/results/runtime/Greedy-local-search: CPLEX "
        "Re-optimization/results_dataset_5.json",
        "data/results/runtime/Active-time-IP/results_dataset_5.json",
        "data/results/runtime/Earliest-released-first-with-density-heuristic/results_dataset_5.json",
        "data/results/runtime/Earliest-released-first/results_dataset_5.json",
    ]
    plot_producer = PlotProducer(files, file_name, dataset_name)
    plot_producer.generate_line_plot("G", "runtime_in_sec", "Batch size", "Running time in seconds")


def objective_plot_5(file_name: str, method: str, dataset_name: str):
    files = [
        f"data/results/objective/{method}/results_{dataset_name}.json",
        f"data/results/objective/Active-time-IP/results_{dataset_name}.json"
    ]
    plot_producer = PlotProducer(files, file_name, dataset_name)
    plot_producer.generate_line_plot("G", "objective_value", "Batch size", "Objective value")


def util_plot_5(file_name: str, dataset_name: str):
    files = [
        "data/results/objective/Greedy-local-search: CPLEX "
        "Re-optimization/results_dataset_5.json",
        "data/results/objective/Active-time-IP/results_dataset_5.json",
        "data/results/objective/Earliest-released-first-with-density-heuristic/results_dataset_5.json",
        "data/results/objective/Earliest-released-first/results_dataset_5.json",
    ]
    plot_producer = PlotProducer(files, file_name, dataset_name)
    plot_producer.generate_bar_plot("G", "batch_utilization", "Batch size", "Average batch utilization %")


# ======== Dataset 6 plots ============
def runtime_plot_6(file_name: str, dataset_name: str):
    files = [
        "data/results/runtime/Greedy-local-search: CPLEX "
        "Re-optimization/results_dataset_6.json",
        "data/results/runtime/Active-time-IP/results_dataset_6.json",
        "data/results/runtime/Earliest-released-first-with-density-heuristic/results_dataset_6.json",
        "data/results/runtime/Earliest-released-first/results_dataset_6.json",
    ]
    plot_producer = PlotProducer(files, file_name, dataset_name)
    plot_producer.generate_line_plot("G", "runtime_in_sec", "Batch size", "Running time in seconds")


def objective_plot_6(file_name: str, method: str, dataset_name: str):
    files = [
        f"data/results/objective/{method}/results_{dataset_name}.json",
        f"data/results/objective/Active-time-IP/results_{dataset_name}.json"
    ]
    plot_producer = PlotProducer(files, file_name, dataset_name)
    plot_producer.generate_line_plot("G", "objective_value", "Batch size", "Objective value")


def util_plot_6(file_name: str, dataset_name: str):
    # create plot
    plt.clf()
    files = [
        "data/results/objective/Greedy-local-search: CPLEX "
        "Re-optimization/results_dataset_6.json",
        "data/results/objective/Active-time-IP/results_dataset_6.json",
        "data/results/objective/Earliest-released-first-with-density-heuristic/results_dataset_6.json",
        "data/results/objective/Earliest-released-first/results_dataset_6.json",
    ]
    plot_producer = PlotProducer(files, file_name, dataset_name)
    plot_producer.generate_bar_plot("G", "batch_utilization", "Batch size", "Average batch utilization %")


# ======== Dataset 7 plots ============
def runtime_plot_7(file_name: str, dataset_name: str):
    files = [
        "data/results/runtime/Greedy-local-search: CPLEX "
        "Re-optimization/results_dataset_7.json",
        "data/results/runtime/Active-time-IP/results_dataset_7.json",
        "data/results/runtime/Earliest-released-first-with-density-heuristic/results_dataset_7.json",
        "data/results/runtime/Earliest-released-first/results_dataset_7.json",
    ]
    plot_producer = PlotProducer(files, file_name, dataset_name)
    plot_producer.generate_line_plot("J", "runtime_in_sec", "Number of jobs", "Running time in seconds")


def objective_plot_7(file_name: str, method: str, dataset_name: str):
    files = [
        f"data/results/objective/{method}/results_{dataset_name}.json",
        f"data/results/objective/Active-time-IP/results_{dataset_name}.json"
    ]
    plot_producer = PlotProducer(files, file_name, dataset_name)
    plot_producer.generate_line_plot("J", "objective_value", "Number of jobs", "Objective value")


def util_plot_7(file_name: str, dataset_name: str):
    # create plot
    plt.clf()
    files = [
        "data/results/objective/Greedy-local-search: CPLEX "
        "Re-optimization/results_dataset_7.json",
        "data/results/objective/Active-time-IP/results_dataset_7.json",
        "data/results/objective/Earliest-released-first-with-density-heuristic/results_dataset_7.json",
        "data/results/objective/Earliest-released-first/results_dataset_7.json",
    ]
    plot_producer = PlotProducer(files, file_name, dataset_name)
    plot_producer.generate_bar_plot("J", "batch_utilization", "Number of jobs", "Average batch utilization %")


# ======== GLS comparisons ============
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
