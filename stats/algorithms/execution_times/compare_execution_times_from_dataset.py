import os
import timeit
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from input_generation.problem_instances.parsed_instance import ParsedInstance
from solvers.solver_handler import solve_instance

RESULTS_PATH = os.path.join(os.getcwd(), "stats", "algorithms", "execution_times", "results")


def compare_running_times_on_dataset_with_varying_number_of_jobs(dataset: list[ParsedInstance], dataset_name):
    # ip_model_stats = time_algorithm("Active-time-IP", dataset)
    # greedy_stats = time_algorithm("Greedy-local-search: Pyomo", dataset)
    # greedy_stats_with_opt = time_algorithm("Greedy-local-search: CPLEX (V1)", dataset)
    # greedy_stats_with_opt_v2 = time_algorithm("Greedy-local-search: CPLEX (V2)", dataset)
    greedy_stats_with_reopt = time_algorithm("Greedy-local-search-with-reopt-v2", dataset)

    # max_flow_stats = time_algorithm("Maxflow-LP", dataset)
    # erf_stats = time_algorithm("Earliest-released-first", dataset)

    df = pd.DataFrame(greedy_stats_with_reopt)
    # df = pd.DataFrame(greedy_stats + greedy_stats_with_opt)
    print(df)
    sns.lineplot(x="Number of jobs", y="Average time taken", hue="Algorithm", data=df)
    plt.legend(loc='upper right')
    plt.xlabel("Number of jobs per instance")
    plt.ylabel("Running time in seconds")
    plt.savefig(os.path.join(os.getcwd(),
                             "stats",
                             "algorithms",
                             "execution_times",
                             "plots",
                             f"{dataset_name}"))


def compare_running_times_on_dataset_with_changes_in_t(dataset: list[ParsedInstance], dataset_name):
    if not os.path.exists(RESULTS_PATH):
        os.makedirs(RESULTS_PATH)

    greedy_stats = time_algorithm("Greedy-local-search: Pyomo", dataset)
    greedy_stats_with_opt = time_algorithm("Greedy-local-search: CPLEX (V1)", dataset)
    greedy_stats_with_opt_v2 = time_algorithm("Greedy-local-search: CPLEX (V2)", dataset)

    df = pd.DataFrame(greedy_stats + greedy_stats_with_opt + greedy_stats_with_opt_v2)
    df.to_csv(os.path.join(RESULTS_PATH, f"{dataset_name}"), encoding='utf-8', index=False)
    print(df)
    sns.lineplot(x="Number of timeslots", y="Average time taken", hue="Algorithm", data=df)
    plt.legend(loc='upper right')
    plt.xlabel("Number of timeslots m")
    plt.ylabel("Running time in seconds")
    plt.savefig(os.path.join(os.getcwd(),
                             "stats",
                             "algorithms",
                             "execution_times",
                             "plots",
                             f"{dataset_name}"))


def compare_running_times_on_dataset_with_changes_in_batch_size(dataset: list[ParsedInstance], dataset_name):
    if not os.path.exists(RESULTS_PATH):
        os.makedirs(RESULTS_PATH)

    ip_model_stats = time_algorithm("Active-time-IP", dataset)
    greedy_stats_with_opt = time_algorithm("Greedy-local-search-with-opt", dataset)
    max_flow_stats = time_algorithm("Maxflow-LP", dataset)
    erf_stats = time_algorithm("Earliest-released-first", dataset)

    df = pd.DataFrame(ip_model_stats + max_flow_stats + erf_stats + greedy_stats_with_opt)
    df.to_csv(os.path.join(RESULTS_PATH, f"{dataset_name}"), encoding='utf-8', index=False)
    print(df)
    sns.lineplot(x="Batch size G", y="Average time taken", hue="Algorithm", data=df)
    plt.legend(loc='upper right')
    plt.xlabel("Batch size G")
    plt.ylabel("Running time in seconds")
    plt.savefig(os.path.join(os.getcwd(),
                             "stats",
                             "algorithms",
                             "execution_times",
                             "plots",
                             f"{dataset_name}"))


# Time execution of an algorithm on a list of problem instances.
def time_algorithm(algorithm: str, instances: list[ParsedInstance]):
    stats = []

    for instance in instances:
        t = timeit.Timer(lambda: solve_instance(instance, algorithm, "gurobi"))
        times = t.repeat(3, 3)
        avg_time_taken = min(times) / 3
        stats.append(
            {
                "Instance id": instance.instance_id,
                "Number of jobs": instance.number_of_jobs,
                "Number of timeslots": instance.number_of_timeslots,
                "Batch size G": instance.number_of_parallel_jobs,
                "Algorithm": algorithm,
                "Average time taken": avg_time_taken
            }
        )

    # average_execution_time = total_time_taken / number_of_instances
    return stats
