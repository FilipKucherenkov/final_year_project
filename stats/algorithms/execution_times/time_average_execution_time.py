import os
import timeit
import pandas as pd
from matplotlib import pyplot as plt

from input_generation.dataset_generator import DatasetGenerator
from solvers.models.active_time_ip import solve_active_time_ip
import seaborn as sns

from solvers.greedy_algorithms.greedy_local_search import greedy_local_search


def generate_line_plot_for_running_times():
    generate_line_plot_for_running_time("Large", "Feasible")
    plt.clf()


def generate_line_plot_for_running_time(instance_type: str, schedule_type: str):
    stats = []
    for g in range(1, 100, 5):
        instances = DatasetGenerator.generate_multiple_feasible_instances(1, instance_type, g) \
            if schedule_type == "Feasible" else DatasetGenerator.generate_multiple_instances(1, instance_type, g)
        time_algo1 = time_algorithm("ip_model", instances)
        time_algo2 = time_algorithm("maxflow_greedy", instances)
        stats.append({
            "Instance type": instance_type,
            "G": g,
            "Algorithm": "IP Model",
            "Average running time": time_algo1
        })
        stats.append({
            "Instance type": instance_type,
            "G": g,
            "Algorithm": "Max-flow Greedy",
            "Average running time": time_algo2
        })
    df = pd.DataFrame(stats)

    sns.lineplot(x="G", y="Average running time", hue="Algorithm", data=df)
    plt.title(f"{instance_type} set ({schedule_type})")
    plt.legend(loc='upper right')
    plt.xlabel("Batch size G")
    plt.savefig(os.path.join(os.getcwd(),
                             "stats",
                             "algorithms",
                             "execution_times",
                             "plots",
                             f"avg_running_time_plot_{schedule_type}_{instance_type}"))


# Time execution of an algorithm on a list of problem instances.
def time_algorithm(algorithm: str, instances):
    number_of_instances = len(instances)
    total_time_taken = 0
    for instance in instances:

        if algorithm == "ip_model":
            t = timeit.Timer(lambda: solve_active_time_ip(instance, "gurobi"))
            times = t.repeat(5, 5)
            total_time_taken = min(times) / 5

        elif algorithm == "maxflow_greedy":
            t = timeit.Timer(lambda: greedy_local_search(instance, "gurobi"))
            times = t.repeat(5, 5)
            total_time_taken = min(times) / 5

    # average_execution_time = total_time_taken / number_of_instances
    return total_time_taken
