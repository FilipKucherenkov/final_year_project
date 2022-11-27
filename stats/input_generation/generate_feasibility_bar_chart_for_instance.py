import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from matplotlib.ticker import FuncFormatter

from input_generation.analysis_input_generator import AnalysisInputGenerator


def generate_feasibility_bar_chart_for_instance():
    small_instances = AnalysisInputGenerator.generate_multiple_instances(100, "Small", -1)
    moderate_instances = AnalysisInputGenerator.generate_multiple_instances(100, "Moderate", -1)
    large_instances = AnalysisInputGenerator.generate_multiple_instances(100, "Large", -1)
    stats = generate_instance_stats(small_instances + moderate_instances + large_instances)

    agr = stats.groupby(["Instance type", "Schedule"]).size().reset_index(name="Occurrences")

    ax = sns.barplot(x="Instance type", y="Occurrences", hue="Schedule", errorbar=None, data=agr)
    ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: int(x)))  # Force integer ticks
    plt.title("Generated instances")
    plt.legend(loc='upper right')
    plt.savefig(os.path.join(os.getcwd(),
                             "stats",
                             "input_generation",
                             "plots",
                             "feasibility_bar"))


def generate_instance_stats(instances):
    stats = []
    for i in instances:
        is_feasible = i.is_feasible()
        stats.append({
            "Instance type": i.instance_type,
            "Schedule": "Feasible" if is_feasible else "Infeasible"
        })

    df = pd.DataFrame(stats)
    return df
