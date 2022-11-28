import os
import timeit
import pandas as pd
from matplotlib import pyplot as plt

from algorithms.greedy_with_blackbox_heuristic import greedy_with_blackbox_heuristic
from input_generation.analysis_input_generator import AnalysisInputGenerator
from models.active_time_ip import solve_active_time_ip
import seaborn as sns


def generate_line_plot_for_running_times():
    generate_line_plot_for_running_time("Small", "Feasible")
    plt.clf()
    generate_line_plot_for_running_time("Moderate", "Feasible")
    plt.clf()
    generate_line_plot_for_running_time("Large", "Feasible")
    plt.clf()


def generate_line_plot_for_running_time(instance_type: str, schedule_type: str):
    stats = []
    for g in range(1, 100, 5):
        instances = AnalysisInputGenerator.generate_multiple_feasible_instances(10, instance_type, g) \
            if schedule_type == "Feasible" else AnalysisInputGenerator.generate_multiple_instances(10, instance_type, g)
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
            t = timeit.Timer(lambda: solve_active_time_ip(instance))
            total_time_taken = total_time_taken + t.timeit(number=1)
        elif algorithm == "maxflow_greedy":
            t = timeit.Timer(lambda: greedy_with_blackbox_heuristic(instance))
            total_time_taken = total_time_taken + t.timeit(number=1)

    average_execution_time = total_time_taken / number_of_instances
    return average_execution_time
